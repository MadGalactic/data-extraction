import json
import requests
from bs4 import BeautifulSoup


# [URLSCAN]
try: 
    response = requests.get('https://urlscan.io/api/v1/search/')
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx and 5xx)

    try: 
        response_json = response.json() # Directly parse JSON instead of using json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f'Failed to decode JSON: {e}')
    else:
        for item in response_json.get('results', []): # Use .get() to avoid KeyErrors 
            try:
                print(item['task']['url'])
            except KeyError as e:
                print(f'Missing expected key: {e}')
except requests.exceptions.RequestException as e:
    print(f'Error fetching data: {e}')
    

# [PHISHSTATS]
phish_response = requests.get('https://phishstats.info:2096/api/phishing?_where=')
phish_response_json = json.loads(phish_response.text)

for item in phish_response_json:
    try:
        print(item['url'])
    except Exception as e:
        print('An error occurred: {e}')

# [Phishing.Database]
repository_url = 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-NEW-today.txt'
page = requests.get(repository_url)
soup = BeautifulSoup(page.text, 'html.parser')

try: 
    print(soup.contents)
except Exception as e:
    print('An error occurred: {e}')

# [OPENPHISH]
openphish_url = 'https://www.openphish.com/feed.txt'
openphish_page = requests.get(openphish_url)
phish_soup = BeautifulSoup(openphish_page.text, 'html.parser')

try:    
    # Print the content
    print(phish_soup.contents)
except Exception as e:
    print('An error occurred: {e}')