"""
Course: CST-205
Title: Photo and Image Search
Authors: Jonathan Ngo, Judah Silva, Michael Huziy, Nikolas Lopez
Date: 05/14/2024
Abstract: This project creates a Flask app that allows the user to search for images and videos based on entered key words. Also generates AI images based on the tags of the returned images.
Github: https://github.com/StealthCSUMBStudent/CST205Final-Team3476/tree/main
"""

import requests
import random
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap5
from images_api import *
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired

#flask --app app --debug run
app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Store tags and terms for AI Image route to use
tags = []
terms = ''

# Route to handle image and video api calls, and to render index page
#Started by Nikolas, finished by Michael
@app.route('/', methods=['GET', 'POST'])
def index():
    pixa_bay_key= '43673995-6b601f29737528af485dab3da'#pixabay
    pexel_key = "3ZbuUWVJF64tauy9edJRIy3Bg9keAIAAjIzgbI2Q6IhMiK4IhAexJhad"

    #images api
    #https://www.pexels.com/api/documentation/
    global terms
    search_term = request.args.get('searchterm')  # Extract search term from query parameters
    search_type = request.args.get('searchtype')
    generateAI= request.args.get('generateAI')
    terms = search_term
    print(f"SEARCH TERM: {search_term}")
    print(f"TYPE:{search_type}")
    print(f'AI?: {generateAI}')

    # Call imported functions and store info
    photos = []
    illustrations = []
    unique_tags = []
    if search_term:
       photos,unique_tags = get_photos(search_term,pixa_bay_key)
       illustrations = get_illustrations(search_term,pixa_bay_key)

    global tags
    tags = unique_tags.copy()

    #Video api, Michael
    videos = []
    headers = {
    'Authorization': pexel_key
    }
    payload = {
        'query': search_term #Can add query for different pages or number of videos returned
    }
    endpoint = 'https://api.pexels.com/videos/search'
    if search_term:
        print('getting videos')
        r = requests.get(endpoint, params=payload,headers=headers)
        if r.status_code == 200:
            data = r.json()
            # print(data)
            # Pull out relevant info from json
            for video in data["videos"]:
                vid_data:dict = {}
                vid_data["mp4"] = video["video_files"][0]["link"]#can add filters for different video quality returned
                vid_data["vid_url"] = video["url"]
                vid_data["author"] = video["user"]
                videos.append(vid_data)
                # print(vid_data)
        else:
            print('Video Api failed to return')
    
    # Shuffle returned images and videos
    random.shuffle(photos)
    random.shuffle(illustrations)
    random.shuffle(videos)
    # print(videos)

    return render_template('index.html', photos=photos, illustrations=illustrations, unique_tags=unique_tags, 
                            videos=videos, term=search_term, type=search_type)


# API route that will be called in the javascript
# Worked on by Judah Silva
@app.route('/api/aiImages')
def aiGeneration():
    print("INSIDE AI API")
    # Create prompt based off of tags/search terms
    prompt = ' '.join(tags)
    # prompt = terms

    # Check prompt is not empty
    if (len(prompt) == 0):
        return jsonify({'error': 'Nothing returned from API'})

    # Set up requests
    url = "https://text-to-image13.p.rapidapi.com/"
    payload = { "prompt": prompt }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8867e01260msha8bab1ebf526c14p17d658jsn7f3f3686d05d",
        "X-RapidAPI-Host": "text-to-image13.p.rapidapi.com"
    }

    # Make 3 requests to the api and store the info in images array
    images = []
    for i in range(0, 3):
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            try:
                # API returns raw binary info, so handle that
                # Credit: https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
                image_data = BytesIO(response.content)
                img = base64.b64encode(image_data.getvalue()).decode()
                images.append({'data': img})
            except:
                print('didn\'t work')
        else:
            print(f'Error: {response.status_code} code from API')

    # Return json of image data
    if len(images) != 0:
        return jsonify(images)
    else:
        return jsonify({'error': 'Nothing returned from API'})

# Don't think we need this
# if __name__ == '__main__':
#     my_key = "N8DEUbwaWvewRx1e5S9tnHTKUGFcLvcHHEeXPaz2a378J5cAfLpaQVdu"
#     headers = {
#     'Authorization': my_key
#     }
#     payload = {
#         'query':'people',
#         'page':'`'
#     }
#     endpoint = 'https://api.pexels.com/videos/search?'
#     try:
#         r = requests.get(endpoint, params=payload,headers=headers)
#         data = r.json()
#         print(f'Current page:{data["page"]}')
#         print(f'Photos per page:{data["per_page"]}')
#         #pprint.pprint(data.)
#     except requests.RequestException as e:
#         print('Error:', e)
#         print('Response content:', r.content)  # Display the response content if available
#         print('Please try again')
