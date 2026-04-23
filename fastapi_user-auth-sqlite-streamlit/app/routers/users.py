from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import create_access_token, verify_password
from app.database import get_db

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="이미 사용 중인 username 입니다.")

    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="이미 사용 중인 email 입니다.")

    created_user = crud.create_user(
        db=db,
        username=user.username,
        email=user.email,
        nickname=user.nickname,
        password=user.password,
    )
    return created_user


@router.post("/login", response_model=schemas.TokenResponse)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, login_data.username_or_email, login_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다.")

    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "로그인 성공"
    }


@router.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user






@router.post("/users/{user_key}/change-password")
def change_password(
    user_key: str,
    body: schemas.PasswordChangeRequest,
    db: Session = Depends(get_db),
):
    if user_key.isdigit():
        user = crud.get_user_by_id(db, int(user_key))
    else:
        user = crud.get_user_by_username(db, user_key)

    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    if not verify_password(body.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="현재 비밀번호가 일치하지 않습니다.")

    crud.change_password(db, user.id, body.new_password)

    return {"message": "비밀번호 변경 완료"}