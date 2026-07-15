"""
MC Atelier — Camada de dados (session_state + persistência JSON)
Conteúdo personalizado: assessora de investimentos, trabalho híbrido,
estilo clássico/casual com autoridade, baixinha + quadril largo,
coloração quente, orçamento até ~R$300 por peça.
"""
import streamlit as st
import store


# ---------------------------------------------------------------------------
# Perfil de estilo — "Clássica Descomplicada"
# ---------------------------------------------------------------------------

def _init_perfil():
    return {
        "_v": 2,  # versão do perfil (bump força atualização do conteúdo padrão)
        "arquetipo":     "Clássica Descomplicada",
        "arquetipo_sub": "Elegância sem esforço · Outono Quente",
        "manifesto": (
            "Você é Outono Quente: subtono dourado e quente. Base em neutros quentes "
            "(camel, cru, caramelo) que iluminam a sua pele, cortes de cintura alta que "
            "respeitam a sua altura e o seu quadril, e peças que funcionam no dia híbrido — "
            "do cliente à bike. Elegância sem esforço e sem gastar muito."
        ),
        "citacao": "Menos peças, melhor combinadas. Autoridade está no caimento, não no preço.",

        # Coloração (análise Warm Autumn)
        "estacao": "Outono Quente (Warm Autumn)",
        "subtono": "Quente dourado · neutro-quente",
        "metais":  "Ouro, ouro rosé e bronze — evite prata e platina.",

        # Paleta Warm Autumn — (nome, hex, descrição)
        "paleta": [
            ("Camel",         "#b98a5e", "Sua cor principal. Warm beige que realça o seu glow dourado."),
            ("Off-white / Cru","#ece6da", "Use no lugar do branco gelado — mais quente e favorável."),
            ("Caramelo",      "#a5673f", "Quente e rico, ótimo pro dia a dia com elegância."),
            ("Verde-oliva",   "#6b6f3a", "Terroso e naturalmente harmônico com o seu tom."),
            ("Marinho",       "#26314a", "Âncora de autoridade que complementa o seu subtono."),
            ("Deep Teal",     "#1f5c57", "Seu acento perfeito — profundidade e sofisticação sem te apagar."),
        ],
        "evitar_cores": ["Preto puro (colado no rosto)", "Cinza-carvão", "Azul elétrico",
                         "Lavanda fria", "Pink / fúcsia", "Neons"],
        "combinacoes": [
            ("Monocromático quente", ["#b98a5e", "#ece6da", "#a5673f"]),
            ("Terroso",              ["#6b6f3a", "#9c4a2f", "#d8c3a5"]),
            ("Pop elegante",         ["#26314a", "#b98a5e", "#1f5c57"]),
        ],

        # Caimento — regras para baixinha + quadril mais largo (título, desc)
        "caimento": [
            ("Cintura sempre alta",            "Marca seu ponto mais fino e alonga a perna — regra de ouro pra baixinha."),
            ("Coluna de uma cor só",           "Cima e baixo no mesmo tom criam uma linha contínua que estica a silhueta."),
            ("Blazer curto, não longo",        "Blazer na altura do quadril ou mais curto valoriza; o longo encurta você."),
            ("Estrutura em cima, fluidez calculada embaixo", "Ombro definido equilibra o quadril; calça reta/wide que só resvala, sem volume demais."),
            ("Meio-tucado",                    "Prender a frente da blusa marca a cintura e organiza o look — adeus sensação de 'bagunçado'."),
            ("Bico fino alonga; tênis branco mantém autoridade", "Sandália/scarpin nude estica a perna; no dia de bike, tênis branco de couro limpo não perde a seriedade."),
        ],

        # Regras práticas — mandamentos / proibições
        "mandamentos": [
            ("Compre pensando em 3 looks", "Só entra peça que combina com pelo menos 3 que você já tem."),
            ("Ajuste na costureira",       "R$20 de bainha resolve 80% da sensação de caimento ruim."),
            ("Neutro quente como base",    "Camel, cru, chocolate e marinho já se combinam entre si sozinhos."),
        ],
        "proibicoes": [
            ("Comprimento errado de calça", "Calça que arrasta no chão ou corta no tornozelo encurta a perna."),
            ("Largo em cima E embaixo",     "Volume dos dois lados apaga a cintura — escolha um só."),
            ("Impulso fora da paleta",      "A peça 'linda' que não combina com nada vira dinheiro parado no armário."),
        ],

        # Pilares de autoridade — (nome, descrição, completo)
        "pilares": [
            ("Caimento",        "O ajuste certo pro seu corpo vale mais que a marca. Bainha, cintura e comprimento no ponto.", True),
            ("Cores quentes",   "Camel, cru, chocolate e marinho iluminam sua pele e combinam entre si.",                      True),
            ("Versatilidade",   "Peças que vão do cliente à bike sem trocar de identidade.",                                  False),
            ("Autoridade casual","Como ficar séria de tênis: alfaiataria + tênis branco + um bom acessório.",                 True),
        ],
        "maturity": 70,

        # Checklist rápido antes de sair
        "checklist": [
            ("Cintura marcada?",     "Meio-tuck ou cintura alta no lugar."),
            ("Uma cor dominante?",   "Coluna monocromática ou base neutra + 1 acento."),
            ("Comprimento certo?",   "Calça resvalando o chão, blazer no quadril."),
            ("Sapato alonga?",       "Bico fino/nude — ou tênis branco limpo no dia casual."),
            ("Um ponto de brilho?",  "Colar ou brinco dourado — um só."),
        ],

        # Ocasiões — (ocasião, look, evitar)
        "ocasioes": [
            ("Cliente presencial",       "Blazer camel curto + blusa lisa + calça marinho cintura alta + sandália nude.", "Blazer longo, calça que arrasta."),
            ("Reunião online",           "Cor sólida quente no busto (camel, vinho, azul) + colar dourado. Enquadramento limpo.", "Estampa miúda e branco puro que estoura na luz."),
            ("Casual com autoridade (bike)","Suéter/blusa + calça marrom cintura alta + tênis branco + jaqueta estruturada.", "Moletom largo, tênis esportivo colorido."),
            ("Escritório com parceiros", "Bomber ou blazer + top camel + calça alfaiataria + cinto marcando a cintura.", "Excesso de camadas largas."),
        ],
    }


