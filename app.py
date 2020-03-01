from flask import Flask, render_template, redirect
from scrape_mars import scrape
import pymongo

app = Flask(__name__)

CONN = "mongodb://localhost:27017"
client = pymongo.MongoClient(CONN)
db = client.mars_db


@app.route("/")
def home_page():
	result = db.mars_collection.find_one()
	return render_template("index.html", mars=result)

@app.route("/scrape")
def scrape_data():
	mars_dict = scrape()
	print(mars_dict)
	db.mars_collection.update({}, mars_dict, upsert=True)
	return redirect('/', code=302)



#  main

if __name__ == "__main__":
	app.run(debug=True)

