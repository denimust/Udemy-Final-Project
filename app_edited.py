from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pandas
from geopy.geocoders import Nominatim
import numpy

#Setting up variables for flask and connecting to database on SQL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='connect to DB'
db=SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique = True)
    height_=db.Column(db.Integer)
    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

#connecting to Nominatim, used to get longtitude and latitude data for addresses        
geolocator=Nominatim(user_agent="geolocatorssss")

#Main function of the app. 
@app.route("/success", methods=['POST'])
def success():
    #uploaded file
    global file
    
    #file that was saved to the system when uploaded and used for the editing
    global edited_file
    
    #returned file for user to be able to download
    global geofile
    if request.method=='POST':
        file=request.files["file"]
        file.save(secure_filename("uploaded"+file.filename))
        with open("uploaded"+file.filename) as f:
            edited_file=pandas.read_csv(f)

            #Loop that uses Nominatim to add geocode information to the file
            for ad, ind in zip(edited_file["Address"], edited_file.index):
                location = geolocator.geocode(ad)
                edited_file.loc[ind, "Coordinates"] = str(location.latitude) + ", " + str(location.longitude)
            edited_file.to_csv("Edited"+file.filename)
            geofile = "Edited"+file.filename




        #Display the table on the website
        return render_template("index.html",tables=[edited_file.to_html(classes='data')],titles=edited_file.columns.values, btn="download.html")

#Allowing the user to download the edited file.
@app.route("/download")
def download():
    return send_file("Edited"+file.filename, attachment_filename="Edited_file.csv", as_attachment=True,cache_timeout=0)



if __name__ == '__main__':
    app.debug = True
    app.run()
