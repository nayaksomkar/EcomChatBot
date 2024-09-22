import pickle

from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.python.keras.models import load_model
from responsefunction import *

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load the words and classes
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('responseEngine.h5') # Load the trained model

def predict_class(sentence): # Predict the class of the sentence
    bow_sentence = bow(sentence, words, show_details=True)
    prediction = model.predict(np.array([bow_sentence]))[0]
    max_index = np.argmax(prediction)
    predicted_class = classes[max_index]
    confidence = prediction[max_index]
    
    print(f"Predicted class: {predicted_class}")
    print(f"Confidence: {confidence}")
    
    return predicted_class, confidence

def process_query(query):
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
    user_query = request.json.get('message')  # Get the message from the request
    print(f"User query: {user_query}")  # Print the user query on the server-side
   
    response = process_query(user_query)  # Process the query and generate a response
    return jsonify({"response": response})

if __name__ == '__main__':
    print("Loaded words:", words[:10], "...")  # Print first 10 words
    print("Loaded classes:", classes)
    print("Number of intents:", len(intents['intents']))
    app.run(debug=True)