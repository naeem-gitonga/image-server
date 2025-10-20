
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def maybe_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    user = os.environ.get("BASIC_AUTH_USER")
    pwd = os.environ.get("BASIC_AUTH_PASS")
    if not user and not pwd:
        return
    if credentials is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    ok_user = secrets.compare_digest(credentials.username, user or "")
    ok_pwd = secrets.compare_digest(credentials.password, pwd or "")
    if not (ok_user and ok_pwd):
        raise HTTPException(status_code=401, detail="Unauthorized")
