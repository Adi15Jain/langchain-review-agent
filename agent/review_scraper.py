from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

from apify_client import ApifyClient

def fetch_reviews_from_apify(dataset_id: str) -> list[dict]:
    client = ApifyClient("apify_api_....")
    try:
        list_page = client.dataset(dataset_id).list_items()
        items = list_page.items[:]
        reviews = [item for item in items if isinstance(item, dict)]
        return reviews
    except Exception as e:
        print("Error fetching from Apify:", e)
        return []


    
