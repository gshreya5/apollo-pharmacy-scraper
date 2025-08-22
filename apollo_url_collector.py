import requests
import csv
import time

API_URL = "https://api.apollo247.com/"
PAGE_SIZE = 1000
OUTPUT_FILE = "apollo_all_medicine_urls.csv"

headers = {
    "Authorization": "Bearer <bearer_code>",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def get_total_count():
    payload = {
        "operationName": "medicinesUrlsList",
        "variables": {
            "pageSize": 1,
            "pageNumber": 1
        },
        "query": """
        query medicinesUrlsList($pageSize: Int!, $pageNumber: Int!) {
          medicinesUrlsList(pageSize: $pageSize, pageNumber: $pageNumber) {
            urlsCount
            medicinesUrls {
              url
              urlName
            }
          }
        }
        """
    }

    res = requests.post(API_URL, headers=headers, json=payload)
    res.raise_for_status()
    return res.json()["data"]["medicinesUrlsList"]["urlsCount"]

def save_to_csv(data, file_exists=False):
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "urlName"])
        if not file_exists:
            writer.writeheader()
        for item in data:
            writer.writerow(item)

def scrape_all_urls():
    total_count = get_total_count()
    total_pages = (total_count + PAGE_SIZE - 1) // PAGE_SIZE
    print(f"🧮 Total medicines: {total_count} across {total_pages} pages")

    file_exists = False

    for page_number in range(1, total_pages + 1):
        print(f"📄 Fetching page {page_number}/{total_pages}")

        payload = {
            "operationName": "medicinesUrlsList",
            "variables": {
                "pageSize": PAGE_SIZE,
                "pageNumber": page_number
            },
            "query": """
            query medicinesUrlsList($pageSize: Int!, $pageNumber: Int!) {
              medicinesUrlsList(pageSize: $pageSize, pageNumber: $pageNumber) {
                urlsCount
                medicinesUrls {
                  url
                  urlName
                }
              }
            }
            """
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()["data"]["medicinesUrlsList"]["medicinesUrls"]
            save_to_csv(data, file_exists)
            file_exists = True
        except Exception as e:
            print(f"❌ Failed to fetch page {page_number}: {e}")
            continue

        time.sleep(0.3)

    print("✅ All URLs saved!")

if __name__ == "__main__":
    scrape_all_urls()
