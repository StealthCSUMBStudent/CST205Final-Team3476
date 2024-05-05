from flask import Flask, render_template, request, jsonify
from PIL import Image
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

@app.route('/ai')
def route():
    print('working')
    return render_template('ai.html')

@app.route('/api/aiImages')
def aiGeneration():
    url = "https://stable-diffusion9.p.rapidapi.com/generate"

    payload = {
        "prompt": "dogs",
        "style": "manga",
        "seed": 2
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8867e01260msha8bab1ebf526c14p17d658jsn7f3f3686d05d",
        "X-RapidAPI-Host": "stable-diffusion9.p.rapidapi.com"
    }

    images = []
    for i in range(0, 2):
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            try:
                images.append(response.json()['url'])
            except:
                print('didn\'t work')
        else:
            print(f'Error: {response.status_code} code from API')

    if len(images) != 0:
        return jsonify(images)
    else:
        return None


"""
0:
name:"cinematic"
1:
name:"photographic"
2:
name:"anime"
3:
name:"manga"
4:
name:"digital-art"
5:
name:"pixel-art"
6:
name:"fantasy-art"
7:
name:"neonpunk"
8:
name:"3d-model"
9:
name:"analog"
10:
name:"comic-book"
11:
name:"craft-clay"
12:
name:"enhance"
13:
name:"isometric"
14:
name:"line-art"
15:
name:"lowpoly"
16:
name:"origami"
17:
name:"pixel-art"
18:
name:"texture"
19:
name:"watercolor"
20:
name:"artstyle-hyperrealism"
21:
name:"paper-quilling"
22:
name:"photo-hdr"
23:
name:"horror"
24:
name:"dreamscape"
25:
name:"game-bubble-bobble"
26:
name:"game-cyberpunk-game"
27:
name:"game-fighting-game"
28:
name:"game-gta"
29:
name:"game-mario"
30:
name:"game-minecraft"
31:
name:"game-pokemon"
32:
name:"game-retro-arcade"
33:
name:"game-retro-game"
34:
name:"game-rpg fantasy-game"
35:
name:"game-strategy-game"
36:
name:"game-streetfighter"
37:
name:"game-zelda"
38:
name:"furry"
"""