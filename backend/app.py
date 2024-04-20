from flask import Flask, request, jsonify
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time  # Import the time module

app = Flask(__name__)

# Load pre-trained BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

@app.route('/', methods=['GET'])
def home():
    return "Hello, world!"

@app.route('/predict_sentiment', methods=['POST'])
def predict_sentiment():
    try:
        # Get data and type from JSON input
        data = request.json.get('data', '')
            # If data type is text, perform sentiment analysis
        review = data
        tokens = tokenizer.encode(review, return_tensors='pt')
        with torch.no_grad():
            result = model(tokens)
        sentiment_score = int(torch.argmax(result.logits)) + 1
        senticlass = get_sentiment_class(sentiment_score)
        return jsonify({'sentiment_score': sentiment_score, 'sentiment_class': senticlass})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/upload', methods=['POST'])
def upload():
    if 'text_data' not in request.form:
        return jsonify({"error": "No text data provided"}), 400

    text_data = request.form['text_data']
    print("Received text data:", text_data)

    return jsonify({"message": "Text data received and printed successfully"}), 200


def get_sentiment_class(sentiment_score):
    # Define your sentiment classes based on the sentiment score
    # Adjust this function based on your specific requirements
    # Example:
    if sentiment_score == 1:
        return 'Strongly negative'
    elif sentiment_score == 2:
        return 'Mildly negative'
    elif sentiment_score == 3:
        return 'Neutral'
    elif sentiment_score == 4:
        return 'Mildly positive'
    elif sentiment_score == 5:
        return 'Strongly positive'
    else:
        return 'Unable to process please try with a better review'

if __name__ == '__main__':
    app.run(debug=True)