from django.contrib import admin
from .models import * #imporata nossos models

class FabricanteAdmin(admin.ModelAdmin):
    date_hierarchy = 'criado_em'

class ProdutoAdmin(admin.ModelAdmin):
    date_hierarchy = 'criado_em'
    list_display = ('Produto', 'destaque', 'promocao', 'msgPromocao','preco', 'categoria',)
    empty_value_display = 'Vazio'
    fields = ('Produto', 'destaque', 'promocao','msgPromocao', 'preco', 'categoria',)
    search_fields = ('Produto',)

admin.site.register(Fabricante,FabricanteAdmin)
admin.site.register(Categoria)
admin.site.register(Produto, ProdutoAdmin)