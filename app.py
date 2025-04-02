from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from models.user import User

# Initialize extensions
login_manager = LoginManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    login_manager.init_app(app)
    cors.init_app(app, supports_credentials=True)
    
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
            password_hash VARCHAR(255) NOT NULL  # Changed column name
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
    return User.get(user_id)

if __name__ == '__main__':
    app.run(debug=True)