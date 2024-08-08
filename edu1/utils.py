
from django.core.mail import send_mail
from django.conf import settings
import random
import string

def generate_random_password(length=8):
    """Generate a random password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def send_welcome_email(to_email, username, password):
    subject = 'Your New Teacher Account'
    message = f'Hello {username},\n\nYour teacher account has been created.\n\nUsername: {username}\nPassword: {password}\n\nPlease change your password after logging in.\n\nBest regards,\nYour School'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to_email])
