
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserView, UserLogin
from ..models import User
from ..database import get_db
from ..utils import hash_password,verify_password
router = APIRouter()

@router.get("/", response_model=list[UserView])
def view_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/login")
def login(userLogin: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == userLogin.email).first()

    if not db_user or not verify_password(userLogin.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"id": db_user.user_id, "username": db_user.username, "email": db_user.email}


@router.post("/register", response_model=UserView)
def create_user(userCreate: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == userCreate.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    print(userCreate)
    hashed_password = hash_password(userCreate.password)
    db_user = User(username=userCreate.username, email=userCreate.email, password_hash=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user = db.query(User).filter(User.email == userCreate.email).first()

    return db_user