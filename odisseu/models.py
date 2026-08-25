from django.db import models
from .validators import validate_cpf, validate_cns, validate_nome, validate_telefone
from django.core.exceptions import ValidationError


class Paciente(models.Model):
    nome = models.CharField(max_length=200, validators=[validate_nome])
    cpf = models.CharField(max_length=14, validators=[validate_cpf])
    cns = models.CharField(max_length=18, validators=[validate_cns])
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, validators=[validate_telefone])

    def __str__(self):
        return self.nome


class Agendamento(models.Model):

    EXAMES = [
        ('glicemia', 'Glicemia'),
        ('hemograma', 'Hemograma'),
        ('proteina', 'Proteína C reativa'),
        ('sumario_urina', 'Sumário de Urina')
    ]
    solicitante = models.CharField(max_length=200, blank=True, validators=[validate_nome])
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    exame = models.CharField(max_length=50, choices=EXAMES)
    data = models.DateField()

    def __str__(self):
        return f'{self.paciente.nome} - {self.exame} - {self.data}'


class Resultado(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='resultado')
    observacao = models.TextField(blank=True)
    liberado = models.BooleanField(default=False)

    def __str__(self):
        return f'Resultado - {self.agendamento}'

    def _valores_calculados(self):
        parametros = list(self.parametros.all())

        leucocitos = None
        for p in parametros:
            if p.nome == 'Leucócitos':
                try:
                    leucocitos = float(p.valor.replace(',', '.'))
                except (ValueError, AttributeError):
                    leucocitos = None
                break

        valores = {}
        for p in parametros:
            valor_exibido = p.valor

            if p.percentual:
                try:
                    pct = float(p.percentual.replace(',', '.'))
                    if leucocitos is not None:
                        valor_exibido = f'{(pct / 100) * leucocitos:.0f}'
                except (ValueError, AttributeError):
                    pass

            valores[p.nome] = {
                'nome': p.nome,
                'percentual': p.percentual,
                'valor': valor_exibido,
                'unidade': p.unidade,
                'referencia': p.referencia,
            }

        return valores

    def secoes_calculadas(self):
       
        from .exames import EXAMES

        exame_config = EXAMES[self.agendamento.exame]
        valores = self._valores_calculados()

        if 'secoes' not in exame_config:
            parametros = list(valores.values())
            return [{'nome': None, 'parametros': parametros}]

        secoes = []
        for secao in exame_config['secoes']:
            parametros = [
                valores[p['nome']] for p in secao['parametros'] if p['nome'] in valores
            ]
            secoes.append({'nome': secao['nome'], 'parametros': parametros})

        return secoes


class ResultadoParametro(models.Model):

    resultado = models.ForeignKey(
        Resultado,
        on_delete=models.CASCADE,
        related_name='parametros'
    )

    nome = models.CharField(max_length=100)

    valor = models.CharField(max_length=100, blank=True)
    percentual = models.CharField(max_length=20, blank=True)

    unidade = models.CharField(max_length=50, blank=True)
    referencia = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.nome}: {self.valor}'