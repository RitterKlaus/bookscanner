# Erstellt mit Hilfe des KI-Assistenten Github Copilot und Claude Sonnet 3.5 * 0.9x
# und mit Hilfe von https://www.thedataschool.co.uk/salome-grasland/using-the-isbndb-api-with-python/
import os
from dotenv import load_dotenv
import requests
import csv
import time

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('API_KEY')
base_url = 'https://api2.isbndb.com/book/'

class RateLimiter:
    def __init__(self, calls_per_second):
        self.calls_per_second = calls_per_second
        self.interval = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait(self):
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()

rate_limiter = RateLimiter(1) # Allow 1 call per second

isbns_to_process = [
"9783453323476",
"9783423214483",
"9781800817746"
]

with open('book_information.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['ISBN', 'Title', 'Author', 'Publisher', 'Pages', 'Date Published', 'Subjects', 'Binding', 'Synopsis', 'Language', 'Edition', 'Dimensions', 'MSRP', 'Image', 'Status']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for isbn in isbns_to_process:
        url = f'{base_url}{isbn}'
        headers = {'Authorization': api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            book_info = response.json().get('book', {})
            writer.writerow({
                'ISBN': isbn,
                'Title': book_info.get('title', ''),
                'Author': ', '.join(book_info.get('authors', [])),
                'Publisher': book_info.get('publisher', ''),
                'Pages': book_info.get('pages', ''),
                'Date Published': book_info.get('date_published', ''),
                'Subjects': ', '.join(book_info.get('subjects', [])),  # Add subjects here
                'Binding': book_info.get('binding', ''),
                'Synopsis': book_info.get('synopsis', ''),
                'Language': book_info.get('language', ''),
                'Edition': book_info.get('edition', ''),
                'Dimensions': book_info.get('dimensions', ''),
                'MSRP': book_info.get('msrp', ''),
                'Image': book_info.get('image', ''),
                'Status': 'Success'
            })
        else:
            print(f"Error for ISBN {isbn}: {response.status_code}")
            writer.writerow({
                'ISBN': isbn,
                'Status': 'Error',
                'Title': '',
                'Author': '',
                'Publisher': '',
                'Pages': '',
                'Date Published': '',
                'Binding': '',
                'Synopsis': '',
                'Language': '',
                'Edition': '',
                'Dimensions': '',
                'MSRP': '',
                'Image': ''
            })

        rate_limiter.wait()  # Pause according to the rate limiter
    print("CSV file created successfully.")