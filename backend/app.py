from flask import Flask, request, jsonify
import html, os, psycopg2

app = Flask(__name__)

# Access the environment variable
db_dbname = os.environ.get("WS_OSM_DB_NAME")
db_host = os.environ.get("WS_OSM_DB_HOST")
db_user = os.environ.get("WS_OSM_DB_USER")
db_password = os.environ.get("WS_OSM_DB_PASS")

def get_db_connection(sanitizedWorkspaceId):
    conn = psycopg2.connect(
        host=db_host,
        database=db_dbname,
        user=db_user,
        password=db_password
    )
    return conn

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    workspaceId = request.args.get('filterWorkspace')
    time = request.args.get('filterTime')

    interval = '100 years'
    match time:
        case 'week':
            interval = '1 week'
        case 'month':
            interval = '1 month'

    sanitizedWorkspaceId = html.escape(workspaceId)
    conn = get_db_connection(sanitizedWorkspaceId)
    cursor = conn.cursor()

    schema_query = "SET search_path TO workspace-{sanitizedWorkspaceId}, public;"
    cursor.execute(schema_query)

    query = """
        SELECT u.display_name AS name, c.num_changes AS score 
        FROM changesets c 
        INNER JOIN users u ON c.user_id = u.id
        WHERE c.closed_at >= NOW() - INTERVAL %s 
        GROUP BY c.user_id 
        ORDER BY score DESC;
    """
    
    cursor.execute(query, (interval))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'name': row[0], 'score': row[1]} for row in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
