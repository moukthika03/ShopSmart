import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def term_frequency_matrix(documents):
    tfidf = TfidfVectorizer()
    result = tfidf.fit_transform(documents)
    print(result)

# documents is a 2D array representing the term frequency matrix for all documents
# query is a 1D array representing the term frequency vector for the query
# relevant_docs is a list of indices of the relevant documents
# irrelevant_docs is a list of indices of the irrelevant documents
# alpha, beta, and gamma are tuning parameters
def rocchio_algorithm(documents, query, relevant_docs, irrelevant_indices, alpha=1, beta=0.75, gamma=0.25):
    documents = term_frequency_matrix(documents)
    
    # Compute the centroid of the relevant documents
    relevant_centroid = np.mean(documents[relevant_docs], axis=0)

    # # Compute the centroid of the irrelevant documents
    irrelevant_centroid = np.mean(documents[irrelevant_docs], axis=0)

    # # Update the query vector using the Rocchio Algorithm
    new_query = alpha * query + beta * relevant_centroid - gamma * irrelevant_centroid

    return new_query
