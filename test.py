import requests 

def is_server_active(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
    
url = "https://www.google.com/"
if is_server_active(url):
    print("server is active")
else:
    print("Server is not active")