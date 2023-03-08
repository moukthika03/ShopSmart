# Document preprocessing steps
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

def text_lowercase(text):
	return text.lower()

def remove_punctuation(text):
	translator = str.maketrans('', '', string.punctuation)
	return text.translate(translator)

def remove_stopwords(text):
	stop_words = set(stopwords.words("english"))
	word_tokens = word_tokenize(text)
	filtered_text = [word for word in word_tokens if word not in stop_words]
	return ' '.join(filtered_text)

stemmer = PorterStemmer()
def stem_words(text):
	word_tokens = word_tokenize(str(text))
	stems = [stemmer.stem(word) for word in word_tokens]
	return ' '.join(stems)

lemmatizer = WordNetLemmatizer()
def lemmatize_word(text):
	word_tokens = word_tokenize(str(text))
	lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in word_tokens]
	return ' '.join(lemmas)

