from django import forms
from .models import Paciente, Agendamento, Resultado
from .exames import EXAMES
from .validators import validate_future_date

class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'cns', 'data_nascimento', 'telefone']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'edit-forms',
                'placeholder': 'ex.: Rubens de Souza Magalhães'
            }),

            'cpf': forms.TextInput(attrs={
                'class': 'edit-forms',
                'placeholder': '999.999.999-99'
            }),

            'cns': forms.TextInput(attrs={
                'class': 'edit-forms',
                'placeholder': '123 4567 8901 2345'
            }),

            'telefone': forms.NumberInput(attrs={
                'class': 'edit-forms',
                'placeholder': '(99) 9999999-99',
                'type': 'int'
            }),

            'data_nascimento': forms.DateInput(attrs={
                'class': 'edit-forms',
                'type': 'date'
            }),
        }


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
        validators=[validate_future_date],
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )
    solicitante = forms.CharField(
        max_length=200,
        required=False,
        label='Solicitante'
    )

class ResultadoForm(forms.ModelForm):

    class Meta:
        model = Resultado
        fields = ['observacao']