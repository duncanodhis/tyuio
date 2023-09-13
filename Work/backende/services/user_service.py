from models.user import User
from app import db

class UserService:
    def get_users(self):
        users = User.query.all()
        return [self._convert_to_dict(user) for user in users]

    def get_user(self, user_id):
        user = User.query.get(user_id)
        return self._convert_to_dict(user) if user else None

    def create_user(self, data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return self._convert_to_dict(user)

    def update_user(self, user_id, data):
        user = User.query.get(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return self._convert_to_dict(user)
        return None

    def delete_user(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return user
        return None

    
    def _convert_to_dict(self, user):
        if user:
            return {key: getattr(user, key) for key in user.__dict__.keys() if not key.startswith('_')}
        return None
