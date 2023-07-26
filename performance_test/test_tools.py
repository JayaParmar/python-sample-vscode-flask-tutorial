import requests
from datetime import datetime 
import os

import socket

process_id = os.getpid()
# reset orion-ws and orion-answer queue
def reset_queues():
    for name in ['orion-ws', 'orion-answer']:
        data = {"queue": name}
        resp = requests.post(f'http://localhost:5555/queue/reset', json=data)
        print(resp.text)

# create orion-ws and orion-answer queue
def create_queues():
    for name in ['orion-ws', 'orion-answer']:
        data = {"name": name}
        resp = requests.post(f'http://localhost:5555/queue/create', json=data)
        print(resp.text)

# put 10 messages for calling orion ws on a queue called orion-ws
def put_messages_on_queue():
    for cust_id in [188934,164070, 164496, 3000090, 100002, 3010, 5010, 267038, 267038, 1240608]:
        print(f"i is now {cust_id}")
        data = {"queue": 'orion-ws', 
                "message": f'customer id {cust_id}'}
        resp = requests.post(f'http://localhost:5555/queue/put', json=data)
        print(resp)
        
# one by one empty orion-ws queue and call orion-ws and record result on orion-answer queue
def empty_messages_on_queue():
    empty = False
    while not empty:
        data = {"queue": 'orion-ws', 
                }
        resp = requests.post(f'http://localhost:5555/queue/take', json=data)
        if resp.json().get('message') == "Queue is empty.":
            empty = True
        else:
            cust_id = resp.json().get('message')[12:]
            # print(resp.json().get('message'))
            resp = requests.get(f'http://localhost:8444/customer?customer-id={cust_id}')
            duration = resp.elapsed.total_seconds()
            ip_address = socket.gethostbyname(socket.gethostname())
            user_agent = resp.request.headers.get('User-Agent')
            
            print("Got a reply from Orion WS  ")
            print(resp.json())
            device_id = resp.json()

            payload = {
                    "devices": f'response{device_id}',
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "process id": process_id,
                    "duration": duration,
                    "user agent": user_agent,
                     "ip address": ip_address }
            data = {"queue": 'orion-answer', "message": payload}
            resp = requests.post(f'http://localhost:5555/queue/put', json=data)
            print(resp)

if __name__ == '__main__':
    # create_queues()
    reset_queues()
    put_messages_on_queue()
    empty_messages_on_queue()


# Questions 26/07- 
#  Identify what user information is needed - https://requests.readthedocs.io/en/latest/api/ 
# how to use a SQL alchemy connection pool in this test script (Snowflake data) ?