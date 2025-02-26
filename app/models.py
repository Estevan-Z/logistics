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
        # Generar un código único si está vacío
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


   