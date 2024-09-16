import jwt
from typing import Annotated
from fastapi import Header, HTTPException

def verify_token(x_token: Annotated[str | None, Header()] = None):
    try:
        jwt.decode(x_token, "mysecretpassword", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")