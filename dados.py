# Módulo: Habitação
# Foco: Suporte à vida e acomodação da tripulação

habitacao = {
    "nome": "Módulo de Habitação Alpha",
    "consumo_energetico_kw": 45.5,
    "prioridade_operacional": 2,
    "capacidade_armazenamento": {
        "agua_litros": 5000,
        "suprimentos_dias": 30
    },
    "necessidade_comunicacao": "alta",
    "status_operacional": "ativo"
}

# Módulo: Centro de Controle
# Foco: O cérebro da colônia Aurora Siger
centroDeControle = {
    "nome": "Núcleo de Comando Central",
    "consumo_energetico_kw": 60.0,
    "prioridade_operacional": 1,
    "capacidade_armazenamento": {
        "backups_dados_tb": 500
    },
    "necessidade_comunicacao": "critica",
    "status_operacional": "ativo"
}

# Módulo: Armazenamento de Energia
# Foco: Banco de baterias principais da base
energia = {
    "nome": "Matriz de Baterias de Estado Sólido",
    "consumo_energetico_kw": 5.0,
    "prioridade_operacional": 1,
    "capacidade_armazenamento": {
        "energia_mwh": 150.0
    },
    "necessidade_comunicacao": "alta",
    "status_operacional": "ativo"
}

# Módulo: Agricultura
# Foco: Estufas hidropônicas para produção de alimentos e reciclagem de CO2
agricultura = {
    "nome": "Estufa Hidropônica Biosfera-2",
    "consumo_energetico_kw": 35.0,
    "prioridade_operacional": 3,
    "capacidade_armazenamento": {
        "alimentos_kg": 1200,
        "sementes_variedades": 45
    },
    "necessidade_comunicacao": "media",
    "status_operacional": "ativo"
}

# Módulo: Laboratório Científico
# Foco: Análise de solo marciano e experimentos biológicos
laboratorioCientifico = {
    "nome": "Laboratório de Análise Geológica e Biológica",
    "consumo_energetico_kw": 55.0,
    "prioridade_operacional": 4,
    "capacidade_armazenamento": {
        "amostras_solitarias_unidades": 250
    },
    "necessidade_comunicacao": "media",
    "status_operacional": "em manutenção"
}

# Módulo: Comunicação
# Foco: Antenas de longo alcance (Deep Space) e rede local
comunicacao = {
    "nome": "Matriz de Antenas de Telecomunicação Terra-Marte",
    "consumo_energetico_kw": 40.0,
    "prioridade_operacional": 2,
    "capacidade_armazenamento": {
        "buffer_dados_gb": 10240
    },
    "necessidade_comunicacao": "critica",
    "status_operacional": "ativo"
}

# Módulo: Suporte Médico
# Foco: Ala médica e UTI para a tripulação
suporteMedico = {
    "nome": "Unidade Médica e de Bioanálise",
    "consumo_energetico_kw": 25.0,
    "prioridade_operacional": 2,
    "capacidade_armazenamento": {
        "medicamentos_kits": 150,
        "leitos_disponiveis": 4
    },
    "necessidade_comunicacao": "alta",
    "status_operacional": "ativo"
}

# Módulo: Produção de Oxigênio
# Foco: Extração de O2 da atmosfera (estilo MOXIE) e craqueamento de água
producaoDeOxigenio = {
    "nome": "Urgina Extratora de Oxigênio Atmosférico",
    "consumo_energetico_kw": 75.0,
    "prioridade_operacional": 1,
    "capacidade_armazenamento": {
        "oxigenio_litros_compressos": 20000
    },
    "necessidade_comunicacao": "alta",
    "status_operacional": "em alerta"
}