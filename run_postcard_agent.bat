@echo off
REM Run the postcard agent from the project directory

cd /d "%~dp0"

REM Activate virtual environment (assumes .venv exists)
call .venv\Scripts\activate

REM Run the agent
python main.py

REM Keep window open to see output/errors
pause
