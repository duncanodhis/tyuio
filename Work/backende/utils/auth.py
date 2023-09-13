from passlib.hash import bcrypt

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(password, hashed_password):
    return bcrypt.verify(password, hashed_password)

def generate_token(user_id):
    # Code to generate and return a token
    pass

def decode_token(token):
    # Code to decode and return the user ID from the token
    pass
