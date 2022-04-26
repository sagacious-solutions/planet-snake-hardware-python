echo off

set which_env=%1

python -m pip install --upgrade pip

if %which_env%==dev (
    pip install -r requirements/dev.txt
)

if %which_env%==prod (
    pip install -r requirements/prod.txt
)