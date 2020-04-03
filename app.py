from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pandas
from geopy.geocoders import Nominatim
import numpy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@127.0.0.1/height_collector'
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

geolocator=Nominatim(user_agent="geolocatorssss")
@app.route("/success", methods=['POST'])
def success():
    global file
    global edited_file
    global geofile
    if request.method=='POST':
        file=request.files["file"]
        file.save(secure_filename("uploaded"+file.filename))
        with open("uploaded"+file.filename) as f:
            edited_file=pandas.read_csv(f)


            for ad, ind in zip(edited_file["Address"], edited_file.index):
                location = geolocator.geocode(ad)
                edited_file.loc[ind, "Coordinates"] = str(location.latitude) + ", " + str(location.longitude)
            edited_file.to_csv("Edited"+file.filename)
            geofile = "Edited"+file.filename





        return render_template("index.html",tables=[edited_file.to_html(classes='data')],titles=edited_file.columns.values, btn="download.html")

@app.route("/download")
def download():
    return send_file("Edited"+file.filename, attachment_filename="Anything_else.csv", as_attachment=True,cache_timeout=0)



if __name__ == '__main__':
    app.debug = True
    app.run()
