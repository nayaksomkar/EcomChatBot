"""
Neural network model training script for EcomChatBot.
Builds and trains a Keras model for intent classification.
"""

import pickle

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.optimizers import gradient_descent_v2
from responsefunction import *

# Download required NLTK data packages
nltk.download('punkt')
nltk.download('wordnet')

# Initialize containers for training data
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Process the intents from JSON and create training documents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and lowercase each word, then remove duplicates
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# Serialize vocabulary and classes for later use
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create bag-of-words training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Shuffle training data and convert to numpy array
random.shuffle(training)
training = np.array(training, dtype=object)

# Separate features and labels
train_x = np.array([item[0] for item in training])
train_y = np.array([item[1] for item in training])

# Build the neural network model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Configure training parameters
sgd = gradient_descent_v2.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Persist the trained model
model.save('responseEngine.h5')
print("Model trained and saved successfully!")
model.summary()