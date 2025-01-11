"""
Tools used for generating secret keys to confirm Email or Changing password
"""
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings


# Set up a serializer with a secret key
SECRET_KEY = settings.SECRET_KEY
SALT = settings.SALT  # Replace with your actual salt
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_token(email, password, user_id):
    """
    Generate a token using the user's email and password.

    Parameters:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        str: The generated token.
    """
    data = f"{email}:{password}:{user_id}"
    token = serializer.dumps(data, salt=SALT)
    return token


def decrypt_token(token, max_age=3600):
    """
    Decrypt the token to extract the email and password.

    Parameters:
        token (str): The token to decrypt.
        max_age (int): The maximum age of the token in seconds. Default is 3600 (1 hour).

    Returns:
        tuple: (email, password) if the token is valid, None otherwise.
    """
    try:
        data = serializer.loads(token, salt=SALT, max_age=max_age)
        email, password, user_id = data.split(":")
        return email, password, user_id
    except SignatureExpired:
        print("Token has expired.")
        return None, None, None
    except BadSignature:
        print("Invalid token.")
        return None, None, None
