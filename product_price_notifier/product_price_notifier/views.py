from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup 
from .constants import *
from .document_preprocess import *
from .web_scrape import *



def home(request):
    if request.method == "POST":
        product_name = preprocess(request.POST.get("product_name"))
        product_list_flipkart = web_scrape(FLIPKART_URL, product_name, FLIPKART_PRODUCT_DIV, 
        FLIPKART_PRICE_DIV, FLIPKART_TITLE_DIV)
        print(product_name)
        print(product_list_flipkart)
        
    return render(request,"home.html")