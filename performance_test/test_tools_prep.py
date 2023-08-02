import requests
#from datetime import datetime 

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
    for cust_id in [188934,164070, 164496, 3000090, 100002, 3010, 5010, 267038, 100002, 1240608]:
        print(f"i is now {cust_id}")
        data = {"queue": 'orion-ws', 
                "message": f'customer id {cust_id}'}
        resp = requests.post(f'http://localhost:5555/queue/put', json=data)
        print(resp)

# delete/remove myqueue from queues
def remove_queue():
    #for name in ['myqueue']:
    data = {"queue": "myqueue"} 
    resp = requests.post(f'http://localhost:5555/queue/delete', json=data)
    print(resp.text)

if __name__ == '__main__':
    # create_queues()
    reset_queues()
    put_messages_on_queue()
    # remove_queue()
    