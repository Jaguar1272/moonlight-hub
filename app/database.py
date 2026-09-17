import sqlite3
import os

DB_PATH = "app/database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. 문의 및 외주 신청 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,       -- 'cs' 또는 'design'
            author TEXT NOT NULL,
            contact TEXT NOT NULL,
            designer TEXT,                -- 'luna', 'aring', 'any' 등
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. 운영진 계정 테이블 (아이디, 비밀번호, 직급)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL           -- 'CEO', 'GM', 'AM', 'Designer'
        )
    """)

    # 제시해주신 초기 계정 목록 삽입 (기본 비밀번호는 모두 통일하거나 임의 지정 후 변경 가능)
    # 초기 비번은 임시로 'moonlight1234!' 로 설정해드립니다.
    default_admins = [
        ("may_0329", "moonlight1234!", "CEO"),
        ("ggangho06", "moonlight1234!", "GM"),
        ("1503gongsajangjigweon8519", "moonlight1234!", "GM"),
        ("dnjsfna", "moonlight1234!", "GM"),
        ("shiba_.09", "moonlight1234!", "AM"),
        ("runa_.04_", "moonlight1234!", "Designer"),
        ("aring_u", "moonlight1234!", "Designer")
    ]
    
    for username, pwd, role in default_admins:
        cursor.execute("""
            INSERT OR IGNORE INTO admins (username, password, role) VALUES (?, ?, ?)
        """, (username, pwd, role))

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn