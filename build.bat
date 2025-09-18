@echo off
echo Building main.exe ...
pyinstaller --onefile --noconfirm --clean ^
--add-data "images;images" ^
--add-data "accounts.txt;." ^
--distpath . ^
main.py
echo.
echo Done! main.exe is ready.
pause
