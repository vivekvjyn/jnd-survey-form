import os
import random
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

# Flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

# Database connection
uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.dbm54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[os.getenv('DB_NAME')]
collection = db[os.getenv('COLLECTION_NAME')]

# Form configuration
num_samples = int(os.getenv('NUM_SAMPLES'))
num_pages = 3
samples_per_page = num_samples // num_pages

# Load audio sample filenames
positives = [
    f"positives/{sample}" for sample in os.listdir("static/audio/positives")
]
negatives = [
    f"negatives/{sample}" for sample in os.listdir("static/audio/negatives")
]

# Concatenate and shuffle positive and negative samples
samples = positives + negatives
random.shuffle(samples)

@app.route("/")
def index():
    """
    Render the welcome page.
    """
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    """
    Render the survey form.
    """
    page = int(request.args.get("page", 1))
    curr_samples = samples[(page - 1) * samples_per_page: page * samples_per_page]

    if request.method == "POST":
        responses = [request.form.get(f"sample-{i}") for i in range(samples_per_page)]
        responses = [1 if response == "yes" else 0 for response in responses]
        
        prev_samples = samples[(page - 2) * samples_per_page: (page - 1) * samples_per_page]
        for sample, response in zip(prev_samples, responses):
            session[sample] = response
    else:
        session.clear()

    return render_template("form.html", samples=curr_samples, page=page, enumerate=enumerate)
    
@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Save the responses to the database,  and render a confirmation page.
    """
    if request.method == "POST":
        responses = [request.form.get(f"sample-{i}") for i in range(samples_per_page)]
        responses = [1 if response == "yes" else 0 for response in responses]

        prev_responses = []
        prev_samples = samples[: (num_pages - 1) * samples_per_page]
        for sample in prev_samples:
            prev_responses.append(session.get(sample))

        collection.insert_one({"samples": samples, "responses": prev_responses + responses})

        session.clear()
        return render_template("feedback.html")

if __name__ == "__main__":
    app.run(debug=True)
