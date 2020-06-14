#!/usr/local/python3/bin/python3

from flask import Flask, request
import json
import datetime

app = Flask(__name__)


@app.route('/callback', methods=['POST'])
def callback():
    d = json.loads(request.get_data())
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"'{timestamp}' taskID = {d['taskID']}, {d['sum']}")
    return json.dumps({"msg": 'ok', "code": '0'})

if __name__ == '__main__':
    app.run(port='5002', debug=True)
