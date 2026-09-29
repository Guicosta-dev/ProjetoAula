from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Produto

# --- VIEWS DA LOJA ---

def home(request):
    produtos = Produto.objects.all().order_by('-criado_em')
    return render(request, 'home.html', {'produtos': produtos})

def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'detalhe.html', {'produto': produto})

# --- VIEWS DE AUTENTICAÇÃO ---

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        # --- ADICIONE ESTE BLOCO ---
        # Aplica a classe do Bootstrap em todos os campos automaticamente
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = ' '
        # ---------------------------
    
    return render(request, 'cadastro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProdutoForm
from django.shortcuts import render, redirect, get_object_or_404

# --- PAINEL DO ADMINISTRADOR ---

@staff_member_required
def painel(request):
    produtos = Produto.objects.all().order_by('-criado_em')
    return render(request, 'painel/painel.html', {'produtos': produtos})

@staff_member_required
def painel_adicionar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('painel')
    else:
        form = ProdutoForm()
    return render(request, 'painel/form_produto.html', {'form': form, 'titulo': 'Adicionar Produto'})

@staff_member_required
def painel_editar(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('painel')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'painel/form_produto.html', {'form': form, 'titulo': 'Editar Produto'})

@staff_member_required
def painel_deletar(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('painel')
    return render(request, 'painel/confirmar_delete.html', {'produto': produto})