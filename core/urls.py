from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views
from rest_framework.routers import DefaultRouter

# Router para la API de Insumos
router = DefaultRouter()
router.register(r'insumos', views.InsumoViewSet)

urlpatterns = [
    # --- RUTAS DE AUTENTICACIÓN ---
    path('accounts/', include('django.contrib.auth.urls')),

    # --- RUTAS WEB ---
    path('', views.catalogo, name='catalogo'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle'),
    path('solicitar/', views.crear_pedido, name='crear_pedido'),
    path('seguimiento/<uuid:token>/', views.seguimiento, name='seguimiento'),
    
    # --- ESTA ES LA RUTA QUE TE FALTA (Agrega esto) ---
    path('buscar/', views.buscar_pedido, name='buscar_pedido'), 
    
    path('reporte/', views.reporte_dashboard, name='reporte'),
    path("admin/", admin.site.urls),

    # --- RUTAS API ---
    path('api/', include(router.urls)), 
    path('api/pedidos/crear/', views.PedidoCreateView.as_view(), name='api_pedido_crear'),
    path('api/pedidos/editar/<int:pk>/', views.PedidoUpdateView.as_view(), name='api_pedido_editar'),
    path('api/pedidos/filtrar/', views.filtrar_pedidos, name='api_pedido_filtro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)