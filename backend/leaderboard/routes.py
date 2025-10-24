from flask import Blueprint, request, jsonify
from flask_cors import CORS
from extensions import get_workspace_cursor, time_to_interval

leaderboard_bp = Blueprint('leaderboard', __name__)
CORS(leaderboard_bp, origins=["http://localhost:*", "http://*.sidewalks.washington.edu", "https://*.sidewalks.washington.edu"])

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    team = request.args.get('filterTeam')
    time = request.args.get('filterTime')
    workspaceId = request.args.get('filterWorkspace')

    cursor = get_workspace_cursor(workspaceId)
    
    match team:
        case "team":
            query = """
                SELECT t.id AS id, t.name, SUM(c.num_changes) AS score 
                FROM changesets c 
                INNER JOIN users u ON c.user_id = u.id
                INNER JOIN team_user tu ON u.id = tu.user_id
                INNER JOIN team t ON tu.team_id = t.id
                WHERE c.closed_at >= NOW() - INTERVAL %s 
                GROUP BY t.name, t.id
                ORDER BY score DESC;
            """
        case _:
            query = """
                SELECT u.id AS id, u.display_name AS name, SUM(c.num_changes) AS score 
                FROM changesets c 
                INNER JOIN users u ON c.user_id = u.id
                WHERE c.closed_at >= NOW() - INTERVAL %s 
                GROUP BY display_name, u.id
                ORDER BY score DESC;
            """
    
    interval = time_to_interval(time)

    cursor.execute(query, (interval,))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{'id': row[0], 'name': row[1], 'score': row[2]} for row in rows])