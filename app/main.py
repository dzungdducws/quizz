from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, question, answer, user_quest
from .database import get_db
from sqlalchemy.orm import Session
from .models import Question, Answer
from .utils import dataraw
import random 
from .routers import user, question, answer, user_quest, ai_translate
import os
import base64
import string

# Create FastAPI app
app = FastAPI()
text_lines = dataraw()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,  # Allow sending cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)




# Include routers
@app.post("/fetchdataDienTu/")
def fetchdata(db: Session = Depends(get_db)):
    for line in text_lines:
        words = line.split()  # Tách dòng thành từng từ
        for i in range(len(words)):
            if random.randint(0, 5) > 2:
                break
            missing_word = words[i]
            remaining_sentence = " ".join(words[:i] + ["___"] + words[i+1:])
            db_question = Question(set_id=2, question_text=remaining_sentence)
            db.add(db_question)
            db.commit()
            db.refresh(db_question)

            db1 = db.query(Question).filter(Question.question_text == remaining_sentence).first()
            db_ans = Answer(question_id=db1.question_id, answer_text=missing_word, is_correct=1)
            db.add(db_ans)
            db.commit()
            db.refresh(db_ans)

    return {"s": "dientu"}

@app.post("/fetchdataChon/")
def fetchdata22(db: Session = Depends(get_db)):
    for line in text_lines:
        words = line.split()  
        for i in range(len(words)):
            if random.randint(0, 5) > 2:
                break
            missing_word = words[i]
            remaining_sentence = " ".join(words[:i] + ["___"] + words[i+1:])
            
            db_question = Question(set_id=1, question_text=remaining_sentence)
            db.add(db_question)
            db.commit()
            db.refresh(db_question)

            db_ans = Answer(question_id=db_question.question_id, answer_text=missing_word, is_correct=1)
            db.add(db_ans)

            count = 0
            selected_indices = set()
            selected_indices.add(i)

            while count < 3:
                x = random.randint(0, len(words) - 1)
                if x != i and x not in selected_indices:
                    selected_indices.add(x)
                    count += 1
                    db_wrong_ans = Answer(question_id=db_question.question_id, answer_text=words[x], is_correct=0)
                    db.add(db_wrong_ans)                                            

    return {"s": "chon"}


@app.post("/fetchdataanh/")
def fetchdataanh(db: Session = Depends(get_db)):

    base64_results = {}
    res = []
    for filename in os.listdir("./img"):
        file_path = os.path.join("./img", filename)
        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            with open(file_path, "rb") as image_file:
                base64_string = base64.b64encode(image_file.read()).decode('utf-8')
                base64_results[filename] = base64_string
    
    
    for filename, base64_string in base64_results.items():
        db_question = Question(set_id=3,question_text="Chọn từ trong hình mô tả:",question_img=base64_string)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        db_ans = Answer(question_id=db_question.question_id, answer_text=filename.rsplit('.', 1)[0], is_correct=1)
        db.add(db_ans)
        for i in range(3):
            x = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10)))
            db_wrong_ans = Answer(question_id=db_question.question_id, answer_text=x, is_correct=0)
            db.add(db_wrong_ans) 

    return "ok"


app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(question.router, prefix="/questions", tags=["questions"])
app.include_router(answer.router, prefix="/answers", tags=["answers"])
app.include_router(user_quest.router, prefix="/user_quests", tags=["user_quests"])
app.include_router(ai_translate.router, prefix="/ai_translate", tags=["ai_translate"])

