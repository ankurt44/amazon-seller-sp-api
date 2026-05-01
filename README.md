# Amazon SP-API — Create Dog Bed Listing

A Python script to create a new product listing on Amazon using the Selling Partner API (SP-API).

---

## Prerequisites

- Python 3.8 or higher
- An Amazon Seller Central account (Professional plan)
- An SP-API developer application with the **Amazon Listings Items** role enabled

---

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:ankurt44/amazon-seller-sp-api.git
cd amazon-seller-sp-api
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

```bash
cp .env.example .env
```

Open `.env` and fill in each variable (see the section below).

---

## Filling in `.env`

```
LWA_APP_ID=...
LWA_CLIENT_SECRET=...
REFRESH_TOKEN=...
SELLER_ID=...
AWS_ENV=SANDBOX
```

### `LWA_APP_ID` and `LWA_CLIENT_SECRET`

1. Log in to [Seller Central](https://sellercentral.amazon.com)
2. Go to **Apps & Services → Develop Apps**
3. Click your app name
4. Under **LWA credentials**, click **View**
5. Copy **Client ID** → `LWA_APP_ID`
6. Copy **Client Secret** → `LWA_CLIENT_SECRET`

### `REFRESH_TOKEN`

The refresh token is obtained by authorizing your app via the OAuth flow:

1. In Seller Central, go to **Apps & Services → Develop Apps**
2. Click **Authorize** on your app and complete the OAuth flow
3. At the end you will receive an **authorization code**
4. Exchange it for a refresh token:

```bash
curl -X POST https://api.amazon.com/auth/o2/token \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_AUTH_CODE" \
  -d "client_id=YOUR_LWA_APP_ID" \
  -d "client_secret=YOUR_LWA_CLIENT_SECRET"
```

5. Copy the `refresh_token` value from the response → `REFRESH_TOKEN`

### `SELLER_ID`

1. In Seller Central, go to **Settings → Account Info**
2. Under **Business Information**, find **Merchant Token**
3. Copy that value → `SELLER_ID`

### `AWS_ENV`

| Value | Description |
|-------|-------------|
| `SANDBOX` | Use the Amazon sandbox environment (for testing) |
| `PRODUCTION` | Use the live Amazon environment |

---

## Running the script

### Create a listing

```bash
python create_listing.py
```

On success you will see:

```
Creating listing for SKU: DOG-BED-PREMIUM-001
Marketplace: ATVPDKIKX0DER (US)

Success! Listing submitted.
  SKU:    DOG-BED-PREMIUM-001
  Status: ACCEPTED
```

### Verify the listing was created

```bash
python create_listing.py get
```

This fetches the listing back from Amazon and prints its full details.

---

## Customising the listing

Open `create_listing.py` and edit the following near the top of the file:

| Variable | Description |
|----------|-------------|
| `SKU` | Your unique product identifier |
| `list_price` | Sale price in USD |
| `quantity` | Available stock |
| `fulfillment_channel_code` | `DEFAULT` for self-fulfilled, `AMAZON_NA` for FBA |

All other product attributes (title, description, bullet points, dimensions) are in the `LISTING_PAYLOAD` dictionary.

---

## Troubleshooting

**`Auth Error: invalid_client`**
Your `LWA_APP_ID`, `LWA_CLIENT_SECRET`, or `REFRESH_TOKEN` is incorrect. Double-check each value in `.env`.

**`API Error: Unauthorized`**
Your SP-API app is missing the **Amazon Listings Items** role. Go to Seller Central → Develop Apps → edit your app → enable the role, then re-authorize to get a new refresh token.

**`ModuleNotFoundError`**
Make sure your virtual environment is activated (`source venv/bin/activate`) and dependencies are installed (`pip install -r requirements.txt`).
