import nltk
import numpy as np
import json
import random

from autocorrect import Speller
from googletrans import Translator
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer() # Initialize the lemmatizer
translator = Translator() # Initialize the translator
spell = Speller() # Initialize spell checker

with open('response.json') as file: # Load intents from the JSON file
    intents = json.load(file)

def standardQuery(query):
    # Translate the input text to English (US)
    translation = translator.translate(query, dest='en', src='auto')
    return translation.text

def processedQuery(query):
    corrected_sentence = spell(query)  # Correct spelling errors
    print(f"Corrected Sentence: {corrected_sentence}")
    return corrected_sentence

def bow(sentence, words, show_details=False):
    sentence_words = nltk.word_tokenize(sentence) # Tokenize and lemmatize the sentence
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

    bag = [0] * len(words)  # Create the bag of words array
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1

    if show_details:
        print(f"Sentence: {sentence}")
        print(f"Bag of Words: {bag}")
    
    return np.array(bag)

def generate_response(tag, confidence):
    print(f"Generating response for tag: {tag}")
    for intent in intents['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            print(f"Selected response: {response}")
            return response
        
    print("No matching intent found")
    return f"I'm not sure how to respond to that. (Predicted intent: {tag}, confidence: {confidence:.2f})"