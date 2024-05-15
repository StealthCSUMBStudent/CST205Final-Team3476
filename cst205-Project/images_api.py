from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import requests
import json
import pprint
import random

def get_photos(search_term, pixa_bay_key):
    photos = []
    unique_tags = []
    photo_r= requests.get(f"https://pixabay.com/api/?key={pixa_bay_key}&q={search_term}&image_type=photo")

    if photo_r.status_code == 200:
        data = photo_r.json()
        if (data['total'] != 0):
            #pprint.pprint(data["hits"])  # Debug print statement to check fetched data
            for photo in data['hits']:
                #print(f"Type: {photo["type"]}")
                photos.append(photo['webformatURL'])
                tags = photo['tags'].split(',')
                for tag in tags:
                    tag = tag.strip()
                    if tag not in unique_tags:
                        unique_tags.append(tag)
                #pprint.pprint(images)  # Debug print statement to check fetched images
                #print(unique_tags)  # Debug print statement to check fetched unique tags
    return photos,unique_tags

def get_illustrations(search_term, pixa_bay_key):
    illustrations = []
    illustration_r = requests.get(f"https://pixabay.com/api/?key={pixa_bay_key}&q={search_term}&image_type=illustration")
    vector_r =  requests.get(f"https://pixabay.com/api/?key={pixa_bay_key}&q={search_term}&image_type=vector") 
    #Was thinking of combing vecotor with illustrations as one result, or make another category
    #for users who want svg images specfically to view/download
    if illustration_r.status_code == 200:
        data = illustration_r.json()
        if (data['total'] != 0):
            for illustration in data['hits']:
                #print(f"Type: {illustration["type"]}")
                illustrations.append(illustration['webformatURL'])
    return illustrations