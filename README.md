# EcomChatBot

An intelligent e-commerce chatbot built with Natural Language Processing (NLP) techniques, integrated within a Flask API. This chatbot leverages deep learning and various NLP libraries to provide natural, context-aware customer interactions.

[EcomChatBot Demo](https://raw.githubusercontent.com/nayaksomkar/EcomChatBot/main/EcomChatBot.mov)

## Features

- **Multilingual Support**: Handles customer queries in multiple languages using Google Translate integration
- **Intelligent Spell Correction**: Automatically fixes typos and spelling mistakes using the `autocorrect` library
- **Advanced Intent Classification**: Uses deep learning to accurately identify customer intents
- **Context-Aware Conversations**: Maintains conversation context for more natural interactions
- **Neural Network Backend**: Powered by Keras with TensorFlow for robust intent classification

## Prerequisites

- Python 3.7+
- pip package manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nayaksomkar/EcomChatBot
   cd EcomChatBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup and Running

1. **Train the Model** (if not already trained):
   - Run `responseEngine.py` to train the model on your data
   - This will generate required binary files and the model file (`responseEngine.h5`)
   - Training uses the `response.json` file for intent data

2. **Start the Backend**:
   - Run `backend.py` to start the test server
   - This establishes the connection between frontend and backend

3. **Launch the Frontend**:
   - Open `index.html` in a web browser
   - The chatbot interface will connect to the backend server
   - Start interacting with the chatbot!

## Model Training

The chatbot uses a neural network model for intent classification. If you want to train it on new data:
1. Update the `response.json` file with your custom intents and responses
2. Run `responseEngine.py` to generate a new model
3. The new model will be saved as `responseEngine.h5`

