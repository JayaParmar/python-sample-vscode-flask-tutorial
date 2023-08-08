from config import snowflake_config
import snowflake.connector
import pandas as pd
import requests
import matplotlib.pyplot as plt
import sqlite3
import sys
from datetime import datetime


def snowflake_cust_ids():
    """ Import Snowflake data in a csv file for testing"""
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()
    query = """select * from TALEND_DB.TALEND_SCH.SNOWFLAKE_ASSET"""
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows)
    output_file = "snowflake_data.csv"
    df.to_csv(output_file)


def response_queue_to_python(db_file):
    """Read orion-answer queue into my_database.db"""
    url = "http://localhost:5555/queue/read"
    query_params = {"queue": "orion-answer"}
    start_time = "9999"
    end_time = ""
    try:
        response = requests.get(url, params=query_params)

        if response.status_code == 200:
            data_dict = response.json()
            
            conn = sqlite3.connect(db_file)
            cursor = conn.execute('''
                CREATE TABLE IF NOT EXISTS new_data (
                devices TEXT, 
                duration FLOAT, 
                ip_address TEXT, 
                process_id INTEGER, 
                timestamp TEXT 
                )'''
            )
            
            stmnt = '''
                INSERT INTO new_data 
                (devices, duration, ip_address, process_id, timestamp)
                VALUES '''
            for row in data_dict['messages']:
                stmnt += f'''(
                    "{row.get('devices',    '')}",
                    "{row.get('duration',  0.0)}",
                    "{row.get('ip address', '')}",
                    "{row.get('process id',  0)}",
                    "{row.get('timestamp',  '')}"
                ) ,'''
                start_time = min(start_time, row.get('timestamp',  '9999-'))
                end_time = max(end_time, row.get('timestamp',  ''))
            stmnt = stmnt[:-1]
            cursor = conn.execute(stmnt)           
            conn.commit()
            stmnt = '''SELECT max(run_no) as last_run_no from last_run_info'''
            cursor = conn.execute(stmnt)           
            row = cursor.fetchone()
            
            last_run_no = row[0] if row and row[0] else 0

            stmnt = f'''INSERT INTO last_run_info 
                        (start_timestamp, end_timestamp, run_no)
                        VALUES ('{start_time}', '{end_time}', {last_run_no+1})'''
            print(stmnt)
            cursor = conn.execute(stmnt)
            conn.commit()
            cursor.close()
            conn.close()
            return last_run_no
        
        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the request: {e}")
  

def create_last_run_table(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # stmnt = ''' CREATE TABLE IF NOT EXISTS last_run_info (start_timestamp TEXT, end_timestamp TEXT, run_no INTEGER)'''
    stmnt = '''DROP TABLE last_run_info'''
    cursor.execute(stmnt)
    conn.commit()
    stmnt = ''' CREATE TABLE IF NOT EXISTS last_run_info (start_timestamp TEXT, end_timestamp TEXT, run_no INTEGER)'''
    cursor.execute(stmnt)
    conn.commit()
    cursor.close()
    conn.close()    


def table_with_run_no(db_file, run_no):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    result = []
    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS new_data_with_run_no (devices, duration, ip_address, process_id, timestamp, run_no)''')
    # Insert data from the "new_data" table
    cursor.execute('''INSERT INTO new_data_with_run_no(devices, duration, ip_address, process_id, timestamp) SELECT devices, duration, ip_address, process_id, timestamp FROM new_data''')
    
    # Get the latest run_no from the user or take the latest run_no
    if run_no is None:
        stmnt = ''' SELECT MAX(run_no) FROM last_run_info)'''
        cursor.execute(stmnt)
        result = cursor.fetchone()
        if run_no is not None:
            run_no = result[0]

    if (not result or len(result) == 0):
        # Update run_no for the newly inserted rows based on the timestamp
        stmnt = ''' UPDATE new_data_with_run_no SET run_no = ? WHERE timestamp BETWEEN ? AND ? '''
        cursor.execute(stmnt, (result[2], result[0], result[1]))
    
    conn.commit()
    cursor.close()
    conn.close()  


def plot_duration_vs_processid(db_file):
    """Plot duration versus processid 
    i. without connection pool;    ii. with connection pool, three workers without gunicorn;    iii. with connection pool, three workers with gunicorn """

    run_no = input("Please enter experiment_run_id to see the plot: ")
        
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if run_no:
        stmnt = '''SELECT * FROM new_data_with_run_no WHERE run_no = ?'''
        cursor.execute(stmnt, (run_no))
    else:
        stmnt = '''SELECT * FROM new_data'''
        cursor.execute(stmnt)
     
    df = pd.read_sql_query(stmnt, conn)
    #print(df.head)

    total_duration_by_process = df.groupby('process_id')['duration'].sum()
    total_jobs = df.groupby('process_id')['duration'].count()
    average_duration_per_process = df.groupby('process_id')['duration'].mean()
    
    with open('performance_duration.txt', 'a') as f:  # Redirect the print statement to the file
        sys.stdout = f
        print(f"Average duration per process: {average_duration_per_process}")
        print(f"Total duration: {total_duration_by_process}")
        print(f"Total jobs: {total_jobs}")
    sys.stdout = sys.__stdout__

    plt.scatter(df['timestamp'], df['duration']*1000)
    plt.xlabel('Timestamp')
    plt.xticks([df['timestamp'].iloc[0], df['timestamp'].iloc[-1]], rotation=45)
    plt.ylabel('Duration (ms)')
    plt.title(db_file)
    plt.grid(True)
    plt.tight_layout()  
    plt.savefig(db_file+' plot.png')

 
if __name__ == '__main__':
    #snowflake_cust_ids    
    db_file = "db_wo_cp.db"
    #db_file = "db_w_cp.db"
    #db_file = "db_w_cp_g.db"
    create_last_run_table(db_file)
    run_no = response_queue_to_python(db_file)
    #response_queue_to_python(db_file)
    table_with_run_no(db_file, run_no)
    plot_duration_vs_processid(db_file)
