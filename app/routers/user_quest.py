
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import UserQuestView
from ..models import UserQuest
from ..database import get_db


router = APIRouter()

@router.get("/", response_model=list[UserQuestView])
def view_user_quests(db: Session = Depends(get_db)):
    user_quests = db.query(UserQuest).all()
    for quest in user_quests:
        if quest.completed_at:
            quest.completed_at = quest.completed_at.isoformat()
    return user_quests

@router.get("/{user_id}", response_model=list[UserQuestView])
def view_user_quests_by_id(user_id: int, db: Session = Depends(get_db)):
    user_quests = db.query(UserQuest).filter(UserQuest.user_id == user_id).all()
    for quest in user_quests:
        if quest.completed_at:
            quest.completed_at = quest.completed_at.isoformat()
    return user_quests