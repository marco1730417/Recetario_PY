entramos hasta Recetario_PY
# Creamos el entorno

python -m venv entorno

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\entorno\Scripts\Activate

entramos a backend

pip install django
pip install python-dotenv
pip install djangorestframework
pip install mysqlclient
pip install django-autoslug

# a cada libreria instalada es bueno crear un archivo requirements

pip freeze > requirements.txt

# cuando queramos instalarlas en otro entorno 

pip install -r requirements.txt


python manage.py runserver
