::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJGuB5E0jFBNVXgCLLya7CLQQ8fL+0/mVoXEPUfEwbZ3Y36eyN+8c7gjmeZcu3TRTm8Rs
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSjk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCuDJGuB5E0jFBNVXgCLLya7CLQQ8fL+0+iOrHE1ddAbUbyb+7qPLPkJ7wvhbZNN
::YB416Ek+Zm8=
::
::
::978f952a14a936cc963da21a135fa983
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