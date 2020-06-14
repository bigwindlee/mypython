#!/usr/local/python3/bin/python3

import json
import requests
from multiprocessing import Pool


def send_request(task_id, x, y):
    url = 'http://127.0.0.1:5000/asynsum'
    d = dict()
    d['taskID'] = task_id
    d['x'] = x
    d['y'] = y
    d['callBackURL'] = 'http://127.0.0.1:5002/callback'
    headers = {"Content-Type": "text/json"}
    requests.post(url, headers=headers, data=json.dumps(d))


if __name__ == '__main__':
    p = Pool(5)
    for i in range(10):
        task_id = f'{10000000 + i}'
        x = i + 1
        y = x * 3
        p.apply_async(send_request, args=(task_id, x, y,))

    p.close()
    p.join()
