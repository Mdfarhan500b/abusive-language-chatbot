import pickle
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def load_offensive_words(file_path):
    """Load offensive words from file with validation"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [line.strip().lower() for line in f if line.strip() and len(line.strip()) > 1]
            print(f"Loaded {len(words)} words from {file_path}")  # Debugging
            return words
    except FileNotFoundError:
        print(f"File not found: {file_path}")  # Debugging
        return []

# Load and combine offensive words
english_words = load_offensive_words('data/offensive_words_english.txt')
hindi_words = load_offensive_words('data/offensive_words_hindi.txt')
bengali_words = load_offensive_words('data/offensive_words_bengali.txt')
offensive_words = english_words + hindi_words + bengali_words
print(f"Total offensive words loaded: {len(offensive_words)}")  # Debugging

# Load model assets
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
except Exception as e:
    print(f"Error loading model files: {str(e)}")
    model = None
    vectorizer = None

def contains_offensive_language(text):
    """Check for offensive content using exact word matching and return list of detected words"""
    text_lower = text.lower()
    print(f"Checking text: {text_lower}")  # Debugging
    
    detected_words = []
    # Check against offensive words list
    for word in offensive_words:
        if re.search(rf'\b{re.escape(word)}\b', text_lower):
            print(f"Offensive word detected: {word}")  # Debugging
            detected_words.append(word)
    
    return detected_words

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    try:
        if not request.json or 'message' not in request.json:
            return jsonify({'response': 'Invalid request', 'color': 'blue'})
            
        user_message = request.json['message'].strip()
        
        if not user_message:
            return jsonify({'response': 'Empty message', 'color': 'blue'})
        
        # Convert to lowercase once
        user_message_lower = user_message.lower()
          # 1. Check for special whitelisted phrases first
        if "how are you" in user_message_lower:
            # Only flag if other offensive content exists
            detected_words = contains_offensive_language(user_message_lower)
            if detected_words:
                response = "I detected offensive language in your message. Please keep our conversation respectful."
                return jsonify({
                    'response': response, 
                    'color': 'red',
                    'detected_words': detected_words
                })
            response = "Thank you for your message. It appears to be appropriate and respectful."
            return jsonify({'response': response, 'color': 'green', 'detected_words': []})
        
        # 2. Check against offensive words list
        detected_words = contains_offensive_language(user_message_lower)
        if detected_words:
            response = "I detected offensive language in your message. Please keep our conversation respectful."
            return jsonify({
                'response': response, 
                'color': 'red',
                'detected_words': detected_words
            })
        
        # 3. Fall back to model prediction if available
        if model and vectorizer:
            try:
                user_message_tfidf = vectorizer.transform([user_message])
                proba = model.predict_proba(user_message_tfidf)[0]
                
                # Only flag if high confidence (adjust threshold as needed)
                if proba[1] > 0.7:  # 70% confidence threshold                    response = "I detected offensive language in your message. Please keep our conversation respectful."
                    return jsonify({'response': response, 'color': 'orange', 'detected_words': ["AI detected offensive content"]})
            except Exception as e:
                print(f"Model prediction error: {str(e)}")
        
        # Default to non-offensive
        response = "Thank you for your message. It appears to be appropriate and respectful."
        return jsonify({'response': response, 'color': 'green', 'detected_words': []})
        
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return jsonify({'response': 'Error processing your message.', 'color': 'blue'})

if __name__ == '__main__':
    app.run(debug=True)