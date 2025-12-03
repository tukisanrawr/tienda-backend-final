from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_email', 'cliente_telefono', 
                  'producto_referencia', 'descripcion_solicitud', 
                  'imagen_referencia', 'fecha_solicitada']
        widgets = {
            'fecha_solicitada': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_solicitud': forms.Textarea(attrs={'rows': 3}),
        }