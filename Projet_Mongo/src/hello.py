# from virtualenv import cli_run

# cli_run(["venv"])
from main import displayAllDb
from pymongo import MongoClient
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/route/API')
def display():
    df = displayAllDb()
    return 'My name is Ali !!!'

@app.route('/home', methods=['GET'])
def home():
    df = displayAllDb()
    print(df)
    ret = "<h1>Distant Reading Archive</h1>{df}<p>This site is a prototype API for distant reading of science fiction novels.</p>"
    return jsonify(df)
