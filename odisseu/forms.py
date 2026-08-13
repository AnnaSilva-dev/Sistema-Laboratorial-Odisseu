from django import forms
from .models import Paciente, Agendamento, Resultado


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'telefone']

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'exame', 'data']
class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['valor', 'observacao']