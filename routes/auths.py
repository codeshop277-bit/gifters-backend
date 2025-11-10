from dotenv import load_dotenv
from fastapi import APIRouter, Request, Depends, HTTPException
from authlib.integrations.starlette_client import OAuth
from database import SessionLocal
from models import ExternalUser
import os
from jose import jwt
from sqlalchemy.orm import Session
load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.get("/google/login")
# async def google_login(request: Request):
#     redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.get("/google/callback")
# async def google_callback(request: Request, db: Session = Depends(get_db)):
    # token = await oauth.google.authorize_access_token(request)
    # user_info = await oauth.google.parse_id_token(request, token)

    # if not user_info:
    #     raise HTTPException(status_code=400, detail="Google login failed")

    # google_id = user_info["sub"]
    # email = user_info.get("email")
    # name = user_info.get("name")

    # # Check if user already exists
    # existing = db.query(ExternalUser).filter_by(google_id=google_id).first()
    # if not existing:
    #     new_user = ExternalUser(google_id=google_id, email=email, name=name)
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)
    #     user_id = new_user.id
    # else:
    #     user_id = existing.id

    # # Generate JWT
    # jwt_secret = os.getenv("JWT_SECRET")
    # payload = {"user_id": user_id, "email": email, "role": "external"}
    # access_token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    # # Redirect back to frontend with token (for now just return)
    # return {"access_token": access_token, "token_type": "bearer"}