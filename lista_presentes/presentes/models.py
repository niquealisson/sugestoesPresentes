from django.db import models

class Presente(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)  # Disponível ou já escolhido
    imagem = models.ImageField(upload_to='presentes/', blank=True, null=True)  # Novo campo para imagem

    def __str__(self):
        return self.nome
