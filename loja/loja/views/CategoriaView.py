from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Categoria
from datetime import datetime
from django.utils import timezone

def list_categoria_view(request, id=None):
    categorias = Categoria.objects.all()
    
    if id is not None:
        categorias = categorias.filter(id=id)
    
    context = {
        'categorias': categorias
    }
    return render(request, template_name='categoria/categoria.html', context=context, status=200)

def create_categoria_view(request):
    if request.method == 'POST':
        nome = request.POST.get("Categoria")
        try:
            obj_categoria = Categoria()
            obj_categoria.Categoria = nome
            obj_categoria.criado_em = timezone.now()
            obj_categoria.alterado_em = obj_categoria.criado_em
            obj_categoria.save()
            return redirect("/categoria")
        except Exception as e:
            print("Erro inserindo categoria: %s" % e)
            return redirect("/categoria")
    
    return render(request, template_name='categoria/categoria-create.html', status=200)

def edit_categoria_view(request, id=None):
    if id is not None:
        categoria = get_object_or_404(Categoria, id=id)
        
        if request.method == 'POST':
            nome = request.POST.get("Categoria")
            try:
                categoria.Categoria = nome
                categoria.alterado_em = timezone.now()
                categoria.save()
                return redirect("/categoria")
            except Exception as e:
                print("Erro editando categoria: %s" % e)
                return redirect("/categoria")
        
        context = {
            'categoria': categoria
        }
        return render(request, template_name='categoria/categoria-edit.html', context=context, status=200)
    return redirect("/categoria")

def delete_categoria_view(request, id=None):
    if id is not None:
        categoria = get_object_or_404(Categoria, id=id)
        
        if request.method == 'POST':
            try:
                categoria.delete()
                return redirect("/categoria")
            except Exception as e:
                print("Erro excluindo categoria: %s" % e)
                return redirect("/categoria")
        
        context = {
            'categoria': categoria
        }
        return render(request, template_name='categoria/categoria-delete.html', context=context, status=200)
    return redirect("/categoria")