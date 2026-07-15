"""
MC Atelier — Guia de Estilo
Elegância Estratégica · Paleta Curada · Silhuetas · Mandamentos · Pilares de Autoridade
"""
import streamlit as st
import components as C


def render():
    C.topbar()
    p = st.session_state.perfil

    # ── Hero: Elegância Estratégica ──────────────────────────────
    col_txt, col_img = st.columns([1.15, 1], gap="large")
    with col_txt:
        st.markdown(f"""
        <div style="padding-top:14px;">
          <div style="font-family:'Playfair Display',serif;font-size:52px;font-weight:700;
               line-height:1.02;letter-spacing:-.02em;border-bottom:1px solid var(--ink);
               padding-bottom:14px;margin-bottom:22px;display:inline-block;">Elegância Estratégica</div>
          <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:18px;
               color:var(--muted);line-height:1.7;max-width:52ch;margin-bottom:26px;">"{p['manifesto']}"</div>
          <div>{C.chip('Arquétipo · ' + p['arquetipo'])}{C.chip('Quiet luxury', 'soft')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_img:
        st.markdown(
            C.tile("#3a3d44", mono="✦", ratio="4 / 3"),
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:56px;"></div>', unsafe_allow_html=True)

    # ── A Paleta Curada ──────────────────────────────────────────
    st.markdown(
        '<div class="serif-lg" style="border-bottom:1px solid var(--line);'
        'padding-bottom:14px;margin-bottom:26px;">A Paleta Curada</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(len(p["paleta"]), gap="small")
    for col, (nome, hx, desc) in zip(cols, p["paleta"]):
        with col:
            st.markdown(f"""
            <div>
              <div style="height:150px;background:{hx};border:1px solid var(--line);"></div>
              <div style="font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
                   color:var(--ink);margin-top:14px;">{nome}</div>
              <div style="font-size:11.5px;color:var(--faint);line-height:1.5;margin-top:8px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:52px;"></div>', unsafe_allow_html=True)

    # ── Silhuetas Principais ─────────────────────────────────────
    st.markdown(
        '<div class="serif-lg" style="margin-bottom:26px;">Silhuetas Principais</div>',
        unsafe_allow_html=True,
    )
    s1, s2 = p["silhuetas"]
    c1, c2 = st.columns([1, 1.4], gap="medium")
    with c1:
        st.markdown(f"""
        <div style="background:var(--paper);border:1px solid var(--line);padding:28px;height:100%;">
          <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:20px;margin-bottom:12px;">{s1[0]}</div>
          <div style="font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:22px;">{s1[1]}</div>
          {C.tile('#141414', mono='', ratio='1 / 1')}
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="position:relative;height:100%;min-height:360px;overflow:hidden;
             background:linear-gradient(160deg,#b8b0a2 0%,#7d7368 100%);">
          <div style="position:absolute;left:26px;bottom:24px;color:#fff;max-width:80%;">
            <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:24px;margin-bottom:8px;">{s2[0]}</div>
            <div style="font-size:13px;line-height:1.6;opacity:.95;">{s2[1]}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:52px;"></div>', unsafe_allow_html=True)

    # ── Mandamentos / Proibições ─────────────────────────────────
    m, pr = st.columns(2, gap="large")
    with m:
        rows = _rulelist(p["mandamentos"])
        st.markdown(f"""
        <div style="background:var(--paper);border:1px solid var(--line);padding:36px;height:100%;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:26px;">
            <span style="font-size:18px;">◍</span>
            <span style="font-family:'Playfair Display',serif;font-size:22px;letter-spacing:.02em;">Os Mandamentos</span>
          </div>
          {rows}
        </div>""", unsafe_allow_html=True)
    with pr:
        rows = _rulelist(p["proibicoes"])
        st.markdown(f"""
        <div style="background:var(--panel);border:1px solid var(--line);padding:36px;height:100%;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:26px;">
            <span style="font-size:18px;color:#8a2b2b;">⊘</span>
            <span style="font-family:'Playfair Display',serif;font-size:22px;letter-spacing:.02em;">As Proibições</span>
          </div>
          {rows}
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:64px;"></div>', unsafe_allow_html=True)

    # ── Checklist de Autoridade (4 pilares) ──────────────────────
    top_l, top_r = st.columns([1.6, 1], gap="large")
    with top_l:
        st.markdown("""
        <div class="eyebrow" style="margin-bottom:14px;">Estratégia pessoal</div>
        <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;
             line-height:1.05;margin-bottom:16px;">Checklist de Autoridade</div>
        <div style="font-size:14px;color:var(--muted);line-height:1.65;max-width:52ch;">
             Eleve sua presença visual através de quatro pilares estratégicos. Cada elemento
             é uma escolha calculada na arquitetura da sua identidade profissional.</div>
        """, unsafe_allow_html=True)
    with top_r:
        mat = p["maturity"]
        st.markdown(f"""
        <div style="background:var(--paper);border:1px solid var(--line);padding:26px;margin-top:6px;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px;">
            <span style="font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);">Score de maturidade</span>
            <span style="font-family:'Playfair Display',serif;font-size:26px;">{mat}<span style="font-size:14px;">%</span></span>
          </div>
          <div style="height:3px;background:var(--line);">
            <div style="height:100%;width:{mat}%;background:var(--ink);"></div>
          </div>
          <div style="font-size:12px;color:var(--faint);margin-top:12px;font-style:italic;">Pilar: Acessórios incompleto</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:26px;"></div>', unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")
    for col, (nome, desc, done) in zip(cols, p["pilares"]):
        with col:
            mark   = "●" if done else "○"
            border = "2px solid var(--ink)" if not done else "1px solid var(--line)"
            action = "Ver padrões" if done else "Completar pilar"
            st.markdown(f"""
            <div style="background:var(--paper);border:{border};padding:28px 24px;height:330px;
                 display:flex;flex-direction:column;justify-content:space-between;">
              <div>
                <div style="display:flex;justify-content:flex-end;font-size:16px;color:var(--ink);margin-bottom:14px;">{mark}</div>
                <div style="font-family:'Playfair Display',serif;font-size:26px;margin-bottom:14px;">{nome}</div>
                <div style="font-size:12.5px;color:var(--muted);line-height:1.55;">{desc}</div>
              </div>
              <div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
                   border-top:1px solid var(--line);padding-top:16px;">{action} →</div>
            </div>""", unsafe_allow_html=True)


def _rulelist(items):
    out = ""
    for i, (t, d) in enumerate(items):
        top = "" if i == 0 else "border-top:1px solid var(--line);"
        out += (f'<div style="{top}padding:18px 0;">'
                f'<div style="font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);margin-bottom:6px;">{t}</div>'
                f'<div style="font-size:13px;color:var(--muted);line-height:1.55;">{d}</div></div>')
    return out
