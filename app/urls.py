from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('lista_proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('editar_proveedor/<str:id_proveedor>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<str:id_proveedor>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    path('parametros_producto/', views.parametros_producto, name='parametros_producto'),
    path('listar_parametros/', views.listar_parametros, name='listar_parametros'),
    path('eliminar_parametro/<int:parametro_id>/', views.eliminar_parametro, name='eliminar_parametro'),
    path('editar_parametro/<int:parametro_id>/', views.editar_parametro, name='editar_parametro'),

    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('editar_producto/<str:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<str:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    path('entrada-mercancia/', views.registrar_entrada, name='registrar_entrada'),


    path('subir_excel/', views.subir_excel, name='subir_excel'),
    path('Entradas/Vista_Entradapdf/<str:entrada_id>/', views.Vista_Entradapdf, name='Vista_Entradapdf'),
    path('guardar_entrada/', views.guardar_entrada, name='guardar_entrada'),
    path('lista_numero_entradas/', views.listar_numero_entradas, name='lista_numero_entradas'),

]
