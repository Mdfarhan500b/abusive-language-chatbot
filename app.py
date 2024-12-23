import pickle
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# List of predefined offensive words
offensive_words = ["fuck", "kill", "fool", "asshole", "bitch", "damn", "bastard", "whore", "slut", "pussy", "dickhead", "cunt"]

# Load the trained model and vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html exists in 'templates' folder

# Route for handling user messages
@app.route('/get-response', methods=['POST'])
def get_response():
    try:
        user_message = request.json['message']  # Get the message from the user

        # First, check if the message contains "how are you" without considering offensive words
        if "how are you" in user_message.lower():
            if any(offensive_word in user_message.lower() for offensive_word in offensive_words):
                return jsonify({'response': 'This message contains offensive language.', 'color': 'red'})
            return jsonify({'response': 'This message is not offensive.', 'color': 'green'})

        # Check for predefined offensive words
        if any(offensive_word in user_message.lower() for offensive_word in offensive_words):
            return jsonify({'response': 'This message contains offensive language.', 'color': 'red'})

        # If no predefined offensive words, check using the model
        user_message_tfidf = vectorizer.transform([user_message])  # Convert the message into TF-IDF format
        prediction = model.predict(user_message_tfidf)  # Get the model's prediction

        # Respond based on the prediction
        if prediction == 1:  # Assuming 1 represents offensive language
            return jsonify({'response': 'This message contains offensive language.', 'color': 'red'})
        else:
            return jsonify({'response': 'This message is not offensive.', 'color': 'green'})

    except Exception as e:
        # If there's an error in processing the request, return an error message
        return jsonify({'response': f'Error: {str(e)}', 'color': 'green'})

if __name__ == '__main__':
    app.run(debug=True)
