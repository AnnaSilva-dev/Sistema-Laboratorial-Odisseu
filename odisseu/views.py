from django.shortcuts import render, redirect
from .forms import PacienteForm
from .models import Paciente

def index(request):
    return render(request, "index.html")

def pacientes(request):
    pacientes= Paciente.objects.all()

    return render(request, 'pacientes.html', {
        'pacientes': pacientes
    })


def cadastrar_paciente(request):
    if request.method == 'POST':
        form= PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form= PacienteForm()

    context = {
        'form': form, 
    }

    return render(request, 'cadastrar_paciente.html', context)

