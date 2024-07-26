from models import User, session
from werkzeug.security import generate_password_hash

def register_user(username, password):
    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash)
    session.add(user)
    session.commit()
