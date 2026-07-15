"""
MC Atelier — Guia de Estilo (em abas)
Paleta · Caimento · Regras · Pilares  +  editor de perfil
"""
import streamlit as st
import components as C
import data as D


def render():
    C.topbar()
    p = st.session_state.perfil

    # ── Hero ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:18px;">
      <div class="eyebrow" style="margin-bottom:14px;">Guia de Estilo · Seu perfil</div>
      <div style="font-family:'Playfair Display',serif;font-size:46px;font-weight:700;
           line-height:1.03;letter-spacing:-.02em;margin-bottom:14px;">{p['arquetipo']}</div>
      <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:16px;
           color:var(--muted);margin-bottom:14px;">{p['arquetipo_sub']}</div>
      <div style="font-size:14px;color:var(--muted);line-height:1.65;max-width:64ch;margin-bottom:18px;">{p['manifesto']}</div>
      <div>{C.chip('Coloração quente')}{C.chip('Baixinha + quadril', 'soft')}{C.chip('Orçamento até R$300', 'soft')}</div>
    </div>
    """, unsafe_allow_html=True)

    _editor(p)

    tab_pal, tab_cai, tab_reg, tab_pil = st.tabs(
        ["Paleta", "Caimento", "Regras", "Pilares"]
    )

    # ── Paleta ───────────────────────────────────────────────────
    with tab_pal:
        st.markdown('<div class="serif-lg" style="margin-bottom:6px;">Sua Paleta Quente</div>'
                    '<div class="sec-sub" style="margin-bottom:26px;">Cores que iluminam a sua pele e combinam entre si — tudo o que você vestir sai daqui.</div>',
                    unsafe_allow_html=True)
        cols = st.columns(len(p["paleta"]), gap="small")
        for col, cor in zip(cols, p["paleta"]):
            nome, hx, desc = cor[0], cor[1], cor[2]
            with col:
                st.markdown(f"""
                <div>
                  <div style="height:160px;background:{hx};border:1px solid var(--line);"></div>
                  <div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
                       color:var(--ink);margin-top:14px;">{nome}</div>
                  <div style="font-size:11.5px;color:var(--faint);line-height:1.5;margin-top:8px;">{desc}</div>
                </div>""", unsafe_allow_html=True)

    # ── Caimento (regras pro corpo) ──────────────────────────────
    with tab_cai:
        st.markdown('<div class="serif-lg" style="margin-bottom:6px;">Caimento para Você</div>'
                    '<div class="sec-sub" style="margin-bottom:26px;">Baixinha e com quadril mais largo tem uma silhueta ótima de valorizar. '
                    'Estas seis regras acabam com a sensação de "bagunçado".</div>',
                    unsafe_allow_html=True)
        for i in range(0, len(p["caimento"]), 2):
            cols = st.columns(2, gap="large")
            for j, (col, item) in enumerate(zip(cols, p["caimento"][i:i+2])):
                t, d = item[0], item[1]
                num = i + j + 1
                with col:
                    st.markdown(f"""
                    <div style="border-top:1px solid var(--ink);padding:18px 0 22px;">
                      <div style="display:flex;gap:14px;align-items:flex-start;">
                        <div style="font-family:'Playfair Display',serif;font-size:18px;color:var(--faint);flex:none;">{num:02d}</div>
                        <div>
                          <div class="chk-title" style="margin-bottom:5px;">{t}</div>
                          <div class="chk-desc">{d}</div>
                        </div>
                      </div>
                    </div>""", unsafe_allow_html=True)

    # ── Regras ───────────────────────────────────────────────────
    with tab_reg:
        m, pr = st.columns(2, gap="large")
        with m:
            st.markdown(f"""
            <div style="background:var(--paper);border:1px solid var(--line);padding:34px;height:100%;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:22px;">
                <span style="font-size:16px;">◍</span>
                <span style="font-family:'Playfair Display',serif;font-size:20px;">Sempre</span>
              </div>
              {_rulelist(p['mandamentos'])}
            </div>""", unsafe_allow_html=True)
        with pr:
            st.markdown(f"""
            <div style="background:var(--panel);border:1px solid var(--line);padding:34px;height:100%;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:22px;">
                <span style="font-size:16px;color:#8a2b2b;">⊘</span>
                <span style="font-family:'Playfair Display',serif;font-size:20px;">Evite</span>
              </div>
              {_rulelist(p['proibicoes'])}
            </div>""", unsafe_allow_html=True)

    # ── Pilares ──────────────────────────────────────────────────
    with tab_pil:
        top_l, top_r = st.columns([1.7, 1], gap="large")
        with top_l:
            st.markdown("""
            <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;
                 margin-bottom:12px;">Pilares da sua Autoridade</div>
            <div style="font-size:13.5px;color:var(--muted);line-height:1.65;max-width:52ch;">
                 Quatro frentes que sustentam a sua imagem. O foco agora é a versatilidade —
                 peças que vão do cliente à bike.</div>
            """, unsafe_allow_html=True)
        with top_r:
            mat = p["maturity"]
            st.markdown(f"""
            <div style="background:var(--paper);border:1px solid var(--line);padding:24px;">
              <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px;">
                <span style="font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);">Evolução do estilo</span>
                <span style="font-family:'Playfair Display',serif;font-size:24px;">{mat}<span style="font-size:13px;">%</span></span>
              </div>
              <div style="height:3px;background:var(--line);"><div style="height:100%;width:{mat}%;background:var(--ink);"></div></div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
        cols = st.columns(4, gap="medium")
        for col, (nome, desc, done) in zip(cols, p["pilares"]):
            with col:
                mark   = "●" if done else "○"
                border = "2px solid var(--ink)" if not done else "1px solid var(--line)"
                st.markdown(f"""
                <div style="background:var(--paper);border:{border};padding:26px 22px;height:250px;">
                  <div style="display:flex;justify-content:flex-end;font-size:15px;margin-bottom:12px;">{mark}</div>
                  <div style="font-family:'Playfair Display',serif;font-size:22px;margin-bottom:12px;">{nome}</div>
                  <div style="font-size:12.5px;color:var(--muted);line-height:1.55;">{desc}</div>
                </div>""", unsafe_allow_html=True)


