# -*- coding: utf-8 -*-
# ================================================================================
# ARQUIVO PRINCIPAL DO NOSSO PROJETO - COLÔNIA AURORA
# ================================================================================
# Desenvolvido para a entrega da faculdade.
# O sistema mostra o mapa da colônia espacial e roda buscas em grafos e menor caminho.
#
# Estrutura do nosso projeto:
# ├── codigo_fonte.py (Este arquivo aqui com o menu do terminal)
# └── arquivos_auxiliares/
#     ├── dados.py (Onde guardamos as listas, dicionários e matrizes de conexões)
#     └── algoritmos.py (Onde codificamos a BFS, DFS e o algoritmo de Dijkstra)
# ================================================================================

import sys
from arquivos_auxiliares.dados import modulos_rede, dados_infraestrutura, conexoes_rede, matriz_distancias
from arquivos_auxiliares.algoritmos import bfs, dfs, dijkstra, obter_modulos_bloqueados

# Cores ANSI para o terminal ficar bonitinho e organizado
COR_VERDE = "\033[92m"
COR_AMARELO = "\033[93m"
COR_VERMELHO = "\033[91m"
COR_AZUL = "\033[94m"
COR_CIANO = "\033[96m"
COR_NEGRITO = "\033[1m"
COR_RESET = "\033[0m"

def cabecalho(titulo):
    # Desenha uma bordinha padrão para as telas do menu
    print("\n" + "=" * 80)
    print(f"{COR_NEGRITO}{COR_CIANO}{titulo.center(80)}{COR_RESET}")
    print("=" * 80)

def consultar_modulos():
    # Mostra a lista dos prédios com consumo de energia, prioridade e status
    cabecalho("CONSULTA DE MÓDULOS DA INFRAESTRUTURA")
    print(f"{COR_NEGRITO}{'Módulo':<30} | {'Consumo (MW)':<12} | {'Prioridade (1-4)':<15} | {'Status':<15}{COR_RESET}")
    print("-" * 80)
    
    for idx, modulo in enumerate(modulos_rede, 1):
        consumo, prioridade, status = dados_infraestrutura[modulo]
        
        # Se estiver quebrado/manutenção, pinta de vermelho
        if status == "Operacional":
            status_colorido = f"{COR_VERDE}{status:<15}{COR_RESET}"
        else:
            status_colorido = f"{COR_VERMELHO}{status:<15}{COR_RESET}"
            
        print(f"{idx}. {modulo:<27} | {consumo:<12.1f} | {prioridade:<15} | {status_colorido}")
    print("-" * 80)

def visualizar_rede():
    # Mostra quem está conectado com quem (grafo) e a matriz de distâncias
    cabecalho("VISUALIZAÇÃO DA REDE DA COLÔNIA (LISTA DE ADJACÊNCIA)")
    for modulo, vizinhos in conexoes_rede.items():
        bloqueados = obter_modulos_bloqueados()
        mod_status = f"{COR_VERMELHO}[BLOQUEADO]{COR_RESET}" if modulo in bloqueados else f"{COR_VERDE}[ATIVO]{COR_RESET}"
        print(f"\n{COR_NEGRITO}{modulo}{COR_RESET} {mod_status} está conectado a:")
        for vizinho, distancia in vizinhos.items():
            viz_status = f"{COR_VERMELHO}(Em Manutenção){COR_RESET}" if vizinho in bloqueados else ""
            print(f"  └─► {vizinho:<25} (Distância: {COR_AMARELO}{distancia}m{COR_RESET}) {viz_status}")

    # Imprime a matriz na tela usando tabulação simples
    cabecalho("MATRIZ DE DISTÂNCIAS DA REDE (MATRIZ DE ADJACÊNCIA)")
    print("Legenda dos Módulos:")
    for idx, mod in enumerate(modulos_rede):
        print(f"  [{idx}] {mod}")
    print()
    
    # Cabeçalho com os índices das colunas
    print("      ", end="")
    for i in range(len(modulos_rede)):
        print(f" [{i}] ", end=" ")
    print("\n  " + "-" * (len(modulos_rede) * 5 + 4))
    
    # Linhas da matriz
    for idx_linha, linha in enumerate(matriz_distancias):
        print(f" [{idx_linha}] |", end="")
        for dist in linha:
            if dist == 0:
                print(f"  -  ", end="") # Sem ligação
            else:
                print(f" {dist:>3} ", end="")
        print("|")
    print("  " + "-" * (len(modulos_rede) * 5 + 4))

