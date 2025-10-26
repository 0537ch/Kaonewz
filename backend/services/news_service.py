import os
import logging
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NewsService:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = os.getenv('NEWS_API_BASE_URL', 'https://newsapi.org/v2')
        self.default_page_size = int(os.getenv('DEFAULT_PAGE_SIZE', 10))
        
        if not self.api_key:
            raise ValueError("NEWS_API_KEY environment variable is not set")

    def get_news_for_country(
        self,
        country_code: str,
        page_size: int = None,
        page: int = 1,
        category: str = None
    ) -> List[Dict]:
        """
        Fetch news articles for a specific country
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'us', 'gb')
            page_size: Number of results to return per page (1-100)
            page: Page number to return
            category: News category (business, entertainment, general, health, science, sports, technology)
            
        Returns:
            List of news articles
        """
        if not country_code or len(country_code) != 2:
            raise ValueError("Invalid country code. Must be a 2-letter ISO 3166-1 alpha-2 code.")
        
        params = {
            'country': country_code.lower(),
            'pageSize': min(page_size or self.default_page_size, 100),  # Max 100 per page
            'page': max(1, page),
            'apiKey': self.api_key
        }
        
        if category:
            params['category'] = category.lower()
        
        try:
            response = requests.get(
                f"{self.base_url}/top-headlines",
                params=params,
                timeout=10  # 10 seconds timeout
            )
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'ok':
                raise Exception(f"News API error: {data.get('message', 'Unknown error')}")
                
            return data.get('articles', [])
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching news: {str(e)}")
            raise Exception("Failed to fetch news. Please try again later.")
    
    def search_news(
        self,
        query: str,
        country_code: str = None,
        language: str = 'en',
        sort_by: str = 'publishedAt',
        page_size: int = None,
        page: int = 1
    ) -> List[Dict]:
        """
        Search for news articles
        
        Args:
            query: Search keywords or phrases
            country_code: ISO 3166-1 alpha-2 country code
            language: Language code (e.g., 'en', 'es', 'fr')
            sort_by: Sort order (relevancy, popularity, publishedAt)
            page_size: Number of results to return per page (1-100)
            page: Page number to return
            
        Returns:
            List of news articles matching the search criteria
        """
        params = {
            'q': query,
            'language': language,
            'sortBy': sort_by,
            'pageSize': min(page_size or self.default_page_size, 100),
            'page': max(1, page),
            'apiKey': self.api_key
        }
        
        if country_code:
            params['country'] = country_code.lower()
        
        try:
            response = requests.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'ok':
                raise Exception(f"News API error: {data.get('message', 'Unknown error')}")
                
            return data.get('articles', [])
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error searching news: {str(e)}")
            raise Exception("Failed to search for news. Please try again later.")

# Singleton instance
news_service = NewsService()
