# Importing required modules
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import requests
from bs4 import BeautifulSoup

# Producer function to fetch HTML content from a given URL and put it into a queue
def producer(url, q):
    try:
        # Sending a GET request to the URL
        response = requests.get(url)
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Adding the HTML content to the queue
            q.put(response.text)
    except Exception as e:
        # Printing an error message if the request fails
        print(f"Error fetching {url}: {e}")

# Consumer function to process the HTML content in the queue and extract links
def consumer(q):
    # Looping until the queue is empty
    while not q.empty():
        # Getting HTML content from the queue
        html = q.get()
        # Parsing the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        # Extracting all hyperlinks from the HTML content
        links = [a['href'] for a in soup.find_all('a', href=True)]
        # Printing the extracted links
        print(f"Extracted links: {links}")

# Main function
def main():
    # Creating a new queue
    q = Queue()
    
    # Reading URLs from a text file and storing them in a list
    urls = []
    with open('urls.txt', 'r') as file:
        for line in file:
            urls.append(line.strip())

    # Using ThreadPoolExecutor to fetch HTML content concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(lambda url: producer(url, q), urls)

    # Consuming the HTML content in the queue to extract links
    consumer(q)

if __name__ == '__main__':
    main()