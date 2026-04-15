# ClassSync - Assignment Management System

A minimal, locally runnable assignment management system built with FastAPI, Next.js, and SQLite.

## Prerequisites
- Python 3.10+
- Node.js 18+
- npm or pnpm

## Getting Started

### 1. Backend (FastAPI)
```bash
cd backend
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8000
```
The backend will be available at `http://localhost:8000`. It automatically initializes a SQLite database (`classsync.db`) and seeds two dummy users:
- Faculty: `f1` (faculty@test.com)
- Student: `s1` (student@test.com)

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:3000`.

## Project Structure
- `backend/main.py`: Single-file FastAPI backend with SQLite integration.
- `frontend/src/app/layout.tsx`: Root layout with navigation.
- `frontend/src/app/faculty/page.tsx`: Faculty dashboard to create assignments.
- `frontend/src/app/faculty/assignments/[id]/page.tsx`: Faculty view to grade submissions.
- `frontend/src/app/student/page.tsx`: Student dashboard to view and submit assignments.

## Features
- **Faculty Dashboard**: Create assignments with title, description, deadline, and total marks.
- **Student Dashboard**: View all assignments and submit text-based answers.
- **Grading**: Faculty can view submissions, check for lateness, and assign grades/feedback.
- **SQLite Database**: Local data persistence without external dependencies.
