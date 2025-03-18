import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Create a folder to store downloaded pages
DOWNLOAD_FOLDER = "downloaded_pages"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_content(url):
    """Fetches and saves the content of a live URL."""
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()

        # Extract domain name for file naming
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace("www.", "")  # e.g., "example.com"

        # Generate a unique filename
        filename = os.path.join(DOWNLOAD_FOLDER, f"{domain}.html")

        # Save content
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"[DOWNLOADED] {url} → {filename}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to download {url}: {e}")



def check_url_live(url):
    # check if a URL is live by making an HTTP request
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code < 400: 
            print(f"[LIVE] {url} - Status: {response.status_code}")
            download_content(url)  # Download content if live
        else: 
            print(f"[DEAD] {url} - Status: {response.status_code}")
    except requests.exceptions.RequestException:
        print(f"[ERROR] Could not reach {url}")


# [URLSCAN]
try: 
    response = requests.get('https://urlscan.io/api/v1/search/')
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx and 5xx)

    try: 
        response_json = response.json() # Directly parse JSON instead of using json.loads(response.text)
        for item in response_json.get('results', []):
            try:
                url = item['task']['url']
                check_url_live(url)
            except KeyError as e:
                 print(f'Missing expected key: {e}')
    except json.JSONDecodeError as e:
        print(f'Failed to decode JSON: {e}')
except requests.exceptions.RequestException as e:
    print(f'Error fetching data: {e}')
    

# [PHISHSTATS]
try:    
    phish_response = requests.get('https://phishstats.info:2096/api/phishing?_where=')
    phish_response.raise_for_status()

    try: 
        phish_response_json = phish_response.json()
        for item in phish_response_json:
            try:
                url = item['url']
                check_url_live(url)
            except KeyError as e:
                print(f'Missing expected key in PhishStats data: {e}')
    except json.JSONDecodeError as e:
        print(f'Failed to decode JSON from PhishStats: {e}')
except requests.exceptions.RequestException as e:
    print(f'Error fetching PhishStats data: {e}')

# [Phishing.Database] 
repository_url = 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-NEW-today.txt'

try:
    page = requests.get(repository_url, timeout=10)
    page.raise_for_status()

    try:
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.get_text().splitlines() # Extract each line as a separate URL
        for url in links:
            if url in links:
                if url.strip(): # Ignore empty lines
                    check_url_live(url.strip())
    except Exception as e:
        print(f'An error occurred while parsing HTML: {e}')
except requests.exceptions.RequestException as e:
    print(f'Error fetching Phishing Database: {e}')

# [OPENPHISH]
openphish_url = 'https://www.openphish.com/feed.txt'

try: 
    openphish_page = requests.get(openphish_url, timeout=10)
    openphish_page.raise_for_status()  # Ensures request was successful

    try:
        phish_soup = BeautifulSoup(openphish_page.text, 'html.parser')
        phish_links = phish_soup.get_text().splitlines()  # Extract each line as a URL
        for url in phish_links:
            if url.strip(): # Ignore empty lines
                check_url_live(url.strip()) # Check if URL is live   
    except Exception as e:
        print(f'An error occurred while parsing OpenPhish data: {e}')
except requests.exceptions.RequestException as e:
    print(f'Error fetching OpenPhish data: {e}')