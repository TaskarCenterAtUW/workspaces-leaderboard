from flask import Flask
from flask_cors import CORS
from leaderboard.routes import leaderboard_bp
from extensions import get_db_connection, close_db_connection

app = Flask(__name__)
CORS(app)

# Register the blueprints
app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')

# Ensure the database connection is closed after each request
app.teardown_appcontext(close_db_connection)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
