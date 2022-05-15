from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from PIL import Image

# Starts Flask application
app = Flask(__name__)
# Class for multimedia filters.
class ImageFilter():
    def __init__(self, file_data, filter):
        # super().__init__()
        self.file_name = file_data.filename
        self.image = Image.open(file_data)
        self.filter = filter
        self.applyfilter()

    def applyfilter(self):
        if self.filter == "grayscale":
            self.grayscale_filter()
        elif self.filter == 'negative':
            self.negative_filter()
        elif self.filter == 'sepia':
            self.sepia_filter()
        elif self.filter == 'scale':
            self.thumbnail_filter(5)

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

    def thumbnail_filter(self, scale):
        # Thumbnail
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

        # Implement a scale up image function.

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
    form = ImageUpload()
    if form.validate_on_submit():

        if  form.image_file.data.filename[form.image_file.data.filename.find('.'):] in ALLOWED_EXTENSIONS:
            file = form.image_file.data # First grab the file
            test = ImageFilter(file, filter)
            return render_template("website_code.html", form=form, ran_filter = 'True')
    return render_template("website_code.html", form=form, ran_filter = 'False')

