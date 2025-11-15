from sqlalchemy.orm import Session # type: ignore
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import hash_password, pwd_context
from app.dependencies import get_db
from app.core.jwt import verify_token, create_token


def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=str(user.email), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_token(db_user.id, db_user.username)
    return JSONResponse(content={"username": db_user.username, "email": db_user.email, "message": "User created successfully","token":token})

def authenticate_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.email == str(user.email)).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    #Verify hashed password
    valid_password = pwd_context.verify(user.password, db_user.password)
    if not valid_password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(db_user.id, db_user.username)

    return JSONResponse(content={"message": f"Welcome back, {db_user.username}!","token":token})


security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user