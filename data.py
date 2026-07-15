"""
MC Atelier — Camada de dados (in-memory com session_state)
Perfil de estilo, guarda-roupa, looks e lista de compras estratégica.
Conteúdo baseado nas telas "Atelier Digital" (Google Stitch).
"""
import streamlit as st


# ---------------------------------------------------------------------------
# Perfil de estilo — arquétipo "Elegância Atemporal / Estratégica"
# ---------------------------------------------------------------------------

def _init_perfil():
    return {
        "arquetipo":     "Elegância Estratégica",
        "arquetipo_sub": "Clássica refinada · quiet luxury",
        "manifesto": (
            "Meu estilo não é uma reação a tendências, mas uma declaração de intenção. "
            "Cada peça é escolhida por sua integridade arquitetônica, sua conversa com o meu "
            "legado e sua capacidade de fortalecer a mulher profissional através de precisão curada."
        ),
        "citacao": "O estilo é um ativo estratégico. Use com intenção.",

        # Paleta curada — (nome, hex, descrição)
        "paleta": [
            ("Preto Obsidiana", "#0a0a0a", "Fundação da autoridade. Alfaiataria e couro que ancoram a silhueta."),
            ("Off-white",       "#f2efe8", "Neutro de alto contraste. Ideal para blusas de seda e camisaria estruturada."),
            ("Cinza Ardósia",   "#3e434c", "O tom-ponte. Essencial para malhas e casacos, adiciona dimensão suave."),
            ("Champagne",       "#e0b25f", "Só como acento. Reservado para hardware, joias e forros de seda."),
            ("Marinho Noturno", "#5f6d88", "A alternativa suave ao preto. Perfeito para casacos de lã e tecidos pesados."),
        ],

        # Silhuetas principais — (nome, descrição)
        "silhuetas": [
            ("O Blazer Arquitetônico", "Ombros como fundação. Lapelas marcadas e cintura ajustada criam um perfil de comando."),
            ("Proporção Fluida",       "Calças de cintura alta com volume, equilibradas por tops ajustados para presença estatuária."),
        ],

        # Mandamentos / Proibições — (título, descrição)
        "mandamentos": [
            ("Profundidade Monocromática", "Misture texturas (seda, lã, couro) na mesma família de cor para criar interesse sem poluição."),
            ("Integridade Estrutural",     "Cada peça deve manter a forma. Priorize tecidos encorpados que projetam permanência."),
            ("Luxo Invisível",             "Foco em alfaiataria perfeita e botões de qualidade, acima de marca visível ou logos."),
        ],
        "proibicoes": [
            ("Tendências Efêmeras",     "Evite silhuetas ou cores 'fast fashion' que serão irreconhecíveis em seis meses."),
            ("Excesso de Ornamentação", "Descarte babados, paetês ou estampas que competem com o foco no rosto."),
            ("Bases Mal Ajustadas",     "Nunca aceite 'de prateleira' sem ajuste. Caimento ruim é falha de estratégia."),
        ],

        # Pilares de autoridade — (nome, descrição, completo)
        "pilares": [
            ("Caimento",   "Alfaiataria precisa como fundação do respeito. A silhueta deve comunicar estrutura e intenção.", True),
            ("Cores",      "Paletas estratégicas que comandam atenção sem gritar. Marinho, carvão e champagne.",            True),
            ("Acessórios", "Os 5% finais que definem o todo. Qualidade acima de quantidade. Peças minimalistas de luxo.",   False),
            ("Mensagem",   "Sinalização psicológica através de textura e corte. Uma narrativa de confiabilidade e sucesso.", True),
        ],
        "maturity": 75,

        # Padrões de acessórios (detalhe do pilar) — (título, descrição)
        "padroes_acessorios": [
            ("A Regra do Relógio",  "Prefira mecanismos de qualidade com caixa proporcional ao pulso. Couro para formalidade, aço para versatilidade."),
            ("Coesão de Metais",    "Todo hardware (relógio, fivela, brincos) deve combinar em tom. Champagne é uma alternativa quente ao prata."),
            ("Qualidade Funcional", "Todo acessório deve ter propósito. Evite peças puramente decorativas que poluem a silhueta limpa."),
        ],

        # Checklist rápido antes de sair
        "checklist": [
            ("Caimento",    "Ombro no lugar, barra certa, nada sobrando no corpo."),
            ("Paleta",      "Dentro das cores curadas, no máximo 3 peças coloridas."),
            ("Ponto focal", "Um destaque por look — o resto permanece neutro."),
            ("Acabamento",  "Sapato limpo, sem fio solto, sem amassado."),
            ("Contexto",    "O look conversa com a ocasião de hoje?"),
        ],

        # Ocasiões — (ocasião, look, evitar)
        "ocasioes": [
            ("Reunião / negócios",  "Alfaiataria completa em marinho ou carvão, blusa de seda, base impecável.", "Cores fortes, casual demais."),
            ("Câmera / conteúdo",   "Cores sólidas e quentes (camel, cru, champagne); contraste com o fundo.",   "Branco puro e xadrez fino que tremem na tela."),
            ("Criativo / dia a dia","A mesma cápsula em modo relaxado: tricô de qualidade + calça reta + mocassim.","Peças 'de qualquer jeito' sem estrutura."),
            ("Evento / networking", "Uma peça-statement na paleta sobre base neutra impecável.",                 "Improviso de última hora."),
        ],
    }


