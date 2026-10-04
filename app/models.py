from django.db import models
from django.utils import timezone

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    
    categoria = models.CharField(max_length=50, blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    tamanho = models.CharField(max_length=10, blank=True, null=True)

    GENEROS = [('male', 'Male'), ('female', 'Female')]
    genero = models.CharField(max_length=10, choices=GENEROS, default='male')
    
    # MUDANÇA AQUI: de ImageField para URLField
    imagem = models.URLField(max_length=500, blank=True, null=True, verbose_name='Imagem (link)')
    foto = models.ImageField(upload_to='produtos/', blank=True, null=True, verbose_name='Foto (enviar arquivo)')
    
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome
    
    @property
    def imagem_url(self):
        if self.foto:
            return self.foto.url
        return self.imagem or ''