from bs4 import BeautifulSoup
import requests

# repository_url = 'https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-NEW-today.txt'
# page = requests.get(repository_url)
# soup = BeautifulSoup(page.text, 'html.parser')

# try: 
#     print(soup.contents)
# except Exception as e:
#     print('An error occurred: {e}')


openphish_url = 'https://www.openphish.com/feed.txt'
openphish_page = requests.get(openphish_url)
phish_soup = BeautifulSoup(openphish_page.text, 'html.parser')

try:    
    # Print the content
    print(phish_soup.contents)
except Exception as e:
    print('An error occurred: {e}')
