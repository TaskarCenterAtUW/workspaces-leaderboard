from flask import Blueprint, request, jsonify
from flask_cors import CORS
from extensions import get_workspace_cursor, time_to_interval

profile_bp = Blueprint('profile', __name__)
CORS(profile_bp, origins=["http://localhost:*", "https://*.sidewalks.washington.edu"])

@profile_bp.route('/map/', methods=['GET'])
def get_profile_map():
    id = request.args.get('filterId')
    team = request.args.get('filterTeam')
    time = request.args.get('filterTime')
    workspaceId = request.args.get('filterWorkspace')

    cursor = get_workspace_cursor(workspaceId)

    query = """
        SELECT c.id, n.latitude, n.longitude
        FROM changesets c 
        INNER JOIN nodes n ON c.id = n.changeset_id
        WHERE c.closed_at >= NOW() - INTERVAL %s
    """

    match team:
        case "team":
            query += " AND c.user_id IN (SELECT user_id FROM team_user WHERE team_id = %s);"
        case _:
            query += " AND c.user_id = %s;"

    interval = time_to_interval(time)

    cursor.execute(query, (interval,id,))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{'id': row[0], 'latitude': row[1], 'longitude': row[2]} for row in rows])

@profile_bp.route('/stats/', methods=['GET'])
def get_profile_stats():
    id = request.args.get('filterId')
    team = request.args.get('filterTeam')
    workspaceId = request.args.get('filterWorkspace')

    cursor = get_workspace_cursor(workspaceId)

    match team:
        case "team":
            query = """
                SELECT id, name, '' AS created
                FROM teams
                WHERE id = %s;
            """
        case _:
            query = """
                SELECT id, display_name AS name, creation_time AS created
                FROM users 
                WHERE id = %s;
            """

    cursor.execute(query, (id,))
    row = cursor.fetchone()
    cursor.close()
    return jsonify({'id': row[0], 'name': row[1], 'created': row[2]})