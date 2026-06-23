# SIGIC - Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia (Aurora Siger)

## Participantes

Eduardo Lopes da Silveira Mota -RM 563418

Gabriel Luís de Lima Ramos - RM 568984

Mayara Luisa Vicente Rosa - RM 571955

Guilherme Alves Nunes - RM 572754

Este é o projeto de entrega da nossa faculdade desenvolvido para a **FIAP**. O objetivo do sistema é representar, monitorar e otimizar as conexões de energia, suporte de vida e comunicações da colônia espacial **Aurora Siger** em Marte, utilizando conceitos de Teoria dos Grafos e algoritmos de busca/caminho mínimo.

---

##  Estrutura do Projeto

Nossa entrega está organizada da seguinte forma:

```text
├── codigo_fonte.py                  # Arquivo principal para rodar o sistema
├── arquivos_auxiliares/
│   ├── dados.py                     # Estruturas de dados (listas, dicionários, matrizes)
│   └── algoritmos.py                # Algoritmos de grafos (BFS, DFS, Dijkstra)
├── rede_colonia.pdf                 # Mapa visual do grafo de conexões
├── documentacao_complementar.pdf    # Relatório detalhado do projeto
└── link_video.txt                   # Link do vídeo explicativo publicado no YouTube
```

---

##  Como Executar o Sistema

O sistema foi feito utilizando apenas a biblioteca padrão do Python, ou seja, **não precisa instalar nenhuma biblioteca externa** para rodá-lo. 

### Pré-requisitos:
* Ter o Python 3 instalado no computador.

### Passo a Passo para rodar:
1. Abra o terminal (Prompt de Comando ou PowerShell).
2. Vá até a pasta onde estão os arquivos do projeto.
3. Digite o seguinte comando e aperte Enter:
   ```bash
   python codigo_fonte.py
   ```
4. Navegue pelo menu interativo digitando os números correspondentes às opções que você deseja executar!

---

##  Funcionalidades do Sistema

1. **Visualizar a Rede da Colônia:** Mostra a lista de conexões de cada módulo e exibe na tela a matriz de distâncias de toda a base marciana.
2. **Consultar Detalhes dos Módulos:** Exibe o consumo de energia em MW, prioridade operacional e o status operacional atual.
3. **Calcular Caminho Mínimo (Dijkstra):** Calcula a melhor rota de distribuição física e a menor distância física acumulada entre dois módulos, desviando automaticamente de módulos com falha.
4. **Simular Contingências Operacionais:** Permite ligar/desligar módulos (mudar status para "Em Manutenção" ou "Operacional") para simular falhas e ver o Dijkstra recalcular a rota em tempo real.
5. **Executar Algoritmos de Busca (BFS & DFS):** Demonstra de forma prática a ordem de varredura na rede a partir de um módulo de início escolhido pelo usuário.
6. **Detectar Pontos Críticos na Rede (Busca com DFS):** Identifica automaticamente quais módulos (pontos de articulação) e conexões (pontes) são vitais para a rede, cuja queda ou interrupção isolaria partes da colônia.
