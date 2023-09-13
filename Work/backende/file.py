from app import db
from models.user import User

new_user = User(username='nickc', email='nickc@example.com', password='password123')
db.session.add(new_user)
db.session.commit()

