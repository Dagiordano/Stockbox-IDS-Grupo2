from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Home page
    path("", views.home, name="home"),
    
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    
    # Gestionar
    path("gestionar/", views.gestionar, name="gestionar"),
    
    # Login/Logout
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    
    # Productos CRUD
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/crear/", views.crear_producto, name="crear_producto"),
    path("productos/editar/<int:id>/", views.editar_producto, name="editar_producto"),
    path("productos/eliminar/<int:id>/", views.eliminar_producto, name="eliminar_producto"),
    
    # Prendas CRUD
    path("prendas/", views.lista_prendas, name="lista_prendas"),
    path("prendas/crear/", views.crear_prenda, name="crear_prenda"),
    path("prendas/editar/<int:id>/", views.editar_prenda, name="editar_prenda"),
    path("prendas/eliminar/<int:id>/", views.eliminar_prenda, name="eliminar_prenda"),
    
    # Bodegas CRUD
    path("bodegas/", views.lista_bodegas, name="lista_bodegas"),
    path("bodegas/crear/", views.crear_bodega, name="crear_bodega"),
    path("bodegas/editar/<int:id>/", views.editar_bodega, name="editar_bodega"),
    path("bodegas/eliminar/<int:id>/", views.eliminar_bodega, name="eliminar_bodega"),
    
    # PrendaBodega CRUD
    path("prenda-bodega/", views.lista_prenda_bodega, name="lista_prenda_bodega"),
    path("prenda-bodega/crear/", views.crear_prenda_bodega, name="crear_prenda_bodega"),
    path("prenda-bodega/editar/<int:id>/", views.editar_prenda_bodega, name="editar_prenda_bodega"),
    path("prenda-bodega/eliminar/<int:id>/", views.eliminar_prenda_bodega, name="eliminar_prenda_bodega"),
    
    # Movimientos CRUD
    path("movimientos/", views.lista_movimientos, name="lista_movimientos"),
    path("movimientos/crear/", views.crear_movimiento, name="crear_movimiento"),
    path("movimientos/editar/<int:id>/", views.editar_movimiento, name="editar_movimiento"),
    path("movimientos/eliminar/<int:id>/", views.eliminar_movimiento, name="eliminar_movimiento"),
]