from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PacienteForm, AgendamentoForm, ResultadoForm, UsuarioForm
from .models import Paciente, Agendamento, Resultado, ResultadoParametro
from datetime import date, datetime, timezone, timedelta
from .exames import EXAMES, parametros_do_exame
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_permission_decorator
from django.contrib.auth.decorators import login_required
from .roles import Farmaceutico, Administrador, TecnicoLaboratorial, Recepcionista
from django.utils import timezone
from django.contrib import messages
from rolepermissions.checkers import has_role

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


    inicio_mes = hoje.replace(day=1)
    if hoje.month == 12:
        inicio_prox_mes = date(hoje.year + 1, 1, 1)
    else:
        inicio_prox_mes = date(hoje.year, hoje.month + 1, 1)

    fim_mes_anterior = inicio_mes - timedelta(days=1)
    inicio_mes_anterior = fim_mes_anterior.replace(day=1)


    exames_mes = Agendamento.objects.filter(
        data__gte=inicio_mes,
        data__lt=inicio_prox_mes,
        resultado__isnull=False
    ).count()

    exames_mes_anterior = Agendamento.objects.filter(
        data__gte=inicio_mes_anterior,
        data__lt=inicio_mes,
        resultado__isnull=False
    ).count()

    if exames_mes_anterior > 0:
        variacao = (
            (exames_mes - exames_mes_anterior)
            / exames_mes_anterior
        ) * 100
    else:
        variacao = 0

    return render(
        request,
        'index.html',
        {
            'pacientes_agendados': pacientes_agendados,
            'resultados_pendentes': resultados_pendentes,
            'exames_pendentes': exames_pendentes,

            'exames_mes': exames_mes,
            'variacao': variacao,
        }
    )


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
            'Tecnicolaboratorial': TecnicoLaboratorial}
            role = ROLES[perfil]
            assign_role(user, role)
            if form.is_valid():
                messages.success(request, 'Usuário cadastrado com sucesso!')
            else:
                messages.error(request, 'Ocorreu um erro')

            return redirect('cadastrar_usuario')
        
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
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('cadastrar_paciente')
        else:
            messages.error(request, 'Ocorreu um erro')
        
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
            messages.success(request, 'Exame agendado com sucesso!')

            return redirect('agendar_exame')

        else:
            messages.error(request, 'Ocorreu um erro')

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
@has_permission_decorator('exibir_rotina')
def rotina(request):

    data_str = request.GET.get('data')

    if data_str:

        data = datetime.strptime(
            data_str,
            '%Y-%m-%d'
        ).date()

    else:

        data = date.today()


    agendamentos = Agendamento.objects.filter(
        data=data
    )


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

@login_required
@has_permission_decorator('digitar_resultados')
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
            messages.success(request, 'Resultado salvo com sucesso!')

        else:
            messages.error(request, 'Ocorreu um erro')

        return redirect(f'/rotina?data={agendamento.data.strftime("%Y-%m-%d")}')

    else:
        form = ResultadoForm()

    return render(request, 'digitar_resultados.html', {'form': form, 'agendamento': agendamento, 'exame': exame})

from rolepermissions.checkers import has_permission

@login_required
@has_permission_decorator('ver_resultados')
def ver_resultados(request, paciente_id, data):

    paciente = Paciente.objects.get(id=paciente_id)
    data = datetime.strptime(data, '%Y-%m-%d').date()

    resultados = Resultado.objects.filter(
        agendamento__paciente=paciente,
        agendamento__data=data,
    )

    if not has_permission(request.user, 'liberar_resultado'):
        resultados = resultados.filter(liberado=True)

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
            messages.success(request, 'Paciente editado com sucesso!')
            return redirect('pacientes')
        else:
            messages.error(request, 'Ocorreu um erro')

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
        messages.success(request, 'Resultado editado com sucesso!')

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
    messages.success(request, 'Agendamento excluido com sucesso!')

    return redirect(
        f'/rotina?data={data.strftime("%Y-%m-%d")}'
    )



