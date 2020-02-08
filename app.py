import os
from flask import Flask, render_template, redirect, request, url_for
import pymongo
from flask_pymongo import PyMongo

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_DBNAME = os.environ.get("MONGO_DBNAME")  #insert your mongo database name
MONGO_URI = os.environ.get("MONGO_URI") #insert your own URI

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

# a reminder to put method=POST in your HTML form side as well 
@app.route("/add_data", methods=["POST"])
def confirm_add_data():
    # this establishes connection to Mongo
    conn = get_connection()
    # this requests from your html a "Name = insert_name"
    name = request.form["insert_name"]
    # this is the code that inserts the data into Mongo
    # the name is from the variable above
    insert_name = conn[MONGO_DBNAME]["sample1"].insert({
        name:name
    })
    
    return render_template("template.table.html")

@app.route("/search")
def search():
    return render_template("template.addData.html")

@app.route("/search", methods=["POST"])
def execute_search():
    conn = get_connection()
    search = request.form["insert_name"]
    search_name = conn[MONGO_DBNAME]["sample1"].find()
    return render_template("template.addData.html",search_name=search_name)

#ignore this. i'm using local drive so this is my setup.
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
