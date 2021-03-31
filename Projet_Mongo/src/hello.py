# from virtualenv import cli_run

# cli_run(["venv"])

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/route/API')
def display():
    return 'My name is Ali !!!'