def _editor(p):
    with st.expander("✎  Editar meu perfil e paleta"):
        with st.form("edit_perfil"):
            a, b = st.columns(2)
            arqu = a.text_input("Arquétipo", value=p["arquetipo"])
            sub  = b.text_input("Subtítulo", value=p["arquetipo_sub"])
            manifesto = st.text_area("Descrição", value=p["manifesto"], height=90)
            citacao   = st.text_input("Frase-mantra", value=p["citacao"])

            st.markdown('<div class="eyebrow" style="margin:10px 0 8px;">Paleta</div>', unsafe_allow_html=True)
            nova_paleta = []
            for i, cor in enumerate(p["paleta"]):
                nome, hx, desc = cor[0], cor[1], cor[2]
                c1, c2, c3 = st.columns([1, 2, 3])
                nhx  = c1.color_picker(f"Cor {i+1}", value=hx, key=f"col_{i}")
                nnm  = c2.text_input("Nome", value=nome, key=f"nom_{i}", label_visibility="collapsed")
                ndsc = c3.text_input("Descrição", value=desc, key=f"dsc_{i}", label_visibility="collapsed")
                nova_paleta.append([nnm, nhx, ndsc])

            if st.form_submit_button("Salvar perfil"):
                p["arquetipo"]     = arqu.strip() or p["arquetipo"]
                p["arquetipo_sub"] = sub.strip()
                p["manifesto"]     = manifesto.strip()
                p["citacao"]       = citacao.strip()
                p["paleta"]        = nova_paleta
                st.session_state.perfil = p
                D.persist()
                st.rerun()


def _rulelist(items):
    out = ""
    for i, (t, d) in enumerate(items):
        top = "" if i == 0 else "border-top:1px solid var(--line);"
        out += (f'<div style="{top}padding:16px 0;">'
                f'<div style="font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);margin-bottom:6px;">{t}</div>'
                f'<div style="font-size:13px;color:var(--muted);line-height:1.55;">{d}</div></div>')
    return out
