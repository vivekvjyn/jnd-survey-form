# Just Noticeable Difference (JND) Survey Form

This repository is used to host the **Just Noticeable Difference (JND)** survey form as part of the **Sound and Music Computing** program at **UPF** for the **Music Cognition and Perception** course.

### [Take the Test](https://jnd-survey.vercel.app)

## Use template
Clone the Repository.
```bash
git clone https://github.com/enter-opy/jnd-survey.git
cd jnd-survey
```
Create a virtual environment.
```bash
python -m venv .venv
```
   **Windows:**
```bash
venv\Scripts\activate
```
   **Linux:**
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```

Add `.env` file in the root directory.

```makefile
SECRET_KEY=secret_key
USER=username
PASSWORD=password
DB_NAME=database_name
COLLECTION_NAME=collection_name
NUM_SAMPLES=num_samples
```

Set up a MongoDB database `DB_NAME` with collection `COLLECTION_NAME`.

```bash
cd static/audio
```
Place your positive and negative samples here.

To run locally,

```bash
python -m flask run
```

## License
This project is licensed under the GNU General Public License. See the [LICENSE](https://github.com/enter-opy/jnd-survey/blob/main/LICENSE) for details.