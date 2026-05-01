"""
Creates a new Amazon dog bed listing using the SP-API Listings Items API.

Setup:
  1. cp .env.example .env
  2. Fill in your credentials in .env
  3. pip install -r requirements.txt
  4. python create_listing.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from spapi import SPAPIClient, SPAPIConfig, ListingsApi, ApiException

MARKETPLACE_ID = "ATVPDKIKX0DER"  # US
SELLER_ID = os.environ["SELLER_ID"]
SKU = "DOG-BED-PREMIUM-001"

LISTING_PAYLOAD = {
    "productType": "PET_BED",
    "requirements": "LISTING",
    "attributes": {
        "item_name": [
            {
                "value": "Premium Orthopedic Dog Bed - Memory Foam, Machine Washable Cover",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "brand": [
            {
                "value": "PawComfort",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "product_description": [
            {
                "value": (
                    "Give your dog the rest they deserve with our premium orthopedic memory foam dog bed. "
                    "Designed to relieve joint pain and pressure points, this bed is perfect for dogs of all ages. "
                    "The removable, machine-washable cover makes cleaning easy. "
                    "Non-slip bottom keeps the bed in place on any surface."
                ),
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "bullet_point": [
            {
                "value": "ORTHOPEDIC MEMORY FOAM: Relieves joint pain and pressure points for dogs of all ages",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            },
            {
                "value": "MACHINE WASHABLE: Removable zip-off cover is easy to clean",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            },
            {
                "value": "NON-SLIP BOTTOM: Stays securely in place on hardwood, tile, or carpet",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            },
            {
                "value": "DURABLE COVER: Made with soft, pet-friendly Oxford fabric",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            },
            {
                "value": "SIZE: 36 x 28 x 4 inches — ideal for medium to large dogs up to 70 lbs",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            },
        ],
        "list_price": [
            {
                "currency": "USD",
                "value": 49.99,
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "condition_type": [
            {
                "value": "new_new",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "material": [
            {
                "value": "Memory Foam",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "color": [
            {
                "value": "Gray",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "size": [
            {
                "value": "Large",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "item_dimensions": [
            {
                "length": {"value": 36, "unit": "inches"},
                "width": {"value": 28, "unit": "inches"},
                "height": {"value": 4, "unit": "inches"},
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "item_weight": [
            {
                "value": 5.5,
                "unit": "pounds",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "target_species": [
            {
                "value": "Dog",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "main_product_image_locator": [
            {
                # Replace with a real publicly accessible image URL before going to production
                "media_location": "https://images.example.com/dog-bed-main.jpg",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "other_product_image_locator_1": [
            {
                "media_location": "https://images.example.com/dog-bed-side.jpg",
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
        "fulfillment_availability": [
            {
                "fulfillment_channel_code": "DEFAULT",  # Merchant fulfilled; use "AMAZON_NA" for FBA
                "quantity": 100,
                "marketplace_id": MARKETPLACE_ID,
            }
        ],
    },
}


def get_client():
    required = ["LWA_APP_ID", "LWA_CLIENT_SECRET", "REFRESH_TOKEN", "SELLER_ID"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    region = os.environ.get("AWS_ENV", "SANDBOX")

    config = SPAPIConfig(
        client_id=os.environ["LWA_APP_ID"],
        client_secret=os.environ["LWA_CLIENT_SECRET"],
        refresh_token=os.environ["REFRESH_TOKEN"],
        region=region,
        scope=None,
    )
    return SPAPIClient(config)


def create_listing():
    client = get_client()
    listings_api = ListingsApi(client.api_client)

    print(f"Creating listing for SKU: {SKU}")
    print(f"Marketplace: {MARKETPLACE_ID} (US)")
    print(f"Region: {os.environ.get('AWS_ENV', 'SANDBOX')}")

    try:
        response = listings_api.put_listings_item(
            seller_id=SELLER_ID,
            sku=SKU,
            marketplace_ids=[MARKETPLACE_ID],
            body=LISTING_PAYLOAD,
            issue_locale="en_US",
        )

        status = response.status
        if status == "ACCEPTED":
            print(f"\nSuccess! Listing submitted.")
            print(f"  SKU:    {response.sku}")
            print(f"  Status: {status}")

            if response.issues:
                print("\nWarnings/Issues returned by Amazon:")
                for issue in response.issues:
                    print(f"  [{issue.severity}] {issue.message}")
        else:
            print(f"\nListing not accepted. Status: {status}")
            if response.issues:
                for issue in response.issues:
                    print(f"  [{issue.severity}] {issue.message}")

    except ApiException as e:
        print(f"\nAPI Error {e.status}: {e.reason}")
        print(e.body)
        sys.exit(1)


def get_listing():
    client = get_client()
    listings_api = ListingsApi(client.api_client)

    try:
        response = listings_api.get_listings_item(
            seller_id=SELLER_ID,
            sku=SKU,
            marketplace_ids=MARKETPLACE_ID,
            included_data=["summaries", "attributes", "issues"],
        )
        import json
        print(json.dumps(response.to_dict(), indent=2))
    except ApiException as e:
        print(f"\nAPI Error {e.status}: {e.reason}")
        print(e.body)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "get":
        get_listing()
    else:
        create_listing()
