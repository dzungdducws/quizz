
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import QuestionSetView, QuestionView, QuestionAndAnwerSetView, AnswerView, QuestionSetCreate, QuestionViewOnly
from ..models import QuestionSet, Question, Answer
from ..database import get_db

router = APIRouter()

@router.get("/sets", response_model=list[QuestionSetView])
def view_question_sets(db: Session = Depends(get_db)):
    question_sets = db.query(QuestionSet).all()
    return question_sets


@router.get("/set/{set_id}", response_model=QuestionAndAnwerSetView)
def view_question_and_anwser_by_set(set_id: int, db: Session = Depends(get_db)):
    question_set = db.query(QuestionSet).filter(QuestionSet.set_id == set_id).first()
    
    if not question_set:
        return {"error": "Set not found"}
    listQuestion = db.query(Question).filter(Question.set_id == set_id).all()

    listAnswerByQuestion = db.query(Question).filter(Question.set_id == set_id).all()
    
    # Prepare the response model
    response = QuestionAndAnwerSetView(
        set_id=question_set.set_id,
        title=question_set.title,
        type=question_set.type,
        list=[QuestionView(
            question_id=question.question_id,
            set_id=question.set_id,
            question_text=question.question_text,
            list=[AnswerView(
                answer_text=answer.answer_text,
                is_correct=answer.is_correct
            ) for answer in question.answers]
        ) for question in question_set.questions]
    )

    return response


@router.post("/create_question_set")
def create_question_sets(questionSetCreate: QuestionSetCreate, db: Session = Depends(get_db)):
    db_update = QuestionSet(title=questionSetCreate.title, type=questionSetCreate.type)

    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    
    return {"id": db_update.set_id, "title": db_update.title, "type": db_update.type}


@router.get("/", response_model=list[QuestionViewOnly])
def view_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions
