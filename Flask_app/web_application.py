"""
Course: CST 205
Title: CST 205 Final Project: Image Filtering
Abstract: This program runs a flask application where the user can upload their desired images and 
select an image filter(Grayscale, Negative, Sepia) to apply to the image. It then saves the changed 
image with the filter to the computer where the user can access it and displays the result in the 
web page.There is a weather filter that makes use of a weather API to change the image to a filter 
that goes according to the weather in the region through zipcode input. Another feature is that 
the program produces a image collage of a single image. There is also an ASCII filer
that transforms any image into a text file using ASCII characters.
Authors: Oswaldo Cortes-Tinoco, Edgar Hernadez, Fernando Pullido, and Carlos Santiago-Pacheco

Oswaldo's Contributions: He wrote the basic classes for the forms and the filters as well as setting up the 
routes for the flask appication in the "web_application.py" file. He also worked on the "website.html" file
to send the user to a distinct webpage that displayed different pages for the filter pages.

Edgar's Contributions: He worked on the weather filter where he used a weather API and set it up so that the API 
request takes in a zipcode as userinput and retrieves a city's weather conditions. Through json, he extraced the weather 
condition (Clear, Clouds, Thunderstorm, Snow, Rain, Blurry, Drizzle) and used OpenCV to apply COLORMAP filters depending
on such wender conditions.

Fernando Pulido's Contributions: He worked on the space collage filter class that connects to the flask app and 
set it up so that when a user uploads an image, that image is resized and pasted onto a background image in a 
pattern that resembles that of a collage.

Carlos's Contributions: He worked on the ASCII filter that uses the flask apps decorator route to allow the user
to upload an image. With this inputted image, the next decorator route will display instructions as to how to
access the text file that is produced. This text file looks like the inputted image but just with ASCII texts.

Github Repository Link https://github.com/OsCortes88/CST-205-Final-Project.git

Date: 5-19-2022
"""

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField, SelectField, validators
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os, cv2, requests, json
from wtforms.validators import InputRequired
from PIL import Image
import numpy as np

from hashlib import new
import re
import PIL.Image

