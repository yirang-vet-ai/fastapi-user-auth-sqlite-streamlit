from fastapi import FastAPI

from app.database import Base, engine
from app.routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI 😊 회원가입 로그인 인증 API",
    version="1.0.0"
)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "회원가입/로그인 인증 API 서버 실행 중"}