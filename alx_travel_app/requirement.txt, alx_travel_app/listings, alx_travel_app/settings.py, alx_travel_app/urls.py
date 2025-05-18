
1.1 Create and activate virtual environment
bash
Copy
Edit
python3 -m venv env
source env/bin/activate
1.2 Install necessary packages
bash
Copy
Edit
pip install django djangorestframework django-cors-headers mysqlclient drf-yasg django-environ celery
Note: Install RabbitMQ separately on your machine (or via Docker).

✅ Step 2: Create Django Project and App
bash
Copy
Edit
django-admin startproject alx_travel_app
cd alx_travel_app
python manage.py startapp listings
✅ Step 3: Configure settings.py
3.1 Modify INSTALLED_APPS
python
Copy
Edit
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'listings',
]
3.2 Middleware Settings
Make sure corsheaders.middleware.CorsMiddleware is near the top:

python
Copy
Edit
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
3.3 REST Framework Settings
python
Copy
Edit
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
3.4 CORS Settings
python
Copy
Edit
CORS_ALLOW_ALL_ORIGINS = True  # For dev only
✅ Step 4: Set Up .env and Database Configuration
4.1 Install and load django-environ
bash
Copy
Edit
pip install django-environ
4.2 Create .env file in project root
env
Copy
Edit
DEBUG=True
SECRET_KEY=your_secret_key_here
DB_NAME=alx_db
DB_USER=alx_user
DB_PASSWORD=secure_password
DB_HOST=127.0.0.1
DB_PORT=3306
4.3 Update settings.py to use django-environ
python
Copy
Edit
import environ
import os

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
✅ Step 5: Add Swagger Documentation
5.1 In your urls.py
python
Copy
Edit
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel App API",
      default_version='v1',
      description="API documentation for ALX Travel App",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
Now Swagger UI is available at http://127.0.0.1:8000/swagger/.

✅ Step 6: Initialize Git Repository
bash
Copy
Edit
git init
echo "env/" > .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
git add .
git commit -m "Initial Django project setup with Swagger and MySQL config"
✅ Optional: Celery and RabbitMQ Setup
You can integrate Celery with RabbitMQ like this (add in alx_travel_app/__init__.py):

python
Copy
Edit
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ('celery_app',)
Create celery.py inside the project directory:

python
Copy
Edit
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
And add this to settings.py:

python
Copy
Edit
CELERY_BROKER_URL = 'amqp://localhost'
