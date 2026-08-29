from django.db.models import Count
from django.shortcuts import render, redirect
from .forms import PacienteForm, AgendamentoForm, ResultadoForm, UsuarioForm
from .models import Paciente, Agendamento, Resultado, ResultadoParametro
from datetime import date, datetime, timezone
from .exames import EXAMES, parametros_do_exame
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_permission_decorator
from django.contrib.auth.decorators import login_required
from .roles import Farmaceutico, Administrador, TecnicoLaboratorial, Recepcionista
from django.utils import timezone

@login_required
def index(request):
    hoje = timezone.localdate()

    pacientes_agendados = Agendamento.objects.filter(
        data=hoje
    ).values('paciente').distinct().count()

    resultados_pendentes = Agendamento.objects.filter(
        resultado__isnull=True
    ).count()

    exames_pendentes = Agendamento.objects.filter(
        resultado__isnull=True
    ).values('exame').distinct().count()

    return render(
        request,
        'index.html',
        {
            'pacientes_agendados': pacientes_agendados,
            'resultados_pendentes': resultados_pendentes,
            'exames_pendentes': exames_pendentes,
        }
    )

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})
    else:
        return render(request, 'login.html')

@login_required
@has_permission_decorator('cadastrar_usuario')
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            perfil = form.cleaned_data['perfil']
            ROLES = {
            'Administrador': Administrador,
            'Farmaceutico': Farmaceutico,
            'Recepcionista': Recepcionista,
            'TecnicoLaboratorial': TecnicoLaboratorial}
            role = ROLES[perfil]
            assign_role(user, role)
            return redirect('index')
        
    else:
        form = UsuarioForm()
    return render(request, 'cadastrar_usuario.html', {'form': form})

@login_required
@has_permission_decorator('cadastrar_paciente')
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

@login_required
@has_permission_decorator('agendar_exame')
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
        {
            'form': form,
        }
    )

@login_required
@has_permission_decorator('visualizar_rotina')
def rotina(request):
    data = request.GET.get('data') or date.today().strftime('%Y-%m-%d')

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
@login_required
@has_permission_decorator('visualizar_resultados')
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
        return redirect('editar_resultado', resultado_id=agendamento.resultado.id)

    exame = EXAMES[agendamento.exame]

    if request.method == 'POST':
        form = ResultadoForm(request.POST)

        if form.is_valid():
            resultado = form.save(commit=False)
            resultado.agendamento = agendamento
            resultado.save()

            for parametro in parametros_do_exame(exame):
                if parametro.get('tipo') == 'diferencial':
                    ResultadoParametro.objects.create(
                        resultado=resultado,
                        nome=parametro['nome'],
                        percentual=request.POST.get(parametro['nome'], ''),
                        valor='',
                        unidade=parametro['unidade'],
                        referencia=parametro['referencia'],
                    )
                else:
                    ResultadoParametro.objects.create(
                        resultado=resultado,
                        nome=parametro['nome'],
                        valor=request.POST.get(parametro['nome'], ''),
                        unidade=parametro['unidade'],
                        referencia=parametro['referencia'],
                    )

        return redirect(f'/rotina?data={agendamento.data.strftime("%Y-%m-%d")}')

    else:
        form = ResultadoForm()

    return render(request, 'digitar_resultados.html', {'form': form, 'agendamento': agendamento, 'exame': exame})
@login_required
@has_permission_decorator('visualizar_resultados')
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

@login_required
@has_permission_decorator('visualizar_pacientes')
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

@login_required
@has_permission_decorator('editar_paciente')
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

@login_required
@has_permission_decorator('editar_resultado')
def editar_resultado(request, resultado_id):
    resultado = Resultado.objects.get(id=resultado_id)
    agendamento = resultado.agendamento
    parametros = resultado.parametros.all()

    if request.method == 'POST':
        for parametro in parametros:
            if parametro.percentual != '' or parametro.nome in [
                'Neutrófilos', 'Linfócitos', 'Monócitos', 'Eosinófilos', 'Basófilos'
            ]:
                parametro.percentual = request.POST.get(f'parametro_{parametro.id}', '')
            else:
                parametro.valor = request.POST.get(f'parametro_{parametro.id}', '')
            parametro.save()

        resultado.observacao = request.POST.get('observacao', '')
        resultado.save()
        return redirect(f'/rotina?data={agendamento.data.strftime("%Y-%m-%d")}')

    return render(request, 'editar_resultado.html', {
        'resultado': resultado, 'agendamento': agendamento, 'parametros': parametros,
    })

@login_required
@has_permission_decorator('excluir_agendamento')
def excluir_agendamento(request, agendamento_id):

    agendamento = Agendamento.objects.get(id=agendamento_id)

    data = agendamento.data

    agendamento.delete()

    return redirect(
        f'/rotina?data={data.strftime("%Y-%m-%d")}'
    )
def rotina_impressao(request):

    data = request.GET.get('data')

    if data:
        agendamentos = Agendamento.objects.filter(
            data=data
        ).select_related(
            'paciente'
        ).order_by(
            'paciente__nome'
        )
    else:
        data = date.today()

        agendamentos = Agendamento.objects.filter(
            data=data
        ).select_related(
            'paciente'
        ).order_by(
            'paciente__nome'
        )

    exames_impressao = []

    for agendamento in agendamentos:

        exame = EXAMES.get(agendamento.exame)

        if not exame:
            continue

        exames_impressao.append({
            'agendamento': agendamento,
            'exame': exame,
        })

    return render(
        request,
        'rotina_impressao.html',
        {
            'data': data,
            'exames_impressao': exames_impressao,
        })