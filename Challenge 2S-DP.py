from collections import deque, defaultdict
import unicodedata
from datetime import date

# ===================== Utils =====================
def normaliza(s: str) -> str:
    """Remove acentos/variações e baixa caixa para comparação robusta."""
    nfkd = unicodedata.normalize("NFKD", s)
    sem_acentos = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acentos.casefold().strip()

def eh_numerico(s: str) -> bool:
    s = s.strip()
    if not s:
        return False
    s = s.replace(",", ".")
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_validade_str(s: str) -> date | None:
    """Converte string de validade em objeto date (YYYY-MM-DD)."""
    s = str(s).strip()
    if s.lower().startswith("validade:"):
        s = s.split(":", 1)[1].strip()
    try:
        y, m, d = map(int, s.split("-"))
        return date(y, m, d)
    except Exception:
        return None

def print_tabela(insumos):
    """Exibe insumos em formato tabular."""
    if not insumos:
        print("∅ Sem itens.")
        return
    largura_nome = max(len("Insumo"), *(len(n) for n, _, _ in insumos))
    largura_qtd  = max(len("Qtd"), *(len(str(q)) for _, q, _ in insumos))
    largura_val  = max(len("Validade"), *(len(str(v)) for *_, v in insumos))
    cab = f"{'Insumo':<{largura_nome}}  {'Qtd':>{largura_qtd}}  {'Validade':<{largura_val}}"
    print(cab)
    print("-" * len(cab))
    for n, q, v in insumos:
        print(f"{n:<{largura_nome}}  {q:>{largura_qtd}}  {str(v):<{largura_val}}")

def ordenar_por_validade(insumos):
    """Ordena insumos pela data de validade (menor para maior)."""
    return sorted(insumos, key=lambda t: (parse_validade_str(str(t[2])) or date.max))

# ===================== Modelo de Dados =====================
class ControleInsumos:
    """Mantém fila (cronológica) e pilha (recente primeiro) dos consumos."""
    def __init__(self):
        self.fila_consumo = deque()
        self.pilha_consumo = []

    def registrar_consumo(self, insumo):
        self.fila_consumo.append(insumo)
        self.pilha_consumo.append(insumo)

    def mostrar_fila(self):
        return list(self.fila_consumo)

    def mostrar_pilha(self):
        return list(reversed(self.pilha_consumo))

# ===================== Buscas =====================
def busca_sequencial_exata(insumos, alvo_nome):
    alvo = normaliza(alvo_nome)
    passos = 0
    for idx, (nome, qtd, val) in enumerate(insumos):
        passos += 1
        if normaliza(nome) == alvo:
            return (insumos[idx], passos, idx)
    return (None, passos, -1)

def preparar_indice_ordenado_por_nome(insumos):
    pares = [(normaliza(nome), (nome, qtd, val)) for (nome, qtd, val) in insumos]
    pares.sort(key=lambda x: x[0])
    return pares

def busca_binaria_exata(indice_ordenado, alvo_nome):
    alvo = normaliza(alvo_nome)
    esquerda, direita = 0, len(indice_ordenado) - 1
    passos = 0
    while esquerda <= direita:
        passos += 1
        meio = (esquerda + direita) // 2
        chave_meio = indice_ordenado[meio][0]
        if chave_meio == alvo:
            return (indice_ordenado[meio][1], passos, meio)
        if chave_meio < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return (None, passos, -1)

# ===================== Ordenações (exemplos) =====================
def merge_sort(v):
    if len(v) <= 1:
        return v
    m = len(v)//2
    esq = merge_sort(v[:m])
    dir = merge_sort(v[m:])
    return merge(esq, dir)

def merge(esq, dir):
    i = j = 0
    out = []
    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:
            out.append(esq[i]); i += 1
        else:
            out.append(dir[j]); j += 1
    out.extend(esq[i:]); out.extend(dir[j:])
    return out

def quick_sort(v):
    if len(v) <= 1:
        return v
    p = v[0]
    menores = [x for x in v[1:] if x <= p]
    maiores = [x for x in v[1:] if x > p]
    return quick_sort(menores) + [p] + quick_sort(maiores)

