from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='members'),
    path('historial/', views.historial, name='historial'),
    path('descargar_reporte_csv/', views.descargar_reporte_csv, name='descargar_reporte_csv'),
]