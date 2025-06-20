@echo off
REM Clean old PyInstaller build artifacts and rebuild tray_app.exe from latest tray_app.py, including tray_icon.png
if exist tray_app\build rmdir /s /q tray_app\build
if exist tray_app\dist rmdir /s /q tray_app\dist
if exist tray_app\tray_app.spec del tray_app\tray_app.spec
call venv\Scripts\activate
cd tray_app
pyinstaller --onefile --windowed tray_app.py --name tray_app --add-data "tray_icon.png;."
cd ..
echo Build complete! Find tray_app.exe in tray_app\dist\
pause
