# Convo

Convo is a Python based Flask app that allows users to submit questions and answers, up vote questions and answers, search keywords, and investigate trending words. As a community, the users on Convo engage with each other to learn different perspectives, share a space of mutual betterment, and recognize the strength in understanding.

<img src="/static/Convo_home.png">


# Stack

Python/Flask backend, PostgreSQL database, SQLalchemy, Jinja templating, Facebook Login/Logout API, AWS deployment

### Live Demo

https://www.youtube.com/watch?v=M_NJNVTsh1E&feature=youtu.be

# Features

## Safe Login/Logout with Facebook API

### Initial Login

<img src="/static/Convo_login.png">


### Authentication with Facebook

<img src="/static/Convo_login_cont.png">


### Submit a Question

<img src="/static/Convo_questions.png">


### Submit an Answer

<img src="/static/Convo_submit_answ.png">

### Edit an Answer

<img src="/static/Convo_edit_answ2.png">


### Up Vote a Question or Answer

<img src="/static/Convo_vote_up.png">


### Search 

<img src="/static/Convo_search.png">


# Installation

Install the dependencies and start the server.

```
cd HBF_PROJECT 
pip install virtualenv 
virtualenv env 
source env/bin/activate 
pip install -r requirements.txt 
python server.py
```

# Tests
There are tests covering all routes.

```
python test.py
```
