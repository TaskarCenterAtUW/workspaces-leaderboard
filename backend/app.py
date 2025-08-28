from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection(sanitizedWorkspaceId):
    conn = psycopg2.connect(
        host="localhost",
        database="workspace" + "-" + sanitizedWorkspaceId,
        user="postgres",
        password="password"
    )
    return conn

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    '''
    workspaceId = request.args.get('filterWorkspace')
    time = request.args.get('filterTime')

    interval = '100 years' // all time
    match time:
        case 'week':
            interval = '1 week'
        case 'month':
            interval = '1 month'

    sanitizedWorkspaceId = html.escape(workspaceId)
    conn = get_db_connection(sanitizedWorkspaceId)
    cursor = conn.cursor()
    query = '''
        SELECT c.user_id AS name, c.num_changes AS score 
        FROM changesets c 
        WHERE c.closed_at >= NOW() - INTERVAL %s 
        GROUP BY c.user_id 
        ORDER BY score DESC;
    '''
    cursor.execute(query, (interval))
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
