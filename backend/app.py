from flask import Flask
from leaderboard.routes import leaderboard_bp
from extensions import get_db_connection, close_db_connection  # Import database utilities

app = Flask(__name__)

# Register the leaderboard blueprint
app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')

# Ensure the database connection is closed after each request
app.teardown_appcontext(close_db_connection)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
