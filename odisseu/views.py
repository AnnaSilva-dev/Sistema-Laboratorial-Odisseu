from django.shortcuts import render, redirect
from .forms import PacienteForm, AgendamentoForm, ResultadoForm
from .models import Paciente, Agendamento, Resultado
from datetime import date

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
            form.save()
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

            return redirect('resultados')

    else:
        form = ResultadoForm()

    return render(
        request,
        'digitar_resultados.html',
        {
            'form': form,
            'agendamento': agendamento,
        }
    )

def adicionar_exame(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    if request.method == 'POST':
        exame = request.POST.get('exame')
        data = request.POST.get('data')

        if exame and data:
            Agendamento.objects.create(
                paciente=paciente,
                exame=exame,
                data=data
            )

    return redirect('rotina')