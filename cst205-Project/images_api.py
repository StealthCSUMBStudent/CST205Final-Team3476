"""
Course: CST-205
Title: Photo and Image Search
Authors: Jonathan Ngo, Judah Silva, Michael Huziy, Nikolas Lopez
Date: 05/14/2024
Abstract: This project creates a Flask app that allows the user to search for images and videos based on entered key words. Also generates AI images based on the tags of the returned images.
Github: https://github.com/StealthCSUMBStudent/CST205Final-Team3476/tree/main
"""
import requests
# from flask import Flask, render_template, request
# from flask_bootstrap import Bootstrap5
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# from datetime import datetime

# Function to call image api and return array of jsons and array of strings
# Created by Nikolas
def get_photos(search_term, pixa_bay_key):
    photos = []
    unique_tags = []
    photo_r= requests.get(f"https://pixabay.com/api/?key={pixa_bay_key}&q={search_term}&image_type=photo")

    if photo_r.status_code == 200:
        data = photo_r.json()
        # Check if data is not empty, and pull relevant information out
        if (data['total'] != 0):
            #pprint.pprint(data["hits"])  # Debug print statement to check fetched data
            for photo in data['hits']:
                #print(f"Type: {photo["type"]}")
                photos.append(photo['webformatURL'])
                tags = photo['tags'].split(',')
                for tag in tags:
                    tag = tag.strip()
                    # Pull out unique tags
                    if tag not in unique_tags:
                        unique_tags.append(tag)
                #pprint.pprint(images)  # Debug print statement to check fetched images
                #print(unique_tags)  # Debug print statement to check fetched unique tags
    return photos,unique_tags

# Function to call image api for illustrations and return array of jsons
# Worked on by Michael
def get_illustrations(search_term, pixa_bay_key):
    illustrations = []
    illustration_r = requests.get(f"https://pixabay.com/api/?key={pixa_bay_key}&q={search_term}&image_type=illustration")
    # vector_r =  requests.get(f"https://pixabay.com/api/?key={pixa_bay_key}&q={search_term}&image_type=vector") 
    #Was thinking of combing vecotor with illustrations as one result, or make another category
    #for users who want svg images specfically to view/download

    if illustration_r.status_code == 200:
        data = illustration_r.json()
        # Check if data is not empty and pull relevant information out
        if (data['total'] != 0):
            for illustration in data['hits']:
                #print(f"Type: {illustration["type"]}")
                illustrations.append(illustration['webformatURL'])
    return illustrations