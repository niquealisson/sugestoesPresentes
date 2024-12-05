from django.contrib import admin
from .models import Presente

@admin.register(Presente)
class PresenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'status','imagem')
