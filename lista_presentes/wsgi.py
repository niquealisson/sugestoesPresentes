import os
from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lista_presentes.settings')

# Cria e retorna a aplicação WSGI para o servidor
application = get_wsgi_application()
