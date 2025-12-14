from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from .models import Producto, Pedido, Categoria, Insumo
from .forms import PedidoForm
from django.contrib.auth.decorators import login_required, user_passes_test

# --- IMPORTS PARA LA API
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InsumoSerializer, PedidoSerializer

# ==========================================
#           VISTAS WEB 
# ==========================================

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

# --- NUEVA VISTA PARA EL BUSCADOR DEL MENÚ ---
def buscar_pedido(request):
    token = request.GET.get('token')
    if token:
        return redirect('seguimiento', token=token)
    return redirect('catalogo')


# ==========================================
#           ZONA DE APIS
# ==========================================

# API 1: CRUD de Insumos
class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

# API 2: Crear Pedidos
class PedidoCreateView(generics.CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

# API 2: Editar Pedidos
class PedidoUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

# API 3: Filtro personalizado
@api_view(['GET'])
def filtrar_pedidos(request):
    """
    Filtra pedidos por rango de fechas, estado y límite.
    Usa los campos: fecha_solicitada, estado_pedido
    """
    pedidos = Pedido.objects.all()

    # 1. Filtro por Fechas
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')
    
    if fecha_inicio and fecha_fin:
        try:
            pedidos = pedidos.filter(fecha_solicitada__range=[fecha_inicio, fecha_fin])
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)

    # 2. Filtro por Estado
    estado = request.query_params.get('estado')
    if estado:
        pedidos = pedidos.filter(estado_pedido=estado)

    # 3. Límite de resultados
    limite = request.query_params.get('limite')
    if limite:
        try:
            pedidos = pedidos[:int(limite)]
        except ValueError:
            pass 

    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)


# ==========================================
#           ZONA DE REPORTE 
# ==========================================

# Función auxiliar para verificar si es admin
def es_admin(user):
    return user.is_staff

@login_required
@user_passes_test(es_admin)
def reporte_dashboard(request):
    # 1. Gráfico de Estados (Solicitado, Aprobado, etc.)
    datos_estados = Pedido.objects.values('estado_pedido').annotate(total=Count('id'))

    # 2. Gráfico de Pagos (Pendiente, Pagado)
    datos_pagos = Pedido.objects.values('estado_pago').annotate(total=Count('id'))

    # 3. Gráfico de Plataformas (Web, Instagram, etc.)
    datos_plataforma = Pedido.objects.values('plataforma').annotate(total=Count('id'))

    # 4. Tabla de Productos más solicitados (Top 5)
    datos_productos = Pedido.objects.values('producto_referencia__nombre').annotate(total=Count('id')).order_by('-total')[:5]

    return render(request, 'store/reporte.html', {
        'datos_estados': datos_estados,
        'datos_pagos': datos_pagos,
        'datos_plataforma': datos_plataforma,
        'datos_productos': datos_productos
    })