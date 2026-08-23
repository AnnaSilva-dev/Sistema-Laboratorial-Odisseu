EXAMES = {
    'glicemia': {
        'nome': 'Glicemia',
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
            {
                'nome': 'Plaquetas',
                'unidade': '/mm³',
                'referencia': '150.000–450.000 /mm³',
            },
        ],
    },
    'proteina': {
            'nome': 'Proteína C reativa',
            'amostra':'soro',
            'metodo':'algoooo',
            'parametros': [
                {
                    'nome': 'resultado',
                    'unidade': 'mg/dL',
                    'referencia': 'Adultos: 60–99 mg/dL\nPré-termo: 20-60mg/dL',
                },
            ],
        },
}
