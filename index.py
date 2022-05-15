from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


# import declared routes
from endpoints import soccer_endpoints
from endpoints import nba_endpoints
