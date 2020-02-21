import os
from flask import Flask, render_template, redirect, request, url_for
import pymongo
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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

    return render_template("addData.html")

# a reminder to put method=POST in your HTML form side as well 
@app.route("/add_data", methods=["POST"])
def confirm_add_data():
    # this establishes connection to Mongo
    conn = get_connection()
    # this requests from your html a "Name = insert_name"
    name = request.form["insert_name"]
    contact = request.form["insert_contact"]
    address = request.form["insert_address"]
    # this is the code that inserts the data into Mongo
    # the name is from the variable above
    insert_name = conn[MONGO_DBNAME]["sample1"].insert({
        "name":name,
        "contact":contact,
        "address":address
    })
    
    return redirect("/add_data")

@app.route("/search")
def search():
    
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def confirm_search():
    conn = get_connection()
    search = request.form["search-value"]
    search_bar = request.form["search-bar"]

    if search_bar == "name":
        search_tag="name"
    elif search_bar == "contact":
        search_tag="contact"
    else:
        search_tag="address"

    search_name = conn[MONGO_DBNAME]["sample1"].find({search_tag: {"$regex":search, "$options":"i"}})
    return render_template("search.html",search_name=search_name)

@app.route("/edit/<current_id>")
def edit(current_id):

    conn = get_connection()
    
    search = conn[MONGO_DBNAME]["sample1"].find_one({
        "_id": ObjectId(current_id)
    })

    return render_template("update.html", current_id=current_id, search=search)

@app.route("/edit/<current_id>", methods=["POST"])
def confirm_edit(current_id):

    conn = get_connection()
    
    name = request.form["insert_name"]
    contact = request.form["insert_contact"]
    address = request.form["insert_address"]
    
    conn[MONGO_DBNAME]["sample1"].update({
        "_id":ObjectId(current_id)    
    },
    {"$set":
        {
        "name":name,
        "contact":contact,
        "address":address
        }
    })

    return redirect(url_for("index"))

@app.route("/delete/<current_id>")
def delete(current_id):

    conn = get_connection()
    
    search = conn[MONGO_DBNAME]["sample1"].find_one({
        "_id": ObjectId(current_id)
    })

    return render_template("delete.html", current_id=current_id, search=search)

@app.route("/delete/<current_id>", methods=["POST"])
def confirm_delete(current_id):

    conn = get_connection()
    
    conn[MONGO_DBNAME]["sample1"].delete_one({
        "_id": ObjectId(current_id)
    })

    return redirect(url_for("index"))


#ignore this. i'm using local drive so this is my setup.
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
