from flask import Blueprint, request, jsonify
from flask_cors import CORS
from extensions import get_workspace_cursor, time_to_interval

leaderboard_bp = Blueprint('leaderboard', __name__)
CORS(leaderboard_bp) #, origins=["http://localhost:*", "http://*.sidewalks.washington.edu", "https://*.sidewalks.washington.edu"])

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    team = request.args.get('filterTeam')
    time = request.args.get('filterTime')
    workspaceId = request.args.get('filterWorkspace')

    cursor = get_workspace_cursor(workspaceId)
    
    match team:
        case "team":
            query = """
                SELECT t.id AS id, t.name, SUM(COALESCE(c.num_changes, 0)) AS score 
                FROM teams t
                INNER JOIN team_user tu ON t.id = tu.team_id
                INNER JOIN users u ON tu.user_id = u.id
                LEFT OUTER JOIN changesets c on c.user_id = u.id
                AND c.closed_at >= NOW() - INTERVAL %s
                WHERE t.workspace_id = %s
                GROUP BY t.name, t.id
                ORDER BY score DESC;
            """
            params = (time_to_interval(time), workspaceId)
        case _:
            query = """
                SELECT u.id AS id, u.display_name AS name, SUM(c.num_changes) AS score 
                FROM changesets c 
                INNER JOIN users u ON c.user_id = u.id
                WHERE c.closed_at >= NOW() - INTERVAL %s 
                GROUP BY display_name, u.id
                ORDER BY score DESC;
            """
            params = (time_to_interval(time),)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{'id': row[0], 'name': row[1], 'score': row[2]} for row in rows])