# chirpr_api
A Twitter esque social media with search Bookmark functionality

## Introduction

## Overview
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

## Development Setup
### **Download the project starter code locally**
```
git clone https://github.com/jefedcreator/chirpr_api.git
cd chirpr_api/
```
These are the files relevant for this project:
```bash
.
├── flaskr
    ├── __init__.py
├── README.md
├── requirements.txt
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

### **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

## API Example

`GET '/api/v1.0/users'`
