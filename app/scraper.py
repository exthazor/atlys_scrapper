import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import time
import asyncio

def fetch_page(url: str, proxy: Optional[str] = None, user_agent: str = None, retries=3, delay=3) -> str:
    """
    Fetch the HTML content of a page with optional proxy and user-agent settings and retry logic.
    """
    headers = {
        'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

def parse_page(html_content: str) -> List[Dict[str, str]]:
    """
    Parse the HTML content to extract product details.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    for product in soup.find_all('div', class_='product-inner'):
        title = product.find('h2', class_='woo-loop-product__title').find('a').get_text(strip=True) if product.find('h2', class_='woo-loop-product__title') and product.find('h2', class_='woo-loop-product__title').find('a') else "No title available"
        price = product.find('span', class_='woocommerce-Price-amount').get_text(strip=True) if product.find('span', class_='woocommerce-Price-amount') else "No price available"
        image_url = product.find('img')['src'] if product.find('img') and 'src' in product.find('img').attrs else "No image available"
        products.append({
            'product_title': title,
            'product_price': price,
            'path_to_image': image_url
        })
    return products

def scrape_products(base_url: str, page_limit: int = 5, proxy: Optional[str] = None, rate_limit_seconds: int = 1) -> List[Dict[str, str]]:
    """
    Scrape products from a catalogue, respecting the rate limit.
    """
    products = []
    for page_number in range(1, page_limit + 1):
        url = f"{base_url}?page={page_number}"
        html_content = fetch_page(url, proxy)
        products.extend(parse_page(html_content))
        time.sleep(rate_limit_seconds)
    return products
