""" scraping price of a product 
    used library: beatifulsoup, request, unicodata???
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas
from lxml import etree as et
import csv
from sending_email import send_email


# adding a header to avoid the anti scraping from amazon
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

product_list = ['https://www.amazon.com/Headphones-Surround-Effects-Karaoke-Earphones/dp/B09LHMHVY2/',
                'https://www.amazon.com/Singtrix-Bundle-Premium-Karaoke-System/dp/B00JBJ2HNO/'
                ]

def get_name(dom):
    try:
        name = dom.xpath('//span[@id="productTitle"]/text()')
        name = [name.strip(' ') for name in name][0]
        return name
    except:
        print('N/A')
        return None

def get_price(dom):
    try:
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        return float(price.replace(",", "").replace("$", "").replace(".00", ""))   
    except:
        print('N/A')
        return None


if __name__ == '__main__':
    with open('amazon_price_tracking.csv', 'w') as price_file:
        writer = csv.writer(price_file)
        writer.writerow(['Product', 'Price', 'Link'])
        message = ''
        for url in product_list:
            response = requests.get(url, headers=HEADER)    
            soup = BeautifulSoup(response.content, 'html.parser')
            dom = et.HTML(str(soup))

            name = get_name(dom)
            price = get_price(dom)

            writer.writerow([name, price, url])
            
            message += f"{name}\n"
            message += f"Price: ${price}\n"
            message += f"{url}\n\n"
        send_email(message)
    

    
