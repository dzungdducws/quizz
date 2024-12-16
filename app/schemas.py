from pydantic import BaseModel, EmailStr, Field
import streamlit
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

class AnswerView(BaseModel):
    answer_text: str
    is_correct: int

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    question_text: str
    question_img: str
    set_id: int 
    ans: List[AnswerView]

class QuestionSetView(BaseModel):
    set_id: int
    title: str
    type: str

    class Config:
        from_attributes = True

class AnswerToCheck(BaseModel):
    user_id: int
    question_id: int
    answer_text: str

    class Config:
        from_attributes = True

class QuestionViewOnly(BaseModel):
    question_id: int
    set_id: int
    question_text: str
    class Config:
        from_attributes = True        

class QuestionView1(BaseModel):
    question_id: int
    question_text: str
    list: List[AnswerView]
    class Config:
        from_attributes = True


class QuestionView2(BaseModel):
    question_id: int
    question_text: str
    question_img: str   
    list: List[AnswerView]
    class Config:
        from_attributes = True

class QuestionAndAnwerSetView1(BaseModel):
    set_id: int
    title: str
    type: str
    list: List[QuestionView1]
    class Config:
        from_attributes = True


class QuestionAndAnwerSetView2(BaseModel):
    set_id: int
    title: str
    type: str
    list: List[QuestionView2]
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



class InputTranslate(BaseModel):
    text: str
    source_lang: str
    target_lang: str

    class Config:
        from_attributes = True

class OutputTranslate(BaseModel):
    text: str

    class Config:
        from_attributes = True
        
    