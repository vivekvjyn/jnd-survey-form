import os
import random
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

# Database connection
uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@cluster0.dbm54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[os.getenv('DB_NAME')]
collection = db["responses"]

# Total number of audio samples for the survey
n_samples = 12

# Load the positive audio sample filenames
positives = [
    f"positives/{sample}" for sample in os.listdir("static/audio/positives")
]
positives = random.sample(positives, n_samples - 3) # Randomly select required positive samples

# Load the negative audio sample filenames
negatives = [
    f"negatives/{sample}" for sample in os.listdir("static/audio/negatives")
]

# Combine positives and negatives, then shuffle the samples
samples = positives + negatives
random.shuffle(samples)

@app.route("/")
def index():
    """
    Render the welcome page.
    """
    return render_template("index.html")

@app.route("/form", methods=["GET"])
def form():
    """
    Render the survey form.
    """
    return render_template("form.html", samples=samples, enumerate=enumerate)
    
@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Save the responses to the database,  and render a confirmation page.
    """
    if request.method == "POST":
        # Get the responses from the submitted form
        responses = [request.form.get(f"sample-{i}") for i in range(n_samples)]

        # Convert 'yes'/'no' responses to binary (1/0)
        responses = [1 if response == "yes" else 0 for response in responses]

        # Save the responses to the database
        collection.insert_one({"samples": samples, "responses": responses})

        # Render the confirmation
        return render_template("feedback.html")

if __name__ == "__main__":
    app.run(debug=True)
