from django.http import HttpResponse
from loja.models import Produto
def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    produtos = Produto.objects.all()
    #print(produtos)
    if produto is not None:
        produtos = produtos.filter(Produto=produto)
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    if categoria is not None:
        produtos = produtos.filter(categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante=fabricante)
    if id is not None:
        produtos = produtos.filter(id=id)
    print(produtos)
    return HttpResponse('<h1>Produto de id %s!</h1>' % id)

