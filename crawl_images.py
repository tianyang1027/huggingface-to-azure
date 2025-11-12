import requests
from bs4 import BeautifulSoup
import json
import time

# Keywords to search
keywords = ["Seattle", "Washington", "Tokyo"]


# Store results
result = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
}

for keyword in keywords:
    # Construct the search URL
    url = f"https://stock.adobe.com/search/free?k={keyword}"
    print(f"Scraping: {keyword} -> {url}")

    # Send request
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the container with id="search-results"
    container = soup.find("div", {"id": "search-results"})

    images = []
    if container:
        # Extract image URLs only inside the search results container
        for img in container.find_all("a"):
            href = img.get("href")
            if href and "https://" in href:
                images.append(href)
    else:
        print(f"No search results container found for {keyword}")

    # Append group result
    result.append({
        "keyword": keyword,
        "images": images
    })

    # Sleep to avoid sending requests too fast
    time.sleep(2)

# Save results into JSON file
with open("adobe_stock_images_free.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Done! Results saved to adobe_stock_images.json")
