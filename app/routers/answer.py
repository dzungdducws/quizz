
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import AnswerView
from ..models import Answer
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=list[AnswerView])
def view_answers(db: Session = Depends(get_db)):
    answers = db.query(Answer).all()
    return answers
