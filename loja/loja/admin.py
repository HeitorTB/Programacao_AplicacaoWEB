from django.contrib import admin
from .models import * #imporata nossos models
admin.site.register(Fabricante) #adiciona a interface do adm
admin.site.register(Categoria)
admin.site.register(Produto)
