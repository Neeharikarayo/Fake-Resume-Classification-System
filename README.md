# AI Fake Resume Detector

A full-stack AI application designed to detect fraudulent and AI-generated resumes using XGBoost and TF-IDF analysis.

## Project Structure

- **frontend/**: Next.js 15 application with Tailwind CSS, Clerk Auth, and MongoDB integration.
- **backend/**: FastAPI service for ML model inference.
- **model/**: (Root) Original training scripts and data.

## Features

- **Real-time Detection**: Analyzes text patterns to identify suspicious resumes.
- **Heuristic Analysis**: Detects timeline inconsistencies and skill-to-experience ratios.
- **Authentication**: Secure access via Clerk.
- **History Tracking**: Saves every analysis result in MongoDB.

## Getting Started

### Backend Setup (FastAPI)

1. Navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python run.py
   ```

### Frontend Setup (Next.js)

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables in `.env.local`:
   ```env
   MONGODB_URI=
   DATABASE_NAME=resume_detector
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
   CLERK_SECRET_KEY=
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```

## API Documentation

The backend exposes a POST endpoint:
- `POST /predict`
  - Input: `{ "resume_text": "..." }`
  - Output: Detection status, confidence, and identified issues.
