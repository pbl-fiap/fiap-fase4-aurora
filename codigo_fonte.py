# -*- coding: utf-8 -*-
"""
================================================================================
  SIGIC - SISTEMA INTELIGENTE DE GERENCIAMENTO DA INFRAESTRUTURA DA COLÔNIA
================================================================================
  Este é o arquivo principal de execução do sistema da Colônia Aurora (FIAP).
  
  Funcionalidades do sistema:
  - Consulta detalhada aos módulos (Consumo, Prioridade e Status).
  - Visualização da Rede de Conexões (Lista de Adjacência e Matriz de Distâncias).
  - Execução de buscas em redes (BFS - Busca em Largura e DFS - Busca em Profundidade).
  - Cálculo de rotas otimizadas com desvio dinâmico de falhas (Dijkstra).
  - Simulação de contingências operacionais (Alteração de status do módulo).
  - Detecção de conexões/pontos críticos da rede (Requisito 1.3).
  
  Estrutura do projeto:
  codigo_fonte.py (Arquivo Principal)
  arquivos_auxiliares/
      dados.py (Módulo com as estruturas de dados: Listas, Dicts e Matrizes)
      algoritmos.py (Implementação de BFS, DFS, Dijkstra e Pontos Críticos)
================================================================================
"""

import sys
from arquivos_auxiliares.dados import modulos_rede, dados_infraestrutura, conexoes_rede, matriz_distancias, status_infraestrutura
from arquivos_auxiliares.algoritmos import bfs, dfs, dijkstra, obter_modulos_bloqueados, detectar_pontos_criticos

# Cores
COR_VERDE = "\033[92m"
COR_AMARELO = "\033[93m"
COR_VERMELHO = "\033[91m"
COR_AZUL = "\033[94m"
COR_CIANO = "\033[96m"
COR_NEGRITO = "\033[1m"
COR_RESET = "\033[0m"

def cabecalho(titulo):
    """Exibe um cabeçalho decorado para as seções do sistema."""
    print("\n" + "=" * 80)
    print(f"{COR_NEGRITO}{COR_CIANO}{titulo.center(80)}{COR_RESET}")
    print("=" * 80)

def consultar_modulos():
    """Exibe a lista de todos os módulos e seus detalhes operacionais."""
    cabecalho("CONSULTA DE MÓDULOS DA INFRAESTRUTURA")
    print(f"{COR_NEGRITO}{'Módulo':<30} | {'Consumo (MW)':<12} | {'Prioridade (1-4)':<15} | {'Status':<15}{COR_RESET}")
    print("-" * 80)
    
    for idx, modulo in enumerate(modulos_rede, 1):
        consumo, prioridade, _, _ = dados_infraestrutura[modulo]
        status = status_infraestrutura[modulo]
        
        # Colorir status conforme a situação operacional
        if status == "Operacional":
            status_colorido = f"{COR_VERDE}{status:<15}{COR_RESET}"
        else:
            status_colorido = f"{COR_VERMELHO}{status:<15}{COR_RESET}"
            
        print(f"{idx}. {modulo:<27} | {consumo:<12.1f} | {prioridade:<15} | {status_colorido}")
    print("-" * 80)

def visualizar_rede():
    """Exibe a rede representada por Lista de Adjacência e Matriz de Distâncias."""
    cabecalho("VISUALIZAÇÃO DA REDE DA COLÔNIA (LISTA DE ADJACÊNCIA)")
    for modulo, vizinhos in conexoes_rede.items():
        bloqueados = obter_modulos_bloqueados()
        mod_status = f"{COR_VERMELHO}[BLOQUEADO]{COR_RESET}" if modulo in bloqueados else f"{COR_VERDE}[ATIVO]{COR_RESET}"
        print(f"\n{COR_NEGRITO}{modulo}{COR_RESET} {mod_status} está conectado a:")
        for vizinho, distancia in vizinhos.items():
            viz_status = f"{COR_VERMELHO}(Em Manutenção){COR_RESET}" if vizinho in bloqueados else ""
            print(f"  └─► {vizinho:<25} (Distância: {COR_AMARELO}{distancia}m{COR_RESET}) {viz_status}")

    # Exibição da Matriz de Distâncias formatada
    cabecalho("MATRIZ DE DISTÂNCIAS DA REDE (MATRIZ DE ADJACÊNCIA)")
    print("Módulos de Referência:")
    for idx, mod in enumerate(modulos_rede):
        print(f"  [{idx}] {mod}")
    print()
    
    # Cabeçalho da Matriz
    print("      ", end="")
    for i in range(len(modulos_rede)):
        print(f" [{i}] ", end=" ")
    print("\n  " + "-" * (len(modulos_rede) * 5 + 4))
    
    for idx_linha, linha in enumerate(matriz_distancias):
        print(f" [{idx_linha}] |", end="")
        for dist in linha:
            if dist == 0:
                print(f"  -  ", end="")
            else:
                print(f" {dist:>3} ", end="")
        print("|")
    print("  " + "-" * (len(modulos_rede) * 5 + 4))

