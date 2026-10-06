from django import forms
from .models import Produto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'genero', 'categoria', 'cor', 'tamanho', 'foto', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Camisetas'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Preto'}),
            'tamanho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: M'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagem': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://... (opcional)'}),
        }

class CadastroComEmailForm(UserCreationForm):
    # Adicionamos o campo de e-mail e o tornamos obrigatório
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # Definimos exatamente quais campos vão aparecer no HTML
        fields = ("username", "email")
