import requests
from bs4 import BeautifulSoup
import csv
import shutil

# Send a GET request to the URL
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all div elements with the specified class
div_list = soup.find_all('div', class_='s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t1 puis-include-content-margin puis puis-v132n5e4faosf42v0eo3rf7vw9m s-latency-cf-section s-card-border')

# Create the CSV file and write the data
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Link', 'Title', 'Rating', 'Price'])  # Write header row

    # Iterate over each div element
    for div in div_list:
        # Find the span element for the title
        title_span = div.find('span', class_='a-size-medium a-color-base a-text-normal')
        title = title_span.text if title_span else ''

        # Find the span element for the price
        price_span = div.find('span', class_='a-price-whole')
        price = price_span.text if price_span else ''

        # Find the span element for the rating
        rating_span = div.find('span', class_='a-icon-alt')
        rating = rating_span.text if rating_span else ''

        # Write the data to the CSV file
        writer.writerow([url, title, rating, price])

# Specify the path where you want to save the downloaded file
download_path = "/path/to/download/location/"

# Move the CSV file to the download location
shutil.move('data.csv', download_path + 'data.csv')
