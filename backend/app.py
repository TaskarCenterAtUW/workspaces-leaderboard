from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="leaderboard",
        user="postgres",
        password="password"
    )
    return conn

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        SELECT name, score, timestamp 
        FROM leaderboard 
        WHERE timestamp BETWEEN %s AND %s 
        ORDER BY score DESC;
    '''
    cursor.execute(query, (start_time, end_time))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'name': row[0], 'score': row[1], 'timestamp': row[2]} for row in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
