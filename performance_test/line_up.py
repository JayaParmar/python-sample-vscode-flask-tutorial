from flask import Flask, jsonify, request
import sqlite3
#from werkzeug.local import LocalProxy
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for accessing the Swagger UI
API_URL = '/static/api/line_up.yaml'  # URL where your Swagger YAML file is served

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Message Queuing System API - Line-Up"
    }
)

app = Flask(__name__)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# SQLite database initialization
def get_db_connection():
    conn = sqlite3.connect('queue.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create queues table if it doesn't exist
with app.app_context():
    cursor = get_db_connection()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queues (
            name TEXT PRIMARY KEY,
            messages TEXT
        )
    ''')
    cursor.close()


@app.route('/queue/create', methods=['POST'])
def create_queue():
    queue_name = request.json.get('name')
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO queues (name, messages) VALUES (?, ?)', (queue_name, '[]'))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Queue "{queue_name}" created.'}), 201

@app.route('/queue/put', methods=['POST'])
def put_message():
    queue_name = request.json.get('queue')
    message = request.json.get('message')
    conn = get_db_connection()

    cursor = conn.execute('SELECT messages FROM queues WHERE name = ?', (queue_name,))
    row = cursor.fetchone()

    if row is None:
        return jsonify({'error': 'Queue not found.'}), 404

    messages = eval(row[0])
    messages.append(message)

    cursor.execute('UPDATE queues SET messages = ? WHERE name = ?', (str(messages), queue_name))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Message added to the queue.'}), 201


@app.route('/queue/take', methods=['POST'])
def take_message():
    queue_name = request.json.get('queue')
    conn = get_db_connection()

    cursor = conn.execute('SELECT messages FROM queues WHERE name = ?', (queue_name,))
    row = cursor.fetchone()

    if row is None:
        return jsonify({'error': 'Queue not found.'}), 404

    messages = eval(row[0])

    if len(messages) == 0:
        return jsonify({'message': 'Queue is empty.'}), 200

    message = messages.pop(0)

    conn.execute('UPDATE queues SET messages = ? WHERE name = ?', (str(messages), queue_name))
    conn.commit()
    conn.close()
    return jsonify({'message': message}), 200


@app.route('/queue/read', methods=['GET'])
def read_messages():
    queue_name = request.args.get('queue')
    conn = get_db_connection()

    sql_stmnt = f'SELECT messages FROM queues WHERE name = "{queue_name}"'
    cursor = conn.execute(sql_stmnt)
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return jsonify({'error': 'Queue not found.'}), 404

    messages = eval(row[0])
    return jsonify({'messages': messages}), 200


@app.route('/queue/statistics', methods=['GET'])
def queue_statistics():
    conn = get_db_connection()
    cursor = conn.execute('SELECT name, messages FROM queues')
    rows = cursor.fetchall()
    conn.close()
    statistics = [{'name': row[0], 'count': len(eval(row[1]))} for row in rows]
    return jsonify({'statistics': statistics}), 200


@app.route('/queue/reset', methods=['POST'])
def reset_queue():
    queue_name = request.json.get('queue')

    conn = get_db_connection()
    cursor = conn.execute('SELECT messages FROM queues WHERE name = ?', (queue_name,))
    row = cursor.fetchone()

    if row is None:
        return jsonify({'error': 'Queue not found.'}), 404

    cursor = conn.execute('UPDATE queues SET messages = ? WHERE name = ?', ('[]', queue_name))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Queue reset.'}), 200


@app.route('/queue/delete', methods=['DELETE'])
def delete_queue():
    queue_name = request.json.get('queue')

    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM queues WHERE name = ?', (queue_name,))
    row = cursor.fetchone()

    if row is None:
        return jsonify({'error': 'Queue not found.'}), 404

    conn.execute('DELETE FROM queues WHERE name = ?', (queue_name,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Queue deleted.'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
