from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from decimal import Decimal
from django.views.decorators.http import require_POST
from .models import Produto
from .forms import CadastroComEmailForm  # Importando o novo formulário que criamos
import requests

# --- VIEWS DA LOJA ---

def home(request):
    produtos = Produto.objects.all().order_by('-criado_em')
    genero = request.GET.get('genero')
    if genero in ('male', 'female'):
        produtos = produtos.filter(genero=genero)
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
    # Se o usuário já estiver logado, não precisa ver a tela de cadastro
    if request.user.is_authenticated:
        return redirect('produtos')

    if request.method == 'POST':
        # Usamos o novo formulário que exige o e-mail
        form = CadastroComEmailForm(request.POST)
        
        if form.is_valid():
            # 1. Salva o usuário no banco de dados
            user = form.save()
            
            # --- INTEGRAÇÃO EMAILJS ---
            emailjs_url = 'https://api.emailjs.com/api/v1.0/email/send'
            
            # Monta o pacote de dados para a API
            payload = {
                'service_id': 'service_50i1ldn',     # Ex: service_xxxxx
                'template_id': 'template_022y90h',   # Ex: template_xxxxx
                'user_id': 'Q01y5dVMASTopDWLT',        # Ex: abcdef123456
                'accessToken': 'Dcujf8LbNFJtooiXayMjK',   # A chave secreta do painel
                'template_params': {
                    'nome_usuario': user.username,
                    'email_destino': user.email     # Agora temos a garantia de que o e-mail existe!
                }
            }
            
            # Tenta fazer o disparo sem travar o sistema do aluno caso a internet caia
            try:
                resposta = requests.post(emailjs_url, json=payload)
                if resposta.status_code != 200:
                    print(f"Erro EmailJS: {resposta.text}")
            except Exception as e:
                print(f"Erro de conexão com EmailJS: {e}")
            # --------------------------

            # 2. Faz o login automático e redireciona para a loja
            login(request, user)
            return redirect('produtos')
    else:
        # Se for GET, exibe o formulário vazio
        form = CadastroComEmailForm()

    return render(request, 'cadastro.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProdutoForm
from django.shortcuts import render, redirect, get_object_or_404

# --- PAINEL DO ADMINISTRADOR ---

@staff_member_required(login_url='login')
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

# --- CARRINHO ---

def carrinho(request):
    dados = request.session.get('carrinho', {})
    itens = []
    total = Decimal('0')
    for produto in Produto.objects.filter(id__in=dados.keys()):
        quantidade = dados[str(produto.id)]
        subtotal = produto.preco * quantidade
        total += subtotal
        itens.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})
    return render(request, 'carrinho.html', {'itens': itens, 'total': total})

@require_POST
def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)
    carrinho = request.session.get('carrinho', {})
    chave = str(produto.id)
    quantidade = carrinho.get(chave, 0)

    if quantidade < produto.estoque:
        carrinho[chave] = quantidade + 1
        request.session['carrinho'] = carrinho
    else:
        messages.error(request, f'Estoque máximo de {produto.nome} atingido.')
    return redirect('carrinho')

@require_POST
def remover_carrinho(request, id):
    carrinho = request.session.get('carrinho', {})
    carrinho.pop(str(id), None)
    request.session['carrinho'] = carrinho
    return redirect('carrinho')