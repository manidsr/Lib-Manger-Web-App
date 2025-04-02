from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from models.user import User
from flask import send_from_directory

# Initialize extensions
login_manager = LoginManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Session configuration (ADD THIS)
    app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False,  # Keep False for HTTP development
    SESSION_COOKIE_DOMAIN=None    # Allow both 127.0.0.1 and localhost
    )
    
    # Initialize extensions
    login_manager.init_app(app)
    cors.init_app(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:5000",
        "http://127.0.0.1:5000"  # Add both localhost variants
    ],
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE"]
    )

    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000, http://127.0.0.1:5000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    # Import blueprints
    from routes.auth import auth_bp
    from routes.books import books_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)

    return app

# Create app instance
app = create_app()

# CLI command to create tables
@app.cli.command("create-tables")
def create_tables():
    from utils.db import execute_query
    execute_query('''
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            published_year INT
        )
    ''')
    execute_query('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    ''')
    print("Tables created!")

@app.cli.command("drop-tables")
def drop_tables():
    """DANGER: Deletes all tables and data!"""
    from utils.db import execute_query
    execute_query("DROP TABLE IF EXISTS users")
    execute_query("DROP TABLE IF EXISTS books")
    print("All tables deleted!")

# User loader required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))  # Convert to integer

@app.route('/')
def home():
    return send_from_directory('templates', 'test.html')

if __name__ == '__main__':
    app.run(debug=True)