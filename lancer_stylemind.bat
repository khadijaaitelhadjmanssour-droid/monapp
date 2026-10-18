@echo off
rem ============================================================
rem  STYLEMIND - lancement depuis le dossier de rendu mon_app
rem  (ce script peut aussi etre lance depuis C:\Users\pc\Desktop\Monapp)
rem ============================================================
cd /d "%~dp0"

"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m streamlit run app.py --server.port 8501

pause
