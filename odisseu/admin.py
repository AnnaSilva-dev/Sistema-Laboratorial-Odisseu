from django.contrib import admin
from .models import Paciente,  Agendamento, Resultado

admin.site.register(Paciente)
admin.site.register(Agendamento)
admin.site.register(Resultado)