
from models import User, session
from werkzeug.security import check_password_hash

def login_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

# # Example usage:
# user = login_user('admin', 'admin_password')
# if user:
#     print(f"User {user.username} logged in successfully!")
# else:
#     print("Invalid username or password")