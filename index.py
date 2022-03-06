from flask import Flask, request, abort
from database.db_setup import create_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


# import declared routes
from endpoints import soccer_endpoints
