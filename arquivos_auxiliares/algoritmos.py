# -*- coding: utf-8 -*-
# AQUI FICA A NOSSA PARTE DE ALGORITMOS DE GRAFOS
# Fizemos funções para BFS, DFS e Dijkstra, adaptadas para ignorar os módulos que estão em manutenção.

from heapq import heappush, heappop
from arquivos_auxiliares.dados import dados_infraestrutura, status_infraestrutura

def obter_modulos_bloqueados():
    # Olha o dicionário de status e devolve uma lista com os módulos que não estão "Operacional"
    bloqueados = []
    for modulo, status in status_infraestrutura.items():
        if status != "Operacional":
            bloqueados.append(modulo)
    return bloqueados

def detectar_pontos_criticos(grafo):
    """
    Identifica:
    1. Módulos Críticos (Pontos de Articulação): cuja falha desconecta a rede.
    2. Conexões Críticas (Pontes): cujo rompimento desconecta a rede.
    Utiliza Busca em Profundidade (DFS) para verificar a conectividade do grafo ativo.
    """
    ativos = [no for no in grafo if no not in obter_modulos_bloqueados()]
    if len(ativos) <= 1:
        return [], []

    # 1. Encontrar Módulos Críticos (Pontos de Articulação)
    modulos_criticos = []
    for no_teste in ativos:
        restantes = [n for n in ativos if n != no_teste]
        if not restantes:
            continue
            
        # DFS simples para ver se todos os nós restantes continuam conectados
        inicio = restantes[0]
        visitados = set()
        pilha = [inicio]
        while pilha:
            atual = pilha.pop()
            if atual not in visitados:
                visitados.add(atual)
                for vizinho in grafo[atual]:
                    if vizinho in restantes and vizinho not in visitados:
                        pilha.append(vizinho)
        
        # Se algum nó ficou isolado / inalcançável, no_teste é um ponto de articulação
        if len(visitados) < len(restantes):
            modulos_criticos.append(no_teste)

    # 2. Encontrar Conexões Críticas (Pontes)
    # Como as conexões são bidirecionais, representamos cada aresta ordenada para evitar duplicidade
    arestas = set()
    for no in ativos:
        for vizinho in grafo[no]:
            if vizinho in ativos:
                aresta = tuple(sorted([no, vizinho]))
                arestas.add(aresta)

    conexoes_criticas = []
    for u, v in arestas:
        # Testa remover temporariamente a conexão (u, v) do grafo ativo
        inicio = u
        visitados = set()
        pilha = [inicio]
        while pilha:
            atual = pilha.pop()
            if atual not in visitados:
                visitados.add(atual)
                for vizinho in grafo[atual]:
                    if vizinho in ativos and vizinho not in visitados:
                        # Ignora a conexão (u, v) removida
                        if (atual == u and vizinho == v) or (atual == v and vizinho == u):
                            continue
                        pilha.append(vizinho)
        
        # Se a remoção da conexão desconectou o grafo
        if len(visitados) < len(ativos):
            conexoes_criticas.append((u, v))

    return modulos_criticos, conexoes_criticas

def bfs(grafo, inicio):
    # Busca em Largura: visita os vizinhos mais próximos primeiro (por nível)
    visitados = set()
    fila = [inicio] # Fila para controlar quem a gente vai visitar
    ordem = [] # Guarda a ordem que visitamos para mostrar na tela
    bloqueados = set(obter_modulos_bloqueados())

    while fila:
        atual = fila.pop(0) # Tira o primeiro da fila

        if atual in visitados or atual in bloqueados:
            continue

        visitados.add(atual)
        ordem.append(atual)

        # Adiciona os vizinhos que não foram visitados e não estão bloqueados
        if atual in grafo:
            for vizinho in grafo[atual]:
                if vizinho not in visitados and vizinho not in bloqueados:
                    fila.append(vizinho)
    return ordem

def dfs(grafo, inicio):
    # Busca em Profundidade: vai até o final de um caminho antes de voltar
    visitados = set()
    pilha = [inicio] # Pilha (último a entrar é o primeiro a sair)
    ordem = []
    bloqueados = set(obter_modulos_bloqueados())

    while pilha:
        atual = pilha.pop() # Tira o último da pilha

        if atual in visitados or atual in bloqueados:
            continue

        visitados.add(atual)
        ordem.append(atual)

        # Coloca os vizinhos na pilha
        if atual in grafo:
            vizinhos = list(grafo[atual].keys())
            for vizinho in reversed(vizinhos): # Inverte para visitar na ordem certa
                if vizinho not in visitados and vizinho not in bloqueados:
                    pilha.append(vizinho)
    return ordem

def dijkstra(grafo, inicio, destino):
    # Dijkstra: acha o menor caminho (menor distância acumulada) de um ponto até o outro
    bloqueados = set(obter_modulos_bloqueados())

    # Se a origem ou o destino estiverem bloqueados, nem dá pra ir
    if inicio in bloqueados or destino in bloqueados:
        return None, float("inf")

    # Começa todo mundo com distância infinita e sem pai (anterior)
    distancias = {modulo: float("inf") for modulo in grafo}
    anteriores = {modulo: None for modulo in grafo}
    
    distancias[inicio] = 0
    fila_prioridade = []
    heappush(fila_prioridade, (0, inicio)) # Coloca a origem com peso 0

    while fila_prioridade:
        distancia_atual, atual = heappop(fila_prioridade)

        # Se já achamos um caminho menor para o atual, ignora esse
        if distancia_atual > distancias[atual]:
            continue

        # Se chegou no destino, podemos parar
        if atual == destino:
            break

        if atual in grafo:
            for vizinho, peso in grafo[atual].items():
                if vizinho in bloqueados:
                    continue

                nova_distancia = distancia_atual + peso
                # Se o caminho novo for mais curto, atualiza
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual
                    heappush(fila_prioridade, (nova_distancia, vizinho))

    # Reconstrói o caminho de trás pra frente
    caminho = []
    atual = destino

    # Se o destino continua com distância infinita, significa que não tem caminho
    if distancias[destino] == float("inf"):
        return None, float("inf")

    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse() # Inverte para ficar do início ao fim
    return caminho, distancias[destino]