# ---------------------------------------------------------------------------
# Guarda-roupa — peças reais (das suas fotos)
# ---------------------------------------------------------------------------

def _init_guarda_roupa():
    return [
        {"id": 1,  "categoria": "Blazers",    "marca": "—", "nome": "Blazer camel",            "cor": "Camel",           "tone": "#b98a5e", "ocasiao": "Negócios",  "essencial": True,  "foto": ""},
        {"id": 2,  "categoria": "Camisas",    "marca": "—", "nome": "Blusa azul-serenidade",   "cor": "Azul-serenidade", "tone": "#a9c3e0", "ocasiao": "Câmera",    "essencial": True,  "foto": ""},
        {"id": 3,  "categoria": "Calças",     "marca": "—", "nome": "Calça wide marinho",      "cor": "Marinho",         "tone": "#26314a", "ocasiao": "Negócios",  "essencial": True,  "foto": ""},
        {"id": 4,  "categoria": "Calçados",   "marca": "—", "nome": "Sandália nude de tiras",  "cor": "Nude",            "tone": "#d8c3a5", "ocasiao": "Todas",     "essencial": True,  "foto": ""},
        {"id": 5,  "categoria": "Camisas",    "marca": "—", "nome": "Top marrom cavado",       "cor": "Chocolate",       "tone": "#5a4433", "ocasiao": "Evento",    "essencial": False, "foto": ""},
        {"id": 6,  "categoria": "Calças",     "marca": "—", "nome": "Calça preta cropped",     "cor": "Preto",           "tone": "#1c1c1c", "ocasiao": "Negócios",  "essencial": True,  "foto": ""},
        {"id": 7,  "categoria": "Casacos",    "marca": "—", "nome": "Jaqueta de couro preta",  "cor": "Preto",           "tone": "#17171a", "ocasiao": "Criativo",  "essencial": True,  "foto": ""},
        {"id": 8,  "categoria": "Acessórios", "marca": "—", "nome": "Colar dourado c/ pingente","cor": "Dourado",        "tone": "#c9a24a", "ocasiao": "Todas",     "essencial": True,  "foto": ""},
        {"id": 9,  "categoria": "Malhas",     "marca": "—", "nome": "Suéter canelado camel",   "cor": "Camel",           "tone": "#c39b6e", "ocasiao": "Dia a dia", "essencial": True,  "foto": ""},
        {"id": 10, "categoria": "Calças",     "marca": "—", "nome": "Calça marrom alfaiataria","cor": "Marrom",          "tone": "#6a5140", "ocasiao": "Dia a dia", "essencial": True,  "foto": ""},
        {"id": 11, "categoria": "Casacos",    "marca": "—", "nome": "Bomber creme",            "cor": "Creme",           "tone": "#e4dcc7", "ocasiao": "Criativo",  "essencial": False, "foto": ""},
        {"id": 12, "categoria": "Acessórios", "marca": "—", "nome": "Cinto de fivela dourada", "cor": "Caramelo",        "tone": "#7a5a3a", "ocasiao": "Todas",     "essencial": True,  "foto": ""},
    ]


# ---------------------------------------------------------------------------
# Looks — dos seus dias reais
# ---------------------------------------------------------------------------

