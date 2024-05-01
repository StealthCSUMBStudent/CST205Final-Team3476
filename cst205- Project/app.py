from flask import Flask, render_template, request
import requests

app = Flask(__name__)

open_ai_key = 'sk-proj-gd0elrXdmLbvGSWqbujDT3BlbkFJI3PTDMXa5lyk6WxD6GWf'

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    if request.method == 'POST':
        author = request.form.get('author')
        response = requests.get('https://picsum.photos/v2/list')
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/ai')
def aiGeneration():
    endpoint = 'https://api.openai.com/v1/images/generations'
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {open_ai_key}'
    }
    params = {
        'model': 'dall-e-3',
        'prompt': 'a white fox',
    }

    response = requests.post(endpoint, json=params, headers=header)

    print(response.json())
    return render_template('index.html')
