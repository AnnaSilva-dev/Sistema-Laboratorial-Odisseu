from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'cadastrar_usuario': True,
        'cadastrar_paciente': True,
        'editar_paciente': True,
        'agendar_exame': True,
        'exibir_rotina': True,
        'digitar_resultados': True,
        'pdf_resultados': True,
        'imprimir_rotina': True,
    }

class Farmaceutico(AbstractUserRole):
    available_permissions = {
        'agendar_exame': True,
        'exibir_rotina': True,
        'digitar_resultados': True,
        'pdf_resultados': True,
        'imprimir_rotina': True,
        'liberar_resultados': True
    }

class Recepcionista(AbstractUserRole):
    available_permissions = {
        'agendar_exame': True,
        'cadastrar_paciente': True,
        'editar_paciente':True,
    }

class TecnicoLaboratorial(AbstractUserRole):
    available_permissions = {
        'exibir_rotina': True,
        'digitar_resultados': True,
    }