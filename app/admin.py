from django.contrib import admin
from .models import EntradaMercancia

@admin.register(EntradaMercancia)
class EntradaMercanciaAdmin(admin.ModelAdmin):
    list_display = ('id_entrada', 'fecha_entrada', 'proveedor', 'producto', 'lote', 'fecha_vencimiento', 'cantidad')
    search_fields = ('id_entrada', 'proveedor__nombre_comercial', 'producto__nombre_producto', 'lote')
    list_filter = ('fecha_entrada', 'proveedor', 'fecha_vencimiento')