# Starts Flask application
app = Flask(__name__)

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Class for multimedia filters.
class ImageFilter():
    def __init__(self, file_data, filter, scale, direction):
        # Stores the name of the file so we can then use it to name the file we will save.
        self.file_name = file_data.filename
        # Creates a Pillow object so we can access pixel data
        self.image = Image.open(file_data)
        self.filter = filter
        self.scale = scale
        self.direction = direction
        self.ascii_width = 0
        self.ascii_height = 0
        # The following will apply the filter depending on what the user selected
        self.applyfilter()

    # It checks for which filter was selected and applies the filter selected.
    def applyfilter(self):
        if self.filter == "grayscale":
            self.grayscale_filter()
        elif self.filter == 'negative':
            self.negative_filter()
        elif self.filter == 'sepia':
            self.sepia_filter()
        elif self.filter == 'scale':
            self.thumbnail_filter(self.scale, self.direction)
        elif self.filter == 'space collage':
            self.space_collage()
        elif self.filter == "ASCII":
            self.ascii_filter()


    def ascii_filter(self):
        self.new_image_data = self.pixels_to_ascii(self.grayify(self.resize_image(self.image)))
        self.pixel_count = len(self.new_image_data)
        self.ascii_image = "\n".join(self.new_image_data[i:(i+self.ascii_width)] for i in range(0, self.pixel_count, self.ascii_width))
        with open(f"static/files/ascci_image.txt", "w") as f:
            f.write(self.ascii_image)

    # resizing image according to new width
    def resize_image(self, image, new_width=100):
        self.width, self.height = image.size
        self.ratio = self.height / self.width
        self.new_height = int(new_width * self.ratio)
        self.ascii_height = self.new_height
        self.ascii_width = new_width
        resized_image = image.resize((self.ascii_width, self.new_height)) #delete self from width
        return (resized_image)

    # convert pixels to grayscale
    def grayify(self, image):
        self.grayscale_image = image.convert("L")
        return(self.grayscale_image)

    # convert pixels to string of ASCII chars
    def pixels_to_ascii(self, image):
        self.pixels = image.getdata()
        self.characters = "".join([ASCII_CHARS[pixel//25] for pixel in self.pixels])
        return(self.characters)

    def grayscale_filter(self):
        # Grayscale by illuminance method.
        # The following retrieves the pixel and uses the color channels to calculate the grayscale value.
        self.img_list = [ ( ( (299*p[0])+(587*p[1])+(114*p[2]) ) //1000,) *3 for p in self.image.getdata()]

        # It changes the pixel value in the original picture to the grayscale pixel
        self.image.putdata(list(self.img_list))
        # Saves the image to the files directory
        self.image.save(f"static/files/{self.file_name}")

    def negative_filter(self):
        # Negative
        # The following retrieves the pixel and uses the color channels to calculate the negative value.
        self.img_list = [ ( (299-p[0]), (255-p[1]), (255-p[2]) )  for p in self.image.getdata()]
        
        # It changes the pixel value in the original picture to the negative pixel
        self.image.putdata(list(self.img_list))
        # Saves the image to the files directory
        self.image.save(f"static/files/{self.file_name}")

    def thumbnail_filter(self, scale, direction):
        if direction == "Reduce Image":
            # Scale down
            self.w, self.h = self.image.width//scale, self.image.height//scale
            # Creates a new Pillow object where the resized image will be.
            self.my_trgt = Image.new('RGB', (self.w, self.h))

            self.target_x = 0
            # The loop skips pixels to make image small
            for source_x in range(0, self.image.width, scale):
                self.target_y = 0
                for source_y in range(0, self.image.height, scale):
                    self.p = self.image.getpixel((source_x, source_y))
                    # Once the index is out of bounds the loop breaks
                    try:
                        self.my_trgt.putpixel((self.target_x,self.target_y), self.p)
                    except:
                        break
                    self.target_y += 1
                self.target_x += 1
                
            self.my_trgt.save(f"static/files/{self.file_name}")
        else:
            # scale up
            # Calculates the new width and height for the image
            w, h = self.image.width*scale, self.image.height*scale

            self.my_trgt = Image.new('RGB', (w, h))
            target_x = 0
            # The loop repeats the pixels in both x and y coordinates to enlarge the image
            for source_x in np.repeat(range(self.image.width), scale):
                target_y = 0
                for source_y in np.repeat(range(self.image.height), scale):
                    p = self.image.getpixel((int(source_x), int(source_y)))
                    self.my_trgt.putpixel((target_x, target_y), p)
                    target_y += 1
                target_x += 1

            self.my_trgt.save(f"static/files/{self.file_name}")


    def sepia(self, p):
        self.p = p
        self.tuple = (0,0,0)
        # tint shadows
        if self.p[0] < 63:
            self.r,self.g,self.b = int(self.p[0] * 1.1), self.p[1], int(self.p[2] * 0.9)

        # tint midtones
        elif self.p[0] > 62 and self.p[0] < 192:
            self.r,self.g,self.b = int(self.p[0] * 1.15), self.p[1], int(self.p[2] * 0.85)

        # tint highlights
        else:
            self.r = int(self.p[0] * 1.08)
            self.g,self.b = self.p[1], int(self.p[2] * 0.5)
        
        return self.r, self.g, self.b

    def sepia_filter(self):
        # Sepia
        self.lumi_list = [ self.sepia(p) for p in self.image.getdata()]

        self.image.putdata(list(self.lumi_list))
        self.image.save(f"static/files/{self.file_name}")

    # Space-Collage 
    def space_collage(self):
        self.new = Image.open("static/files/space.jpg")
        self.new = self.new.resize((800,800))
        self.img = Image.open(f"static/files/{self.file_name}")
        self.img = self.img.resize((200,200))
        self.new.paste(self.img, (0,0))
        self.new.paste(self.img, (0, 400))
        self.new.paste(self.img, (0, 800))
        self.new.paste(self.img, (200,200))
        self.new.paste(self.img, (200, 600))
        self.new.paste(self.img, (400, 0))
        self.new.paste(self.img, (400,400))
        self.new.paste(self.img, (400, 800))
        self.new.paste(self.img, (600,600))
        self.new.paste(self.img, (600, 200))
        self.new.save(f"static/files/{self.file_name}")

# The key is needed for the forms
app.config['SECRET_KEY'] = 'mediaproject22'
# Used to save the images into a directory when not using pillow
app.config['UPLOAD_FOLDER'] = 'static/files'

# Used for HTML fomrmating/styles
bootstrap = Bootstrap5(app)

# Acceptable file types list
ALLOWED_EXTENSIONS = set([".jpg", ".png", ".PNG"])

# Class for the file submission form
class ImageUploadForScale(FlaskForm):
    # Makes button for the image upload and checks that someth data was uploaded
    image_file = FileField("File", [validators.DataRequired()])
    # Makes a submit button that will check if the user is done with his form
    submit = SubmitField("Upload File")
    # Makes a field for the user to enter a number between 2-10
    scale = IntegerField("Scale Factor", [validators.DataRequired(), validators.NumberRange(2, 10)])
    # Makes a field for the user to select an option between reducing and enlarging an image
    up_or_down = SelectField(u'Scale Choice', choices = ['Reduce Image', 'Enlarge Image'])

class ImageUploadForWeather(FlaskForm):
    image_file = FileField("File", [validators.DataRequired()])
    submit = SubmitField("Upload File")                                #99950 is the highest zipcode value
    zipcode = IntegerField("Zipcode", [validators.DataRequired(), validators.NumberRange(0, 99950)])

class ImageUpload(FlaskForm):
    image_file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

# This is the home page
@app.route('/', methods =['GET', "POST"] )
def run_home():
    return render_template('home.html')

# This is the upload page that is used to sumbit the image
@app.route("/upload-image/<filter>", methods=["GET", "POST"])
def upload_image(filter):
    if filter == 'scale':
        # Creates the form to retrieve data needed from the user to scale the image.
        form = ImageUploadForScale()
        # Checks if everything in the form has valid input
        if form.validate_on_submit():
            # Checks if the image file extension is valid
            if  form.image_file.data.filename[form.image_file.data.filename.find('.'):] in ALLOWED_EXTENSIONS:
                # Grabs the file uploaded
                file = form.image_file.data 
                # runs filter
                test = ImageFilter(file, filter, form.scale.data, form.up_or_down.data)
            # Changes the page to display the image and allow the user to go back to the home page
            return render_template("website_code.html", form=form, filter = filter,  ran_filter = 'True')
    
    elif filter == 'weather':
        # template used for uploading images but with zipcode input
        form = ImageUploadForWeather()

        # API Key generated from https://openweathermap.org
        key = '4d8b7e6fe5aa71ef536bceab4839c750'
        # Used OpenCV to apply Color Map filters depending on current wether

        payload = {
        'api_key': key,
        'start_date': '2022-05-16',
        'end_date': '2022-05-16'
        }

        zipcode = form.zipcode.data
        # country code is used in API call, the weather filter will only work in cities in the US
        country_code = 'US'
        # API Call
        endpoint = f'https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{country_code}&appid={key}'

        try:
            r = requests.get(endpoint, params=payload)
            # Get weather data from weather API
            data = r.json()
            weather_id = data['weather'][0]['id']
            if weather_id > 700 and weather_id < 800:
                # When weather ID was between 700-800 there were multiple weather conditions
                # So I classified these weather conditions as 'Blurry' for simplification
                # Instead of dealing with all seven similair weather conditions
                weather = 'Blurry'
            else:
                # In JSON file, this was how to acces the weather condition
                weather = data['weather'][0]['main']
        except:
            data = "empty"

        if form.validate_on_submit():

            if  form.image_file.data.filename[form.image_file.data.filename.find('.'):] in ALLOWED_EXTENSIONS:
                file = form.image_file.data # Grabs the file
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                
                cv = cv2.imread(f'static/files/{file.filename}')

                if(weather == 'Rain' or weather == 'Drizzle'):
                    cv = cv2.applyColorMap(cv, cv2.COLORMAP_OCEAN)
                elif(weather == 'Clear'): 
                    cv = cv2.applyColorMap(cv, cv2.COLORMAP_HOT)
                    cv = cv2.applyColorMap(cv, cv2.COLORMAP_PINK)
                elif(weather == 'Snow'):
                    cv = cv2.applyColorMap(cv, cv2.COLORMAP_OCEAN)
                elif(weather == 'Thunderstorm'):
                    cv = cv2.applyColorMap(cv, cv2.COLORMAP_TWILIGHT)
                elif(weather == 'Clouds' or weather == 'Blurry'):
                    cv = cv2.applyColorMap(cv, cv2.COLORMAP_PINK)
                    cv = cv2.applyColorMap(cv, cv2.COLORMAP_BONE)
                else:
                    cv = cv
                cv2.imwrite(f'static/files/{file.filename}', cv)

                return render_template("website_code.html", form=form, filter = filter, weather = weather, ran_filter = 'True')

        return render_template("website_code.html", form=form, filter = filter, ran_filter = 'False')

    elif filter == 'ASCII':
        form = ImageUpload()
        if form.validate_on_submit():
            file = form.image_file.data
            # Runs filter but sets scale and direction parameters to values that will not make a difference.
            # run ascii filter class
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

            test = ImageFilter(file, filter, 1, "")   
            return render_template("website_code.html", form=form, filter = filter, ran_filter = 'True')

        return render_template("website_code.html", form=form, filter = filter, ran_filter = 'False')

    else:
        # Uses basic form template for uploading images
        form = ImageUpload()
        if form.validate_on_submit():

            if  form.image_file.data.filename[form.image_file.data.filename.find('.'):] in ALLOWED_EXTENSIONS:
                file = form.image_file.data
                # Runs filter bufile.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                test = ImageFilter(file, filter, 1, "")
            return render_template("website_code.html", form=form, filter = filter, ran_filter = 'True')

    return render_template("website_code.html", form=form, filter = filter, ran_filter = 'False')

