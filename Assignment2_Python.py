import requests
from bs4 import BeautifulSoup
import csv
from google.colab import files

# Set the base URL for the search
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"

# Create an empty list to store the scraped data
data = []

# Iterate over 20 pages
for page in range(1, 21):
    # Construct the URL for the current page
    url = base_url + str(page)

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the desired product elements
    product_list = soup.find_all('div', class_='sg-col-inner')

    # Iterate over each product element
    for product in product_list:
        # Find the title element
        title_element = product.find('span', class_='a-size-medium a-color-base a-text-normal')
        title = title_element.text.strip() if title_element else ''

        # Find the price element
        price_element = product.find('span', class_='a-price-whole')
        price = price_element.text.strip() if price_element else ''

        # Find the rating element
        rating_element = product.find('span', class_='a-icon-alt')
        rating = rating_element.text.strip() if rating_element else ''

        # Find the product URL
        url_element = product.find('a', class_='a-link-normal a-text-normal')
        product_url = 'https://www.amazon.in' + url_element['href'] if url_element else ''

        # Send a GET request to the product URL
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        # Find the description
        description_element = product_soup.find('div', id='feature-bullets')
        description = description_element.get_text(strip=True) if description_element else ''

        # Find the ASIN
        asin_element = product_soup.find('th', string='ASIN')
        asin = asin_element.find_next_sibling('td').get_text(strip=True) if asin_element else ''

        # Find the product description
        product_description_element = product_soup.find('div', id='productDescription')
        product_description = product_description_element.get_text(strip=True) if product_description_element else ''

        # Find the manufacturer
        manufacturer_element = product_soup.find('a', id='bylineInfo')
        manufacturer = manufacturer_element.get_text(strip=True) if manufacturer_element else ''

        # Append the data to the list
        data.append([product_url, title, price, rating, description, asin, product_description, manufacturer])

# Create the CSV file and write the data
with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])  # Write header row
    writer.writerows(data)

# Download the CSV file in Google Colab
files.download('data.csv')
