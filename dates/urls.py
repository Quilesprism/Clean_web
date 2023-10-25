from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('descargar_archivo/<int:ano>/<int:mes>/', views.descargar_archivo, name='descargar_archivo'),
    path('mostrar_mes/', views.mostrar_todos_los_meses, name='mostrar_mes'),
    path('mostrar_anio/', views.mostrar_todos_los_anios, name='mostrar_anio'),
]