def executar_caminho_minimo():
    # Pergunta a origem e destino para rodar o algoritmo de Dijkstra
    cabecalho("ROTAS DE DISTRIBUIÇÃO E TRANSPORTE (DIJKSTRA)")
    
    for idx, mod in enumerate(modulos_rede, 1):
        print(f" [{idx}] {mod}")
        
    try:
        origem_op = int(input(f"\nSelecione o número do módulo de ORIGEM: "))
        destino_op = int(input("Selecione o número do módulo de DESTINO: "))
        
        if 1 <= origem_op <= len(modulos_rede) and 1 <= destino_op <= len(modulos_rede):
            origem = modulos_rede[origem_op - 1]
            destino = modulos_rede[destino_op - 1]
            
            # Chama a função que importamos
            caminho, distancia = dijkstra(conexoes_rede, origem, destino)
            
            print(f"\n{COR_NEGRITO}Resultado do cálculo de menor caminho:{COR_RESET}")
            if caminho is None:
                print(f"{COR_VERMELHO}ERRO: Não conseguimos achar uma rota entre '{origem}' e '{destino}'.{COR_RESET}")
                print("Motivo: Tem algum módulo quebrado ou em manutenção no caminho.")
            else:
                print(f"Origem:  {COR_CIANO}{origem}{COR_RESET}")
                print(f"Destino: {COR_CIANO}{destino}{COR_RESET}")
                print(f"Rota calculada: {COR_VERDE}{' -> '.join(caminho)}{COR_RESET}")
                print(f"Distância total: {COR_AMARELO}{distancia} metros{COR_RESET}")
        else:
            print(f"{COR_VERMELHO}Opção inválida! Escolha de 1 a {len(modulos_rede)}.{COR_RESET}")
    except ValueError:
        print(f"{COR_VERMELHO}Entrada errada! Digite apenas números inteiros.{COR_RESET}")

def simular_infraestrutura():
    # Permite mudar o status operacional de qualquer módulo para ver o impacto em tempo real
    cabecalho("SIMULADOR DE FALHAS E CONEXÕES")
    
    for idx, mod in enumerate(modulos_rede, 1):
        status = dados_infraestrutura[mod][2]
        status_color = COR_VERDE if status == "Operacional" else COR_VERMELHO
        print(f" [{idx}] {mod:<25} -> Status: {status_color}{status}{COR_RESET}")
        
    try:
        opcao = int(input("\nSelecione o módulo para mudar o status dele: "))
        if 1 <= opcao <= len(modulos_rede):
            modulo_selecionado = modulos_rede[opcao - 1]
            status_atual = dados_infraestrutura[modulo_selecionado][2]
            
            # Inverte o status operacional
            novo_status = "Em Manutenção" if status_atual == "Operacional" else "Operacional"
            dados_infraestrutura[modulo_selecionado][2] = novo_status
            
            status_color = COR_VERMELHO if novo_status == "Em Manutenção" else COR_VERDE
            print(f"\n{COR_VERDE}✔ Status de '{modulo_selecionado}' mudado para {status_color}{novo_status}{COR_RESET}!")
            
            # Simula de forma automática se o fornecimento de energia vai continuar funcionando ou não
            print(f"\n[TESTANDO ROTA DE ENERGIA] Armazenamento de Energia -> Suporte Médico...")
            caminho, dist = dijkstra(conexoes_rede, "Armazenamento de Energia", "Suporte Médico")
            if caminho:
                print(f"Nova rota encontrada: {COR_VERDE}{' -> '.join(caminho)}{COR_RESET} ({dist}m)")
            else:
                print(f"{COR_VERMELHO}ALERTA: O fornecimento de energia caiu! Não sobrou nenhuma rota livre.{COR_RESET}")
        else:
            print(f"{COR_VERMELHO}Opção inválida!{COR_RESET}")
    except ValueError:
        print(f"{COR_VERMELHO}Entrada incorreta! Digite apenas números.{COR_RESET}")

