# app.py
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import uuid4

app = FastAPI()


DB = {"students": {}, "users": {"admin": "password"}}  # username:password
TOKENS = {}  # token -> username

class StudentIn(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class StudentOut(StudentIn):
    id: str

@app.post("/auth/login")
def login(username: str, password: str):
    pw = DB["users"].get(username)
    if not pw or pw != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid4())
    TOKENS[token] = username
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = parts[1]
    user = TOKENS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

@app.post("/students", status_code=201, response_model=StudentOut)
def create_student(student: StudentIn, user: str = Depends(get_current_user)):
    sid = str(uuid4())
    data = student.dict()
    data["id"] = sid
    DB["students"][sid] = data
    return data

@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: str, user: str = Depends(get_current_user)):
    stu = DB["students"].get(student_id)
    if not stu:
        raise HTTPException(status_code=404, detail="Student not found")
    return stu

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: str, user: str = Depends(get_current_user)):
    if student_id in DB["students"]:
        del DB["students"][student_id]
        return {}
    raise HTTPException(status_code=404, detail="Student not found")

@app.get("/users/me")
def me(user: str = Depends(get_current_user)):
    return {"username": user}
