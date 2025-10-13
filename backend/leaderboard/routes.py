from flask import Blueprint, request, jsonify
from flask_cors import CORS
from extensions import get_db_connection  # Use the global database connection
import html

leaderboard_bp = Blueprint('leaderboard', __name__)
CORS(leaderboard_bp)

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    workspaceId = request.args.get('filterWorkspace')
    time = request.args.get('filterTime')

    conn = get_db_connection()  # Use the globally available database connection
    cursor = conn.cursor()

    schema_query = "SET search_path TO %s, public;"
    schemaId = "workspace-" + html.escape(workspaceId)
    cursor.execute(schema_query, (schemaId,))

    query = """
        SELECT u.display_name AS name, SUM(c.num_changes) AS score 
        FROM changesets c 
        INNER JOIN users u ON c.user_id = u.id
        WHERE c.closed_at >= NOW() - INTERVAL %s 
        GROUP BY display_name
        ORDER BY score DESC;
    """
    
    interval = '100 years'
    match time:
        case 'week':
            interval = '1 week'
        case 'month':
            interval = '1 month'

    cursor.execute(query, (interval,))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{'name': row[0], 'score': row[1]} for row in rows])
