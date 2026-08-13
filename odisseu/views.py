from django.shortcuts import render, redirect
from .forms import PacienteForm, AgendamentoForm, ResultadoForm
from .models import Paciente, Agendamento, Resultado
from datetime import date
from collections import defaultdict


def index(request):
    return render(request, "index.html")

def cadastrar_paciente(request):
    if request.method == 'POST':
        form= PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_paciente')
    else:
        form= PacienteForm()

    context = {
        'form': form, 
    }

    return render(request, 'cadastrar_paciente.html', context)

def agendar_exame(request):

    if request.method == 'POST':

        form = AgendamentoForm(request.POST)

        if form.is_valid():

            paciente = form.cleaned_data['paciente']
            exames = form.cleaned_data['exames']
            data = form.cleaned_data['data']

            for exame in exames:

                Agendamento.objects.create(
                    paciente=paciente,
                    exame=exame,
                    data=data
                )

            return redirect('agendar_exame')

    else:
        form = AgendamentoForm()

    return render(
        request,
        'agendar_exame.html',
        {'form': form}
    )

def rotina(request):
    data = request.GET.get('data')

    if data:
        agendamentos = Agendamento.objects.filter(data=data)
    else:
        data = date.today()
        agendamentos = Agendamento.objects.filter(data=data)

    return render(
        request,
        'rotina.html',
        {
            'agendamentos': agendamentos,
            'data': data,
        }
    )
def resultados(request):
    agendamentos = Agendamento.objects.filter(
        resultado__isnull=True
    )

    return render(
        request,
        'resultados.html',
        {'agendamentos': agendamentos}
    )
def digitar_resultados(request, agendamento_id):

    agendamento = Agendamento.objects.get(id=agendamento_id)

    if request.method == 'POST':

        form = ResultadoForm(request.POST)

        if form.is_valid():

            resultado = form.save(commit=False)
            resultado.agendamento = agendamento
            resultado.save()

            return redirect(
                'digitar_resultados',
                agendamento_id=agendamento.id
            )

    else:
        form = ResultadoForm()

    resultado_existe = Resultado.objects.filter(
        agendamento=agendamento
    ).exists()

    return render(
        request,
        'digitar_resultados.html',
        {
            'form': form,
            'agendamento': agendamento,
            'resultado_existe': resultado_existe,
        }
    )

def ver_resultados(request, paciente_id, data):

    paciente = Paciente.objects.get(id=paciente_id)

    resultados = Resultado.objects.filter(
        agendamento__paciente=paciente,
        agendamento__data=data
    )

    return render(
        request,
        'ver_resultados.html',
        {
            'paciente': paciente,
            'resultados': resultados,
            'data': data,
        }
    )