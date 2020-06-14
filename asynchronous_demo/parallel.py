#!/usr/local/python3/bin/python3

from flask import Flask, request
from celery import Celery
import json
import requests
import time

app = Flask(__name__)
#celery = Celery(app.name, broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379//0')
celery = Celery(app.name, broker='redis://127.0.0.1:6379')


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/asynsum', methods=['GET', 'POST'])
def asynsum_dispatch():
    if request.method == 'POST':
        d = json.loads(request.get_data())
        add.delay(d)
        return json.dumps({"msg": 'ok', "code": '0'})
    else:
        return json.dumps({'msg': '', 'code': '1'})


@celery.task
def add(json_d):
    time.sleep(5)
    x = json_d['x']
    y = json_d['y']
    result = dict()
    result['taskID'] = json_d['taskID']
    result['sum'] = f'{x} + {y} = {x+y}'
    callback = json_d['callBackURL']
    headers = {"Content-Type": "text/json"}
    requests.post(callback, headers=headers, data=json.dumps(result, ensure_ascii=False))
    return


if __name__ == '__main__':
    app.run(debug=True)
