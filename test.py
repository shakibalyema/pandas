import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL pattern for the paginated site
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Dictionary to map text ratings to clean integers
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_books(max_pages=5):
    all_books = []
    
    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Finished or page not found at page {page}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                # 1. Get full title
                title = book.h3.a['title']
                
                # 2. Get price and completely strip out character encoding artifacts
                price_text = book.find('p', class_='price_color').text
                clean_price = price_text.replace('£', '').replace('Â', '').strip()
                price_numeric = float(clean_price)  # Converts it to a clean decimal (e.g., 51.77)
                
                # 3. Clean Availability (removes massive leading/trailing spaces)
                availability = book.find('p', class_='instock availability').text.strip()
                
                # 4. Clean Rating (converts text words to clean integers)
                rating_classes = book.find('p', class_='star-rating')['class']
                rating_text = rating_classes[1] if len(rating_classes) > 1 else "None"
                rating_numeric = RATING_MAP.get(rating_text, 0) 
                
                # Append the beautifully structured data
                all_books.append({
                    'Title': title,
                    'Price': price_numeric,
                    'Rating (Out of 5)': rating_numeric,
                    'Availability': availability
                })
                
            # Pause slightly between pages to respect the server
            time.sleep(1)
            
        except Exception as e:
            print(f"An error occurred on page {page}: {e}")
            break
            
    return all_books

# Run the scraper for the first 5 pages
scraped_data = scrape_books(max_pages=5)

# Convert to a pandas DataFrame
df = pd.DataFrame(scraped_data)

# Save to CSV using 'utf-8-sig' to guarantee perfect display in Excel/VS Code
df.to_csv('books_dataset.csv', index=False, encoding='utf-8-sig')

print(f"\nSuccessfully scraped {len(df)} books and saved to 'books_dataset.csv'!")