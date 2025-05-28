import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Ensure image download directory exists
os.makedirs("downloaded_images", exist_ok=True)

def extract_web_data(url):
    data = {
        "title": "",
        "images": [],
        "links": [],
        "headings": [],
        "word_count": 0,
        "tag_counts": {},
        "broken_links": []
    }

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        data["error"] = str(e)
        return data

    soup = BeautifulSoup(response.text, 'html.parser')

    # Title
    data["title"] = soup.title.string if soup.title else "No title found"

    # Download Images
    images = soup.find_all('img')
    for i, img in enumerate(images):
        src = img.get('src')
        if src:
            img_url = urljoin(url, src)
            data["images"].append(img_url)
            try:
                img_data = requests.get(img_url).content
                filename = os.path.join("downloaded_images", f"image_{i+1}.jpg")
                with open(filename, 'wb') as f:
                    f.write(img_data)
            except:
                continue

    # Extract Links
    links = soup.find_all('a')
    all_links = [link.get('href') for link in links if link.get('href')]
    data["links"] = all_links

    # Word and Tag Count
    text = soup.get_text()
    data["word_count"] = len(text.split())
    data["tag_counts"] = {tag: len(soup.find_all(tag)) for tag in ['p', 'div', 'span', 'a']}

    # Headings
    for level in range(1, 7):
        for heading in soup.find_all(f'h{level}'):
            data["headings"].append((f"h{level}", heading.get_text(strip=True)))

    # Broken Links
    for link in all_links:
        full_url = urljoin(url, link)
        try:
            r = requests.head(full_url, allow_redirects=True, timeout=5)
            if r.status_code >= 400:
                data["broken_links"].append(full_url)
        except:
            data["broken_links"].append(full_url)

    return data
