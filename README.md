# CST-205-Final-Project
Course: CST 205

Date: 5-19-2022

Title: CST 205 Final Project: Image Filtering

Team Members: Oswaldo Cortes-Tinoco, Edgar Hernadez, Fernando Pulido, and Carlos Santiago-Pacheco
Oswaldo's Contributions: He wrote the basic classes for the forms and the filters as well as setting up the 
routes for the flask appication in the "web_application.py" file. He also worked on the "website.html" file
to send the user to a distinct webpage that displayed different pages for the filter pages. 
Edgar Hernandez's Contributions: He worked on the weather filter where he used a weather API and set it up so that the API request takes in a zipcode as userinput and retrieves a city's weather conditions. Through json, he extraced the weather condition (Clear, Clouds, Thunderstorm, Snow, Rain, Blurry, Drizzle) and used OpenCV to apply COLORMAP filters depending on such wender conditions.
Fernando Pulido's Contributions: He worked on the space collage filter class that connects to the flask app and set it up so that when a user uploads an image, that image is resized and pasted onto a background image in a pattern that resembles that of a collage.
Carlos's Contributions: He worked on the ASCII filter that uses the flask apps decorator route to allow the user
to upload an image. With this inputted image, the next decorator route will display instructions as to how to
access the text file that is produced. This text file looks like the inputted image but just with ASCII texts.


Date: 5-19-2022

Running the progam:
To run the program, first download the code in the folder.
Then make sure that your virtual enironment is active and has following packages/libraries installed.
 
Packages/Libraries    |     If you don't have them run the following command
Needed                |     in the terminal with your virtual environment active.
                      |     Using pip install      
- Flask               |     flask, bootstrap-flask
- Flask WTForms       |     flask-wtf
- Pillow              |     pil
- OpenCV              |     opencv-python
- Numpy               |     numpy
- Requests            |     requests

Once you have the libraries/packages installed move into the Flask_App directory using the cd command in the terminal.
Once there, enter the following commands one at a tme:
1. $env:FLASK_APP = ".\web_application.py"
2. $env:FLASK_DEBUG = "1"
3. flask run

Then copy the link to the server that you see in the terminal to a browser. (Prefferably on Google Chrome) Once you copy the address
you are now done and can see the code in action. Once done using the program. Go back to the terminal and kill the server by pressing ctrl+C

Link to Github Repository: https://github.com/OsCortes88/CST-205-Final-Project.git

Future Work: We would like to add more filters to the program as well as adding filters to an image that can
add objects to a person's face, like adding sunglasses, hats, or ties. We would have also liked to style our Flask App with bootstrap to make it look nicer and clean.
