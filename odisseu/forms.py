from django import forms
from .models import Paciente, Agendamento, Resultado
from .exames import EXAMES
from .validators import validate_future_date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
import re


class UsuarioForm(UserCreationForm):

    perfil = forms.ChoiceField(
        label='Perfil',
        choices=[
            ('', 'Selecione seu perfil'),
            ('Administrador', 'Administrador'),
            ('Farmaceutico', 'Farmaceutico'),
            ('Recepcionista', 'Recepcionista'),
            ('Tecnicolaboratorial', 'Técnico Laboratorial'),
        ],
        widget=forms.Select(attrs={
            'class': 'perfil edit-forms',
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',        
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'nome edit-forms',
                'placeholder': 'ex.: Souzinha'
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'nome edit-forms',
                'placeholder': 'Ex.: Rubens'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'nome edit-forms',
                'placeholder': 'Ex.: Magalhães'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'email edit-forms',
                'placeholder': 'Ex.: exemplo@email.com',
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['password1'].widget.attrs.update({
            'class': 'senha edit-forms',
            'placeholder': 'Digite sua senha',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'senha edit-forms',
            'placeholder': 'Confirme sua senha',
        })

        
class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'cns', 'data_nascimento', 'telefone']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'nome edit-forms',
                'placeholder': 'ex.: Rubens de Souza Magalhães'
            }),

            'cpf': forms.TextInput(attrs={
                'class': 'cpf edit-forms',
                'placeholder': '999.999.999-99'
            }),

            'cns': forms.TextInput(attrs={
                'class': 'cns edit-forms',
                'placeholder': '123 4567 8901 2345'
            }),

            'telefone': forms.TelInput(attrs={
                'class': 'telefone edit-forms',
                'placeholder': '(81) 99999-9999',
            }),

            'data_nascimento': forms.DateInput(attrs={
                'class': 'data edit-forms',
                'type': 'date',
                'value': 'aaaa/mm/dd'
            }),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return re.sub(r'\D', '', cpf)

    def clean_cns(self):
        cns = self.cleaned_data['cns']
        return re.sub(r'\D', '', cns)


class AgendamentoForm(forms.Form):


    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        # label='Paciente'
        empty_label='Selecione o paciente',
        widget=forms.Select(attrs={
                'class': 'paciente',
            })
    )

    exames = forms.MultipleChoiceField(
        choices=Agendamento.EXAMES,
        widget=forms.CheckboxSelectMultiple,
        label='Exames',
        
    )

    
    data = forms.DateField(
        label='Data',
        initial=date.today(),
        validators=[validate_future_date],
        widget=forms.DateInput(attrs={
            'class': 'data edit-forms',
            'type': 'date',
        })
    )

    solicitante = forms.CharField(
        max_length=200,
        required=False,
        label='Solicitante',
        widget=forms.TextInput(attrs={
            'class': 'solicitante edit-forms',
            'placeholder': 'Nome do solicitante',
        })
    )

class ResultadoForm(forms.ModelForm):

    class Meta:
        model = Resultado
        fields = ['observacao']