from flask import Flask, render_template, redirect, jsonify,url_for
import pymongo
from flask_pymongo import PyMongo
from scrape_mars import scrapebot
import sys
from datetime import datetime

sys.setrecursionlimit(2000)
app = Flask(__name__)

#client= pymongo.MongoClient()
#db=client.mars_db
#collection=db.mars

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
app.config['MONGO_DBNAME'] = 'mars_db'
mongo = PyMongo(app)

client = pymongo.MongoClient("mongodb://localhost:27017/mars_db")
db = client['mars_db']
collection = db['mars']

@app.route('/')
def home():
    #data=mongo.db.mars.find_one()
    data=mongo.db.mars.find_one({}, sort=[('_id', pymongo.DESCENDING)])
    alldata=mongo.db.mars.find().sort([("timestamp", pymongo.DESCENDING)])
    #data=collection.find()
    #mars=list(db.mars.find())
    return render_template("index.html",mars=data,allmars=alldata)

@app.route('/archives/<archivetimestamp>', methods=['GET', 'POST'])
def archives(archivetimestamp):
    #data=mongo.db.mars.find_one()
    archivetimestamp=archivetimestamp.replace(" ","T")
    archivetimestamp=datetime.strptime(archivetimestamp, "%Y-%m-%dT%H:%M:%S.%f")
    #archivetimestamp=archivetimestamp.replace(" ","T").replace("000","+00:00")
    data=mongo.db.mars.find_one({'timestamp' : archivetimestamp})
    alldata=mongo.db.mars.find().sort([("timestamp", pymongo.DESCENDING)])
    #data=collection.find()
    #mars=list(db.mars.find())
    return render_template("archive.html",mars=data,allmars=alldata)


@app.route('/addscrape')
def marsfirstscrape():
    #mars = mongo.db.mars
    mars_data=scrapebot.scrape()
    db.mars.insert_one(mars_data)
    return redirect(url_for('home'))

@app.route('/scrape')
def scrapemars():
    mars_data=scrapebot.scrape()
    #db.mars.update({},mars_data,upsert=True)
    #mongo.db.mars.update({},mars_data,upsert=True)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
