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
        SELECT u.id AS id, u.display_name AS name, SUM(c.num_changes) AS score 
        FROM changesets c 
        INNER JOIN users u ON c.user_id = u.id
        WHERE c.closed_at >= NOW() - INTERVAL %s 
        GROUP BY display_name, u.id
        ORDER BY score DESC;
    """
    
    interval = '100 years'
    match time:
        case 'week':
            interval = '1 week'
        case 'month':
            interval = '1 month'
        case 'day':
            interval = '1 day'

    cursor.execute(query, (interval,))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{'id': row[0], 'name': row[1], 'score': row[2]} for row in rows])

@leaderboard_bp.route('/profile/map/', methods=['GET'])
def get_profile_map():
    id = request.args.get('filterId')
    time = request.args.get('filterTime')
    workspaceId = request.args.get('filterWorkspace')

    conn = get_db_connection()  # Use the globally available database connection
    cursor = conn.cursor()

    schema_query = "SET search_path TO %s, public;"
    schemaId = "workspace-" + html.escape(workspaceId)
    cursor.execute(schema_query, (schemaId,))

    query = """
        SELECT c.id, n.latitude, n.longitude
        FROM changesets c 
        INNER JOIN nodes n ON c.id = n.changeset_id
        WHERE c.closed_at >= NOW() - INTERVAL %s AND c.user_id = %s;
    """
    
    interval = '100 years'
    match time:
        case 'week':
            interval = '1 week'
        case 'month':
            interval = '1 month'
        case 'day':
            interval = '1 day'

    cursor.execute(query, (interval,id,))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{'id': row[0], 'latitude': row[1], 'longitude': row[2]} for row in rows])

@leaderboard_bp.route('/profile/stats/', methods=['GET'])
def get_profile_stats():
    id = request.args.get('filterId')
    time = request.args.get('filterTime')
    workspaceId = request.args.get('filterWorkspace')

    conn = get_db_connection()  # Use the globally available database connection
    cursor = conn.cursor()

    schema_query = "SET search_path TO %s, public;"
    schemaId = "workspace-" + html.escape(workspaceId)
    cursor.execute(schema_query, (schemaId,))

    query = """
        SELECT id, display_name AS name, creation_time AS created
        FROM users 
        WHERE id = %s;
    """
    
    interval = '100 years'
    match time:
        case 'week':
            interval = '1 week'
        case 'month':
            interval = '1 month'
        case 'day':
            interval = '1 day'

    cursor.execute(query, (id,))
    row = cursor.fetchone()
    cursor.close()
    return jsonify({'id': row[0], 'name': row[1], 'created': row[2]})