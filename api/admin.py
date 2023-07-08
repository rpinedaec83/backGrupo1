from django.contrib import admin

from api.models import Cupon, Estado_pedido, Categoria, Cliente, Producto, Pedido, Detalle_pedido

class cuponAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'descuento' )

class estado_pedidoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', )

class categoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

class clienteAdmin(admin.ModelAdmin):
    list_display = ('username', 'nombre', 'email', 'password')

class productoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'categoria', 'igv', 'imagen', 'precio', 'descuento')
class pedidoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'subtotal', 'igv', 'total', 'cliente', 'estado', 'cupon')

class detalle_pedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'subtotal')

admin.site.register(Cupon, cuponAdmin)
admin.site.register(Estado_pedido, estado_pedidoAdmin)
admin.site.register(Categoria, categoriaAdmin)
admin.site.register(Cliente, clienteAdmin)
admin.site.register(Producto, productoAdmin)
admin.site.register(Pedido, pedidoAdmin)
admin.site.register(Detalle_pedido, detalle_pedidoAdmin)