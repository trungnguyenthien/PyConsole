## 1) Install (Only 1 time after checking source)

Create Environment

```sh
python -m venv env
```

### 📔 Install / Update Package

```sh
source env/bin/activate # Active môi trường
pip install -r requirements.txt
deactivate # Deactivate
```

## 2) Active/Deactivate ENV (Everytime start developing)

```sh
# Active
source env/bin/activate

# Deactivate
deactivate
```

## 3) Build / Run

```sh
# Run (cd to project)
python manage.py runserver --noreload
```

## 4) Other

```sh
# Update requirements.txt
pip freeze > requirements.txt

# Create Migration code
python manage.py makemigrations

# Execute Migrate DB
python manage.py migrate

```

## 5) Setup in CPanel

After push app to FTP
Open terminal then

```
source /home/tsrqcmjv/virtualenv/py/slack/project/3.8/bin/activate && cd /home/tsrqcmjv/py/slack/project && pip install -r requirements.txt
```

Kill Server

```
pkill -f runserver
```

```
pip install aiohttp mysqlclient psycopg2-binary openai slack_sdk APScheduler

```
