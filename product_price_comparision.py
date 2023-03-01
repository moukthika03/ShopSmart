import requests
from bs4 import BeautifulSoup #For web scraping
flipkart_product_url = "https://www.amazon.in"
webpage = requests.get(flipkart_product_url)
soup = BeautifulSoup(webpage.content, "html.parser")
print(soup.prettify())

text = soup.get_text().strip() # Will get text from html tags
# print(text)