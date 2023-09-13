from flask_mail import Message
from backend import mail

def send_email(subject, sender, recipients, body):
    """Send an email using Flask-Mail."""
    message = Message(subject=subject, sender=sender, recipients=recipients)
    message.body = body
    mail.send(message)

def generate_email_confirmation_link(user):
    """Generate an email confirmation link for a user."""
    # Code to generate the confirmation link for the user
    confirmation_link = f"https://example.com/confirm/{user.id}"
    return confirmation_link

def send_email_confirmation(user):
    """Send an email confirmation email to the user."""
    subject = "Email Confirmation"
    sender = "noreply@example.com"
    recipients = [user.email]
    confirmation_link = generate_email_confirmation_link(user)
    body = f"Please click the following link to confirm your email: {confirmation_link}"
    send_email(subject, sender, recipients, body)
