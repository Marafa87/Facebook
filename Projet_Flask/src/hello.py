# from virtualenv import cli_run

# cli_run(["venv"])
import contextvars
from main import displayAllDb
from form import formulaire
from pymongo import MongoClient
from flask import Flask, request
from flask import jsonify
# from flask import *
# import flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"
    # "Bonjour Mr Vous allez bien j'espère..????"

@app.route('/route/API')
def display():
    df = displayAllDb()
    return 'My name is Ali !!!'

@app.route('/user/API')
def usere():
    fo=formulaire()
    return fo

@app.route('/home', methods=['GET'])
def home():
    df = displayAllDb()
    print(df)
    ret = "<h1>Distant Reading Archive</h1>{df}<p>This site is a prototype API for distant reading of science fiction novels.</p>"
    return jsonify(df)
