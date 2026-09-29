from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'categoria', 'cor', 'tamanho', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Camisetas'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Preto'}),
            'tamanho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: M'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }