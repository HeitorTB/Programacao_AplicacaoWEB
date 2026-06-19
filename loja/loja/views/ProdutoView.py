from django.shortcuts import render, redirect
from loja.models import Produto, Fabricante, Categoria
from datetime import timedelta
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import os

def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    
    context = {
        'produto': produto, 
        'fabricantes': Fabricantes, 
        'categorias': Categorias
    }
    return render(request, template_name='produto/produto-edit.html', context=context, status=200)

def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")
    produtos = Produto.objects.all()
    
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
        
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
        
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
        
    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)
        
    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)
        
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)
        
    if id is not None:
        produtos = produtos.filter(id=id)
        
    context = {
        'produtos': produtos
    }
    return render(request, template_name='produto/produto.html', context=context, status=200)

def edit_produto_postback(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            if obj_produto:
                obj_produto.Produto = produto
                obj_produto.destaque = (destaque is not None)
                obj_produto.promocao = (promocao is not None)
                if msgPromocao is not None:
                    obj_produto.msgPromocao = msgPromocao
                obj_produto.categoria = Categoria.objects.filter(id=categoria_id).first()
                obj_produto.fabricante = Fabricante.objects.filter(id=fabricante_id).first()
                obj_produto.alterado_em = timezone.now()
                
                # --- CORREÇÃO: Captura a nova imagem enviada pelo formulário de edição ---
                if request.FILES and 'image' in request.FILES:
                    imagefile = request.FILES['image']
                    
                    # Se o produto já tinha uma imagem antes, remove o arquivo físico antigo do disco
                    if obj_produto.image:
                        try:
                            old_image_path = obj_produto.image.path
                            if os.path.exists(old_image_path):
                                os.remove(old_image_path)
                        except Exception as path_err:
                            print("Aviso ao remover imagem antiga: %s" % path_err)

                    # Salva o novo arquivo
                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)
                    if (filename is not None) and (filename != ""):
                        obj_produto.image = filename
                # ------------------------------------------------------------------------

                obj_produto.save()
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def details_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    
    context = {
        'produto': produto,
        'fabricantes': Fabricantes,
        'categorias': Categorias
    }
    return render(request, template_name='produto/produto-details.html', context=context, status=200)

def delete_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = whitespaces = produtos.first()
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    
    context = {
        'produto': produto,
        'fabricantes': Fabricantes,
        'categorias': Categorias
    }
    return render(request, template_name='produto/produto-delete.html', context=context, status=200)

def delete_produto_postback(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            if obj_produto:
                if obj_produto.image:
                    image_path = obj_produto.image.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                obj_produto.delete()
        except Exception as e:
            print("Erro ao excluir produto: %s" % e)
    return redirect("/produto")

def create_produto_view(request, id=None):
    if request.method == 'POST':
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        
        try:
            obj_produto = Produto()
            obj_produto.Produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
            obj_produto.preco = 0
            if (preco is not None) and (preco != ""):
                obj_produto.preco = preco
            
            obj_produto.categoria = Categoria.objects.filter(id=categoria_id).first()
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante_id).first()
            obj_produto.criado_em = timezone.now()
            obj_produto.alterado_em = obj_produto.criado_em
            
            if request.FILES:
                num_files = len(request.FILES.getlist('image'))
                if num_files > 0:
                    imagefile = request.FILES['image']
                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)
                    if (filename is not None) and (filename != ""):
                        obj_produto.image = filename
                        
            obj_produto.save()
            return redirect("/produto")
        except Exception as e:
            print("Erro inserindo produto: %s" % e)
            return redirect("/produto")
            
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {
        'fabricantes': Fabricantes,
        'categorias': Categorias
    }
    return render(request, template_name='produto/produto-create.html', context=context, status=200)