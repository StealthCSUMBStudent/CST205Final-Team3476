import requests
import json
import random
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from images_api import *
# from ai_api import get_ai_images

#flask --app app --debug run
app = Flask(__name__)
bootstrap = Bootstrap5(app)

tags = []

@app.route('/', methods=['GET', 'POST'])
def index():
    pixa_bay_key= '43673995-6b601f29737528af485dab3da'#pixabay
    pexel_key = "N8DEUbwaWvewRx1e5S9tnHTKUGFcLvcHHEeXPaz2a378J5cAfLpaQVdu"
    #images api
    #https://www.pexels.com/api/documentation/
    search_term = request.args.get('searchterm')  # Extract search term from query parameters
    search_type = request.args.get('searchtype')
    print(f"SEARCH TERM: {search_term}")
    print(f"TYPE:{search_type}")
    photos = []
    illustrations = []
    unique_tags = []
    if search_term:
       photos,unique_tags = get_photos(search_term,pixa_bay_key)
       illustrations = get_illustrations(search_term,pixa_bay_key)

    global tags
    tags = unique_tags.copy()

    #Video api
    videos = []
    headers = {
    'Authorization': pexel_key
    }
    payload = {
        'query': search_term #Can add query for different pages or number of videos returned
    }
    endpoint = 'https://api.pexels.com/videos/search?'
    if search_term:
        r = requests.get(endpoint, params=payload,headers=headers)
        if r.status_code == 200:
            data = r.json()
            for video in data["videos"]:
                vid_data:dict = {}
                vid_data["mp4"] = video["video_files"][0]["link"]#can add filters for different video quality returned
                vid_data["vid_url"] = video["url"]
                vid_data["author"] = video["user"]
                #print(vid_data["url"])
                #print(vid_data["author"]["name"])
                #print(f'Current page:{data["page"]}')
                #print(f'Videos per page:{data["per_page"]}')
                #pprint.pprint(len(data["videos"]))
                #pprint.pprint(data["videos"][0])
                #pprint.pprint(len(data["videos"][0]["video_files"]))
                #pprint.pprint(data["videos"][0]["video_files"][0])
                videos.append(vid_data)
                #pprint.pprint(vid_data)
        else:
            print('Video Api failed to return')
    random.shuffle(photos)
    random.shuffle(illustrations)
    random.shuffle(videos)
    #photos = []
    #illustrations = []
    return render_template('index.html', photos=photos, illustrations=illustrations, unique_tags=unique_tags, 
                            videos=videos, term=search_term, type=search_type)


@app.route('/api/aiImages')
def aiGeneration():
    # url = "https://stable-diffusion9.p.rapidapi.com/generate"

    prompt = ' '.join(tags)
    print(prompt)
    # payload = {
    #     "prompt": prompt,
    #     "style": "photographic",
    #     "seed": 0
    # }
    # headers = {
    #     "content-type": "application/json",
    #     "X-RapidAPI-Key": "8867e01260msha8bab1ebf526c14p17d658jsn7f3f3686d05d",
    #     "X-RapidAPI-Host": "stable-diffusion9.p.rapidapi.com"
    # }

    url = "https://text-to-image13.p.rapidapi.com/"

    payload = { "prompt": prompt }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "5bf9d2f08cmshd09cc10a30ac230p1c0176jsnf088f771ba07",
        "X-RapidAPI-Host": "text-to-image13.p.rapidapi.com"
    }

    images = []
    # response = requests.post(url, json=payload, headers=headers)
    for i in range(0, 3):
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            try:
                # print(response.content)
                image_data = BytesIO(response.content)
                img = base64.b64encode(image_data.getvalue()).decode()
                images.append({'data': img})
            except:
                print('didn\'t work')
        else:
            print(f'Error: {response.status_code} code from API')

    if len(images) != 0:
        return jsonify(images)
    else:
        return jsonify({'error': 'Nothing returned from API'})


if __name__ == '__main__':
    my_key = "N8DEUbwaWvewRx1e5S9tnHTKUGFcLvcHHEeXPaz2a378J5cAfLpaQVdu"
    headers = {
    'Authorization': my_key
    }
    payload = {
        'query':'people',
        'page':'`'
    }
    endpoint = 'https://api.pexels.com/videos/search?'
    try:
        r = requests.get(endpoint, params=payload,headers=headers)
        data = r.json()
        print(f'Current page:{data["page"]}')
        print(f'Photos per page:{data["per_page"]}')
        #pprint.pprint(data.)
    except requests.RequestException as e:
        print('Error:', e)
        print('Response content:', r.content)  # Display the response content if available
        print('Please try again')