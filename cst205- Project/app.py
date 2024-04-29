from flask import Flask, render_template, request
import requests
#flask --app app --debug run
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
