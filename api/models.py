from django.db import models

# Create your models here.
class Cupon(models.Model):
    codigo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=2000)
    descuento = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.codigo

class Estado_pedido(models.Model):
    descripcion = models.CharField(max_length=200, default="enCarrito")
    def __str__(self):
        return self.descripcion

class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=2000)
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    username = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200,  blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    igv = models.BooleanField(default=True, null=True)
    imagen = models.FileField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    descuento = models.DecimalField(max_digits=10,decimal_places=2)
    imagen1 = models.FileField(blank=True, null=True)
    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    igv = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado_pedido, on_delete=models.CASCADE)
    cupon = models.ForeignKey(Cupon, on_delete=models.CASCADE, blank=True,null=True)

class Detalle_pedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Pedido de {self.pedido.cliente.nombre}"