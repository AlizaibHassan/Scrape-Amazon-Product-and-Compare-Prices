import requests
from bs4 import BeautifulSoup
import csv

def get_amazon_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data
        title_element = soup.find('span', {'id': 'productTitle'})
        print(title_element)
        title = title_element.get_text(strip=True) if title_element else 'N/A'

        description_element = soup.find('meta', {'name': 'description'})
        description = description_element['content'] if description_element else 'N/A'

        asin_element = soup.find('th', string='ASIN')
        asin = asin_element.find_next('td').get_text(strip=True) if asin_element else 'N/A'

        price_element = soup.find('span', {'id': 'priceblock_ourprice'})
        if price_element is None:
            price_element = soup.find('span', {'id': 'priceblock_dealprice'})
        if price_element is None:
            price_element = soup.find('span', {'id': 'priceblock_saleprice'})
        price = price_element.get_text(strip=True) if price_element else 'N/A'

        return {'Title': title, 'Description': description, 'ASIN': asin, 'Price': price}

    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None


def scrape_amazon_urls(input_file, output_file):
    with open(input_file, 'r') as f:
        urls = f.read().splitlines()

    data_list = []

    for url in urls:
        amazon_data = get_amazon_data(url)
        if amazon_data:
            data_list.append(amazon_data)

    if data_list:
        # Writing data to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Title', 'Description', 'ASIN', 'Price']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Writing header
            writer.writeheader()

            # Writing data rows
            for data in data_list:
                writer.writerow(data)

        # Calculate and print statistics
        prices = [float(data['Price'].replace('$', '').replace(',', '')) for data in data_list if data['Price'] != 'N/A']
        if prices:
            avg_price = sum(prices) / len(prices)
            max_price = max(prices)
            min_price = min(prices)

            print(f"Average Price: ${avg_price:.2f}")
            print(f"Max Price: ${max_price:.2f}")
            print(f"Min Price: ${min_price:.2f}")

if __name__ == '__main__':
    scrape_amazon_urls('input.txt', 'output.csv')
