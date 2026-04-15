from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
import uuid

app = FastAPI(title="ClassSync API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Setup
DB_PATH = "classsync.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        full_name TEXT,
        role TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id TEXT PRIMARY KEY,
        faculty_id TEXT,
        title TEXT,
        description TEXT,
        deadline TEXT,
        total_marks INTEGER,
        status TEXT DEFAULT 'published'
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id TEXT PRIMARY KEY,
        assignment_id TEXT,
        student_id TEXT,
        content TEXT,
        is_late BOOLEAN,
        submitted_at TEXT,
        grade REAL,
        feedback TEXT
    )""")
    # Seed dummy users
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('f1', 'faculty@test.com', 'Dr. Smith', 'faculty')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('s1', 'student@test.com', 'John Doe', 'student')")
    conn.commit()
    conn.close()

init_db()

# Schemas
class AssignmentCreate(BaseModel):
    faculty_id: str
    title: str
    description: str
    deadline: str
    total_marks: int

class SubmissionCreate(BaseModel):
    assignment_id: str
    student_id: str
    content: str

class GradeUpdate(BaseModel):
    grade: float
    feedback: str

# Endpoints
@app.get("/assignments")
def get_assignments(db=Depends(get_db)):
    rows = db.execute("SELECT * FROM assignments").fetchall()
    return [dict(row) for row in rows]

@app.post("/assignments")
def create_assignment(data: AssignmentCreate, db=Depends(get_db)):
    id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO assignments (id, faculty_id, title, description, deadline, total_marks) VALUES (?, ?, ?, ?, ?, ?)",
        (id, data.faculty_id, data.title, data.description, data.deadline, data.total_marks)
    )
    db.commit()
    return {"id": id, "status": "created"}

@app.get("/assignments/{assignment_id}/submissions")
def get_submissions(assignment_id: str, db=Depends(get_db)):
    rows = db.execute("SELECT * FROM submissions WHERE assignment_id = ?", (assignment_id,)).fetchall()
    return [dict(row) for row in rows]

@app.post("/submissions")
def submit_assignment(data: SubmissionCreate, db=Depends(get_db)):
    id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    # Simplified late check
    row = db.execute("SELECT deadline FROM assignments WHERE id = ?", (data.assignment_id,)).fetchone()
    is_late = now > row['deadline'] if row else False
    
    db.execute(
        "INSERT INTO submissions (id, assignment_id, student_id, content, is_late, submitted_at) VALUES (?, ?, ?, ?, ?, ?)",
        (id, data.assignment_id, data.student_id, data.content, is_late, now)
    )
    db.commit()
    return {"id": id, "status": "submitted"}

@app.patch("/submissions/{submission_id}/grade")
def grade_submission(submission_id: str, data: GradeUpdate, db=Depends(get_db)):
    db.execute(
        "UPDATE submissions SET grade = ?, feedback = ? WHERE id = ?",
        (data.grade, data.feedback, submission_id)
    )
    db.commit()
    return {"status": "graded"}

@app.get("/users/{user_id}")
def get_user(user_id: str, db=Depends(get_db)):
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not row: raise HTTPException(404)
    return dict(row)
