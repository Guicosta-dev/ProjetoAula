def carrinho_qtd(request):
    return {'carrinho_qtd': sum(request.session.get('carrinho', {}).values())}