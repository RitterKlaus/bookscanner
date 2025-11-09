# Erstellt mit Hilfe des KI-Assistenten Github Copilot und Claude Sonnet 3.5 * 0.9x
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
import time
from is_isbn.is_isbn import is_isbn

# Load environment variables from .env file
load_dotenv()

class IsbnService:
    """Service class for ISBN lookups."""
    
    def __init__(self):
        """Initialize the ISBN service."""
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")
        
        self.base_url = 'https://api2.isbndb.com/book/'
        self._last_call = 0
        self._call_interval = 1.0  # 1 second between calls
    
    def _wait_for_rate_limit(self) -> None:
        """Implement rate limiting."""
        now = time.time()
        elapsed = now - self._last_call
        if elapsed < self._call_interval:
            time.sleep(self._call_interval - elapsed)
        self._last_call = time.time()
    
    def get_book_data(self, isbn: str) -> Dict[str, Any]:
        """
        Get book data for a single ISBN.
        
        Args:
            isbn (str): The ISBN to look up
            
        Returns:
            Dict[str, Any]: Book information including status and any error messages
        """
        # Validate ISBN format
        if not is_isbn(isbn):
            return {
                'status': 'error',
                'message': 'Invalid ISBN format',
                'data': None
            }
        
        # Apply rate limiting
        self._wait_for_rate_limit()
        
        # Make API request
        try:
            url = f'{self.base_url}{isbn}'
            headers = {'Authorization': self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            book_info = response.json().get('book', {})
            
            # Format the response data
            data = {
                'isbn': isbn,
                'title': book_info.get('title', ''),
                'authors': book_info.get('authors', []),
                'publisher': book_info.get('publisher', ''),
                'pages': book_info.get('pages', ''),
                'date_published': book_info.get('date_published', ''),
                'subjects': book_info.get('subjects', []),
                'binding': book_info.get('binding', ''),
                'synopsis': book_info.get('synopsis', ''),
                'language': book_info.get('language', ''),
                'edition': book_info.get('edition', ''),
                'dimensions': book_info.get('dimensions', ''),
                'msrp': book_info.get('msrp', ''),
                'image': book_info.get('image', '')
            }
            
            return {
                'status': 'success',
                'message': 'Book data retrieved successfully',
                'data': data
            }
            
        except RequestException as e:
            return {
                'status': 'error',
                'message': f'API request failed: {str(e)}',
                'data': None
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(e)}',
                'data': None
            }

# Create a singleton instance of the service
_isbn_service = None

def get_isbn_service() -> IsbnService:
    """
    Get the singleton instance of the ISBN service.
    
    Returns:
        IsbnService: The ISBN service instance
    """
    global _isbn_service
    if _isbn_service is None:
        _isbn_service = IsbnService()
    return _isbn_service

# Example usage
if __name__ == '__main__':
    # Test the service
    service = get_isbn_service()
    test_isbn = "9783453323476"
    result = service.get_book_data(test_isbn)
    print(result)