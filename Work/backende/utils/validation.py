import re

def is_valid_email(email):
    """Validate the email format using regular expressions."""
    # Regular expression pattern for email validation
    email_pattern = r'^[\w+\-.]+@[a-z\d\-]+(\.[a-z]+)*\.[a-z]+$'
    return re.match(email_pattern, email) is not None

def is_valid_password(password):
    """Validate the password strength using regular expressions."""
    # Regular expression pattern for password validation (at least 8 characters, one uppercase, one lowercase, and one digit)
    password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'
    return re.match(password_pattern, password) is not None

def sanitize_input(input_data):
    """Sanitize and validate user input."""
    # Code to sanitize and validate the input data, such as removing special characters or ensuring a specific format
    # Modify this function according to your specific requirements

    # Example: Remove leading and trailing whitespaces from the input data
    sanitized_data = input_data.strip()
    return sanitized_data

def validate_user_data(user_data):
    """Validate user data before creating or updating a user."""
    # Code to validate user data, such as checking if required fields are present, validating specific fields, etc.
    # Modify this function according to your specific requirements

    # Example: Validate the email and password fields
    email = user_data.get('email')
    password = user_data.get('password')

    if not email or not is_valid_email(email):
        return False, "Invalid email"

    if not password or not is_valid_password(password):
        return False, "Invalid password"

    return True, "User data is valid"
