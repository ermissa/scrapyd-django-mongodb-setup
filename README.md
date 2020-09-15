This is a setup project to run Scrapy + Django and save parsed data to MongoDB. 

# Installation

## Install Docker and Docker Compose

- Docker Installation: https://docs.docker.com/v17.12/install/
- Docker Compose Installation: https://docs.docker.com/compose/install/

## Create Virtual Environment

```bash
python3 -m venv env
```

## Activate virtual environment

```bash
source env/bin/bash/activate
```

## Install Requirements

```bash
pip3 install -r requirements.txt
```

# Run Project

> ***You should run Scrapyd and Django in virtual environment !***

## 1- Run MongoDB

```bash
docker-compose -f docker-compose.mongo.yml up
```

## 2- Run Scrapyd

Firstly you should create egg file to be able to run scrapyd.

Edit *scrapy.cfg* file as;

```bash
[deploy:target_name]
url = http://localhost:6800/
project = scrapy_project
```

Run below command to deploy:

```bash
scrapyd-deploy target_name -p scrapy_project
```

then run scrapyd;

```bash
scrapyd
```

## 3- Run Django

```bash
cd django_project
python3 manage.py runserver
```

Now, Django is running on http://localhost:8000 and Scrapyd is running on http://localhost:6800.

You can send request to Django to check if the system is working correctly. Demo spider crawls *http://quotes.toscrape.com/*, so you should send this address as URL parameter. 

```bash
curl http://localhost:8000/crawl -d url=http://quotes.toscrape.com/
```

Sample expected response (task_id and unique_id values will be different): 

```
{"task_id": "56a99152f77411ea8a5480e650218898", "unique_id": "36ba7d8b-cdde-4565-a73b-44b10ea55e1d", "status": "started"}
```


This repo is inspired from: https://github.com/adriancast/Scrapyd-Django-Template


## TODO

- [ ] Add system flow diagram