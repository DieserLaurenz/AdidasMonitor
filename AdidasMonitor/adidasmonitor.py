import logging
import random
import time
from typing import List, Dict, Optional

import requests
import tls_client

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),  # Log-Datei
                        logging.StreamHandler()  # Konsole
                    ])

PROXIES_FILE_PATH = "data/proxies.txt"
USE_PROXIES = False
PRODUCT_ID = "IP8158"
REQUEST_INTERVAL = 5


def read_proxies_from_file() -> List[str]:
    try:
        with open(PROXIES_FILE_PATH, 'r') as f:
            return [line.strip() for line in f]
    except Exception as e:
        logging.error(e)
        return []


def fetch_random_proxy(proxies: List[str]) -> Dict[str, str]:
    proxy = random.choice(proxies)
    ip, port, user, password = proxy.split(':')

    proxy_url = f"http://{user}:{password}@{ip}:{port}"

    return {
        "http": proxy_url,
        "https": proxy_url
    }


def extract_available_sizes(data: Dict) -> List[str]:
    available_sizes = []
    for variation in data.get("variation_list", []):
        if variation.get("availability_status") != "NOT_AVAILABLE":
            available_sizes.append(variation.get("size"))
            logging.info(f"Size {variation['size']} is available with status {variation['availability_status']}.")
        if variation.get("availability") != 0:
            logging.info(f"Availability of SKU {variation['sku']} has changed to {variation['availability']}.")
    return available_sizes


def raise_for_status(response):
    """Custom function to raise an HTTPError if the response status indicates an error."""
    if response.status_code != 200:
        raise requests.HTTPError(f'Client Error: {response.status_code} for url: {response.url}')


def check_availability(product_id: str, proxy: Optional[Dict[str, str]] = None) -> None:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    try:
        response = session.get(f"https://www.adidas.de/api/products/{product_id}/availability", headers=headers,
                               proxy=proxy)
        raise_for_status(response)

        logging.info(f"Successful request for product ID {product_id}")
        data = extract_available_sizes(response.json())
        logging.info(f"Available sizes: {data}")
    except Exception as e:
        logging.error(f"Error while sending request for product ID {product_id}: {e}")


if __name__ == "__main__":
    session = tls_client.Session(
        client_identifier="chrome_112",
        random_tls_extension_order=True,
    )

    proxy_list = read_proxies_from_file() if USE_PROXIES else None

    while True:
        proxy = fetch_random_proxy(proxy_list) if USE_PROXIES else None
        check_availability(PRODUCT_ID, proxy)
        time.sleep(REQUEST_INTERVAL)
