from flask_login import UserMixin
from utils.db import execute_query

class User(UserMixin):
    def __init__(self, id, email, password_hash):  # Change parameter name
        self.id = id
        self.email = email
        self.password_hash = password_hash  # Match database column

    @staticmethod
    def get(user_id):
        try:
            user_id_int = int(user_id)  # Convert to integer
        except ValueError:
            return None
            
        user_data = execute_query(
            "SELECT * FROM users WHERE id = %s",
            (user_id_int,)  # Use integer
        )
        if user_data:
            return User(
                id=user_data[0]['id'],
                email=user_data[0]['email'],
                password_hash=user_data[0]['password_hash']
            )
        return None

    @staticmethod
    def get_by_email(email):
        user_data = execute_query(
            "SELECT * FROM users WHERE email = %s",
            (email,),
        )
        if user_data:
            return User(
                id=user_data[0]['id'],
                email=user_data[0]['email'],
                password_hash=user_data[0]['password_hash']  # Match database column name
            )
        return None
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True