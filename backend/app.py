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
    '''
    workspace = request.args.get('filterWorkspace')
    time = request.args.get('filterTime')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        SELECT name, score 
        FROM leaderboard 
        WHERE workspace_id = %s  
        ORDER BY score DESC;
    '''
    cursor.execute(query, (workspace))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'name': row[0], 'score': row[1]} for row in rows])
    '''
    return [
    { "name": "Ostentatious Otters", "score": 1500 },
    { "name": "Bouncy Birbs", "score": 1400 },
    { "name": "Cute Capybaras", "score": 1350 },
    { "name": "Delightful Ducks", "score": 1300 },
    { "name": "Eager Elephants", "score": 1250 }
    ]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
