from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup 

flipkart_url = "https://www.flipkart.com/search?q="
shopclues_url = "https://www.shopclues.com/search?q="

def web_scrape(url, product_name):
    webpage = requests.get(url+product_name)
    soup = BeautifulSoup(webpage.content, "html.parser")
    text = soup.get_text().strip()
    print(text)

def home(request):
    product_name=request.POST.get("product_name")
    web_scrape(flipkart_url, product_name)
    web_scrape(shopclues_url, product_name)
    return render(request,"home.html")