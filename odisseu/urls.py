from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar_paciente', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('agendar_exame', views.agendar_exame, name='agendar_exame' ),
    path('rotina/', views.rotina, name='rotina'),
    path('resultados', views.resultados, name='resultados'),
    path('digitar_resultados/<int:agendamento_id>', views.digitar_resultados, name='digitar_resultados'),
    path('ver_resultados/<int:paciente_id>/<str:data>',views.ver_resultados, name='ver_resultados'
    ),
    path('pacientes',views.pacientes,name='pacientes'),
    path('editar_paciente/<int:paciente_id>',views.editar_paciente, name='editar_paciente'),
    path('editar_resultado/<int:resultado_id>',views.editar_resultado, name='editar_resultado'),
    path(
        'excluir_agendamento/<int:agendamento_id>/',views.excluir_agendamento, name='excluir_agendamento'
    ),
    path('rotina/imprimir/',views.rotina_impressao, name='rotina_impressao'),
    path('logout/', LogoutView.as_view(), name='logout'),
    (path('liberar-resultados/', views.liberar_resultados, name='liberar_resultados')),
    path('usuarios/', views.usuarios, name='usuarios'),

    path('usuarios/editar/<int:id>/', views.editar_usuarios, name='editar_usuarios'),
    path('usuarios/inativar/<int:id>/', views.inativar_usuario, name='inativar_usuario'),
    path('usuarios/ativar/<int:id>/', views.ativar_usuario, name='ativar_usuario'),


    path('paciente/login/', views.paciente_login, name='paciente_login'),
    path('paciente/historico/', views.paciente_historico, name='paciente_historico'),
]

