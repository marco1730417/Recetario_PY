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
pip install django-cors-headers

# a cada libreria instalada es bueno crear un archivo requirements

pip freeze > requirements.txt

# cuando queramos instalarlas en otro entorno 

pip install -r requirements.txt

#Crear super usuario

django-admin createsuperuser

# realizar migraciones 
python manage.py makemigrations // Crear la migracion
python manage.py migrate

python manage.py migrate --fake recetas  // igonarar una tabla especifica de las migraciones

# panel de administracion de usuarios django
para crear un super usuario 
python manage.py createsuperuser

http://127.0.0.1:8000/admin


python manage.py runserver
