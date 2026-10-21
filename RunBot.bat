@echo off
echo Starting YouTube Automation Bot...
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python modules\clipper.py
echo.
echo Bot execution finished!
pause
