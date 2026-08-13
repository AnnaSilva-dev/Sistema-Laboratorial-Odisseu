from django import forms
from .models import Paciente, Agendamento, Resultado


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento', 'telefone']

from django import forms
from .models import Paciente, Agendamento, Resultado


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'cns', 'data_nascimento', 'telefone']


class AgendamentoForm(forms.Form):

    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        label='Paciente'
    )

    exames = forms.MultipleChoiceField(
        choices=Agendamento.EXAMES,
        widget=forms.CheckboxSelectMultiple,
        label='Exames'
    )

    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )



class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['valor', 'observacao']