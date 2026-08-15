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
        ('proteina', 'Proteína C reativa'),
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

    observacao = models.TextField(
        blank=True
    )

    liberado = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'Resultado - {self.agendamento}'

class ResultadoParametro(models.Model):

    resultado = models.ForeignKey(
        Resultado,
        on_delete=models.CASCADE,
        related_name='parametros'
    )

    nome = models.CharField(
        max_length=100
    )

    valor = models.CharField(
        max_length=100,
        blank=True
    )

    unidade = models.CharField(
        max_length=50,
        blank=True
    )

    referencia = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f'{self.nome}: {self.valor}'