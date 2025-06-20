@echo off
REM Sync usage_log.csv to labeled_log.csv with categories
cd backend
..\venv\Scripts\activate && python categorizer.py
cd ..
echo Labeled log updated.
pause
