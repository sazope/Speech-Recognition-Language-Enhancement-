from flask import Flask, render_template, request
import openai
import os
import torch
import numpy as np
import whisper
import openai

app = Flask(__name__)
openai.api_key = "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"
model = whisper.load_model("base")

# Define the spell_check function that uses the OpenAI GPT-3 model
prompt = """
Given a few keyboard inputs, I want you to put together a sentence which makes sense as per the inputs.

Input: {}

Output: 
"""
def spell_check(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
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
    return render_template('index_spell.html')

@app.route('/spell')
def spell():
    return render_template('spell_check.html')

# Define the route for processing the spell check
@app.route('/spell_check', methods=['POST'])
def process_spell_check():
    input_text = request.form['input_text'] 
    prompt_input = prompt.format(input_text)
    output_text = spell_check(prompt_input)
    return render_template('spell_check_result.html', input_text=input_text, output_text=output_text)

if __name__ == '__main__':
    app.run(debug=True)