def _init_looks():
    return [
        {"id": 1, "nome": "Dia de Cliente", "ocasiao": "Cliente presencial", "nivel": "Clássico · Autoridade",
         "descricao": "Blazer camel curto sobre blusa lisa, calça marinho de cintura alta e sandália nude. Seu neutro-poder no comando.",
         "pecas": ["Blazer camel", "Blusa azul-serenidade", "Calça wide marinho", "Sandália nude de tiras"]},
        {"id": 2, "nome": "Câmera Pronta", "ocasiao": "Reunião online", "nivel": "Do busto pra cima, impecável",
         "descricao": "Cor sólida quente no busto e um colar dourado como ponto focal. Simples e eficaz na tela.",
         "pecas": ["Suéter canelado camel", "Colar dourado c/ pingente"]},
        {"id": 3, "nome": "Séria de Tênis", "ocasiao": "Casual com autoridade (bike)", "nivel": "Casual · Autoridade",
         "descricao": "O dia de bike sem perder a seriedade: alfaiataria de cintura alta + tênis branco limpo + jaqueta estruturada.",
         "pecas": ["Suéter canelado camel", "Calça marrom alfaiataria", "Jaqueta de couro preta"]},
        {"id": 4, "nome": "Parceiros no Escritório", "ocasiao": "Escritório com parceiros", "nivel": "Casual estruturado",
         "descricao": "Camada estruturada por cima, cintura marcada e um detalhe dourado. Autoridade descontraída.",
         "pecas": ["Bomber creme", "Calça marrom alfaiataria", "Cinto de fivela dourada"]},
    ]


# ---------------------------------------------------------------------------
# Lista de compras — lacunas úteis, até ~R$300
# ---------------------------------------------------------------------------

def _init_compras():
    return [
        {"id": 1, "item": "Calça alfaiataria reta cintura alta (preta ou marinho)", "prioridade": "Alta",
         "motivo": "A base coringa que falta: alonga a perna, marca a cintura e vai do cliente ao escritório.",
         "tags": [("Custo por uso", "Baixo"), ("Onde", "Renner / Amaro")], "preco": 249.0, "tone": "#26314a", "comprado": False},
        {"id": 2, "item": "Blazer curto estruturado (camel ou marinho)", "prioridade": "Alta",
         "motivo": "Curto no quadril valoriza a sua altura; camel ilumina. Autoridade instantânea sobre qualquer look.",
         "tags": [("Caimento", "Comprimento no quadril"), ("Onde", "C&A / Zara")], "preco": 300.0, "tone": "#b98a5e", "comprado": False},
        {"id": 3, "item": "Tênis branco de couro minimalista", "prioridade": "Alta",
         "motivo": "Para os dias de bike sem perder a seriedade. Couro liso, cano baixo, sem logo grande.",
         "tags": [("Versatilidade", "9/10"), ("Onde", "Vizzano / Renner")], "preco": 250.0, "tone": "#ededed", "comprado": False},
        {"id": 4, "item": "Scarpin ou mule bico fino nude (salto médio)", "prioridade": "Média",
         "motivo": "Alonga a perna e combina com tudo. Salto médio pra aguentar o dia inteiro.",
         "tags": [("Alonga", "Sim"), ("Onde", "Vizzano / Beira Rio")], "preco": 200.0, "tone": "#d8c3a5", "comprado": False},
        {"id": 5, "item": "Blusa lisa de cor sólida p/ câmera (azul ou cru)", "prioridade": "Média",
         "motivo": "Cor cheia no busto rende na reunião online. Tecido firme que não amassa.",
         "tags": [("Câmera", "Cor sólida"), ("Onde", "Hering / Renner")], "preco": 130.0, "tone": "#a9c3e0", "comprado": False},
        {"id": 6, "item": "Cinto marrom/caramelo para marcar cintura", "prioridade": "Baixa",
         "motivo": "O truque anti-'bagunçado': define a cintura na hora e organiza o look.",
         "tags": [("Truque", "Meio-tuck"), ("Onde", "Renner")], "preco": 90.0, "tone": "#7a5a3a", "comprado": False},
    ]


def _init_semana():
    """Plano da semana — cada dia aponta para um look (look_id) ou fica livre."""
    return [
        {"dia": "SEG", "ocasiao": "Escritório",       "tag": "Parceiros",         "clima": "sol",   "look_id": 4},
        {"dia": "TER", "ocasiao": "Reunião online",   "tag": "Câmera pronta",     "clima": "sol",   "look_id": 2},
        {"dia": "QUA", "ocasiao": "Casual · bike",    "tag": "Autoridade casual", "clima": "nuvem", "look_id": 3},
        {"dia": "QUI", "ocasiao": "Cliente",          "tag": "Apresentação",      "clima": "sol",   "look_id": 1},
        {"dia": "SEX", "ocasiao": "Business casual",  "tag": "Happy hour",        "clima": "sol",   "look_id": 4},
        {"dia": "SÁB", "ocasiao": "Evento social",    "tag": "Lazer curado",      "clima": "sol",   "look_id": None},
        {"dia": "DOM", "ocasiao": "Descanso",         "tag": "Doméstico",         "clima": "nuvem", "look_id": None},
    ]


