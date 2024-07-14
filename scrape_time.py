import requests
from bs4 import BeautifulSoup

def get_local_time(location):
    # Prepare the search query
    search_query = f"time in {location}"
    url = f"https://www.google.com/search?q={search_query}"

    # Set up headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Send the request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve data")
        return None

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the time from the search results
    try:
        time_div = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
        local_time = time_div.text
        print(f"Current local time in {location.capitalize()}: {local_time}")
        return local_time
    except AttributeError:
        print("Could not find the local time")
        return None

if __name__ == "__main__":
    location = input("Enter location (e.g., Kolkata): ")
    get_local_time(location)
