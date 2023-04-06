from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
import requests
from bs4 import BeautifulSoup 
from .constants import *
from .document_preprocess import *
from .web_scrape import *
from .rank_documents import *
from .cluster import *
from .rochio import rocchio_algorithm
import pandas as pd
import numpy as np
from .models import Products

filename = 'retrieved_products.csv'

def home(request):
    if request.method == "POST":
        f = open(filename, 'w', encoding='UTF8', newline='')
        writer = csv.writer(f)
        # writer.writerow(["Index", "Product Name", "Price", "Website"])
        product_name = preprocess(request.POST.get("product_name"))
        request.session["input_product"] = product_name
        if Products.objects.filter(query = product_name).exists():
            return redirect("display_products")
        else:
            product_list_flipkart = web_scrape(writer, FLIPKART_URL, product_name, FLIPKART_PRODUCT_DIV, 
            FLIPKART_PRICE_DIV, FLIPKART_TITLE_DIV, FLIPKART_PRODUCT_LINK )

            product_list_snapdeal = web_scrape(writer, SNAPDEAL_URL, product_name, SNAPDEAL_PRODUCT_DIV, 
            SNAPDEAL_PRICE_DIV, SNAPDEAL_TITLE_DIV, SNAPDEAL_PRODUCT_LINK)

            f.close()
            return redirect("display_products")

    return render(request,"home.html")

def display_products(request, **kwargs):
    product_name = request.session.get("input_product")

    # If user has submitted relevance feedback already
    if Products.objects.filter(query = product_name, relevant = True).exists():
        rps = Products.objects.filter(query = product_name, relevant = True)
        relevant_products = pd.DataFrame.from_records(rps.values_list())
        relevant_products.columns = [col for col in rps[0].__dict__.keys()][1:]
        recommended_products = relevant_products.to_numpy()

    else:
        rps = Products.objects.filter(query = product_name) 
        total_products = pd.DataFrame.from_records(rps.values_list())
        total_products.columns = [col for col in rps[0].__dict__.keys()][1:]
        # Rank the documents in accordance with relevance
        ranked_documents = get_ranked_documents(total_products["product_name"], product_name)

        # Find top  10 relevant products
        recommended_products = total_products[total_products['product_name'].isin(list(zip(*ranked_documents[0:10]))[0])].to_numpy()        
        recommended_products = recommended_products[recommended_products[:, 2].argsort()]
    
    if request.method == "POST":
        checked_items = request.POST.getlist("relevant_products")
        relevant_indices = [int(x) - 1 for x in checked_items]
        irrelevant_indices = [i for i in range(10) if i not in relevant_indices]
        new_relevant_docs = rocchio_algorithm(recommended_products[:, 1], product_name, relevant_indices, irrelevant_indices)
        titles = list(recommended_products[:, 1])
        for title in titles:
            change = Products.objects.get(query = product_name, product_name=title)
            change.relevant=True
            change.save()
        # recommended_products = list(recommended_products)
        # final_recommended_products = [recommended_products[titles.index(x)] for x in new_relevant_docs]
        rps = Products.objects.filter(query = product_name, relevant = True)
        relevant_products = pd.DataFrame.from_records(rps.values_list())
        relevant_products.columns = [col for col in rps[0].__dict__.keys()][1:]
        final_recommended_products = relevant_products.to_numpy()
        
        return render(request, "display_products.html",{'products': final_recommended_products[0:5]})
    # Display top 5 cheapest products
    return render(request, "display_products.html",{'products': recommended_products[0:5]})
