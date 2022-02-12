from flask import Flask, request, abort
from database.db_setup import create_connection

app = Flask(__name__)


# import declared routes
from endpoints import soccer_endpoints
