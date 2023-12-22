rem This script generates Python project to standalone EXEx64 to deploy
rem Alexander.Golyshkin

rem INIT
@rmdir /S /Q .\\resources
@del EAChecker.exe

rem PROCESS
call pyinstaller --noconfirm --onefile --console --icon "../resources/application.ico" --name EAChecker ../main.py --distpath . --workpath . --specpath .
@mkdir resources
@copy /Y "..\\resources\\configuration.xml" ".\\resources\\configuration.xml"

rem CLEAN-UP
@rmdir /S /Q .\\EAChecker
@del EAChecker.spec
