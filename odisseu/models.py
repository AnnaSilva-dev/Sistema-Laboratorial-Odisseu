from django.db import models


class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11)
    cns = models.CharField(max_length=14)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
class Agendamento(models.Model):

    EXAMES = [
        ('glicemia', 'Glicemia'),
        ('hemograma', 'Hemograma'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE
    )

    exame = models.CharField(
        max_length=50,
        choices=EXAMES
    )

    data = models.DateField()

    def __str__(self):
        return f'{self.paciente.nome} - {self.exame} - {self.data}'

class Resultado(models.Model):
    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.CASCADE,
        related_name='resultado'
    )

    valor = models.CharField(max_length=100)
    observacao = models.TextField(blank=True)
    liberado = models.BooleanField(default=False)

    def __str__(self):
        return f'Resultado - {self.agendamento}'