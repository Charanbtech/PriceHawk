# backend/core/security.py
import time
import jwt
import hashlib
from flask import current_app
from jwt import ExpiredSignatureError, InvalidTokenError

# -------------------------------
# PASSWORD UTILITIES
# -------------------------------
def hash_password(password: str) -> str:
    """Hash a plain password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify if plain password matches the hashed password."""
    return hashlib.sha256(password.encode()).hexdigest() == hashed


# -------------------------------
# JWT UTILITIES
# -------------------------------
def create_jwt(payload: dict, ttl: int = 3600 * 24 * 7) -> str:
    """
    Create a signed JWT token with expiry (default: 7 days).
    """
    secret = current_app.config["JWT_SECRET"]
    data = payload.copy()
    data.update({"exp": int(time.time()) + ttl})
    return jwt.encode(data, secret, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    """
    Decode and validate a JWT. Returns payload if valid, else {}.
    """
    secret = current_app.config["JWT_SECRET"]
    try:
        data = jwt.decode(token, secret, algorithms=["HS256"])
        return data
    except ExpiredSignatureError:
        return {"error": "Token expired"}
    except InvalidTokenError:
        return {"error": "Invalid token"}
    except Exception as e:
        return {"error": str(e)}
