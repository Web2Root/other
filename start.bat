@echo off
color 0A
chcp 65001 > nul

echo Install poetry...
echo ---------------------------------
pip install poetry
cls

echo Configure poetry settings...
echo ---------------------------------
poetry config virtualenvs.in-project true
cls

echo Install dependencies...
echo ---------------------------------
poetry install --no-root
cls

poetry run python -B -m src.main
pause
