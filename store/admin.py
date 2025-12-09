from django.contrib import admin

from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Categoria, Insumo, Producto, Pedido

# --- Funcionalidad Extra: Acción para exportar a CSV ---
def exportar_pedidos_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Cliente', 'Estado', 'Pago', 'Total', 'Fecha'])
    
    for pedido in queryset:
        writer.writerow([pedido.id, pedido.cliente_nombre, pedido.estado_pedido, pedido.estado_pago, pedido.created_at])
    return response

exportar_pedidos_csv.short_description = "Exportar selección a CSV"

# --- Configuración de Modelos ---

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'destacado')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'estado_pedido', 'estado_pago', 'plataforma', 'token')
    list_filter = ('estado_pedido', 'estado_pago', 'plataforma')
    search_fields = ('cliente_nombre', 'token')
    readonly_fields = ('token',) 
    actions = [exportar_pedidos_csv] 

admin.site.register(Categoria)
admin.site.register(Insumo)