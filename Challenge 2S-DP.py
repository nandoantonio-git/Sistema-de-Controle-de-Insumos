from collections import deque
import unicodedata

def normaliza(s: str) -> str:
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

class ControleInsumos:
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


def solicitar_nome_valido(nomes_validos):
    mapa_norm = {normaliza(n): n for n in nomes_validos}
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
            return mapa_norm[chave]

        sugestoes = [orig for norm, orig in mapa_norm.items() if chave in norm][:5]
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
        print("0) Voltar ao menu principal")
        opc = solicitar_opcao("Escolha uma opção: ", {"1","2","0"})
        if opc == "0":
            return
        quantidades = [q for (_n, q, _v) in controle.mostrar_fila()]
        if opc == "1":
            print("→ Quantidades ordenadas (Merge Sort):", merge_sort(quantidades))
        elif opc == "2":
            print("→ Quantidades ordenadas (Quick Sort):", quick_sort(quantidades))

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
            print("Fila (ordem cronológica):", controle.mostrar_fila())
        elif opc == "2":
            print("Pilha (ordem inversa):   ", controle.mostrar_pilha())
        elif opc == "3":
            menu_busca(controle)
        elif opc == "4":
            menu_ordenacao(controle)

if __name__ == "__main__":
    menu_principal()