def _init_sugestoes():
    return [
        ("Tênis branco de couro", "Autoridade casual", "#ededed"),
        ("Scarpin nude bico fino", "Alonga a perna",   "#d8c3a5"),
    ]


def _init_agenda():
    return [
        {"hora": "09:00", "titulo": "Reunião com parceiros", "meta": "Escritório · Autoridade casual"},
        {"hora": "11:30", "titulo": "Call com cliente",      "meta": "Online · Câmera pronta"},
        {"hora": "15:00", "titulo": "Reunião presencial",    "meta": "Cliente · Clássico"},
    ]


def _look_of_day():
    return {
        "titulo":    "Dia de Cliente",
        "descricao": "Blazer camel curto sobre blusa lisa, calça marinho de cintura alta e "
                     "sandália nude. Autoridade clássica com o seu neutro-poder.",
        "detalhes": [
            ("Caimento",     "Blazer no quadril e calça cintura alta alongam a silhueta."),
            ("Cor",          "Camel ilumina a sua pele; marinho ancora com autoridade."),
            ("Ponto focal",  "Um brinco ou colar dourado — nada além disso."),
        ],
    }


# ---------------------------------------------------------------------------
# Init + persistência
# ---------------------------------------------------------------------------

_FACTORIES = {
    "perfil":       _init_perfil,
    "guarda_roupa": _init_guarda_roupa,
    "looks":        _init_looks,
    "compras":      _init_compras,
    "sugestoes":    _init_sugestoes,
    "agenda":       _init_agenda,
    "look_of_day":  _look_of_day,
    "semana":       _init_semana,
}


def init_state():
    # Carrega do armazenamento apenas uma vez por sessão (evita ler a nuvem
    # a cada rerun). Depois, o estado vive em st.session_state.
    if not st.session_state.get("_loaded"):
        saved = store.load()
        precisa_salvar = False
        for key, factory in _FACTORIES.items():
            if saved.get(key):
                st.session_state[key] = saved[key]
            else:
                st.session_state[key] = factory()
                precisa_salvar = True
        # Perfil: se a versão mudou, atualiza o conteúdo padrão (paleta etc.);
        # senão, apenas completa chaves faltantes. Guarda-roupa/fotos ficam intactos.
        base = _init_perfil()
        cur = st.session_state.get("perfil")
        if not isinstance(cur, dict) or cur.get("_v") != base.get("_v"):
            st.session_state["perfil"] = base
            precisa_salvar = True
        else:
            st.session_state["perfil"] = {**base, **cur}
        st.session_state["_loaded"] = True
        if precisa_salvar:
            persist()

    if "pagina" not in st.session_state:
        st.session_state.pagina = "Dashboard"


def persist():
    """Grava o estado atual no arquivo JSON."""
    data = {k: st.session_state[k] for k in store.KEYS if k in st.session_state}
    store.save(data)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resumo_guarda_roupa() -> dict:
    gr = st.session_state.guarda_roupa
    cats = {}
    for p in gr:
        cats[p["categoria"]] = cats.get(p["categoria"], 0) + 1
    return {
        "total": len(gr),
        "categorias": cats,
        "essenciais": sum(1 for p in gr if p["essencial"]),
        "cores": len({p["cor"] for p in gr}),
        "com_foto": sum(1 for p in gr if p.get("foto")),
    }


def total_compras() -> float:
    return sum(c["preco"] for c in st.session_state.compras if not c["comprado"])


def look_by_id(look_id):
    """Retorna o look com o id informado, ou None."""
    if look_id is None:
        return None
    for lk in st.session_state.looks:
        if lk["id"] == look_id:
            return lk
    return None


def tone_for(nome: str) -> str:
    """Cor (tone) da peça pelo nome; neutro se não encontrar."""
    for p in st.session_state.guarda_roupa:
        if p["nome"] == nome:
            return p.get("tone", "#3a3c40")
    return "#3a3c40"


def emergencia() -> dict:
    """Look à prova de erro, montado só com peças que ela já tem."""
    return {
        "titulo": "Camel Descomplicado",
        "pecas":  ["Suéter canelado camel", "Calça marrom alfaiataria", "Sandália nude de tiras"],
        "razoes": [
            "Coluna quente monocromática — alonga a silhueta na hora.",
            "Zero decisão: pega e veste nos dias corridos, sem errar.",
        ],
        "custo": "R$ 0 (já é seu)",
    }
