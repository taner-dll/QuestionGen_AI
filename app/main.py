from fastapi import FastAPI

app = FastAPI(
    title="QuestionGen_AI",
    description="A FastAPI application for generating questions using AI.",
    version="0.1.0",
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to QuestionGen_AI!"}


