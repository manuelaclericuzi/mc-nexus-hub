"""
MC Atelier — Dashboard
"""
import streamlit as st
import components as C


def render():
    C.topbar()

    perfil = st.session_state.perfil
    lod    = st.session_state.look_of_day

    # ── Hero: Look do Dia + Checklist de Autoridade ──────────────
    col_hero, col_chk = st.columns([2, 1], gap="medium")

    with col_hero:
        st.markdown(f"""
        <div style="position:relative;height:560px;overflow:hidden;
             background:linear-gradient(155deg,#4a4d55 0%,#26282d 55%,#141517 100%);">
          <div style="position:absolute;inset:0;
               background:linear-gradient(to top, rgba(0,0,0,.62) 0%, rgba(0,0,0,0) 55%);"></div>
          <div style="position:absolute;left:44px;right:44px;bottom:44px;color:#fff;">
            <div style="font-size:11px;font-weight:600;letter-spacing:.3em;
                 text-transform:uppercase;margin-bottom:18px;opacity:.9;">Look do dia</div>
            <div style="font-family:'Playfair Display',serif;font-style:italic;font-weight:600;
                 font-size:46px;line-height:1.05;margin-bottom:16px;max-width:16ch;">{lod['titulo']}</div>
            <div style="font-size:15px;line-height:1.6;max-width:52ch;opacity:.92;margin-bottom:26px;">
                 {lod['descricao']}</div>
            <span style="display:inline-block;background:#fff;color:#000;font-size:11px;font-weight:700;
                 letter-spacing:.2em;text-transform:uppercase;padding:14px 30px;">Detalhar inventário</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_chk:
        itens = "".join(f"""
          <div class="chk-item">
            <div class="chk-mark">●</div>
            <div>
              <div class="chk-title">{t}</div>
              <div class="chk-desc">{d}</div>
            </div>
          </div>""" for t, d in lod["detalhes"])
        st.markdown(f"""
        <div style="height:560px;background:var(--panel);border:1px solid var(--line);
             padding:40px;display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <div class="eyebrow" style="margin-bottom:10px;">Checklist de autoridade</div>
            <div class="serif-md" style="margin-bottom:34px;">Detalhes curados</div>
            {itens}
          </div>
          <div style="border-top:1px solid var(--line);padding-top:26px;">
            <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:16px;
                 color:var(--ink);line-height:1.5;margin-bottom:12px;">"{perfil['citacao']}"</div>
            <div class="eyebrow">— {perfil['arquetipo']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    # ── Agenda + Progresso ───────────────────────────────────────
    col_ag, col_pr = st.columns(2, gap="medium")

    with col_ag:
        rows = "".join(f"""
          <div class="agenda-row">
            <div class="agenda-time">{a['hora']}</div>
            <div>
              <div class="agenda-title">{a['titulo']}</div>
              <div class="agenda-meta">{a['meta']}</div>
            </div>
          </div>""" for a in st.session_state.agenda)
        st.markdown(f"""
        <div style="background:var(--paper);border:1px solid var(--line);padding:36px;height:100%;">
          <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:24px;">
            <div>
              <div class="eyebrow" style="margin-bottom:8px;">Agenda</div>
              <div class="serif-lg">Sua agenda</div>
            </div>
            <span class="sec-link">Ver tudo</span>
          </div>
          {rows}
        </div>
        """, unsafe_allow_html=True)

    with col_pr:
        resumo = _resumo()
        bars = "".join(
            f'<div style="flex:1;background:{"#ffffff" if hl else "rgba(255,255,255,.32)"};'
            f'height:{h}%;"></div>'
            for h, hl in resumo["bars"]
        )
        swatches = "".join(
            f'<div style="width:22px;height:22px;background:{hx};border:1px solid rgba(255,255,255,.25);"></div>'
            for hx in resumo["palette"]
        )
        st.markdown(f"""
        <div style="background:var(--black);color:#fff;padding:36px;height:100%;
             display:flex;flex-direction:column;justify-content:space-between;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:30px;">
            <div>
              <div style="font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;
                   color:rgba(255,255,255,.6);margin-bottom:8px;">Evolução</div>
              <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:28px;">Progresso de estilo</div>
            </div>
            <div style="text-align:right;">
              <div style="font-family:'Playfair Display',serif;font-size:46px;font-weight:700;line-height:1;">{resumo['pct']}%</div>
              <div style="font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.6);">Cápsula utilizada</div>
            </div>
          </div>
          <div style="display:flex;align-items:flex-end;gap:14px;height:150px;margin-bottom:30px;padding:0 4px;">
            {bars}
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;
               border-top:1px solid rgba(255,255,255,.2);padding-top:26px;">
            <div>
              <div style="font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:12px;">Paleta base</div>
              <div style="display:flex;gap:8px;">{swatches}</div>
            </div>
            <div>
              <div style="font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:12px;">Próximo passo</div>
              <div style="font-size:13px;font-weight:600;">Trench coat clássico</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)

    # ── Expansão do guarda-roupa ─────────────────────────────────
    C.sec_header("Expansão do Guarda-roupa", link="Ver compras")

    cards = [
        ("Trench coat",   "Gabardine camel",  "Prioridade alta",  "#a9855f", "T"),
        ("Camisa branca", "Algodão fino",     "Prioridade alta",  "#c9c3b6", "C"),
        ("Scarpin nude",  "Salto médio",      "Prioridade média", "#b79b86", "S"),
        ("Lenço de seda", "Estampa clássica", "Ponto focal",      "#6f2530", "L"),
    ]
    cols = st.columns(4, gap="medium")
    for col, (brand, name, badge, tone, mono) in zip(cols, cards):
        with col:
            C.garment_card(brand, name, tone=tone, mono=mono, badge=badge)


def _resumo():
    gr = st.session_state.guarda_roupa
    total = len(gr)
    essenciais = sum(1 for p in gr if p["essencial"])
    pct = round(essenciais / total * 100) if total else 0
    bars = [(40, False), (62, False), (55, False), (85, True),
            (70, False), (34, False), (24, False)]
    palette = ["#e8e4dc", "#a9855f", "#3a3c40", "#1c2a3a"]
    return {"pct": pct, "bars": bars, "palette": palette}
