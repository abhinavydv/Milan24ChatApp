from fastapi import HTTPException, Header
from google.auth import exceptions
from google.auth.transport import requests
from google.oauth2 import id_token
import os

def try_details(Authorization: str):
    try:
        details = authn_user(Authorization)
        
        if details is None:
            raise HTTPException(
                status_code=498, detail="You are not logged in, please login again."
            )

        GSUITE_DOMAIN_NAME = "iith.ac.in"
        domain = details[0].split("@")[-1]
        # allow domain or subdomains
        if domain != GSUITE_DOMAIN_NAME and not domain.endswith(
            "." + GSUITE_DOMAIN_NAME
        ):
            raise HTTPException(
                status_code=498, detail="Please use your IITH email address to login."
            )
    except exceptions.InvalidValue:
        raise HTTPException(
            status_code=498, detail="Token invalid or expired, please login again."
        )
    return details


def verify_auth_token(Authorization: str = Header()):
    email, name, l_name,f_name = try_details(Authorization)
    return {"email": email, "name": name, "l_name": l_name, "f_name": f_name}


def authn_user(token):
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    print(CLIENT_ID)
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        email = idinfo["email"]
        name = idinfo["name"]
        l_name = idinfo["family_name"]
        f_name = idinfo["given_name"]

        return email, name, l_name, f_name
    except exceptions.InvalidValue as e:
        raise exceptions.InvalidValue("Token is invalid")
    except ValueError:
        # Invalid token
        return None