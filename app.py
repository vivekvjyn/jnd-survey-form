from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import random
import os
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

# Connect to MongoDB
uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.dbm54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the database
db = client["jnd-survey"]
collection = db["responses"]

# Select random audio samples
n_samples = 12
positives = [f"positives/{sample}" for sample in os.listdir("static/audio/positives")]
positives = random.sample(positives, n_samples - 3)
negatives = [f"negatives/{sample}" for sample in os.listdir("static/audio/negatives")]
samples = positives + negatives
random.shuffle(samples)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Get the responses from the form and update the database
        responses = [request.form.get(f"sample-{i}") for i in range(n_samples)]
        responses = [1 if response == "yes" else 0 for response in responses]

        collection.insert_one({"samples": samples, "responses": responses})

        return "Thank you for participating in the survey!"

    else:
        return render_template("form.html", samples=samples, enumerate=enumerate)

if __name__ == "__main__":
    app.run(debug=True)
