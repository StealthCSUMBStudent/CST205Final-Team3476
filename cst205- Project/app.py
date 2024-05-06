from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your Pixabay API key
API_KEY = '43673995-6b601f29737528af485dab3da'
SEARCH_TERM = 'germany'

@app.route('/')
def index():
    images = []
    unique_tags = []  

    author = request.args.get('author') 

    if author:
        response = requests.get(f"https://pixabay.com/api/?key={API_KEY}&q={author}")
        if response.status_code == 200:
            data = response.json()
            print(data)  
            for image in data['hits']:
                images.append(image['webformatURL'])
                tags = image['tags'].split(',')
                for tag in tags:
                    tag = tag.strip()
                    if tag not in unique_tags:
                        unique_tags.append(tag)
            print(images)  
            print(unique_tags)  
        else:
            print("Failed to retrieve data from Pixabay API")
    
    return render_template('index.html', images=images, unique_tags=unique_tags)


if __name__ == '__main__':
    app.run(debug=True)
