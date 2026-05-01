# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows (Git Bash)
pip install -r requirements.txt

# Create a listing
python create_listing.py

# Fetch and inspect an existing listing
python create_listing.py get
```

## Architecture

Single-file script (`create_listing.py`) that talks to the Amazon SP-API Listings Items API.

**Auth flow:** `load_dotenv()` must run before any `spapi` imports because `SPAPIConfig` reads `AWS_ENV` at import time to decide the endpoint base URL (`sandbox.sellingpartnerapi` vs `sellingpartnerapi`). The `get_client()` function builds an `SPAPIClient` from LWA credentials, which handles OAuth token exchange automatically.

**SDK:** Uses the official Amazon SDK `amzn-sp-api` (`spapi` package). The entry point for listing operations is `ListingsApi(client.api_client)`. The `marketplace_ids` parameter must be passed as a list `[MARKETPLACE_ID]`, not a plain string.

**Environment switching:** Controlled by `AWS_ENV` in `.env`. Set to `SANDBOX` for testing (returns Amazon pre-canned mock responses — SKU and product details in the response will differ from what was submitted) or `PRODUCTION` for live.

**Listing payload:** `LISTING_PAYLOAD` at the top of the file defines all product attributes for the `PET_BED` product type. Image URLs in `main_product_image_locator` must be publicly accessible HTTPS URLs before going to production.

## Environment Variables

| Variable | Where to find it |
|---|---|
| `LWA_APP_ID` | Seller Central → Apps & Services → Develop Apps → your app → Client ID |
| `LWA_CLIENT_SECRET` | Same page → Client Secret |
| `REFRESH_TOKEN` | Obtained via OAuth authorization flow in Seller Central |
| `SELLER_ID` | Seller Central → Settings → Account Info → Merchant Token |
| `AWS_ENV` | `SANDBOX` or `PRODUCTION` |
