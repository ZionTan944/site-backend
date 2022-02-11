from flask import Flask, request, abort

app = Flask(__name__)

# import declared routes
from endpoints import soccer_endpoints
