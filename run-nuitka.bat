@set SCRIPT_NAME=GetCodeChangeGUI
@set CFG_NAME=config
@set "NUITKA_OPT=--mingw64 --standalone --onefile --plugin-enable=tk-inter --remove-output --windows-disable-console"

python -m nuitka %NUITKA_OPT% %SCRIPT_NAME%.py

@PAUSE