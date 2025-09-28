from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    path('cursos/', cursos_list, name='cursos_list'),
    path('disciplinas/', disciplinas_list, name='disciplinas_list'),
    path('perfis/', perfis_list, name='perfis_list'),
    path('curso/create/', cursos_create, name='cursos_create'),
    path('disciplina/create/', disciplina_create, name='disciplina_create'),
]