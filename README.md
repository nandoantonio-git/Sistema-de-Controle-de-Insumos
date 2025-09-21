
# Sistema de Controle de Insumos💊

Sistema em Python para simular o controle de consumo diário de insumos em unidades de diagnóstico.
O projeto aplica conceitos de estruturas de dados (fila, pilha, busca e ordenação) em um menu interativo no terminal.

## Requisitos
- Python 3.10+
## Funcionalidades

- Fila (FIFO): registra os insumos em ordem cronológica de consumo.
- Pilha (LIFO): mostra os últimos insumos consumidos primeiro.
- Buscas:
    - Sequencial → percorre item a item, retornando índice e passos.
    - Binária → busca otimizada em lista ordenada, com contagem de passos.
- Ordenações:
    - Merge Sort
    - Quick Sort
- Entradas robustas: não aceita valores numéricos, vazios ou opções inválidas; normaliza acentos e letras maiúsculas/minúsculas.

## Estrutura do Projeto
```
controle-insumos/
│
├── main.py        # código principal com menus, buscas e ordenações
├── README.md      # documentação do projeto
└── .gitignore     # ignora arquivos/pastas locais (PyCharm, venv, etc.)

```

## Como Executar🚀

- Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/controle-insumos.git
cd controle-insumos
```
- Execute o programa:
```bash
python main.py
```
## Dados simulados
```python
    insumos_simulados = [
        ("Reagente A", 5,  "Validade: 2026-02-01"),
        ("Seringa",    10, "Validade: 2027-12-31"),
        ("Reagente B", 7,  "Validade: 2026-05-10"),
        ("Luvas",      20, "Validade: 2025-11-20"),
        ("Álcool 70",  12, "Validade: 2026-08-15"),
    ]
```

    
## Uso/Exemplos

```python
=========== CONTROLE DE INSUMOS ===========
1) Listar consumo (Fila - cronológica)
2) Listar consumo (Pilha - inversa)
3) Buscar insumo
4) Ordenações
0) Sair
Escolha uma opção: 1

Fila (ordem cronológica):
Insumo       Qtd  Validade
--------------------------
Reagente A     5  2026-02-01
Seringa       10  2027-12-31
Reagente B     7  2026-05-10
Luvas         20  2025-11-20
Álcool 70     12  2026-08-15
```
## Estrutura/Algoritmo

- **Fila (Queue - FIFO)**
    - Representa o consumo em ordem cronológica.
    - Permite rastrear o histórico de uso dos insumos conforme foram inseridos.
- **Pilha (Stack - LIFO)**
    - Exibe o histórico em ordem inversa.
    - Facilita visualizar rapidamente os últimos consumos.
- **Busca Sequencial**
    - Percorre a lista item a item.
    - **Retorna:** insumo encontrado, número de passos e índice na lista. Útil quando não há lista ordenada.
- **Busca Binária**
    - Trabalha em lista ordenada por nome.
    - Divide o espaço de busca a cada comparação.
    - **Retorna:** insumo encontrado, número de passos e posição na lista ordenada. Muito mais eficiente para grandes volumes de dados.
- **Ordenação**
    - **Merge Sort** e **Quick Sort** implementados para ordenar os insumos por quantidade.
    -  - **Ordenação por validade** implementada para organizar os insumos pela data de vencimento, priorizando os que expiram primeiro.
    - Permite análises como:
        - Quais insumos são mais consumidos.
         - Priorização de reposição.
- **Entradas Robustas**
    - Impede valores inválidos (vazios ou numéricos).
    - Normaliza acentos e maiúsculas/minúsculas.
    - Oferece opção de voltar ao menu ou sair.
    - Sugere alternativas em caso de digitação incorreta.
      
## Conclusão
O projeto demonstra a aplicação prática de estruturas de dados e algoritmos em um **problema real de gestão de insumos.**
- Fila e pilha organizam o histórico de consumo.
- Buscas oferecem formas diferentes de localizar insumos, com feedback de eficiência.
- Ordenações ajudam a priorizar decisões de compra e reposição.
- O menu interativo torna o sistema acessível e próximo de um software real de apoio à gestão.




