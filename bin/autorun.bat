@echo off
if not exist bin (
	cd ..
)
CALL venv\Scripts\activate.bat
cd src
python main.py || @echo on
echo
echo [INFO] Analysis successfully completed. Navigate to the root directory, then have a look at the plots and the data file.
@echo off
pause