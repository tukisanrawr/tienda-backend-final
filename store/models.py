
from django.db import models
from django.core.exceptions import ValidationError
import uuid

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50) # Ej: Tela, Filamento
    cantidad = models.IntegerField()
    marca = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio_base = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    destacado = models.BooleanField(default=False) # Para funcionalidad extra

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('EN_PROCESO', 'En proceso'),
        ('REALIZADA', 'Realizada'),
        ('ENTREGADA', 'Entregada'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    PAGOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('PAGADO', 'Pagado'),
    ]

    PLATAFORMAS = [
        ('WEB', 'Sitio Web'),
        ('INSTAGRAM', 'Instagram'),
        ('FACEBOOK', 'Facebook'),
        ('WHATSAPP', 'WhatsApp'),
        ('PRESENCIAL', 'Presencial'),
    ]

    # Datos Cliente
    cliente_nombre = models.CharField(max_length=100)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20)
    
    # Datos Pedido
    producto_referencia = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion_solicitud = models.TextField()
    imagen_referencia = models.ImageField(upload_to='referencias/', null=True, blank=True)
    fecha_solicitada = models.DateField(null=True, blank=True, help_text="Fecha en que el cliente necesita el producto")
    
    # Gestión Interna
    plataforma = models.CharField(max_length=20, choices=PLATAFORMAS, default='WEB')
    estado_pedido = models.CharField(max_length=20, choices=ESTADOS, default='SOLICITADO')
    estado_pago = models.CharField(max_length=20, choices=PAGOS, default='PENDIENTE')
    
    # Token y Fechas auto
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre}"

    # REGLA DE NEGOCIO: No finalizar si no está pagado
    def clean(self):
        if self.estado_pedido == 'FINALIZADA' and self.estado_pago != 'PAGADO':
            raise ValidationError("No se puede marcar como 'Finalizada' si el pedido no está totalmente 'Pagado'.")

    def save(self, *args, **kwargs):
        self.full_clean() # Fuerza la validación antes de guardar
        super().save(*args, **kwargs)