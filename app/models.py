from django.db import models
from django.utils.timezone import now
import uuid

class Proveedor(models.Model):
    id_proveedor = models.CharField(
        max_length=10, 
        unique=True, 
        default='', 
        blank=True, 
        primary_key=True
    )
    nombre_comercial = models.CharField(max_length=100)
    representante_legal = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.id_proveedor:
            self.id_proveedor = f"PRV-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_proveedor} - {self.nombre_comercial}"

class ParametrosProducto(models.Model):
    grupo = models.CharField(max_length=100, blank=True, null=True)
    linea = models.CharField(max_length=100, blank=True, null=True)
    unidad = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.grupo} - {self.linea} - {self.unidad}"

class Producto(models.Model):
    id_producto = models.CharField(
        max_length=10, 
        unique=True, 
        default='', 
        blank=True, 
        primary_key=True
    )
    nombre_producto = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.CharField(max_length=100, blank=True, null=True)
    linea = models.CharField(max_length=100, blank=True, null=True)
    unidad = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id_producto:
            self.id_producto = f"PRO-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_producto} - {self.nombre_producto}"

class EntradaProducto(models.Model):  # Se mantiene solo una clase EntradaProducto
    id_entrada = models.CharField(max_length=10, unique=True, blank=True)  
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id_entrada:  
            ultima_entrada = EntradaProducto.objects.order_by('-id').first()
            if ultima_entrada:
                nuevo_id = int(ultima_entrada.id_entrada.split('-')[1]) + 1
            else:
                nuevo_id = 1
            self.id_entrada = f"Ent-{nuevo_id:06d}"  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id_entrada

class EntradaMercancia(models.Model):
    id_entrada = models.CharField(
        max_length=10,
        unique=True,
        default='',
        blank=True,
        primary_key=True
    )
    fecha_entrada = models.DateTimeField(default=now)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    observaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id_entrada:
            self.id_entrada = f"ENT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entrada {self.id_entrada} - {self.producto.nombre_producto} - {self.cantidad} unidades"

class ProductoEntrada(models.Model):
    entrada = models.ForeignKey(EntradaProducto, on_delete=models.CASCADE, related_name="productos")  # ✅ Se cambió "Entrada" por "EntradaProducto"
    nombre = models.CharField(max_length=255)
    lote = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    cantidad = models.PositiveIntegerField()
