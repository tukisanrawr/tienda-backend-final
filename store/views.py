from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Producto, Pedido, Categoria
from .forms import PedidoForm

def catalogo(request):
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    
    productos = Producto.objects.all()
    
    if query:
        productos = productos.filter(nombre__icontains=query)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
        
    categorias = Categoria.objects.all()
    return render(request, 'store/catalogo.html', {
        'productos': productos, 
        'categorias': categorias
    })

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'store/detalle.html', {'producto': producto})

def crear_pedido(request):
    # Si viene desde "Solicitar este producto", pre-llenamos el campo
    producto_id = request.GET.get('producto')
    initial_data = {}
    if producto_id:
        initial_data = {'producto_referencia': producto_id}

    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.plataforma = 'WEB' # Forzamos que sea web
            pedido.save()
            return redirect('seguimiento', token=pedido.token)
    else:
        form = PedidoForm(initial=initial_data)

    return render(request, 'store/formulario_pedido.html', {'form': form})

def seguimiento(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    return render(request, 'store/seguimiento.html', {'pedido': pedido})
