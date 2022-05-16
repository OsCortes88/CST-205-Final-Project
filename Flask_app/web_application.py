from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField, SelectField, validators
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from PIL import Image
import numpy as np

# Starts Flask application
app = Flask(__name__)
# Class for multimedia filters.
class ImageFilter():
    def __init__(self, file_data, filter, scale, direction):
        # super().__init__()
        self.file_name = file_data.filename
        self.image = Image.open(file_data)
        self.filter = filter
        self.scale = scale
        self.direction = direction
        self.applyfilter()

    def applyfilter(self):
        if self.filter == "grayscale":
            self.grayscale_filter()
        elif self.filter == 'negative':
            self.negative_filter()
        elif self.filter == 'sepia':
            self.sepia_filter()
        elif self.filter == 'scale':
            self.thumbnail_filter(self.scale, self.direction)

    def grayscale_filter(self):
        # Grayscale by illuminance method.
        self.img_list = [ ( ( (299*p[0])+(587*p[1])+(114*p[2]) ) //1000,) *3 for p in self.image.getdata()]

        self.image.putdata(list(self.img_list))
        self.image.save(f"static/files/{self.file_name}")

    def negative_filter(self):
        # Negative
        self.img_list = [ ( (299-p[0]), (255-p[1]), (255-p[2]) )  for p in self.image.getdata()]

        self.image.putdata(list(self.img_list))
        self.image.save(f"static/files/{self.file_name}")

    def thumbnail_filter(self, scale, direction):
        if direction == "Reduce Image":
            # Scale down
            self.w, self.h = self.image.width//scale, self.image.height//scale
            self.my_trgt = Image.new('RGB', (self.w, self.h))

            self.target_x = 0
            for source_x in range(0, self.image.width, scale):
                self.target_y = 0
                for source_y in range(0, self.image.height, scale):
                    self.p = self.image.getpixel((source_x, source_y))
                    try:
                        self.my_trgt.putpixel((self.target_x,self.target_y), self.p)
                    except:
                        break
                    self.target_y += 1
                self.target_x += 1
                
            self.my_trgt.save(f"static/files/{self.file_name}")
        else:
            # scale up
            w, h = self.image.width*scale, self.image.height*scale

            self.my_trgt = Image.new('RGB', (w, h))
            target_x = 0
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



app.config['SECRET_KEY'] = 'mediaproject22'
app.config['UPLOAD_FOLDER'] = 'static/files'

# Used for HTML fomrmating/styles
bootstrap = Bootstrap5(app)

# Acceptable file types list
ALLOWED_EXTENSIONS = set([".jpg", ".png", ".PNG"])

# Class for the file submission form
class ImageUploadForScale(FlaskForm):
    image_file = FileField("File", [validators.DataRequired()])
    submit = SubmitField("Upload File")
    scale = IntegerField("Scale Factor", [validators.DataRequired(), validators.NumberRange(2, 10)])
    up_or_down = SelectField(u'Scale Choice', choices = ['Reduce Image', 'Enlarge Image'])

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
        form = ImageUploadForScale()
        if form.validate_on_submit():

            if  form.image_file.data.filename[form.image_file.data.filename.find('.'):] in ALLOWED_EXTENSIONS:
                file = form.image_file.data # First grab the file
                test = ImageFilter(file, filter, form.scale.data, form.up_or_down.data)
            return render_template("website_code.html", form=form, filter = filter,  ran_filter = 'True')
    else:
        form = ImageUpload()
        if form.validate_on_submit():

            if  form.image_file.data.filename[form.image_file.data.filename.find('.'):] in ALLOWED_EXTENSIONS:
                file = form.image_file.data # First grab the file
                test = ImageFilter(file, filter, 1, "")
            return render_template("website_code.html", form=form, filter = filter, ran_filter = 'True')

    return render_template("website_code.html", form=form, filter = filter, ran_filter = 'False')

