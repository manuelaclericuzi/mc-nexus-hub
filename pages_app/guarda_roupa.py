"""
MC Atelier — Guarda-roupa · A Coleção Essencial
"""
import streamlit as st
import components as C
import data as D


CATEGORIAS = ["Blazers", "Camisas", "Calças", "Casacos", "Malhas",
              "Calçados", "Vestidos", "Acessórios"]
OCASIOES   = ["Negócios", "Câmera", "Dia a dia", "Evento", "Criativo", "Todas"]


def render():
    C.topbar()
    resumo = D.resumo_guarda_roupa()

    col_side, col_main = st.columns([1, 3.3], gap="large")

    # ── Rail de filtros ──────────────────────────────────────────
    with col_side:
        cats_html = f"""
          <div style="display:flex;justify-content:space-between;padding:7px 0;
               font-size:12px;font-weight:600;color:var(--ink);border-bottom:1px solid var(--line);">
            <span>Todas as peças</span><span class="mono-num" style="color:var(--faint);">{resumo['total']}</span>
          </div>"""
        for cat in CATEGORIAS:
            n = resumo["categorias"].get(cat, 0)
            if n:
                cats_html += f"""
                  <div style="display:flex;justify-content:space-between;padding:7px 0;
                       font-size:12px;color:var(--muted);">
                    <span>{cat}</span><span class="mono-num" style="color:var(--faint);">{n}</span>
                  </div>"""
        pal = "".join(
            f'<div style="width:24px;height:24px;background:{hx};border:1px solid var(--line);"></div>'
            for _, hx, _ in st.session_state.perfil["paleta"]
        )
        st.markdown(f"""
        <div style="padding-top:8px;">
          <div class="side-label" style="padding-left:0;">Categorias</div>
          {cats_html}
          <div class="side-label" style="padding:24px 0 10px;">Paleta</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">{pal}</div>
          <div class="side-label" style="padding:24px 0 10px;">Verificação de autoridade</div>
          <div>{C.chip('Caimento perfeito')}{C.chip('Alta versatilidade', 'soft')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
        cat_sel = st.selectbox("Filtrar categoria", ["Todas"] + CATEGORIAS, label_visibility="visible")
        occ_sel = st.selectbox("Filtrar ocasião",   ["Todas"] + OCASIOES[:-1], label_visibility="visible")

    # ── Grade principal ──────────────────────────────────────────
    with col_main:
        C.sec_header(
            "A Coleção Essencial",
            subtitle="Ativos estratégicos curados para um guarda-roupa profissional definido por excelência e precisão.",
        )

        # barra de ações
        st.markdown(f"""
        <div style="background:var(--ink);color:#fff;display:flex;align-items:center;
             gap:36px;padding:14px 26px;margin-bottom:28px;font-size:11px;font-weight:600;
             letter-spacing:.14em;text-transform:uppercase;">
          <span>▤ &nbsp;Total: {resumo['total']} peças</span>
          <span style="opacity:.6;">＋ &nbsp;Adicionar peça</span>
          <span style="opacity:.6;">✦ &nbsp;Gerar look</span>
        </div>
        """, unsafe_allow_html=True)

        gr = st.session_state.guarda_roupa
        if cat_sel != "Todas":
            gr = [p for p in gr if p["categoria"] == cat_sel]
        if occ_sel != "Todas":
            gr = [p for p in gr if p["ocasiao"] in (occ_sel, "Todas")]

        if not gr:
            st.markdown('<div style="color:var(--faint);font-style:italic;padding:20px 0;">Nenhuma peça com esses filtros.</div>',
                        unsafe_allow_html=True)
        for start in range(0, len(gr), 3):
            cols = st.columns(3, gap="medium")
            for col, peca in zip(cols, gr[start:start+3]):
                with col:
                    _garment(peca)

        # adicionar peça
        st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
        with st.expander("＋  Adicionar nova peça"):
            with st.form("add_peca", clear_on_submit=True):
                a, b, c = st.columns(3)
                nome  = a.text_input("Nome da peça")
                marca = b.text_input("Marca", value="—")
                cat   = c.selectbox("Categoria", CATEGORIAS)
                d, e, f = st.columns(3)
                cor = d.text_input("Cor")
                oca = e.selectbox("Ocasião", OCASIOES)
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
