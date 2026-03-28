@echo off
cd /d "C:\Users\viroq\OneDrive\Documentos\Projetos - Univesp\projeto-integrador-1"
venv\Scripts\activate
cd sistema_estoque
python manage.py runserver
cmd /k