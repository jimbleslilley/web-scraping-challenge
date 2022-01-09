import pymongo
from flask import Flask, render_template, redirect
from scrape_mars import scrape

app = Flask(__name__)

# Set up MongoDB to store data
mongo = pymongo.MongoClient('mongodb://localhost:27017')
db = mongo.mars_db
mars = db.mars

# App route to scrape
@app.route("/scrape")
def store():
    mars_data = scrape()

    # store/update data
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

@app.route("/")
def main():

    mars_data = mars.find_one()
    return render_template('index.html', data=mars_data)
    
if __name__ == "__main__":
    app.run(debug=True)