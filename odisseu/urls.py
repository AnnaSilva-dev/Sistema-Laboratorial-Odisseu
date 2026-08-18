from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name='login'),
    path("index/", views.index, name="index"),
    # path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar_paciente', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('agendar_exame', views.agendar_exame, name='agendar_exame' ),
    path('rotina', views.rotina, name='rotina'),
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
    

]