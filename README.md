entramos hasta Recetario_PY
# Creamos el entorno

python -m venv entorno


Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\entorno\Scripts\Activate

entramos a backend

pip install django
pip install python-dotenv
pip install djangorestframework
 


python manage.py runserver
