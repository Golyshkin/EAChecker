# EAChecker

EAChecker a Python 3.10x written application (Windows) for simple checking Sparx System Enterprise models for:

1. Package Structure
2. Correct Package Naming
3. Diagrams naming
4. Diagrams specific elements presence
5. etc..

EAChecker is a console application and implement plug-ins approach which allows easy to
add a new checkers to the system and use COM EA API for accessing to EA structure.

The following projects files are responsible for:

1. **plugins** - Plugins files
2. **common** - Common files
3. **utils** - Utility files
4. **interfaces** - SW Interface files
5. **exceptions** - Project used custom exceptions
6. **resources** - Application resources (e.g. configurations, etc.)

An application screenshot is following

![](TODO:URL)

# Build instructions

Actually the project has the following external modules dependency

1. Clone project according to GitHub instructions
2. **$> pip install -r requirements.txt** - need to install required modules for project
3. Run the application using console command: **py Main.py** for getting HELP instruction

PS. For those people who don't want to install the Python 3.10x, there is compiled EXE for
WINDOWSx64 [located here](TODO:URL)

PyToExe Cmd Line used for generating an EXE x64 image: pyinstaller --noconfirm --onefile --console --icon "Z:/Sprint
24/MTS.ico" --name "EAChecker"  "Z:/Projects/EAChecker/main.py"