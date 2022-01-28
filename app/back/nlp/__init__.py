import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.corpus import stopwords
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from langdetect import detect

model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("fr_core_news_md")

words_before_departure = ['de', 'depuis', 'provenance']
words_before_destination = ['à', 'a', 'en', 'jusqu\'a', 'vers', 'par']
example_travel_sentence = ['Je veux prendre un train de paris à lyon']


def get_cities(sentence):
    """ Take a sentence and return all cities within

    Args:
        sentence (str): any sentence

    Returns:
        Array: A list of cities
    """
    cities = []
    doc = nlp(sentence)
    for entity in doc.ents:
        if entity.label_ == "LOC":
            cities.append(entity.text)
    
    return cities


def extract_travel_request(sentences):
    """ Take a list of sentences and return the sentence
        containing a request to travel by train

    Args:
        sentences (Array<str>): List of sentences

    Returns:
        str: travel request sentence or SPAM
    """
    # model must already be loaded

    sentence_embeddings = model.encode(sentences)
    real_sentence_embedding = model.encode(example_travel_sentence)
    similarities = cosine_similarity(
        [real_sentence_embedding[0]],
        sentence_embeddings
    )
    biggest_number = max(similarities[0])
    if biggest_number < 0.75:
        return False
    best_sentence_ind = np.where(similarities[0] == biggest_number)
    return sentences[best_sentence_ind[0][0]]


def determine_departure_destination(sentence):
    """ Take a travel request sentence and
        return the departure and destination

    Args:
        sentence (str): Travel request sentence

    Returns:
        dict: departure and destination as keys
    """
    departure = []
    destination = []
    cities = get_cities(sentence)
    words = word_tokenize(sentence)
    # print("SENTENCE ", sentence)
    # print("CITIES ", cities)
    # print("WORDS ", words)
    for city in cities:
        index = words.index(city)
        if index == 0: continue
        if words[index-1] in words_before_departure: departure.append(city)
        elif words[index-1] in words_before_destination: destination.append(city)
    
    return {
        "departure": departure,
        "destination": destination
    }


def is_french(text):
    """
    Determine if the text provided is in french
    Args:
        text (str): text to analyze

    Returns: True if french or False if not

    """
    return 'fr' == detect(text)


def extract_travel_info(sentences):
    """
    Extract the required information for the text to determine
    the departure and destination
    Args:
        sentences (list<str>): list of sentences

    Returns:
        dict: departure and destination if there is a travel request
        OR False if the given sentences are not valid

    """
    if not is_french(sentences[0]):
        return False

    travel_request = extract_travel_request(sentences)
    if not travel_request:
        return False

    return determine_departure_destination(travel_request)


