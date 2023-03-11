from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

def cluster_documents(documents):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    true_k = 6
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    title=[]
    labels = model.labels_
    clustered_documents = pd.DataFrame(list(zip(documents, labels)), columns=['title','cluster'])
    return clustered_documents.sort_values(by=['cluster'])