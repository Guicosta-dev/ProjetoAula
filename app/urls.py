from django.urls import path
from . import views

urlpatterns = [
    # Site público
    path('', views.home, name='home'),
    path('produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Painel do Admin
    path('painel/', views.painel, name='painel'),
    path('painel/adicionar/', views.painel_adicionar, name='painel_adicionar'),
    path('painel/editar/<int:id>/', views.painel_editar, name='painel_editar'),
    path('painel/deletar/<int:id>/', views.painel_deletar, name='painel_deletar'),

    #Carrinho
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:id>/', views.remover_carrinho, name='remover_carrinho'),
]
