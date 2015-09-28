#!/usr/local/bin/python
from app import app
app.run(debug = True)


def start():
        app.run(host='0.0.0.0', port=80)

start()