# ---------------------------------------------------------------------------
# Guarda-roupa — A Coleção Essencial
# ---------------------------------------------------------------------------

def _init_guarda_roupa():
    return [
        {"id": 1, "categoria": "Blazers",   "marca": "Atelier Sartorial", "nome": "Blazer de Lã Estruturado",  "cor": "Marinho Meia-noite", "tone": "#1c2a3a", "ocasiao": "Negócios",  "essencial": True},
        {"id": 2, "categoria": "Camisas",   "marca": "Linen & Co.",       "nome": "Camisa Oxford Clássica",    "cor": "Branco Puro",        "tone": "#e9e6df", "ocasiao": "Negócios",  "essencial": True},
        {"id": 3, "categoria": "Calças",    "marca": "Modern Tailor",     "nome": "Calça de Lã Slim",          "cor": "Carvão",             "tone": "#3e434c", "ocasiao": "Negócios",  "essencial": True},
        {"id": 4, "categoria": "Casacos",   "marca": "Legacy Outerwear",  "nome": "Sobretudo de Camelo",       "cor": "Tabaco",             "tone": "#a9855f", "ocasiao": "Negócios",  "essencial": True},
        {"id": 5, "categoria": "Camisas",   "marca": "Atelier Sartorial", "nome": "Camisa Dobby Business",     "cor": "Azul Céu",           "tone": "#8ea3c0", "ocasiao": "Câmera",    "essencial": False},
        {"id": 6, "categoria": "Calças",    "marca": "Modern Tailor",     "nome": "Calça Formal de Noite",     "cor": "Preto Meia-noite",   "tone": "#141414", "ocasiao": "Evento",    "essencial": False},
        {"id": 7, "categoria": "Malhas",    "marca": "Casa di Lana",      "nome": "Tricô de Cashmere",         "cor": "Off-white",          "tone": "#e2ddd2", "ocasiao": "Dia a dia", "essencial": True},
        {"id": 8, "categoria": "Calçados",  "marca": "Heritage Shoes",    "nome": "Mocassim de Couro",         "cor": "Café",               "tone": "#4a382c", "ocasiao": "Dia a dia", "essencial": True},
        {"id": 9, "categoria": "Acessórios","marca": "Maison Cuir",       "nome": "Bolsa Estruturada",         "cor": "Camel",              "tone": "#a9855f", "ocasiao": "Todas",     "essencial": True},
        {"id": 10,"categoria": "Vestidos",  "marca": "Atelier Sartorial", "nome": "Vestido Reto Midi",         "cor": "Marinho",            "tone": "#1c2a3a", "ocasiao": "Evento",    "essencial": False},
        {"id": 11,"categoria": "Acessórios","marca": "Horloge",           "nome": "Relógio Minimalista",       "cor": "Champagne",          "tone": "#c9a24a", "ocasiao": "Todas",     "essencial": False},
        {"id": 12,"categoria": "Malhas",    "marca": "Casa di Lana",      "nome": "Blazer de Tricô",           "cor": "Bordô",              "tone": "#6f2530", "ocasiao": "Criativo",  "essencial": False},
    ]


# ---------------------------------------------------------------------------
# Looks montados
# ---------------------------------------------------------------------------

