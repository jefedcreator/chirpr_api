# chirpr_api
A Twitter esque social media with search Bookmark functionality

# Table of Contents
[Intoduction](#Introduction) 

[Getting Started](#getting-started)

[Development Setup](#development-setup)

[API Walkthrough](#api-walkthrough)

[Docker](#docker)

[Testing](#testing)

[Live](#live-server)

## Introduction
Twitter is a popular micro blogging social media where users can share tweets on their timeline, and also save particulat tweets theyre interested in a bookmarks section. but twitter requires users to keep scrolling in their bookmark sections whenever they're in need of a particular bookmarked tweet. Enter chirpr, chirpr aims to solve this UX problem by introducing searchable boomarks in every user's bookmark section, just by typing particular words in the search bar, bookmarked tweets are filtered by the typed keywords. 

### Entity Relationship Diagram
![My Image](chirpr_api_edr.jpg)


## Overview
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/chirpr_api` directory and running:

bash
```
pip install -r requirements.txt
```
##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

## Development Setup
### **Download the project starter code locally**
```
git clone https://github.com/jefedcreator/chirpr_api.git
cd chirpr_api/
```
These are the files relevant for this project:
```bash
.

????????? models.py
????????? settings
    ????????? settings.py
????????? .venv
????????? .env
????????? README.md
????????? test.py
????????? app.py
????????? Procfile
????????? runtime.txt
????????? requirements.txt
????????? wsgi.py
????????? Dockerfile
????????? .gitignore

```

### **To comtribute to the upstream repository path from your local repository, use the commands below:**
```
git remote add upstream https://github.com/jefedcreator/chirpr_api.git
git remote -v 
git checkout -b <branch name>
```
Once you have finished editing your code, you can push the local repository to the Github repository using the following commands.
```
git add . --all   
git commit -m "your comment"
git push -u origin <branch name>
```

### **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

### **Install the dependencies:**
```
pip install -r requirements.txt
```

### **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
flask run
```
To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

alternatively, run

```bash
python wsgi.py
```

### **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

## API Walkthrough

`GET '/api/users'`
- Fetches a dictionary of all users in which the keys are the user ids and the value is the corresponding dictionary of the user  details
- Request Arguments: None
- Returns: An object with a two key,`success`, that contains a value of `True` if successful and `users`, that contains an object of `user_obj ` key: value pairs.

```json
{
  "success" : "True",
  "users": "user_obj"
}
```

`POST '/api/users/create'`

Sends a post request in order to create a new user dictionary with user details
Request Body:

```json
{
    "id": "user id",
    "name": "user name",
    "url": "user url",
    "tweets": "[]",
}
```

Returns: An object with a two key,`success`, that contains a value of `True` if successful and `users`, that contains an object of `user_obj ` key: value pairs.

```json
{
    
    "success" : "True",
    "users": "user_obj"
}
```

`POST '/api/login'`

Sends a post request in order to login an existing user, receives a json request with user details
Request Body:

```json
{
    "id": "user id",
    "name": "user name",
}
```

Returns: An object with a key,`success`, that contains a value of `True` if successful, or `False` is user does not exist

```json
{
    
    "success" : "True",
}
```

`GET '/api/users/${user_id}'`

Fetches entire user details, including tweets for a user specified by their id request argument
Request Arguments: id - string
Returns: A list of objects with user details for the specified user, and a list of all user tweets

```json
{
    "success": "True",
    "user" : "user_list"
}
```

`GET '/api/tweets'`

- Fetches a dictionary of all tweets in which the keys are the tweet ids and the value is the corresponding dictionary of the tweet  details
- Request Arguments: None
- Returns: An object with a two key,`success`, that contains a value of `True` if successful and `tweets`, that contains an object of `tweets ` key: value pairs.

```json
{
  "success" : "True",
  "users": "all_tweets"
}
```

`POST '/api/tweets/create'`

Sends a post request in order to create a new tweet dictionary with tweet details
Request Body:

```json
{
    "id": "tweet id",
    "text": "tweet text",
    "author": "tweet author",
    "timestamp": "123",
    "likes": "[]",
    "replies": "[]",
    "replying_to": ""
}
```

Returns: An object with a two key,`success`, that contains a value of `True` if successful and `tweets`, that contains an object of `all_tweets ` key: value pairs.

```json
{
    
    "success" : "True",
    "tweets": "all_tweets"
}
```

`GET '/api/tweets/${tweet_id}'`

Fetches entire tweet details, including tweets for a user specified by their id request argument
Request Arguments: id - string
Returns: A list of objects with tweet details for the specified tweet id

```json
{
    "success": "True",
    "user" : "tweet_list"
}
```

`PATCH '/api/tweets/${tweet_id}'`

Modifies the `likes` and `replies` column specified by the `tweet_id`. this request checks if a `user's likes` already exists within the likes array and pops it, else appends to it.
this request also checks if a `user's replies` already exists within the replies array and pops it, else appends to it.
this request also checks if a tweet is a reply to another tweet to it, else null.

Request Body:

```json
{
    "likes": "user id",
    "replies": "user replies",
    "replying_to": "tweet id"
}
```

`GET '/api/bookmarks/user_id'`
- Fetches a dictionary of all bookmarks in which the keys are the bookmarks ids and the value is the corresponding dictionary of the bookmark details
- Request Arguments: None
- Returns: An object with a two key,`success`, that contains a value of `True` if successful and `bookmarks`, that contains an object of `bookmarks ` key: value pairs.

```json
{
  "success" : "True",
  "tweets": "all_bookmarks"
}
```

`POST '/api/bookmarks/create'`

Sends a post request in order to create a new bookmark dictionary with tweet details
Request Body:

```json
{
    "id": "bookmark id",
    "text": "bookmark text",
    "author": "bookmark author",
    "timestamp": "123",
    "likes": "[]",
    "replies": "[]",
    "replying_to": ""
}
```

Returns: An object with a two key,`success`, that contains a value of `True` if successful and `tweets`, that contains an object of `all_tweets ` key: value pairs.

```json
{
    
    "success" : "True",
    "tweets": "all_bookmarks"
}
```

`GET '/api/bookmark/${bookmark_id}'`

Fetches entire bookmark details, including bookmarks for a user specified by their id request argument
Request Arguments: id - string
Returns: A list of objects with tweet details for the specified bookmark id

```json
{
    "success": "True",
    "tweets": "bookmark_list"
}
```

`DELETE '/api/bookmark/${bookmark_id}'`

deletes entire bookmark details, including bookmarks for a user specified by their id request argument
Request Arguments: id - string
Returns: `success` with value of `True`

```json
{
    "success": "True"
}
```

`POST '/api/bookmarks/search'`

Receives a json request `search_term` and filters the Bookmark database, and returns a list of Bookmarks containing `id` and `text` object that match specified request

```json
{
    "success": "True",
    "bookmarks": "bookmarks"
}
```

## Docker
After cloning, Navigate to the `chirpr_api` folder
```bash
cd chirpr_api
``` 
Open the VS code editor to display the file content

```bash
code .
```

Build an image

```bash
docker build -t chirprapi .

```
check list of images

```bash
docker image ls

```

Create and run a container

```bash
docker run --name chirprapi -p 80:8080 chirprapi

```

Access the application

```bash
# Mac/Linux users only
curl http://0.0.0.0/
# Windows users using WSL/GitBash
curl http://127.0.0.1:80/
```

## Testing
```bash

python test.py
```

## Live server

<b>[chirpr](https://chirpr-api.herokuapp.com/swagger)