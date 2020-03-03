from flask import Flask, render_template, redirect
from scrape_mars import scrape
import pymongo

app = Flask(__name__)

# setting up MongoDB connection and creating a new database 
CONN = "mongodb://localhost:27017"
client = pymongo.MongoClient(CONN)
db = client.mars_db

# home(/) route retrieves the information from the MongoDB database and displays it on the home page.
@app.route("/")
def home_page():
	result = db.mars_collection.find_one()
	return render_template("index.html", mars=result)

# scrape route scrapes information related to 'Mission to Mars' from various webpages and stores them to the MongoDB database.
@app.route("/scrape")
def scrape_data():
	mars_dict = scrape()
	db.mars_collection.update({}, mars_dict, upsert=True)
	return redirect("/", code=302)


#  main -------------------------------------------------------------

if __name__ == "__main__":
	app.run(debug=True)

