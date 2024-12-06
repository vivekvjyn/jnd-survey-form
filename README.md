# Just Noticeable Difference (JND) Survey Form

This repository is used to host the **Just Noticeable Difference (JND)** survey form as part of the **Sound and Music Computing** program at **UPF** for the **Music Cognition and Perception** course.

### [Take the Test](https://jnd-survey.vercel.app)

## Use template
Clone the Repository.
```bash
git clone https://github.com/enter-opy/strawberry-fields.git
cd sound-of-music
```
### Environment setup
Create a virtual environment.
```bash
pip install virtualenv
virtualenv venv
```
Activate the environment.

   **Windows:**
```bash
venv\Scripts\activate
```

   **Linux:**
```bash
source venv/bin/activate
```

Install the required packages using pip with the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory of your project and copy the following into the file.

```makefile
SECRET_KEY=secret_key
USER=username
PASSWORD=password
DB_NAME=database_name
COLLECTION_NAME=collection_name
```
Configure your `.env` with appropriate variables.

Ensure you have MongoDB installed and running. Create a database named `DB_NAME` with a collection named `COLLECTION_NAME`.

Make desired changes.

### Run the application

```bash
python -m flask run
```

## License
This project is licensed under the GNU General Public License. See the [LICENSE](https://github.com/enter-opy/jnd-survey/blob/main/LICENSE) for details.