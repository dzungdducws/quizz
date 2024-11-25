from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password:str


class UserView(BaseModel):
    user_id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class QuestionSetCreate(BaseModel):
    title: str
    type: str = Field(default="Multiple Choice")

class QuestionSetView(BaseModel):
    set_id: int
    title: str
    type: str

    class Config:
        from_attributes = True

class AnswerView(BaseModel):
    answer_text: str
    is_correct: int

    class Config:
        from_attributes = True

class QuestionViewOnly(BaseModel):
    question_id: int
    set_id: int
    question_text: str
    class Config:
        from_attributes = True        

class QuestionView(BaseModel):
    question_id: int
    question_text: str
    list: List[AnswerView]
    class Config:
        from_attributes = True

class QuestionAndAnwerSetView(BaseModel):
    set_id: int
    title: str
    type: str
    list: List[QuestionView]
    class Config:
        from_attributes = True


class UserQuestView(BaseModel):
    user_quest_id: int
    user_id: int
    question_id: int
    status: bool
    completed_at: str

    class Config:
        from_attributes = True

        
    