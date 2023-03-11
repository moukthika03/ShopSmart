from .document_preprocess import *
import requests
from bs4 import BeautifulSoup 
import csv
import hashlib

def preprocess(text):
    lt = text_lowercase(text)
    rp = remove_punctuation(lt)
    rs = remove_stopwords(lt)
    return lt

def web_scrape(writer, url, product_name, product_div, price_div, title_div):
    webpage = requests.get(url+product_name)
    soup = BeautifulSoup(webpage.content, "html.parser")

    product_price = {}

    prices= [td.find(class_= price_div) for td in soup.findAll("div", class_= product_div)]
    titles = [td.find(class_= title_div) for td in soup.findAll("div", class_= product_div)]

    # Extracting prices
    refined_prices=[]
    for price in prices:
        price = price.get_text() 
        if "rs." in price or "Rs." in price:
            price = price[3:]
        elif "₹" in price:
            price = price[1:]
        price = price.replace(",","")
        refined_prices.append(float(price.strip()))

    # Extracting titles
    refined_titles = []
    for title in titles:
        title = preprocess(title['title'])
        refined_titles.append(title)

    for i in range(0, len(refined_prices)):
        writer.writerow([hashlib.sha256(refined_titles[i].encode('utf-8')), refined_titles[i], refined_prices[i], url])
        product_price[refined_titles[i]] = refined_prices[i]
    return product_price