import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def scrape_books(max_pages=5):
    all_books = []
    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping: {url}")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                break
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                title = book.h3.a['title']
                price_text = book.find('p', class_='price_color').text
                clean_price = price_text.replace('£', '').replace('Â', '').strip()
                price_numeric = float(clean_price)
                
                availability = book.find('p', class_='instock availability').text.strip()
                
                rating_classes = book.find('p', class_='star-rating')['class']
                rating_text = rating_classes[1] if len(rating_classes) > 1 else "None"
                rating_numeric = RATING_MAP.get(rating_text, 0) 
                
                all_books.append({
                    'Title': title,
                    'Price': price_numeric,
                    'Rating (Out of 5)': rating_numeric,
                    'Availability': availability
                })
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break
    return all_books

# 1. Scrape the data and create the initial DataFrame
scraped_data = scrape_books(max_pages=5)
df = pd.DataFrame(scraped_data)

# 2. SAVE FILE #1: Save the complete, main dataset
df.to_csv('books_all_scraped.csv', index=False, encoding='utf-8-sig')
print("Saved all books to 'books_all_scraped.csv'")

# 3. Filter out just the top-tier books
five_star_books = df[df['Rating (Out of 5)'] == 5]

# 4. SAVE FILE #2: Save ONLY the 5-star books to a completely separate file!
five_star_books.to_csv('books_top_rated.csv', index=False, encoding='utf-8-sig')
print("Saved 5-star books to 'books_top_rated.csv'")