from django.core.exceptions import ValidationError
from datetime import date
from validate_docbr import CPF, CNS

def validate_future_date(value):
    if value < date.today():
        raise ValidationError("A data não pode ser no passado.")

def validate_cpf(value):
    cpf_validator = CPF()
    if not cpf_validator.validate(value):
        raise ValidationError("CPF inválido.")

def validate_cns(value):
    cns_validator = CNS()
    if not cns_validator.validate(value):
        raise ValidationError("CNS inválido.")

def validate_nome(value):
    if not value.replace(" ", "").isalpha():
        raise ValidationError("O nome deve conter apenas letras e espaços.")

def validate_telefone(value):
    telefone = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not telefone.isdigit() or len(telefone) < 11 or len(telefone) > 14:
        raise ValidationError("O telefone deve conter apenas números e ter entre 11 e 14 dígitos.")