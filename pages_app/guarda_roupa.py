"""
MC Atelier — Guarda-roupa · A Coleção Essencial (com fotos reais)
"""
import streamlit as st
import components as C
import data as D
import store


CATEGORIAS = ["Blazers", "Camisas", "Calças", "Casacos", "Malhas",
              "Calçados", "Vestidos", "Acessórios"]
OCASIOES   = ["Negócios", "Câmera", "Dia a dia", "Evento", "Criativo"]


def render():
    C.topbar()
    resumo = D.resumo_guarda_roupa()

    C.sec_header(
        "A Coleção Essencial",
        subtitle="Suas peças reais — cadastre com foto e monte looks a partir do que você já tem.",
    )

    # ── Filtro enxuto ────────────────────────────────────────────
    f1, f2, f3 = st.columns([1.3, 1.3, 2], gap="medium")
    cat_sel = f1.selectbox("Categoria", ["Todas"] + CATEGORIAS)
    occ_sel = f2.selectbox("Ocasião", ["Todas"] + OCASIOES)
    f3.markdown(
        f'<div style="padding-top:26px;text-align:right;" class="eyebrow">'
        f'{resumo["total"]} peças · {resumo["com_foto"]} com foto</div>',
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

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    # ── Adicionar peça (com foto) ────────────────────────────────
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
            foto = st.file_uploader("Foto da peça (opcional)", type=["png", "jpg", "jpeg", "webp"])
            if st.form_submit_button("Adicionar à coleção"):
                if nome.strip():
                    nid = max([p["id"] for p in st.session_state.guarda_roupa], default=0) + 1
                    st.session_state.guarda_roupa.append({
                        "id": nid, "categoria": cat, "marca": marca.strip() or "—",
                        "nome": nome.strip(), "cor": cor.strip() or "—", "tone": "#3a3c40",
                        "ocasiao": oca, "essencial": ess,
                        "foto": store.encode_image(foto) if foto else "",
                    })
                    D.persist()
                    st.rerun()

    # ── Gerenciar fotos / remover ────────────────────────────────
    with st.expander("🖼️  Adicionar fotos às peças / remover"):
        st.markdown('<div class="sec-sub" style="margin-bottom:14px;">'
                    'Envie a foto real de cada peça — ela substitui o quadradinho na grade.</div>',
                    unsafe_allow_html=True)
        for peca in st.session_state.guarda_roupa:
            cols = st.columns([2.4, 2.2, 1], gap="small")
            tem = "✓ com foto" if peca.get("foto") else "sem foto"
            cols[0].markdown(
                f'<div style="padding-top:6px;font-size:13px;">'
                f'<b>{peca["nome"]}</b><br><span style="color:var(--faint);font-size:11px;">'
                f'{peca["categoria"]} · {tem}</span></div>',
                unsafe_allow_html=True,
            )
            up = cols[1].file_uploader("foto", type=["png", "jpg", "jpeg", "webp"],
                                       key=f"up_{peca['id']}", label_visibility="collapsed")
            if up is not None:
                peca["foto"] = store.encode_image(up)
                D.persist()
                st.rerun()
            if cols[2].button("Remover", key=f"del_{peca['id']}", type="secondary", use_container_width=True):
                st.session_state.guarda_roupa = [
                    x for x in st.session_state.guarda_roupa if x["id"] != peca["id"]
                ]
                D.persist()
                st.rerun()


def _garment(peca):
    badge = "Essencial" if peca["essencial"] else ""
    st.markdown(f"""
    <div>
      {C.tile(peca['tone'], mono=peca['nome'][:1].upper(), badge=badge, photo=peca.get('foto',''))}
      <div class="g-brand">{peca['marca']}</div>
      <div class="g-name">{peca['nome']}</div>
      <div style="font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
           color:var(--gold);margin-top:8px;">{peca['cor']}</div>
    </div>
    """, unsafe_allow_html=True)
