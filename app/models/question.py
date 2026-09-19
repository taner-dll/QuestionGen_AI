from pydantic import BaseModel, Field

class QuestionGenerateRequest(BaseModel):
    subject: str = Field(..., description="The subject for which questions need to be generated.")
    topic: str
    difficulty: str
    questions_count: int = Field(default=1, ge=1, le=10, 
                                 description="Number of questions to generate (between 1 and 20).")
    
class Question(BaseModel):
    question_text: str
    options: dict[str, str]
    correct_answer: str
    explanation: str
    

class QuestionGenerateResponse(BaseModel):
    questions: list[Question]
    