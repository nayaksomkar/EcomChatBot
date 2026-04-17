"""
Flask backend server for the EcomChatBot application.
Handles API requests and integrates with the trained NLP model.
"""

import pickle

from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.python.keras.models import load_model
from responsefunction import *

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Load the trained model and associated data files
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('responseEngine.h5')


def predict_class(sentence):
    """
    Predict the intent class of a user query.
    
    Args:
        sentence: The input query string.
        
    Returns:
        tuple: Predicted class label and confidence score.
    """
    bow_sentence = bow(sentence, words, show_details=True)
    prediction = model.predict(np.array([bow_sentence]))[0]
    max_index = np.argmax(prediction)
    predicted_class = classes[max_index]
    confidence = prediction[max_index]
    
    print(f"Predicted class: {predicted_class}")
    print(f"Confidence: {confidence}")
    
    return predicted_class, confidence


def process_query(query):
    """
    Process a user query through the complete NLP pipeline.
    
    Args:
        query: The raw user input string.
        
    Returns:
        str: The generated response from the chatbot.
    """
    print(f"Processing query: {query}")
    corrected_query = processedQuery(standardQuery(query))
    intent, confidence = predict_class(corrected_query)
    response = generate_response(intent, confidence)

    # Log the query and response to a file
    with open('response.txt', 'a') as f:
        f.write(f"User Query: {query}\n")
        f.write(f"Corrected Query: {corrected_query}\n")
        f.write(f"Response: {response}\n")
        f.write(f"Confidence: {confidence:.2f}\n")
        f.write("-" * 40 + "\n")
        
    return response


@app.route('/chat', methods=['POST'])
def chat():
    """
    API endpoint for chat interactions.
    
    Expects a JSON body with a 'message' field.
    Returns a JSON response with the chatbot's reply.
    """
    user_query = request.json.get('message')
    print(f"User query: {user_query}")
   
    response = process_query(user_query)
    return jsonify({"response": response})


if __name__ == '__main__':
    print("Loaded words:", words[:10], "...")
    print("Loaded classes:", classes)
    print("Number of intents:", len(intents['intents']))
    app.run(debug=True)