# ===================== Entradas Robustas =====================
def solicitar_nome_valido(nomes_validos):
    """Validador robusto que trata colisões de normalização e sugere alternativas."""
    mapa_norm = defaultdict(list)
    for n in nomes_validos:
        mapa_norm[normaliza(n)].append(n)

    opcoes = ", ".join(nomes_validos)
    while True:
        termo = input(f"\n🔎 Digite o NOME do insumo (opções: {opcoes}) ou 'voltar': ").strip()
        if not termo:
            print("❌ Entrada vazia. Tente novamente.")
            continue
        if termo.lower() in ("voltar", "sair", "menu"):
            return None
        if eh_numerico(termo):
            print("❌ O valor não pode ser numérico. Tente novamente.")
            continue
        chave = normaliza(termo)
        if chave in mapa_norm:
            candidatos = mapa_norm[chave]
            if len(candidatos) == 1:
                return candidatos[0]
            print("Vários itens encontrados com esse nome:")
            for i, c in enumerate(candidatos, 1):
                print(f"{i}) {c}")
            while True:
                es = input("Digite o número desejado ou 'voltar': ").strip()
                if es.lower() in ("voltar", "sair", "menu"):
                    break
                if es.isdigit() and 1 <= int(es) <= len(candidatos):
                    return candidatos[int(es)-1]
            continue

        sugestoes = [orig for norm, origs in mapa_norm.items() if chave in norm for orig in origs][:5]
        if sugestoes:
            print("❌ Item não encontrado. Você quis dizer: " + ", ".join(sugestoes) + "?")
        else:
            print("❌ Item não encontrado. Use exatamente um dos nomes listados.")

def solicitar_opcao(msg, opcoes_validas):
    while True:
        escolha = input(msg).strip()
        if escolha in opcoes_validas:
            return escolha
        print("❌ Opção inválida. Tente novamente.")

# ===================== Menus =====================
def menu_busca(controle: ControleInsumos):
    while True:
        print("\n===== MENU DE BUSCA =====")
        print("1) Busca Sequencial (exata)")
        print("2) Busca Binária (exata)")
        print("0) Voltar ao menu principal")
        opc = solicitar_opcao("Escolha uma opção: ", {"1","2","0"})
        if opc == "0":
            return  # volta ao menu principal

        nomes_disponiveis = [n for (n, *_resto) in controle.mostrar_fila()]
        nome = solicitar_nome_valido(nomes_disponiveis)
        if nome is None:
            continue

        if opc == "1":
            item, passos, idx = busca_sequencial_exata(controle.mostrar_fila(), nome)
            if item:
                print(f"\n✅ Sequencial — Encontrado em {passos} passo(s). Índice: {idx}. Item: {item}")
            else:
                print(f"\n🔎 Sequencial — Não encontrado após {passos} passo(s).")
        elif opc == "2":
            indice = preparar_indice_ordenado_por_nome(controle.mostrar_fila())
            item, passos, pos = busca_binaria_exata(indice, nome)
            if item:
                print(f"\n✅ Binária — Encontrado em {passos} passo(s). Posição na lista ordenada: {pos}. Item: {item}")
            else:
                print(f"\n🔎 Binária — Não encontrado após {passos} passo(s).")

def menu_ordenacao(controle: ControleInsumos):
    while True:
        print("\n===== MENU DE ORDENAÇÃO =====")
        print("1) Ordenar quantidades (Merge Sort)")
        print("2) Ordenar quantidades (Quick Sort)")
        print("3) Ordenar por validade")
        print("0) Voltar ao menu principal")
        opc = solicitar_opcao("Escolha uma opção: ", {"1","2","3","0"})
        if opc == "0":
            return
        quantidades = [q for (_n, q, _v) in controle.mostrar_fila()]
        if opc == "1":
            print("→ Quantidades ordenadas (Merge Sort):", merge_sort(quantidades))
        elif opc == "2":
            print("→ Quantidades ordenadas (Quick Sort):", quick_sort(quantidades))
        elif opc == "3":
            print("\n→ Insumos ordenados por validade:")
            print_tabela(ordenar_por_validade(controle.mostrar_fila()))

def menu_principal():
    # Dados simulados
    insumos_simulados = [
        ("Reagente A", 5,  "2026-02-01"),
        ("Seringa",    10, "2027-12-31"),
        ("Reagente B", 7,  "2026-05-10"),
        ("Luvas",      20, "2025-11-20"),
        ("Álcool 70",  12, "2026-08-15"),
    ]
    controle = ControleInsumos()
    for it in insumos_simulados:
        controle.registrar_consumo(it)

    while True:
        print("\n=========== CONTROLE DE INSUMOS ===========")
        print("1) Listar consumo (Fila - cronológica)")
        print("2) Listar consumo (Pilha - inversa)")
        print("3) Buscar insumo")
        print("4) Ordenações")
        print("0) Sair")
        opc = solicitar_opcao("Escolha uma opção: ", {"1","2","3","4","0"})

        if opc == "0":
            print("👋 Saindo. Até mais!")
            break
        elif opc == "1":
            print("\nFila (ordem cronológica):")
            print_tabela(controle.mostrar_fila())
        elif opc == "2":
            print("\nPilha (ordem inversa):")
            print_tabela(controle.mostrar_pilha())
        elif opc == "3":
            menu_busca(controle)
        elif opc == "4":
            menu_ordenacao(controle)

if __name__ == "__main__":
    menu_principal()
