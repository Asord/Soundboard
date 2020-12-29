@echo off
:startup
python.exe main.py
if %ERRORLEVEL% EQU 1 goto startup