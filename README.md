# Apollo Pharmacy Scraper

This project allows you to collect and scrape detailed medicine data from [Apollo Pharmacy](https://www.apollopharmacy.in).

It runs in **two steps**:

1. **Collect all medicine URLs** from Apollo's internal API.
2. **Scrape product detail pages** to extract drug info like name, ingredients, manufacturer, etc.

---

## 📁 Project Structure

```
.
├── apollo_url_collector.py       # Step 1: Collect all product URLs
├── apollo_drug_scraper.py        # Step 2: Scrape detailed drug info
├── apollo_all_medicine_urls.csv  # Output from step 1
├── apollo_medicine_details.csv   # Output from step 2
└── README.md                     
```
---

## Step 1: Collect All Medicine URLs

Run this script first:

```python
python apollo_url_collector.py
```

It will:
- Connect to Apollo's internal GraphQL API
- Retrieve all product URLs
- Save them to apollo_all_medicine_urls.csv


#### Setting Up Your Bearer Token
Apollo's API is protected - you must provide a valid bearer token to access it.

How to get your bearer token:

1. Go to: https://www.apollopharmacy.in
2. Open Developer Tools → Network → XHR/Fetch
3. Look for a request to https://api.apollo247.com/
4. Click the request → under Request Headers, copy the Authorization value.

It will look like:  `Authorization: Bearer 3d1833da70......`

Paste it into the script:

In `apollo_url_collector.py`, replace `<your_token_here>` with your actual token:

```python
"Authorization": "Bearer <your_token_here>",
```

## Step 2: Scrape Drug Details

Once `apollo_all_medicine_urls.csv` is ready, run:

```python
python apollo_drug_scraper.py
```

It will:
- Load all product URLs from the CSV
- Deduplicate them
- Resume from where it left off (if it crashes or is interrupted)
- Extract fields:
    - `drug_name`
    - `active_ingredient`
    - `legal_manufacturer_name`
    - `dosage_form`
- Save to `apollo_medicine_details.csv`



Built by SG using Python, requests, and BeautifulSoup.