def executar_buscas():
    # Permite escolher um nó inicial para rodar a Busca em Largura e em Profundidade
    cabecalho("RODAR ALGORITMOS DE BUSCA (BFS E DFS)")
    print("Escolha o módulo inicial para a busca:")
    for idx, mod in enumerate(modulos_rede, 1):
        print(f" [{idx}] {mod}")
        
    try:
        opcao = int(input("\nSelecione o módulo de início: "))
        if 1 <= opcao <= len(modulos_rede):
            inicio = modulos_rede[opcao - 1]
            
            print(f"\nRodando buscas começando por: {COR_NEGRITO}{inicio}{COR_RESET}")
            bloqueados = obter_modulos_bloqueados()
            if bloqueados:
                print(f"Módulos ignorados por estarem em manutenção: {COR_VERMELHO}{', '.join(bloqueados)}{COR_RESET}")
                
            ordem_bfs = bfs(conexoes_rede, inicio)
            ordem_dfs = dfs(conexoes_rede, inicio)
            
            print(f"\n{COR_NEGRITO}Ordem da Busca em Largura (BFS):{COR_RESET}")
            print(f"  {COR_VERDE}{' -> '.join(ordem_bfs)}{COR_RESET}")
            
            print(f"\n{COR_NEGRITO}Ordem da Busca em Profundidade (DFS):{COR_RESET}")
            print(f"  {COR_AZUL}{' -> '.join(ordem_dfs)}{COR_RESET}")
        else:
            print(f"{COR_VERMELHO}Opção inválida!{COR_RESET}")
    except ValueError:
        print(f"{COR_VERMELHO}Entrada inválida! Digite números.{COR_RESET}")

def main():
    # Menu principal em loop infinito até o usuário escolher sair
    while True:
        print("\n" + "=" * 80)
        print(f"{COR_NEGRITO}{COR_VERDE}   S I G I C  -  C O L Ô N I A   A U R O R A   ( F I A P )   {COR_RESET}")
        print("=" * 80)
        print(" Menu de Opções:")
        print(f"  [{COR_AMARELO}1{COR_RESET}] Mostrar a Rede da Colônia (Listas e Matriz)")
        print(f"  [{COR_AMARELO}2{COR_RESET}] Consultar Detalhes dos Módulos")
        print(f"  [{COR_AMARELO}3{COR_RESET}] Calcular Caminho Mínimo (Dijkstra)")
        print(f"  [{COR_AMARELO}4{COR_RESET}] Simular Mudança de Status do Módulo (Simulação)")
        print(f"  [{COR_AMARELO}5{COR_RESET}] Executar buscas na rede (BFS e DFS)")
        print(f"  [{COR_AMARELO}0{COR_RESET}] Sair")
        print("=" * 80)
        
        try:
            opcao = input("Selecione uma opção: ").strip()
            if opcao == "1":
                visualizar_rede()
            elif opcao == "2":
                consultar_modulos()
            elif opcao == "3":
                executar_caminho_minimo()
            elif opcao == "4":
                simular_infraestrutura()
            elif opcao == "5":
                executar_buscas()
            elif opcao == "0":
                print(f"\n{COR_VERDE}Finalizando o programa. Trabalho finalizado com sucesso!{COR_RESET}\n")
                break
            else:
                print(f"\n{COR_VERMELHO}Opção inválida! Tente novamente.{COR_RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{COR_VERMELHO}Programa fechado pelo teclado. Falou!{COR_RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
