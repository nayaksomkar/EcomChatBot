"""
NLP processing utilities for EcomChatBot.
Provides functions for text preprocessing, translation, spell correction,
and response generation.
"""

import nltk
import numpy as np
import json
import random

from autocorrect import Speller
from googletrans import Translator
from nltk.stem import WordNetLemmatizer

# Initialize NLP components
lemmatizer = WordNetLemmatizer()
translator = Translator()
spell = Speller()

# Load intent definitions from JSON
with open('response.json') as file:
    intents = json.load(file)


def standardQuery(query):
    """
    Translate input text to English.
    
    Args:
        query: The input string in any language.
        
    Returns:
        str: The translated English text.
    """
    translation = translator.translate(query, dest='en', src='auto')
    return translation.text


def processedQuery(query):
    """
    Apply spell correction to the input query.
    
    Args:
        query: The input string to correct.
        
    Returns:
        str: The spell-corrected string.
    """
    corrected_sentence = spell(query)
    print(f"Corrected Sentence: {corrected_sentence}")
    return corrected_sentence


def bow(sentence, words, show_details=False):
    """
    Convert a sentence to a bag-of-words vector.
    
    Args:
        sentence: The input sentence to tokenize.
        words: The vocabulary list.
        show_details: Whether to print debug information.
        
    Returns:
        numpy.ndarray: Binary vector representing word presence.
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1

    if show_details:
        print(f"Sentence: {sentence}")
        print(f"Bag of Words: {bag}")
    
    return np.array(bag)


def generate_response(tag, confidence):
    """
    Generate a response based on the predicted intent tag.
    
    Args:
        tag: The predicted intent label.
        confidence: The model's confidence score.
        
    Returns:
        str: A response string from the matching intent.
    """
    print(f"Generating response for tag: {tag}")
    for intent in intents['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            print(f"Selected response: {response}")
            return response
        
    print("No matching intent found")
    return f"I'm not sure how to respond to that. (Predicted intent: {tag}, confidence: {confidence:.2f})"