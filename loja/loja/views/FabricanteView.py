from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Fabricante
from loja.forms.FabricanteForm import FabricanteForm
from django.utils import timezone

def list_fabricante_view(request, id=None):
    fabricantes = Fabricante.objects.all()
    
    if id is not None:
        fabricantes = fabricantes.filter(id=id)
    
    context = {
        'fabricantes': fabricantes
    }
    return render(request, template_name='fabricante/fabricante.html', context=context, status=200)

def create_fabricante_view(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            fabricante = form.save(commit=False)
            fabricante.criado_em = timezone.now()
            fabricante.alterado_em = fabricante.criado_em
            fabricante.save()
            return redirect("/fabricante")
    else:
        form = FabricanteForm()
    
    context = {
        'form': form
    }
    return render(request, template_name='fabricante/fabricante-create.html', context=context, status=200)

def edit_fabricante_view(request, id=None):
    if id is not None:
        fabricante = get_object_or_404(Fabricante, id=id)
        
        if request.method == 'POST':
            form = FabricanteForm(request.POST, instance=fabricante)
            if form.is_valid():
                fabricante = form.save(commit=False)
                fabricante.alterado_em = timezone.now()
                fabricante.save()
                return redirect("/fabricante")
        else:
            form = FabricanteForm(instance=fabricante)
        
        context = {
            'form': form,
            'fabricante': fabricante
        }
        return render(request, template_name='fabricante/fabricante-edit.html', context=context, status=200)
    return redirect("/fabricante")

def delete_fabricante_view(request, id=None):
    if id is not None:
        fabricante = get_object_or_404(Fabricante, id=id)
        
        if request.method == 'POST':
            try:
                fabricante.delete()
                return redirect("/fabricante")
            except Exception as e:
                print("Erro excluindo fabricante: %s" % e)
                return redirect("/fabricante")
        
        context = {
            'fabricante': fabricante
        }
        return render(request, template_name='fabricante/fabricante-delete.html', context=context, status=200)
    return redirect("/fabricante")