def executar_caminho_minimo():
    """Calcula a melhor rota entre dois módulos usando o algoritmo de Dijkstra."""
    cabecalho("ROTAS DE DISTRIBUIÇÃO E TRANSPORTE (DIJKSTRA)")
    
    # Exibir lista para o usuário selecionar com facilidade
    for idx, mod in enumerate(modulos_rede, 1):
        print(f" [{idx}] {mod}")
        
    try:
        origem_op = int(input(f"\nSelecione o número do módulo de ORIGEM: "))
        destino_op = int(input("Selecione o número do módulo de DESTINO: "))
        
        if 1 <= origem_op <= len(modulos_rede) and 1 <= destino_op <= len(modulos_rede):
            origem = modulos_rede[origem_op - 1]
            destino = modulos_rede[destino_op - 1]
            
            caminho, distancia = dijkstra(conexoes_rede, origem, destino)
            
            print(f"\n{COR_NEGRITO}Resultado da Otimização:{COR_RESET}")
            if caminho is None:
                print(f"{COR_VERMELHO}ERRO: Não existe caminho viável entre '{origem}' e '{destino}'.{COR_RESET}")
                print("Motivo: Um ou mais módulos no trajeto (ou as extremidades) estão em manutenção.")
            else:
                print(f"Origem:  {COR_CIANO}{origem}{COR_RESET}")
                print(f"Destino: {COR_CIANO}{destino}{COR_RESET}")
                print(f"Rota calculada: {COR_VERDE}{' ➔ '.join(caminho)}{COR_RESET}")
                print(f"Distância total a ser percorrida: {COR_AMARELO}{distancia} metros{COR_RESET}")
        else:
            print(f"{COR_VERMELHO}Opção inválida! Selecione um número de 1 a {len(modulos_rede)}.{COR_RESET}")
    except ValueError:
        print(f"{COR_VERMELHO}Entrada inválida! Digite apenas números inteiros.{COR_RESET}")

def simular_infraestrutura():
    """Permite alterar o status operacional de um módulo para simular falhas e desvios."""
    cabecalho("SIMULADOR DE CONTINGÊNCIAS OPERACIONAIS")
    
    # Mostrar status atualizado
    for idx, mod in enumerate(modulos_rede, 1):
        status = status_infraestrutura[mod]
        status_color = COR_VERDE if status == "Operacional" else COR_VERMELHO
        print(f" [{idx}] {mod:<25} ➔ Status atual: {status_color}{status}{COR_RESET}")
        
    try:
        opcao = int(input("\nSelecione o módulo que deseja ALTERAR o status: "))
        if 1 <= opcao <= len(modulos_rede):
            modulo_selecionado = modulos_rede[opcao - 1]
            status_atual = status_infraestrutura[modulo_selecionado]
            
            # Alternar status
            novo_status = "Em Manutenção" if status_atual == "Operacional" else "Operacional"
            status_infraestrutura[modulo_selecionado] = novo_status
            
            status_color = COR_VERMELHO if novo_status == "Em Manutenção" else COR_VERDE
            print(f"\n{COR_VERDE}✔ Status de '{modulo_selecionado}' atualizado com sucesso para {status_color}{novo_status}{COR_RESET}!")
            
            # Simular impacto dinâmico na rota padrão de energia
            print(f"\n[SIMULAÇÃO DINÂMICA] Recalculando rota crítica: Armazenamento de Energia ➔ Suporte Médico...")
            caminho, dist = dijkstra(conexoes_rede, "Armazenamento de Energia", "Suporte Médico")
            if caminho:
                print(f"Nova Rota de Contingência: {COR_VERDE}{' ➔ '.join(caminho)}{COR_RESET} ({dist}m)")
            else:
                print(f"{COR_VERMELHO}AVISO CRÍTICO: Rota interrompida! Não há caminho operacional alternativo.{COR_RESET}")
        else:
            print(f"{COR_VERMELHO}Opção inválida!{COR_RESET}")
    except ValueError:
        print(f"{COR_VERMELHO}Entrada inválida! Digite números inteiros.{COR_RESET}")

