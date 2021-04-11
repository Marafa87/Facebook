import binascii
import hashlib
import os
import ast
import re
import sys
import uuid
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from functools import wraps

from apispec.ext.marshmallow import MarshmallowPlugin
from flask_json import FlaskJSON, json_response
from flask_cors import CORS
from flask import Flask, g, request, send_from_directory, abort, request_started,render_template
from flask_restful import Resource, Api, reqparse
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_restful_swagger_2 import Api, swagger, Schema

app = Flask(__name__)  # Flask app instance initiated

CORS(app)
FlaskJSON(app)

api = Api(app, title='Social Network Project API', api_version='0.0.10')
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Social Network Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

@api.representation('application/json')
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)

def env(key, default=None, required=True):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError("Missing required environment variable '%s'" % key)



app.config['SECRET_KEY'] = env('SECRET_KEY')

docs = FlaskApiSpec(app)
