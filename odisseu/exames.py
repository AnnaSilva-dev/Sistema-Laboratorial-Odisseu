def parametros_do_exame(exame):
    if 'secoes' in exame:
        parametros = []
        for secao in exame['secoes']:
            parametros.extend(secao['parametros'])
        return parametros
    return exame['parametros']
EXAMES = {
    'glicemia': {
        'nome': 'Glicemia',
        'amosta': 'Sangue',
        'metodo': 'Enzimático-colorimétrico',
        'parametros': [
            {
                'nome': 'Glicemia',
                'unidade': 'mg/dL',
                'referencia': '70–99 mg/dL',
            },
        ],
    },

     'hemograma': {
        'nome': 'Hemograma',
        'secoes': [
            {
                'nome': 'Eritrograma',
                'parametros': [
                    {
                        'nome': 'Hemoglobina',
                        'unidade': 'g/dL',
                        'referencia': '12–16 g/dL',
                    },
                    {
                        'nome': 'Hematócrito',
                        'unidade': '%',
                        'referencia': '36–46 %',
                    },
                ],
            },
            {
                'nome': 'Leucograma',
                'parametros': [
                    {
                        'nome': 'Leucócitos',
                        'unidade': '/mm³',
                        'referencia': '4.000–11.000 /mm³',
                    },
                    {
                        'nome': 'Neutrófilos',
                        'tipo': 'diferencial',
                        'unidade': '/mm³',
                        'referencia': '1.700–8.000 /mm³',
                    },
                    {
                        'nome': 'Linfócitos',
                        'tipo': 'diferencial',
                        'unidade': '/mm³',
                        'referencia': '1.000–4.800 /mm³',
                    },
                    {
                        'nome': 'Monócitos',
                        'tipo': 'diferencial',
                        'unidade': '/mm³',
                        'referencia': '200–1.100 /mm³',
                    },
                    {
                        'nome': 'Eosinófilos',
                        'tipo': 'diferencial',
                        'unidade': '/mm³',
                        'referencia': '100–660 /mm³',
                    },
                    {
                        'nome': 'Basófilos',
                        'tipo': 'diferencial',
                        'unidade': '/mm³',
                        'referencia': '0–220 /mm³',
                    },
                ],
            },
            {
                'nome': 'Plaquetograma',
                'parametros': [
                    {
                        'nome': 'Plaquetas',
                        'unidade': '/mm³',
                        'referencia': '150.000–450.000 /mm³',
                    },
                ],
            },
        ],
    },

    'proteina': {
            'nome': 'Proteína C reativa',
            'amostra':'soro',
            'metodo':'Aglutinação',
            'parametros': [
                {
                    'nome': 'Resultados do Exame',
                    'unidade': 'mg/dL',
                    'referencia': 'Adultos: 60–99 mg/dL\nPré-termo: 20-60mg/dL',
                },
            ],
        },

     'sumario_urina': {
        'nome': 'Sumário de Urina',
        'secoes': [
            {
                'nome': 'Exame Físico',
                'parametros': [
                    {'nome': 'Cor', 'unidade': '', 'referencia': 'Amarelo citrino'},
                    {'nome': 'Aspecto', 'unidade': '', 'referencia': 'Límpido'},
                ],
            },
            {
                'nome': 'Exame Químico',
                'parametros': [
                    {'nome': 'pH', 'unidade': '', 'referencia': '5,0–7,0'},
                    {'nome': 'Proteínas', 'unidade': '', 'referencia': 'Negativo'},
                    {'nome': 'Glicose', 'unidade': '', 'referencia': 'Negativo'},
                ],
            },
            {
                'nome': 'Sedimentoscopia',
                'parametros': [
                    {'nome': 'Leucócitos', 'unidade': '', 'referencia': 'até 5 /campo'},
                    {'nome': 'Hemácias', 'unidade': '', 'referencia': 'até 3 /campo'},
                ],
            },
        ],
    },
    'colesterol_total': {
            'nome': 'Colesterol Total',
            'amostra':'soro',
            'metodo':'Enzimático-Colorimétrico',
            'parametros': [
                {
                    'nome': 'Resultados do Exame',
                    'unidade': 'mg/dL',
                    'referencia': 'desejável: < 200 mg/dL\nlimítrofe: 200 a 239 mg/dL\nelevado: ≥ 240 mg/dL',
                },
            ],
        },
    'also': {
                'nome': 'Antestreptolisina O',
                'amostra':'soro',
                'metodo':'Aglutinação',
                'parametros': [
                    {
                        'nome': 'Resultados do Exame',
                        'unidade': 'UI/mL',
                        'referencia': '< 200 UI/mL',
                    },
                ],
            },
    'ureia': {
                    'nome': 'Uría',
                    'amostra':'soro',
                    'metodo':'Cinético-UV.',
                    'parametros': [
                        {
                            'nome': 'Resultados do Exame',
                            'unidade': 'UI/mL',
                            'referencia': '15 – 45 mg/dL',
                        },
                    ],
                },
    'tgo': {
                'nome': 'TGO',
                'amostra':'soro',
                'metodo':'cinético-UV',
                'parametros': [
                    {
                        'nome': 'Resultados do Exame',
                        'unidade': 'UI/mL',
                        'referencia': 'Homens: 11 - 39 U/L \nMulheres: 10 - 37 U/L',
                    },
                ],
            },
    'tgp': {
                'nome': 'TGP',
                'amostra':'soro',
                'metodo':'Cinético-UV',
                'parametros': [
                    {
                        'nome': 'Resultados do Exame',
                        'unidade': 'UI/mL',
                        'referencia': 'Homens: 11 - 45 U/L \nMulheres: 10 - 37 U/L',
                    },
                ],
            },
    'gp_sanguineo': {
                'nome': 'Grupo sanguíneo e fator RH',
                'amostra':'soro',
                'metodo':'Cinético-UV',
                'parametros': [
                    {
                        'nome': 'Resultados do Exame',
                        'unidade': '',
                        'referencia': '',
                    },
                ],
            },
}
