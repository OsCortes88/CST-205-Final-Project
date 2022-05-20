from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField, SelectField, validators
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os, cv2, requests, json
from wtforms.validators import InputRequired
from PIL import Image
import numpy as np


from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import FileField, SubmitField, IntegerField, SelectField, validators

from hashlib import new
import re
import PIL.Image

app = Flask(__name__)

# ascii characters used ot build the output text
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

class ASCIIFILTER():    
    # resizing image according to new width
    def resize_image(self, image, new_width=100):
        width, height = image.size
        ratio = height / width
        new_height = int(new_width * ratio)
        resized_image = image.resize((new_width, new_height))
        return (resized_image)

    # convert pixels to grayscale
    def grayify(image):
        grayscale_image = image.convert("L")
        return(grayscale_image)

    # convert pixels to string of ASCII chars
    def pixels_to_ascii(image):
        pixels = image.getdata()
        characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
        return(characters)
        
    # def main(new_width=100):
    #     # attempt to open image from user-input
    #     #checks image is there
    #     image = FileField("File", [validators.DataRequired()])
    #     # Submitting button
    #     submit = SubmitField("Upload File")
    #     # convert image to ASCII
    #     new_image_data = pixels_to_ascii(grayify(resize_image(image)))
        
        
        
        # try:
        #     image = PIL.Image.open(path)
        # except:
        #     print(path, "is not a valid pathname to an image.")

        # # convert image to ASCII
        # new_image_data = pixels_to_ascii(grayify(resize_image(image)))

        # format
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

        # print result
        print (ascii_image)

        # save result to "ascii_image.txt"
        with open("ascci_image.txt", "w") as f:
            f.write(ascii_image)

    # main()  

@app.route('/asciiFun')
def ascii_fun():
    return render_template('home.html', ASCIIFILTER=ASCIIFILTER)