def rotina_impressao(request):

    data_str = request.GET.get('data')

    if data_str:

        data = datetime.strptime(
            data_str,
            '%Y-%m-%d'
        ).date()

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

        exame = EXAMES.get(
            agendamento.exame
        )

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
        }
    )
@login_required
@has_permission_decorator('liberar_resultados')
def liberar_resultados(request):

    if request.method == 'POST':

        linhas_afetadas=ids_selecionados = request.POST.getlist('resultados')

        Resultado.objects.filter(
            id__in=ids_selecionados
        ).update(liberado=True)

        if ids_selecionados: 
                linhas_afetadas = Resultado.objects.filter(
                    id__in=ids_selecionados
                ).update(liberado=True)

                if linhas_afetadas > 0:
                    messages.success(request, f'{linhas_afetadas} resultado(s) liberado(s) com sucesso!')
                else:
                    messages.warning(request, 'Os resultados selecionados já estavam liberados ou não foram encontrados.')
        else:
            messages.error(request, 'Nenhum resultado foi selecionado para liberação.')

        return redirect('liberar_resultados')

    resultados_pendentes = Resultado.objects.filter(
        liberado=False
    ).select_related(
        'agendamento__paciente'
    ).order_by(
        'agendamento__paciente__nome',
        'agendamento__data'
    )

    agrupado = {}
    for resultado in resultados_pendentes:
        chave = (resultado.agendamento.paciente_id, resultado.agendamento.data)
        if chave not in agrupado:
            agrupado[chave] = {
                'paciente': resultado.agendamento.paciente,
                'data': resultado.agendamento.data,
                'resultados': [],
            }
        agrupado[chave]['resultados'].append(resultado)
    grupos = list(agrupado.values())

    return render(
        request,
        'liberar_resultados.html',
        {'grupos': grupos}
    )

#usuario

def usuarios(request):
    usuarios= User.objects.all()
    busca = request.GET.get('busca', '').strip()

    if busca:
        usuarios = User.objects.filter(
            first_name__icontains=busca
        ) | User.objects.filter(
            last_name__icontains=busca
        ) | User.objects.filter(
            username__icontains=busca
        ) | User.objects.filter(
            email__icontains=busca
        )
    for usuario in usuarios:
        if has_role(usuario, Administrador):
            usuario.perfil = 'Administrador'
        elif has_role(usuario, Farmaceutico):
            usuario.perfil = 'Farmacêutico'
        elif has_role(usuario, Recepcionista):
            usuario.perfil = 'Recepcionista'
        elif has_role(usuario, TecnicoLaboratorial):
            usuario.perfil = 'Técnico Laboratorial'
   

    return render(
        request,
        'usuarios.html',
        {
            'usuarios': usuarios,
            
        }
    )

def inativar_usuario(request, id):

    if request.method == 'POST':

        usuario = get_object_or_404(User, id=id)

        if request.user.id == usuario.id:

            if has_role(request.user, Administrador):
                administradores_ativos = 0

                for user in User.objects.filter(is_active=True):
                    if has_role(user, Administrador):
                        administradores_ativos += 1

                if administradores_ativos == 1:
                    messages.error(
                        request,
                        'Você não pode inativar sua própria conta, pois é o único administrador ativo do sistema.'
                    )
                    return redirect('usuarios')

        usuario.is_active = False
        usuario.save()
        messages.success(request, "Usuário inativado com sucesso!")
    return redirect('usuarios')

def ativar_usuario(request, id):

  if request.method == 'POST':

    usuario = get_object_or_404(User, id=id)

    usuario.is_active = True
    usuario.save()
    messages.success(request, "Usuário ativado com sucesso!")
    return redirect('usuarios')


def editar_usuarios(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.save()

        return redirect('usuarios')

    usuarios = User.objects.all()

    return render(request, 'usuarios.html', {
        'usuarios': usuarios,
        'usuario_edicao': usuario
    })