"""
MC Atelier — Guarda-roupa · A Coleção Essencial (versão enxuta)
"""
import streamlit as st
import components as C
import data as D


CATEGORIAS = ["Blazers", "Camisas", "Calças", "Casacos", "Malhas",
              "Calçados", "Vestidos", "Acessórios"]
OCASIOES   = ["Negócios", "Câmera", "Dia a dia", "Evento", "Criativo"]


def render():
    C.topbar()
    resumo = D.resumo_guarda_roupa()

    C.sec_header(
        "A Coleção Essencial",
        subtitle="Sua cápsula — poucas peças de qualidade que geram muitos looks.",
    )

    # ── Filtro enxuto no topo ────────────────────────────────────
    f1, f2, f3 = st.columns([1.3, 1.3, 2], gap="medium")
    cat_sel = f1.selectbox("Categoria", ["Todas"] + CATEGORIAS)
    occ_sel = f2.selectbox("Ocasião", ["Todas"] + OCASIOES)
    f3.markdown(
        f'<div style="padding-top:26px;text-align:right;" class="eyebrow">'
        f'{resumo["total"]} peças · {resumo["essenciais"]} essenciais</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # ── Grade ────────────────────────────────────────────────────
    gr = st.session_state.guarda_roupa
    if cat_sel != "Todas":
        gr = [p for p in gr if p["categoria"] == cat_sel]
    if occ_sel != "Todas":
        gr = [p for p in gr if p["ocasiao"] in (occ_sel, "Todas")]

    if not gr:
        st.markdown('<div style="color:var(--faint);font-style:italic;padding:24px 0;">Nenhuma peça com esses filtros.</div>',
                    unsafe_allow_html=True)

    for start in range(0, len(gr), 4):
        cols = st.columns(4, gap="medium")
        for col, peca in zip(cols, gr[start:start+4]):
            with col:
                _garment(peca)

    # ── Adicionar peça (recolhido) ───────────────────────────────
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
    with st.expander("＋  Adicionar nova peça"):
        with st.form("add_peca", clear_on_submit=True):
            a, b, c = st.columns(3)
            nome  = a.text_input("Nome da peça")
            marca = b.text_input("Marca", value="—")
            cat   = c.selectbox("Categoria", CATEGORIAS)
            d, e, f = st.columns(3)
            cor = d.text_input("Cor")
            oca = e.selectbox("Ocasião", OCASIOES + ["Todas"])
            ess = f.checkbox("Essencial da cápsula")
            if st.form_submit_button("Adicionar à coleção"):
                if nome.strip():
                    nid = max([p["id"] for p in st.session_state.guarda_roupa], default=0) + 1
                    st.session_state.guarda_roupa.append({
                        "id": nid, "categoria": cat, "marca": marca.strip() or "—",
                        "nome": nome.strip(), "cor": cor.strip() or "—", "tone": "#3a3c40",
                        "ocasiao": oca, "essencial": ess,
                    })
                    st.rerun()


def _garment(peca):
    badge = "Essencial" if peca["essencial"] else ""
    st.markdown(f"""
    <div>
      {C.tile(peca['tone'], mono=peca['nome'][:1].upper(), badge=badge)}
      <div class="g-brand">{peca['marca']}</div>
      <div class="g-name">{peca['nome']}</div>
      <div style="font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
           color:var(--gold);margin-top:8px;">{peca['cor']}</div>
    </div>
    """, unsafe_allow_html=True)
