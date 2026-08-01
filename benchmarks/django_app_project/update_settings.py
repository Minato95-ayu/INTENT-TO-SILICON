import os

settings_path = 'django_app_project/settings.py'
with open(settings_path, 'r') as f:
    content = f.read()

if 'rest_framework' not in content:
    content = content.replace('INSTALLED_APPS = [', 'INSTALLED_APPS = [\n    \'api_app\',\n    \'rest_framework\',')
    content += '\nREST_FRAMEWORK = { \'DEFAULT_AUTHENTICATION_CLASSES\': [\'api_app.auth.SimpleJWTAuthentication\'] }\n'
    
with open(settings_path, 'w') as f:
    f.write(content)

urls_path = 'django_app_project/urls.py'
with open(urls_path, 'w') as f:
    f.write('''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("api_app.urls")),
]
''')
