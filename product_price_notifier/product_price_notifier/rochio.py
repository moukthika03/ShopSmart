import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import math

# Sample list of strings
def term_frequency_matrix(s):
    vectorizer = CountVectorizer()
    tf_matrix = vectorizer.fit_transform(s).toarray()
    return tf_matrix

def cosine_similarity(doc_vec, query):
    numerator = sum([doc_vec[x] * query[x] for x in range(len(doc_vec))])
    sum1 = sum([x**2 for x in doc_vec])
    sum2 = sum([x**2 for x in query])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# documents is a 2D array representing the term frequency matrix for all documents
# query is a 1D array representing the term frequency vector for the query
# relevant_docs is a list of indices of the relevant documents
# irrelevant_docs is a list of indices of the irrelevant documents
# alpha, beta, and gamma are tuning parameters
def rocchio_algorithm(documents, query, relevant_docs, irrelevant_docs, alpha=1, beta=0.75, gamma=0.25):
    documents_in_string = documents
    documents = np.append(documents, query)
    # print(documents)
    documents = term_frequency_matrix(documents)
    query = documents[len(documents)-1]
    documents = documents[0:len(documents)-1]
    # print(documents)
    # print("Query")
    # print(query)

    # Compute the centroid of the relevant documents
    relevant_centroid = np.mean(documents[relevant_docs], axis=0)

    # # Compute the centroid of the irrelevant documents
    irrelevant_centroid = np.mean(documents[irrelevant_docs], axis=0)

    # # Update the query vector using the Rocchio Algorithm
    new_query = alpha * query + beta * relevant_centroid - gamma * irrelevant_centroid
    cosine_similarity_list = [cosine_similarity(x, new_query) for x in documents]
    cosine_similarity_list_copy = [cosine_similarity(x, new_query) for x in documents]
    cosine_similarity_list.sort(reverse = True)
    documents = list(documents)
    relevant_docs = [documents_in_string[cosine_similarity_list_copy.index(x)] for x in cosine_similarity_list]
    return relevant_docs
