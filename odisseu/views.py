from django.shortcuts import render, redirect
from .forms import PacienteForm, AgendamentoForm, ResultadoForm
from .models import Paciente, Agendamento, Resultado, ResultadoParametro
from datetime import date, datetime
from .exames import EXAMES

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
            solicitante = form.cleaned_data['solicitante']
            for exame in exames:

                Agendamento.objects.create(
                    paciente=paciente,
                    exame=exame,
                    data=data,
                    solicitante=solicitante
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

    if hasattr(agendamento, 'resultado'):

        return redirect(
            'editar_resultado',
            resultado_id=agendamento.resultado.id
        )

    exame = EXAMES[agendamento.exame]

    if request.method == 'POST':

        form = ResultadoForm(request.POST)

        if form.is_valid():

            resultado = form.save(commit=False)
            resultado.agendamento = agendamento
            resultado.save()

            # Salva os parâmetros específicos do exame
            for parametro in exame['parametros']:

                valor = request.POST.get(
                    parametro['nome']
                )

                ResultadoParametro.objects.create(
                    resultado=resultado,
                    nome=parametro['nome'],
                    valor=valor,
                    unidade=parametro['unidade'],
                    referencia=parametro['referencia']
                )
        return redirect(
            f'/rotina?data={agendamento.data.strftime("%Y-%m-%d")}'
        )

    else:
        form = ResultadoForm()

    return render(
        request,
        'digitar_resultados.html',
        {
            'form': form,
            'agendamento': agendamento,
            'exame': exame,
        }
    )
def ver_resultados(request, paciente_id, data):

    paciente = Paciente.objects.get(id=paciente_id)
    data = datetime.strptime(data, '%Y-%m-%d').date()
    resultados = Resultado.objects.filter(
        agendamento__paciente=paciente,
        agendamento__data=data
    )
    for resultado in resultados:

        codigo_exame = resultado.agendamento.exame

        exame = EXAMES[codigo_exame]

        resultado.agendamento.amostra = exame.get('amostra', '')
        resultado.agendamento.metodo = exame.get('metodo', '')

    return render(
        request,
        'ver_resultados.html',
        {
            'paciente': paciente,
            'resultados': resultados,
            'data': data,
        }
    )

def pacientes(request):

    busca = request.GET.get('busca', '').strip()

    pacientes = Paciente.objects.none()

    if busca:

        pacientes = Paciente.objects.filter(
            nome__icontains=busca
        ) | Paciente.objects.filter(
            cpf__icontains=busca
        ) | Paciente.objects.filter(
            cns__icontains=busca
        )

    return render(
        request,
        'pacientes.html',
        {
            'pacientes': pacientes,
            'busca': busca,
        }
    )
def editar_paciente(request, paciente_id):

    paciente = Paciente.objects.get(id=paciente_id)

    if request.method == 'POST':

        form = PacienteForm(
            request.POST,
            instance=paciente
        )

        if form.is_valid():
            form.save()

            return redirect('pacientes')

    else:

        form = PacienteForm(
            instance=paciente
        )

    pacientes = Paciente.objects.all()

    return render(
        request,
        'pacientes.html',
        {
            'pacientes': pacientes,
            'busca': '',
            'paciente_editando': paciente,
            'form_editar': form,
        }
    )

def editar_resultado(request, resultado_id):

    resultado = Resultado.objects.get(id=resultado_id)

    agendamento = resultado.agendamento

    parametros = resultado.parametros.all()

    if request.method == 'POST':

        for parametro in parametros:

            valor = request.POST.get(
                f'parametro_{parametro.id}'
            )

            parametro.valor = valor
            parametro.save()

        resultado.observacao = request.POST.get(
            'observacao',
            ''
        )

        resultado.save()
        return redirect(
                f'/rotina?data={agendamento.data.strftime("%Y-%m-%d")}'
            )


    return render(
        request,
        'editar_resultado.html',
        {
            'resultado': resultado,
            'agendamento': agendamento,
            'parametros': parametros,
        }
    )
def excluir_agendamento(request, agendamento_id):

    agendamento = Agendamento.objects.get(id=agendamento_id)

    data = agendamento.data

    agendamento.delete()

    return redirect(
        f'/rotina?data={data.strftime("%Y-%m-%d")}'
    )