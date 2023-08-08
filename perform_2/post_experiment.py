import requests
import sqlite3
import matplotlib.pyplot as plt


def get_readings_from_queue():
    url = "http://localhost:5555/queue/take"
    query_params = {"queue": "orion-answer"}
    queue_data = []
    message = {}
    message['message'] = 'Queue is empty.'
    while 1 == 1:
        try:
            response = requests.post(url, json=query_params)
            if response.status_code == 200:
                message = response.json()
            if message['message'] == 'Queue is empty.':
                break
            queue_data.append(message['message'])
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during the request: {e}")
    return queue_data


def get_next_run_id():
    #run_id = 0
    stmnt = "SELECT MAX(experiment_run_id) FROM experiments"
    cursor = conn.execute(stmnt)
    row = cursor.fetchone()[-1]
    print(row)
    if not row:
        run_id = 1
    else:
        run_id = row+1
    return run_id


def write_queue_data_to_sqlite(queue_data):
    start_time = "9999"
    end_time = ""
    experiment_run_id = 0
    experiment_run_id = get_next_run_id()
    stmnt = '''
        INSERT INTO readings
        (devices, duration, ip_address, process_id, 
        timestamp, experiment_run_id)
        VALUES '''
    for row in queue_data:
        stmnt += f'''(
            "{row.get('devices',    '')}",
            "{row.get('duration',  0.0)}",
            "{row.get('ip address', '')}",
            "{row.get('process id',  0)}",
            "{row.get('timestamp',  '')}",
            {experiment_run_id}
        ) ,'''
        start_time = min(start_time, row.get('timestamp',  '9999-'))
        end_time = max(end_time, row.get('timestamp',  ''))
    stmnt = stmnt[:-1]
    conn.execute(stmnt)
    conn.commit()
    data_point_count = len(queue_data)
    return start_time, end_time, experiment_run_id, data_point_count


def total_duration(experiment_run_id):
    tot_dur = []
    stmnt = f"""SELECT SUM(duration), process_id FROM readings
                WHERE experiment_run_id = {experiment_run_id}
                GROUP BY process_id"""
    cursor = conn.execute(stmnt)
    rows = cursor.fetchall()
    for row in rows:
        tot_dur.append({"total_duration": row[0], "process_id": row[1]})
    return tot_dur


def avg_duration(experiment_run_id):
    avg_dur = []
    stmnt = f"""SELECT AVG(duration), COUNT(process_id) FROM readings
                WHERE experiment_run_id = {experiment_run_id}
                GROUP BY process_id"""
    cursor = conn.execute(stmnt)
    rows = cursor.fetchall()
    for row in rows:
        avg_dur.append({"avg_duration": row[0], "process_id_count": row[1]})
    return avg_dur


def write_experiment_runid_type_to_sqlite(start_time, 
                                          end_time, 
                                          experiment_run_id, 
                                          experiment_type, 
                                          data_point_count, 
                                          tot_dur, 
                                          avg_dur):
    statistics = {"statistics": 
                  {"total_durations" : tot_dur, 
                   "average_duration": avg_dur, 
                   "no_of_jobs": data_point_count
                   }
                   }
    stmnt = f'''INSERT INTO experiments 
                (start_time, end_time, experiment_run_id, experiment_type, statistics)
                VALUES ('{start_time}', '{end_time}', '{experiment_run_id}', '{experiment_type}', "{statistics}")'''
    conn.execute(stmnt)
    conn.commit()


def plot_duration_vs_process():
    plt_title = []
    run_no = input("Please enter experiment_run_id to see the plot: ")
    stmnt = '''SELECT experiment_type FROM experiments WHERE experiment_run_id = ?'''
    cursor = conn.execute(stmnt, (run_no,))
    title = cursor.fetchall()
    print(title)
    plt_title.extend([title[0][0],"Run_id", run_no])

    stmnt = '''SELECT duration, timestamp FROM readings WHERE experiment_run_id = ?'''
    cursor = conn.execute(stmnt, (run_no,))
    rows = cursor.fetchall()  
    plt.scatter([x[1] for x in rows], [x[0]*1000 for x in rows])
    plt.xlabel('Time')
    plt.xticks([rows[0][1], rows[-1][1]], rotation=45)
    plt.ylabel('Duration (ms)')
    plt.title(plt_title)
    plt.grid(True)
    plt.tight_layout()  
    plt.savefig('plots/' + ' '.join(plt_title) + '.png')


queue_data = [{'devices': "response{'customer devices': [{'DeviceId': '9105000551', 'iv_External_Id__c': '164070'}]}", 'duration': 4.53345, 'ip address': '127.0.1.1', 'process id': 13113, 'timestamp': '2023-08-07 09:23:32'}, {'devices': "response{'customer devices': [{'DeviceId': '2309857521', 'iv_External_Id__c': '164496'}]}", 'duration': 1.526029, 'ip address': '127.0.1.1', 'process id': 13113, 'timestamp': '2023-08-07 09:23:33'}, {'devices': "response{'customer devices': [{'DeviceId': None, 'iv_External_Id__c': '3000090'}]}", 'duration': 1.021782, 'ip address': '127.0.1.1', 'process id': 13113, 'timestamp': '2023-08-07 09:23:34'}, {'devices': "response{'customer devices': [{'DeviceId': '5002000156', 'iv_External_Id__c': '1010'}]}", 'duration': 0.419916, 'ip address': '127.0.1.1', 'process id': 13113, 'timestamp': '2023-08-07 09:23:35'}, {'devices': "response{'customer devices': []}", 'duration': 0.672411, 'ip address': '127.0.1.1', 'process id': 13113, 'timestamp': '2023-08-07 09:23:36'}, {'devices': "response{'customer devices': [{'DeviceId': '4002001445', 'iv_External_Id__c': '100002'}]}", 'duration': 0.788402, 'ip address': '127.0.1.1', 'process id': 13113, 'timestamp': '2023-08-07 09:23:37'}]


conn = sqlite3.connect("database/performance_test")
conn.execute("CREATE TABLE IF NOT EXISTS experiments \
             (start_time TEXT, end_time TEXT, experiment_run_id INTEGER, \
             experiment_type TEXT, statistics TEXT) ")
conn.execute("CREATE TABLE IF NOT EXISTS readings \
             (devices TEXT, duration FLOAT, ip_address TEXT, \
             process_id TEXT, timestamp TEXT, experiment_run_id INTEGER) ")

queue_data = get_readings_from_queue()

start_time, end_time, experiment_run_id, data_point_count = \
    write_queue_data_to_sqlite(queue_data)

tot_dur = total_duration(experiment_run_id)

avg_dur = avg_duration(experiment_run_id)

# experiment_type = 'PT_WO_CP'
# experiment_type = 'PT_W_CP'
experiment_type = 'PT_W_CP_G'

write_experiment_runid_type_to_sqlite(start_time, end_time, experiment_run_id, experiment_type, data_point_count, tot_dur, avg_dur)

plot_duration_vs_process()

conn.close()
