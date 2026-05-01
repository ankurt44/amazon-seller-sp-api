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

# Must load env vars before importing sp_api — the library reads AWS_ENV at import time
load_dotenv()

from sp_api.api import ListingsItems
from sp_api.base import Marketplaces, SellingApiException
from sp_api.auth.exceptions import AuthorizationError

MARKETPLACE = Marketplaces.US  # ATVPDKIKX0DER
SELLER_ID = os.environ["SELLER_ID"]

# Unique seller-defined SKU for this product
SKU = "DOG-BED-PREMIUM-001"

# Product attributes matching Amazon's PET_BED product type.
# Use the Product Type Definitions API to get the full required schema.
LISTING_PAYLOAD = {
    "productType": "PET_BED",
    "requirements": "LISTING",
    "attributes": {
        "item_name": [
            {
                "value": "Premium Orthopedic Dog Bed - Memory Foam, Machine Washable Cover",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "brand": [
            {
                "value": "PawComfort",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
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
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "bullet_point": [
            {
                "value": "ORTHOPEDIC MEMORY FOAM: Relieves joint pain and pressure points for dogs of all ages",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            },
            {
                "value": "MACHINE WASHABLE: Removable zip-off cover is easy to clean",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            },
            {
                "value": "NON-SLIP BOTTOM: Stays securely in place on hardwood, tile, or carpet",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            },
            {
                "value": "DURABLE COVER: Made with soft, pet-friendly Oxford fabric",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            },
            {
                "value": "SIZE: 36 x 28 x 4 inches — ideal for medium to large dogs up to 70 lbs",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            },
        ],
        "list_price": [
            {
                "currency": "USD",
                "value": 49.99,
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "condition_type": [
            {
                "value": "new_new",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "material": [
            {
                "value": "Memory Foam",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "color": [
            {
                "value": "Gray",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "item_dimensions": [
            {
                "length": {"value": 36, "unit": "inches"},
                "width": {"value": 28, "unit": "inches"},
                "height": {"value": 4, "unit": "inches"},
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "item_weight": [
            {
                "value": 5.5,
                "unit": "pounds",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "target_species": [
            {
                "value": "Dog",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "size": [
            {
                "value": "Large",
                "language_tag": "en_US",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "main_product_image_locator": [
            {
                # Replace with a real publicly accessible image URL before going to production
                "media_location": "https://images.example.com/dog-bed-main.jpg",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "other_product_image_locator_1": [
            {
                "media_location": "https://images.example.com/dog-bed-side.jpg",
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
        "fulfillment_availability": [
            {
                "fulfillment_channel_code": "DEFAULT",  # Merchant fulfilled; use "AMAZON_NA" for FBA
                "quantity": 100,
                "marketplace_id": MARKETPLACE.marketplace_id,
            }
        ],
    },
}


def get_credentials():
    required = ["LWA_APP_ID", "LWA_CLIENT_SECRET", "REFRESH_TOKEN", "SELLER_ID"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    return {
        "lwa_app_id": os.environ["LWA_APP_ID"],
        "lwa_client_secret": os.environ["LWA_CLIENT_SECRET"],
        "refresh_token": os.environ["REFRESH_TOKEN"],
    }


def create_listing():
    credentials = get_credentials()

    print(f"Creating listing for SKU: {SKU}")
    print(f"Marketplace: {MARKETPLACE.marketplace_id} (US)")

    listings_api = ListingsItems(
        marketplace=MARKETPLACE,
        credentials=credentials,
    )

    try:
        response = listings_api.put_listings_item(
            sellerId=SELLER_ID,
            sku=SKU,
            marketplaceIds=[MARKETPLACE.marketplace_id],
            body=LISTING_PAYLOAD,
        )

        result = response.payload
        status = result.get("status", "unknown")

        if status == "ACCEPTED":
            print(f"\nSuccess! Listing submitted.")
            print(f"  SKU:    {result.get('sku')}")
            print(f"  Status: {status}")

            issues = result.get("issues", [])
            if issues:
                print("\nWarnings/Issues returned by Amazon:")
                for issue in issues:
                    print(f"  [{issue.get('severity')}] {issue.get('message')}")
        else:
            print(f"\nListing not accepted. Status: {status}")
            for issue in result.get("issues", []):
                print(f"  [{issue.get('severity')}] {issue.get('message')}")

        return result

    except AuthorizationError as e:
        print(f"\nAuth Error: {e}")
        print("Check that your LWA_APP_ID, LWA_CLIENT_SECRET, and REFRESH_TOKEN in .env are correct.")
        sys.exit(1)
    except SellingApiException as e:
        print(f"\nAPI Error: {e.error}")
        print(f"Details: {e.message}")
        sys.exit(1)


def get_listing():
    credentials = get_credentials()
    listings_api = ListingsItems(
        marketplace=MARKETPLACE,
        credentials=credentials,
    )
    try:
        response = listings_api.get_listings_item(
            sellerId=SELLER_ID,
            sku=SKU,
            marketplaceIds=[MARKETPLACE.marketplace_id],
            includedData=["summaries", "attributes", "issues"],
        )
        import json
        print(json.dumps(response.payload, indent=2))
    except SellingApiException as e:
        print(f"\nAPI Error: {e.error}")
        print(f"Details: {e.message}")
        sys.exit(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "get":
        get_listing()
    else:
        create_listing()
