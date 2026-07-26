@echo off
REM Uygulamayi kaynak koddan calistirir (exe derlemeye gerek yok).
cd /d "%~dp0Main"
start "" pythonw main.py
