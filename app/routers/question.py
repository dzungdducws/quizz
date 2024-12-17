
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import QuestionSetView, QuestionCreate, QuestionView1, QuestionView2, QuestionAndAnwerSetView1, QuestionAndAnwerSetView2, AnswerView, QuestionSetCreate, QuestionViewOnly
from ..models import QuestionSet, Question, Answer
from ..database import get_db
import random
router = APIRouter()

@router.get("/sets", response_model=list[QuestionSetView])
def view_question_sets(db: Session = Depends(get_db)):
    question_sets = db.query(QuestionSet).all()
    return question_sets


@router.get("/set/{set_id}")
def view_question_and_anwser_by_set(set_id: int, db: Session = Depends(get_db)):
    question_set = db.query(QuestionSet).filter(QuestionSet.set_id == set_id).first()
    
    if not question_set:
        return {"error": "Set not found"}
    listQuestion = db.query(Question).filter(Question.set_id == set_id).all()

    listAnswerByQuestion = db.query(Question).filter(Question.set_id == set_id).all()
    
    if (set_id != 3):
        response = QuestionAndAnwerSetView1(
            set_id=question_set.set_id,
            title=question_set.title,
            type=question_set.type,
            list=[
                QuestionView1(
                    question_id=question.question_id,
                    set_id=question.set_id,
                    question_text=question.question_text,
                    question_img=question.question_img,
                    list=random.sample(  # Xáo trộn danh sách câu trả lời
                        [
                            AnswerView(
                                answer_text=answer.answer_text,
                                is_correct=answer.is_correct
                            ) for answer in question.answers
                        ], len(question.answers)
                    )
                ) for question in random.sample(question_set.questions, len(question_set.questions))  # Xáo trộn danh sách câu hỏi
            ]
        )
    else:
        response = QuestionAndAnwerSetView2(
            set_id=question_set.set_id,
            title=question_set.title,
            type=question_set.type,
            list=[
                QuestionView2(
                    question_id=question.question_id,
                    set_id=question.set_id,
                    question_text=question.question_text,
                    question_img=question.question_img,
                    list=random.sample(  # Xáo trộn danh sách câu trả lời
                        [
                            AnswerView(
                                answer_text=answer.answer_text,
                                is_correct=answer.is_correct
                            ) for answer in question.answers
                        ], len(question.answers)
                    )
                ) for question in random.sample(question_set.questions, len(question_set.questions))  # Xáo trộn danh sách câu hỏi
            ]
        )


    return response


@router.post("/create_question_set")
def create_question_sets(questionSetCreate: QuestionSetCreate, db: Session = Depends(get_db)):
    db_update = QuestionSet(title=questionSetCreate.title, type=questionSetCreate.type)

    db.add(db_update)
    db.commit()
    db.refresh(db_update)

    
    return {"id": db_update.set_id, "title": db_update.title, "type": db_update.type}



@router.post("/create_question")
def create_question(questionCreate: QuestionCreate, db: Session = Depends(get_db)):
    db_update = Question(question_text=questionCreate.question_text, question_img=questionCreate.question_img, set_id=questionCreate.set_id)
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    
    for i in range(len(questionCreate.ans)):
        db_update_ans =Answer(question_id=db_update.question_id, answer_text=questionCreate.ans[i].answer_text,is_correct=questionCreate.ans[i].is_correct)
        db.add(db_update_ans)
        db.commit()
        db.refresh(db_update_ans)
    return {"id": db_update.question_id}



@router.get("/", response_model=list[QuestionViewOnly])
def view_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions
