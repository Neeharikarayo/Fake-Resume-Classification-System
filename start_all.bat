@echo off
echo Starting Fake Resume Classification System...

echo Starting Backend...
start "Backend Server" cmd /k "cd backend && python run.py"

echo Starting Frontend...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo Both services have been started in separate windows!
exit
