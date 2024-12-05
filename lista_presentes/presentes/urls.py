from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_presentes, name='lista_presentes'),
    path('confirmar/<int:presente_id>/', views.confirmar_presente, name='confirmar_presente'),
]
