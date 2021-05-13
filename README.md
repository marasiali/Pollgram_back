# Pollgram Backend
Pollgram is a poll-based social network. Communicate with people by creating polls and vote for other's polls.

## Usage

### Clone this repository in your terminal
```
git clone https://github.com/marasiali/Pollgram_back.git
```
or

```
git clone git@github.com:marasiali/Pollgram_back.git
```

### Create virtualenv and install dependencies
```
cd Pollgram_back
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Migrations

```
cd pollgram_back
python manage.py makemigrations
python manage.py migrate
```

### Test it
run this code :
```
python manage.py runserver
```
Then, open a browser and go to `http://127.0.0.1:8000/`
