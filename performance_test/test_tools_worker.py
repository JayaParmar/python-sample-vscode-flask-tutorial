import requests
from datetime import datetime 
import socket
import time
import sys 
import os

# one by one empty orion-ws queue and call orion-ws and record result on orion-answer queue
def empty_messages_on_queue():
    empty = False
    while not empty:
        data = {"queue": 'orion-ws', 
                }
        not_ready = True
        while not_ready:
            try:
                resp = requests.post(f'http://localhost:5555/queue/take', json=data)           
                not_ready = False
            except Exception as e:
                print(e)
                time.sleep(10)
                pass         
            time.sleep(1)
        if resp.json().get('message') == "Queue is empty.":
            empty = True
        else:
            cust_id = resp.json().get('message')[12:]
            try:
                resp = requests.get(f'http://localhost:8444/customer?customer-id={cust_id}')
            except Exception as e:
                print("Failed to call Orion-ws")
                print(e)
                sys.exit(1) 
            duration = resp.elapsed.total_seconds()
            ip_address = socket.gethostbyname(socket.gethostname())
            #user_agent = resp.request.headers.get('User-Agent')
        
            
            print("Got a reply from Orion WS  ")
            print(resp.json())
            device_id = resp.json()
            process_id = os.getpid()

            payload = {
                    "devices": f'response{device_id}',
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "process id": process_id,
                    "duration": duration,
                     "ip address": ip_address }
            data = {"queue": 'orion-answer', "message": payload}
            resp = requests.post(f'http://localhost:5555/queue/put', json=data)
            print(resp)

if __name__ == '__main__':
    empty_messages_on_queue()