def _init_looks():
    return [
        {"id": 1, "nome": "A Monocromática Estratégica", "ocasiao": "Negócios", "nivel": "Alto impacto · Formal",
         "descricao": "Uma aula de textura e silhueta. Alfaiataria em tons de cinza que projeta autoridade silenciosa.",
         "pecas": ["Blazer de Lã Estruturado", "Calça de Lã Slim", "Mocassim de Couro"]},
        {"id": 2, "nome": "Camel & Cru", "ocasiao": "Câmera", "nivel": "Semiformal · Texturas",
         "descricao": "Neutros quentes que iluminam na tela sem estourar. Ideal para gravação e conteúdo.",
         "pecas": ["Sobretudo de Camelo", "Camisa Oxford Clássica", "Calça de Lã Slim"]},
        {"id": 3, "nome": "Cápsula Relaxada", "ocasiao": "Dia a dia", "nivel": "Elegância casual",
         "descricao": "A base da semana: qualidade sem esforço aparente.",
         "pecas": ["Tricô de Cashmere", "Calça de Lã Slim", "Mocassim de Couro"]},
        {"id": 4, "nome": "Statement Discreto", "ocasiao": "Evento", "nivel": "Casual elegante · Peça-statement",
         "descricao": "Um único ponto de cor sobre base neutra impecável.",
         "pecas": ["Blazer de Tricô", "Calça Formal de Noite", "Bolsa Estruturada"]},
    ]


# ---------------------------------------------------------------------------
# Lista de compras estratégica (lacunas do cápsula)
# ---------------------------------------------------------------------------

def _init_compras():
    return [
        {"id": 1, "item": "Blazer Azul Marinho Estruturado", "prioridade": "Alta",
         "motivo": "Peça fundamental para reuniões de alta importância. A cor navy projeta confiança e estabilidade, enquanto o corte estruturado reforça a silhueta de autoridade.",
         "tags": [("Custo por uso", "Baixo"), ("Versatilidade", "9/10")],
         "preco": 1800.0, "tone": "#1c2a3a", "comprado": False},
        {"id": 2, "item": "Sapato Oxford Café", "prioridade": "Média",
         "motivo": "Completa o traje formal com elegância discreta. O tom café é mais versátil que o preto para transições do dia para a noite.",
         "tags": [("Custo por uso", "Médio"), ("Qualidade", "Herança")],
         "preco": 1200.0, "tone": "#4a382c", "comprado": False},
        {"id": 3, "item": "Camisa Branca de Popeline", "prioridade": "Alta",
         "motivo": "Item de giro rápido essencial. Substituição necessária para manter o aspecto impecável e o 'frescor' da imagem pessoal.",
         "tags": [("Custo por uso", "Mínimo"), ("Checklist", "Algodão egípcio")],
         "preco": 450.0, "tone": "#e9e6df", "comprado": False},
    ]


def _init_sugestoes():
    return [
        ("Relógio Minimalista 'Ares'", "Especial para o seu perfil", "#232323"),
        ("Óculos de Sol 'Persona'",    "Acessório de transição",     "#3a3c40"),
    ]


def _init_agenda():
    return [
        {"hora": "09:00", "titulo": "Reunião de diretoria",  "meta": "Alto impacto · Formal"},
        {"hora": "13:30", "titulo": "Almoço de estratégia",  "meta": "Semiformal · Texturas"},
        {"hora": "19:00", "titulo": "Abertura de exposição", "meta": "Elegância casual · Statement"},
    ]


def _look_of_day():
    return {
        "titulo":    "A Monocromática Estratégica",
        "descricao": "Uma aula de textura e silhueta. Lã em tons de cinza encontra couro polido "
                     "num conjunto que irradia autoridade silenciosa.",
        "detalhes": [
            ("Caimento",         "Ombro estruturado com leve afunilamento na cintura. Alfaiataria precisa."),
            ("Harmonia de cor",  "Cinzas tonais dão profundidade sem a dureza do preto puro."),
            ("Foco no acessório","Relógio minimalista. Um único ponto de brilho."),
        ],
    }


# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------

def init_state():
    defaults = {
        "perfil":       _init_perfil,
        "guarda_roupa": _init_guarda_roupa,
        "looks":        _init_looks,
        "compras":      _init_compras,
        "sugestoes":    _init_sugestoes,
        "agenda":       _init_agenda,
        "look_of_day":  _look_of_day,
    }
    for key, factory in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = factory()
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Dashboard"


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
    }


def total_compras() -> float:
    return sum(c["preco"] for c in st.session_state.compras if not c["comprado"])
