from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup 
from .constants import *
from .document_preprocess import *
from .web_scrape import *
from .rank_documents import *
from .cluster import *
import pandas as pd

filename = 'retrieved_products.csv'

def home(request):
    if request.method == "POST":
        f = open(filename, 'w', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(["Index", "Product Name", "Price", "Website"])
        product_name = preprocess(request.POST.get("product_name"))
        product_list_flipkart = web_scrape(writer,FLIPKART_URL, product_name, FLIPKART_PRODUCT_DIV, 
        FLIPKART_PRICE_DIV, FLIPKART_TITLE_DIV)

        product_list_snapdeal= web_scrape(writer,SNAPDEAL_URL, product_name, SNAPDEAL_PRODUCT_DIV, 
        SNAPDEAL_PRICE_DIV, SNAPDEAL_TITLE_DIV)

        f.close()
        total_products = pd.read_csv(filename)

        # Rank the documents in accordance with relevance
        ranked_documents = get_ranked_documents(total_products["Product Name"], product_name)
        print(ranked_documents)

        # Cluster the documents - used in user relevance feedback
        clustered_documents = cluster_documents(total_products["Product Name"])

        # Find top 5 cheapest products in top 10 relevant products
        recommended_products = total_products[total_products['Product Name'].isin(list(zip(*ranked_documents[0:10]))[0])].to_numpy()
        recommended_products = recommended_products[recommended_products[:, 2].argsort()]

        return render(request, "display_products.html",{'products': recommended_products[0:5]})

    return render(request,"home.html")