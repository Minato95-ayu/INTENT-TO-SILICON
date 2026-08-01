import os
import sys
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.http import JsonResponse

# Configure Django settings
settings.configure(
    DEBUG=False,
    SECRET_KEY='benchmark',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[],
)

def read_root(request):
    return JsonResponse({"message": "Hello from Django"})

def read_item(request, item_id):
    return JsonResponse({"item_id": item_id, "status": "ok"})

urlpatterns = [
    path('', read_root),
    path('items/<int:item_id>', read_item),
]

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
