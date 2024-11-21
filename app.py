from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import random
import os
import json

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.dbm54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the database
db = client["jnd-survey"]
collection = db["responses"]

# Select 10 random audio samples and get their info
samples = os.listdir("static/audio")
samples = random.sample(samples, 10)
info = json.load(open("static/info.json"))
info = {sample: info[sample] for sample in samples}

print(info.values())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the responses from the form and update the database
        responses = [request.form.get(f"sample-{i}") for i in range(10)]
        responses = [1 if response == "yes" else 0 for response in responses]
        collection.insert_one({"samples": samples, "responses": responses})

        return "Thank you for participating in the survey!"

    else:
        return render_template("index.html", samples=samples, enumerate=enumerate)

if __name__ == "__main__":
    app.run(debug=True)
