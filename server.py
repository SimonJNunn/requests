#!/usr/bin/env python3
from flask import Flask, request
from time import sleep
from random import randint

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    print(request.data.decode())
    sleep(randint(1,10))
    return request.data


if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080)