# ARQUIVO COM OS DADOS DA NOSSA COLÔNIA AURORA
# Aqui definimos as listas, dicionários e matrizes para representar a colônia.

# 1) LISTA DE MÓDULOS 
modulos_rede = [
    "Habitação Alpha",
    "Centro de Controle",
    "Armazenamento de Energia",
    "Suporte Médico",
    "Agricultura Biosfera-2",
    "Laboratório Científico",
    "Produção de Oxigênio",
    "Comunicação Terra-Marte"
]

# 2) DICIONÁRIO DE INFORMAÇÕES DOS MÓDULOS
# A chave é o nome do módulo e os valores são: [Consumo de Energia (MW), Prioridade (1 a 4), Status]
# A prioridade vai de 1 (mais importante) até 4 (menos importante).
dados_infraestrutura = {
    "Habitação Alpha": [45.5, 2, "Operacional"],
    "Centro de Controle": [60.0, 1, "Operacional"],
    "Armazenamento de Energia": [5.0, 1, "Operacional"],
    "Suporte Médico": [25.0, 2, "Operacional"],
    "Agricultura Biosfera-2": [35.0, 3, "Operacional"],
    "Laboratório Científico": [5.0, 4, "Em Manutenção"],
    "Produção de Oxigênio": [75.0, 1, "Operacional"],
    "Comunicação Terra-Marte": [40.0, 2, "Operacional"]
}

# 3) GRAFO DA REDE (Representação por Lista de Adjacência)
# Mostra quais módulos estão conectados entre si e a distância física (peso) em metros.
conexoes_rede = {
    "Habitação Alpha": {
        "Centro de Controle": 15, 
        "Suporte Médico": 5, 
        "Agricultura Biosfera-2": 35
    },
    "Centro de Controle": {
        "Habitação Alpha": 15, 
        "Suporte Médico": 5, 
        "Armazenamento de Energia": 25, 
        "Produção de Oxigênio": 20, 
        "Laboratório Científico": 30
    },
    "Armazenamento de Energia": {
        "Centro de Controle": 25, 
        "Suporte Médico": 10, 
        "Produção de Oxigênio": 15, 
        "Laboratório Científico": 40
    },
    "Suporte Médico": {
        "Habitação Alpha": 5, 
        "Centro de Controle": 5, 
        "Armazenamento de Energia": 10, 
        "Agricultura Biosfera-2": 35, 
        "Laboratório Científico": 30
    },
    "Agricultura Biosfera-2": {
        "Habitação Alpha": 35, 
        "Suporte Médico": 35, 
        "Laboratório Científico": 20
    },
    "Laboratório Científico": {
        "Centro de Controle": 30, 
        "Armazenamento de Energia": 40, 
        "Suporte Médico": 30, 
        "Agricultura Biosfera-2": 20, 
        "Produção de Oxigênio": 40, 
        "Comunicação Terra-Marte": 20
    },
    "Produção de Oxigênio": {
        "Centro de Controle": 20, 
        "Armazenamento de Energia": 15, 
        "Laboratório Científico": 40, 
        "Comunicação Terra-Marte": 50
    },
    "Comunicação Terra-Marte": {
        "Produção de Oxigênio": 50, 
        "Laboratório Científico": 20
    }
}

# 4) MATRIZ DE DISTÂNCIAS (Representação por Matriz de Adjacência)
# Uma tabela de duas dimensões com as distâncias entre todos os pontos.
# O valor 0 significa que não tem caminho direto entre eles (ou que é a distância dele para ele mesmo).
matriz_distancias = [
    [ 0, 15,  0,  5, 35,  0,  0,  0],  # 0: Habitação Alpha
    [15,  0, 25,  5,  0, 30, 20,  0],  # 1: Centro de Controle
    [ 0, 25,  0, 10,  0, 40, 15,  0],  # 2: Armazenamento de Energia
    [ 5,  5, 10,  0, 35, 30,  0,  0],  # 3: Suporte Médico
    [35,  0,  0, 35,  0, 20,  0,  0],  # 4: Agricultura Biosfera-2
    [ 0, 30, 40, 30, 20,  0, 40, 20],  # 5: Laboratório Científico
    [ 0, 20, 15,  0,  0, 40,  0, 50],  # 6: Produção de Oxigênio
    [ 0,  0,  0,  0,  0, 20, 50,  0]   # 7: Comunicação Terra-Marte
]
