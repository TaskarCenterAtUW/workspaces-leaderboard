from flask import Flask
from flask_cors import CORS
from extensions import close_db_connection
from leaderboard.routes import leaderboard_bp
from profile.routes import profile_bp

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app) #, origins=["http://localhost:*", "https://*.sidewalks.washington.edu"])

# Register the blueprints
app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')
app.register_blueprint(profile_bp, url_prefix='/api/leaderboard/profile')

# Ensure the database connection is closed after each request
app.teardown_appcontext(close_db_connection)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
