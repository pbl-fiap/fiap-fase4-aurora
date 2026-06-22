# -*- coding: utf-8 -*-
# AQUI FICA A NOSSA PARTE DE ALGORITMOS DE GRAFOS
# Fizemos funções para BFS, DFS e Dijkstra, adaptadas para ignorar os módulos que estão em manutenção.

from heapq import heappush, heappop
from arquivos_auxiliares.dados import dados_infraestrutura

def obter_modulos_bloqueados():
    # Olha o dicionário e devolve uma lista com os módulos que não estão "Operacional"
    bloqueados = []
    for modulo, info in dados_infraestrutura.items():
        if info[2] != "Operacional":
            bloqueados.append(modulo)
    return bloqueados

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
