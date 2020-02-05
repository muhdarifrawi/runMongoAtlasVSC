import os
from flask import Flask, render_template, redirect, request, url_for
import pymongo
from flask_pymongo import PyMongo

MONGO_DBNAME = 'testBed' #insert your mongo database name
MONGO_URI = 'mongodb+srv://root2:r00t2@cluster0-yggef.mongodb.net/test?retryWrites=true&w=majority' #insert your own URI

def get_connection():
    conn = pymongo.MongoClient(MONGO_URI)
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_connection()
    apple = conn[MONGO_DBNAME]["sample1"].find()
    minPrice = conn[MONGO_DBNAME]["samplePrice"].find({})
    return render_template("index.html", apple2=apple, minPrice=minPrice) #this would pass the data "apple" to the html side called "apple2"

@app.route("/add_data")
def add_data():

    return render_template("template.addData.html")

#a reminder to put method=POST in your HTML form side as well
@app.route("/add_data", methods=["POST"])
def confirm_add_data():
    conn = get_connection()
    
    
    return ("done")

#ignore this. i'm using local drive so this is my setup.
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
