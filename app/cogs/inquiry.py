from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_db_connection, init_db
from datetime import datetime

router = APIRouter(prefix="/inquiry", tags=["Inquiry"])

init_db()

class CSModel(BaseModel):
    author: str
    contact: str
    content: str

class DesignModel(BaseModel):
    author: str
    contact: str
    designer: str  
    content: str

class LoginModel(BaseModel):
    username: str
    password: str

class PasswordChangeModel(BaseModel):
    username: str
    old_password: str
    new_password: str

# CS 및 디자인 등록/조회 API (동일 유지)
@router.post("/cs")
def create_cs(data: CSModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inquiries (category, author, contact, content) VALUES ('cs', ?, ?, ?)", (data.author, data.contact, data.content))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "CS 문의가 접수되었습니다."}

@router.get("/cs")
def get_cs():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM inquiries WHERE category = 'cs' ORDER BY id DESC").fetchall()
    conn.close()
    return {"status": "success", "data": [dict(r) for r in rows]}

@router.post("/design")
def create_design(data: DesignModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inquiries (category, author, contact, designer, content) VALUES ('design', ?, ?, ?, ?)", (data.author, data.contact, data.designer, data.content))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "디자인 외주 신청이 완료되었습니다."}

@router.get("/design")
def get_design():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM inquiries WHERE category = 'design' ORDER BY id DESC").fetchall()
    conn.close()
    return {"status": "success", "data": [dict(r) for r in rows]}

# 아이디/비번 로그인 API
@router.post("/login")
def login(data: LoginModel):
    conn = get_db_connection()
    admin = conn.execute("SELECT * FROM admins WHERE username = ?", (data.username,)).fetchone()
    conn.close()

    if admin and admin["password"] == data.password:
        return {"status": "success", "username": admin["username"], "role": admin["role"]}
    raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")

# 비밀번호 변경 API
@router.post("/change-password")
def change_password(data: PasswordChangeModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    admin = cursor.execute("SELECT * FROM admins WHERE username = ?", (data.username,)).fetchone()
    
    if not admin or admin["password"] != data.old_password:
        conn.close()
        raise HTTPException(status_code=401, detail="기존 비밀번호가 일치하지 않습니다.")
    
    cursor.execute("UPDATE admins SET password = ? WHERE username = ?", (data.new_password, data.username))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "비밀번호가 성공적으로 변경되었습니다."}

# 항목 삭제 API
@router.delete("/{category}/{item_id}")
def delete_item(category: str, item_id: int, username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    admin = cursor.execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()
    
    if not admin or admin["password"] != password:
        conn.close()
        raise HTTPException(status_code=401, detail="권한 인증 실패")
    
    cursor.execute("DELETE FROM inquiries WHERE id = ? AND category = ?", (item_id, category))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "삭제되었습니다."}