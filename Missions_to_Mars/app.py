from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape_info

# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    #destination_data = mongo.db.collection.find_one()

    # Return template and data
    scrape_payload = scrape_info()
    return render_template("index.html", scrape_payload)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    #mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    #mongo.db.collection.update({}, costa_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
