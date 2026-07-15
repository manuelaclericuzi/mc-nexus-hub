"""
MC Atelier — Guia de Estilo (em abas)
Elegância Estratégica · Paleta · Silhuetas · Regras · Pilares
"""
import streamlit as st
import components as C


def render():
    C.topbar()
    p = st.session_state.perfil

    # ── Hero enxuto ──────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:20px;">
      <div class="eyebrow" style="margin-bottom:14px;">Guia de Estilo · Seu arquétipo</div>
      <div style="font-family:'Playfair Display',serif;font-size:48px;font-weight:700;
           line-height:1.02;letter-spacing:-.02em;margin-bottom:16px;">Elegância Estratégica</div>
      <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:17px;
           color:var(--muted);line-height:1.65;max-width:60ch;margin-bottom:20px;">"{p['manifesto']}"</div>
      <div>{C.chip('Arquétipo · ' + p['arquetipo'])}{C.chip('Quiet luxury', 'soft')}</div>
    </div>
    """, unsafe_allow_html=True)

    tab_pal, tab_sil, tab_reg, tab_pil = st.tabs(
        ["Paleta", "Silhuetas", "Regras", "Pilares"]
    )

    # ── Paleta ───────────────────────────────────────────────────
    with tab_pal:
        st.markdown('<div class="serif-lg" style="margin-bottom:6px;">A Paleta Curada</div>'
                    '<div class="sec-sub" style="margin-bottom:26px;">Cinco cores que combinam entre si — tudo o que você vestir sai daqui.</div>',
                    unsafe_allow_html=True)
        cols = st.columns(len(p["paleta"]), gap="small")
        for col, (nome, hx, desc) in zip(cols, p["paleta"]):
            with col:
                st.markdown(f"""
                <div>
                  <div style="height:160px;background:{hx};border:1px solid var(--line);"></div>
                  <div style="font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
                       color:var(--ink);margin-top:14px;">{nome}</div>
                  <div style="font-size:11.5px;color:var(--faint);line-height:1.5;margin-top:8px;">{desc}</div>
                </div>""", unsafe_allow_html=True)

    # ── Silhuetas ────────────────────────────────────────────────
    with tab_sil:
        s1, s2 = p["silhuetas"]
        c1, c2 = st.columns([1, 1.4], gap="medium")
        with c1:
            st.markdown(f"""
            <div style="background:var(--paper);border:1px solid var(--line);padding:30px;height:100%;">
              <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:22px;margin-bottom:14px;">{s1[0]}</div>
              <div style="font-size:13.5px;color:var(--muted);line-height:1.6;">{s1[1]}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="position:relative;height:100%;min-height:300px;overflow:hidden;
                 background:linear-gradient(160deg,#b8b0a2 0%,#7d7368 100%);">
              <div style="position:absolute;left:28px;bottom:26px;color:#fff;max-width:80%;">
                <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:24px;margin-bottom:8px;">{s2[0]}</div>
                <div style="font-size:13.5px;line-height:1.6;opacity:.95;">{s2[1]}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── Regras (mandamentos / proibições) ────────────────────────
    with tab_reg:
        m, pr = st.columns(2, gap="large")
        with m:
            st.markdown(f"""
            <div style="background:var(--paper);border:1px solid var(--line);padding:34px;height:100%;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:22px;">
                <span style="font-size:16px;">◍</span>
                <span style="font-family:'Playfair Display',serif;font-size:20px;">Os Mandamentos</span>
              </div>
              {_rulelist(p['mandamentos'])}
            </div>""", unsafe_allow_html=True)
        with pr:
            st.markdown(f"""
            <div style="background:var(--panel);border:1px solid var(--line);padding:34px;height:100%;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:22px;">
                <span style="font-size:16px;color:#8a2b2b;">⊘</span>
                <span style="font-family:'Playfair Display',serif;font-size:20px;">As Proibições</span>
              </div>
              {_rulelist(p['proibicoes'])}
            </div>""", unsafe_allow_html=True)

    # ── Pilares de autoridade ────────────────────────────────────
    with tab_pil:
        top_l, top_r = st.columns([1.7, 1], gap="large")
        with top_l:
            st.markdown("""
            <div style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;
                 margin-bottom:12px;">Checklist de Autoridade</div>
            <div style="font-size:13.5px;color:var(--muted);line-height:1.65;max-width:52ch;">
                 Quatro pilares que sustentam sua presença. Cada um é uma escolha calculada
                 na arquitetura da sua imagem profissional.</div>
            """, unsafe_allow_html=True)
        with top_r:
            mat = p["maturity"]
            st.markdown(f"""
            <div style="background:var(--paper);border:1px solid var(--line);padding:24px;">
              <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px;">
                <span style="font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);">Score de maturidade</span>
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
                  <div style="font-family:'Playfair Display',serif;font-size:24px;margin-bottom:12px;">{nome}</div>
                  <div style="font-size:12.5px;color:var(--muted);line-height:1.55;">{desc}</div>
                </div>""", unsafe_allow_html=True)


def _rulelist(items):
    out = ""
    for i, (t, d) in enumerate(items):
        top = "" if i == 0 else "border-top:1px solid var(--line);"
        out += (f'<div style="{top}padding:16px 0;">'
                f'<div style="font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);margin-bottom:6px;">{t}</div>'
                f'<div style="font-size:13px;color:var(--muted);line-height:1.55;">{d}</div></div>')
    return out