def executar_buscas():
    """Demonstra o funcionamento dos algoritmos de busca BFS e DFS a partir de um nó."""
    cabecalho("ALGORITMOS DE MAPEAMENTO DA REDE (BFS & DFS)")
    print("Selecione um ponto de início para o mapeamento da rede:")
    for idx, mod in enumerate(modulos_rede, 1):
        print(f" [{idx}] {mod}")
        
    try:
        opcao = int(input("\nSelecione o módulo de início: "))
        if 1 <= opcao <= len(modulos_rede):
            inicio = modulos_rede[opcao - 1]
            
            print(f"\nExecutando buscas a partir de: {COR_NEGRITO}{inicio}{COR_RESET}")
            bloqueados = obter_modulos_bloqueados()
            if bloqueados:
                print(f"Módulos bloqueados (ignorados nas buscas): {COR_VERMELHO}{', '.join(bloqueados)}{COR_RESET}")
                
            ordem_bfs = bfs(conexoes_rede, inicio)
            ordem_dfs = dfs(conexoes_rede, inicio)
            
            print(f"\n{COR_NEGRITO}Busca em Largura (BFS) - Mapeamento por níveis/proximidade:{COR_RESET}")
            print(f"  {COR_VERDE}{' ➔ '.join(ordem_bfs)}{COR_RESET}")
            
            print(f"\n{COR_NEGRITO}Busca em Profundidade (DFS) - Exploração profunda de ramais:{COR_RESET}")
            print(f"  {COR_AZUL}{' ➔ '.join(ordem_dfs)}{COR_RESET}")
        else:
            print(f"{COR_VERMELHO}Opção inválida!{COR_RESET}")
    except ValueError:
        print(f"{COR_VERMELHO}Entrada inválida! Digite números inteiros.{COR_RESET}")

def exibir_pontos_criticos():
    """Exibe os pontos ou conexões críticas da rede que podem comprometer a infraestrutura (Req. 1.3)."""
    cabecalho("DETECÇÃO DE PONTOS CRÍTICOS DA REDE")
    print("Analisando a topologia da rede para identificar pontos de falha única...\n")
    
    # Chama a função e separa as duas listas que o algoritmos.py devolve
    modulos, conexoes = detectar_pontos_criticos(conexoes_rede)
    
    # Verifica se as duas listas estão vazias
    if not modulos and not conexoes:
        print(f"{COR_VERDE}✔ Excelente! Nenhum ponto crítico ou de falha única foi detectado na configuração atual da rede.{COR_RESET}")
    else:
        print(f"{COR_VERMELHO}{COR_NEGRITO}⚠ ALERTA DE VULNERABILIDADE NA INFRAESTRUTURA ⚠{COR_RESET}")
        print("Os elementos listados abaixo são cruciais. Se algum deles falhar ou for isolado,")
        print("a integridade de conexões da colônia estará gravemente comprometida.")
        print("-" * 80)
        
        idx = 1
        # Exibe os módulos críticos (Pontos de articulação)
        if modulos:
            for mod in modulos:
                print(f" [{idx}] Módulo Crítico (Articulação): {COR_VERMELHO}{COR_NEGRITO}{mod}{COR_RESET}")
                idx += 1
                
        # Exibe as conexões críticas (Pontes)
        if conexoes:
            for u, v in conexoes:
                print(f" [{idx}] Conexão Crítica (Ponte): {COR_AMARELO}{u}{COR_RESET} ➔ {COR_AMARELO}{v}{COR_RESET}")
                idx += 1
                
        print("-" * 80)
        print(f"{COR_AMARELO}Recomendação: Planejar rotas redundantes para mitigar os riscos nesses pontos.{COR_RESET}")

def main():
    """Loop principal de navegação do menu."""
    while True:
        print("\n" + "=" * 80)
        print(f"{COR_NEGRITO}{COR_VERDE}   S I G I C  -  C O L Ô N I A   A U R O R A   ( F I A P )   {COR_RESET}")
        print("=" * 80)
        print(" Menu Principal:")
        print(f"  [{COR_AMARELO}1{COR_RESET}] Visualizar a Rede da Colônia (Lista e Matriz)")
        print(f"  [{COR_AMARELO}2{COR_RESET}] Consultar Detalhes dos Módulos")
        print(f"  [{COR_AMARELO}3{COR_RESET}] Calcular Caminho Mínimo (Dijkstra)")
        print(f"  [{COR_AMARELO}4{COR_RESET}] Simular Falhas e Contingências Operacionais")
        print(f"  [{COR_AMARELO}5{COR_RESET}] Executar Mapeamento por Algoritmos de Busca (BFS & DFS)")
        print(f"  [{COR_AMARELO}6{COR_RESET}] Detectar Pontos Críticos na Rede")
        print(f"  [{COR_AMARELO}0{COR_RESET}] Sair do Sistema")
        print("=" * 80)
        
        try:
            opcao = input("Selecione a funcionalidade desejada: ").strip()
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
            elif opcao == "6":
                exibir_pontos_criticos()
            elif opcao == "0":
                print(f"\n{COR_VERDE}Finalizando o SIGIC! Obrigado!{COR_RESET}\n")
                break
            else:
                print(f"\n{COR_VERMELHO}Opção inválida! Escolha um dos números do menu.{COR_RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{COR_VERMELHO}Programa interrompido. Finalizando...{COR_RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()