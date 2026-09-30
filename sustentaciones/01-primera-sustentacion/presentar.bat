@echo off
setlocal
cd /d "%~dp0"
set "PRESENTATION_PORT=8765"
start "" "http://127.0.0.1:%PRESENTATION_PORT%/presentacion-vigente.html"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m http.server %PRESENTATION_PORT% --bind 127.0.0.1
) else (
  python -m http.server %PRESENTATION_PORT% --bind 127.0.0.1
)
endlocal
