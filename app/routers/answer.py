
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import AnswerView, AnswerToCheck
from ..models import Answer, UserQuest
from ..database import get_db
from ..utils import verify_string


router = APIRouter()

@router.get("/", response_model=list[AnswerView])
def view_answers(db: Session = Depends(get_db)):
    answers = db.query(Answer).all()
    return answers
    
@router.post("/check_answer")
def check_answer(answerToCheck: AnswerToCheck, db: Session = Depends(get_db)):
    # Truy vấn đáp án đúng từ database
    correct_answer = db.query(Answer).filter(
        Answer.question_id == answerToCheck.question_id,
        Answer.is_correct == 1
    ).first()
    
    if not correct_answer:
        return {
            "message": "Không tìm thấy đáp án đúng cho câu hỏi này."
        }

    normalized_correct_answer = verify_string(correct_answer.answer_text)
    normalized_user_answer = verify_string(answerToCheck.answer_text)

    db_update = UserQuest(user_id=answerToCheck.user_id, 
                        question_id=answerToCheck.question_id, 
                        status=int(normalized_correct_answer == normalized_user_answer))
    
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    
    return {
        "correct_answer": correct_answer.answer_text,
        "is_correct": int(normalized_correct_answer == normalized_user_answer)
    }


