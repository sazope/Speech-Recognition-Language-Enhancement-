from flask import Flask, render_template, request
import openai
import os
import torch
import numpy as np
import whisper

app = Flask(__name__)
openai.api_key = "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"
model = whisper.load_model("base")

# Define the predict_words function that uses the OpenAI GPT-3 model
prompt1 = """
You are good at completing sentences. Given a few keyboard inputs, 
I want you to give three options as an output which predicts the next words and forms three sentences. 
Input: {}
Output: 
"""

def predict_words(prompt1):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt1,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]['text'].replace('\n', '')

# Define the route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for the words prediction form
@app.route('/words')
def words():
    return render_template('predict_words.html')

# Define the route for processing the words prediction
@app.route('/predict_words', methods=['POST'])
def process_predict_words():
    input_text = request.form['input_text'] 
    prompt_input = prompt1.format(input_text)
    output_text = predict_words(prompt_input)
    print(output_text) # added for debugging
    return render_template('predict_words_result.html', input_text=input_text, output_text=output_text)

if __name__ == '__main__':
    app.run(debug=True)
