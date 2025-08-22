import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import pandas as pd
import os

INPUT_CSV = "apollo_all_medicine_urls.csv"
OUTPUT_CSV = "apollo_medicine_details.csv"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Save row to CSV
def save_to_csv(data, file_exists):
    with open(OUTPUT_CSV, "a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "url", "drug_name", "active_ingredient", "legal_manufacturer_name", "dosage_form"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Scrape 1 product page
def scrape_product(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        scripts = soup.find_all("script", type="application/ld+json")

        if len(scripts) > 1:
            data = json.loads(scripts[1].string)
            return {
                "url": url,
                "drug_name": data.get("name"),
                "active_ingredient": data.get("activeIngredient"),
                "legal_manufacturer_name": data.get("manufacturer", {}).get("legalName"),
                "dosage_form": data.get("dosageForm"),
            }
        else:
            print(f"⚠️ No JSON-LD found on: {url}")
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
    return None

def scrape_all_products():
    # Load input CSV and drop duplicate URLs
    df = pd.read_csv(INPUT_CSV)
    df = df.drop_duplicates(subset=["url"])
    
    # Load already scraped URLs from output CSV if exists
    if os.path.exists(OUTPUT_CSV):
        df_done = pd.read_csv(OUTPUT_CSV)
        scraped_urls = set(df_done["url"].str.strip())
    else:
        scraped_urls = set()

    # Filter URLs to scrape
    df_to_scrape = df[~df["url"].str.strip().isin(scraped_urls)]
    print(f"⚙️ {len(scraped_urls)} URLs already scraped. {len(df_to_scrape)} remaining.")

    file_exists = os.path.exists(OUTPUT_CSV)

    for i, row in df_to_scrape.iterrows():
        url = row["url"].strip()
        print(f"[{i}] Scraping: {url}")
        data = scrape_product(url)
        if data:
            save_to_csv(data, file_exists)
            file_exists = True
        time.sleep(0.2)

    print("✅ All done!")

if __name__ == "__main__":
    scrape_all_products()
