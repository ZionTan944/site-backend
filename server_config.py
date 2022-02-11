import os
from index import *

app.debug = True
host = os.environ.get("IP", "0.0.0.0")
port = int(os.environ.get("PORT", 8080))
app.run(host=host, port=port)
