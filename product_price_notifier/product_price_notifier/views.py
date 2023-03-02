from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup 

flipkart_url = "https://www.flipkart.com/search?q="
shopclues_url = "https://www.shopclues.com/search?q="

def web_scrape(url, product_name):
    webpage = requests.get(url+product_name)
    soup = BeautifulSoup(webpage.content, "html.parser")
    # print(soup.prettify())
    text = soup.get_text().strip()
    prices = soup.find_all("div", class_= '_30jeq3')
    refined_prices=[]
    for price in prices:
        price = price.get_text() # Will get text from html tags
        price = price[1:]
        price = price.replace(",","")
        refined_prices.append(float(price.strip())) # Removing special characters like \n (newline)
    print(refined_prices)

def home(request):
    if request.method == "POST":
        product_name=request.POST.get("product_name")
        web_scrape(flipkart_url, product_name)
        
    return render(request,"home.html")