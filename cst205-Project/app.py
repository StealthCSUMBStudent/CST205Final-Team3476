'''
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    if request.method == 'POST':
        author = request.form.get('author')
        response = requests.get('https://picsum.photos/v2/list')
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

class Playlist(FlaskForm):
    author_title = StringField(
        'Author Search', 
        validators=[DataRequired()]
    )

authors = []

def store_author(my_author):
    authors.append(dict(
        author = my_author,
        date = datetime.today()
    ))

@app.route('/', methods=('GET', 'POST'))
def index():
    form = Playlist()
    if form.validate_on_submit():
        store_author(form.author_title.data)
        return redirect('/view_playlist')
    return render_template('index.html', form=form)

@app.route('/view_playlist')
def vp():
    lowercase_authors = [{'author': item['author'].lower(), 'date': item['date']} for item in authors]
    return render_template('ImageType.html', authors=lowercase_authors)
'''
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

    author = request.args.get('author')  # Extract author from query parameters

    if author:
        response = requests.get(f"https://pixabay.com/api/?key={API_KEY}&q={author}")
        if response.status_code == 200:
            data = response.json()
            print(data)  # Debug print statement to check fetched data
            for image in data['hits']:
                images.append(image['webformatURL'])
                tags = image['tags'].split(',')
                for tag in tags:
                    tag = tag.strip()
                    if tag not in unique_tags:
                        unique_tags.append(tag)
            print(images)  # Debug print statement to check fetched images
            print(unique_tags)  # Debug print statement to check fetched unique tags
        else:
            print("Failed to retrieve data from Pixabay API")
    
    return render_template('index.html', images=images, unique_tags=unique_tags)


if __name__ == '__main__':
    app.run(debug=True)