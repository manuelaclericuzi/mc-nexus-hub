"""
MC Atelier — Dashboard (enxuto)
Saudação + look de hoje em destaque. Semana e emergência ficam recolhidas,
pra tela respirar.
"""
import datetime
import streamlit as st
import components as C
import data as D

_CLIMA = {"sol": "☀", "nuvem": "☁", "chuva": "☂"}


def render():
    C.topbar()

    perfil = st.session_state.perfil
    semana = st.session_state.semana
    hoje_i = min(datetime.datetime.now().weekday(), len(semana) - 1)
    dia = semana[hoje_i]

    # ── Saudação enxuta ──────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:26px;">
      <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;
           line-height:1.02;letter-spacing:-.02em;">Olá, Manuela.</div>
      <div style="font-size:13px;color:var(--muted);margin-top:8px;">
           Hoje é dia de <b style="color:var(--ink);">{dia['ocasiao'].lower()}</b>.
           Aqui está o seu look.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Faixa fina da semana ─────────────────────────────────────
    _week_ribbon(semana, hoje_i)

    st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)

    # ── Look de hoje (herói) ─────────────────────────────────────
    _look_hoje(dia)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
    b1, b2, _ = st.columns([1, 1, 2])
    if b1.button("Montar looks", key="dash_montar", use_container_width=True):
        st.session_state.pagina = "Looks"; st.rerun()
    if b2.button("Ver a semana", key="dash_semana", type="secondary", use_container_width=True):
        st.session_state.pagina = "Calendário"; st.rerun()

    st.markdown('<div style="height:26px;"></div>', unsafe_allow_html=True)

    # ── Recolhido: emergência + dica ─────────────────────────────
    with st.expander("Look de emergência & dica de autoridade"):
        _emergencia_e_dica(perfil)


# ── Faixa fina da semana ─────────────────────────────────────────
def _week_ribbon(semana, hoje_i):
    cells = ""
    for i, d in enumerate(semana):
        hoje = i == hoje_i
        lk = D.look_by_id(d.get("look_id"))
        dot = D.tone_for(lk["pecas"][0]) if (lk and lk.get("pecas")) else "var(--line2)"
        bg = "var(--ink)" if hoje else "var(--paper)"
        fg = "#fff" if hoje else "var(--faint)"
        occ_c = "rgba(255,255,255,.72)" if hoje else "var(--faint)"
        cells += (
            f'<div style="flex:1;background:{bg};border:1px solid var(--line);'
            f'padding:12px 8px;text-align:center;">'
            f'<div style="font-size:10px;font-weight:700;letter-spacing:.12em;color:{fg};">{d["dia"]}</div>'
            f'<div style="width:14px;height:14px;margin:9px auto 0;background:{dot};'
            f'border:1px solid rgba(0,0,0,.08);"></div>'
            f'<div style="font-size:9px;color:{occ_c};margin-top:9px;line-height:1.2;'
            f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{d["ocasiao"]}</div>'
            f'</div>'
        )
    st.markdown(f'<div style="display:flex;gap:6px;">{cells}</div>',
                unsafe_allow_html=True)


# ── Look de hoje ─────────────────────────────────────────────────
def _look_hoje(dia):
    lk = D.look_by_id(dia.get("look_id"))

    st.markdown(f"""
    <div style="display:flex;align-items:flex-end;justify-content:space-between;
         border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:26px;">
      <div>
        <div class="eyebrow" style="margin-bottom:8px;">Look de hoje</div>
        <div class="serif-lg">{lk['nome'] if lk else 'Dia livre'}</div>
      </div>
      <div style="font-size:11px;font-style:italic;color:var(--muted);text-align:right;max-width:38ch;">
        {lk['descricao'] if lk else 'Nenhum look planejado — abra o de emergência abaixo ou monte um novo.'}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not lk or not lk.get("pecas"):
        st.markdown('<div style="background:var(--panel);border:1px dashed var(--line2);'
                    'padding:44px;text-align:center;color:var(--faint);font-size:13px;">'
                    'Sem look para hoje. Planeje na aba <b>Calendário</b> '
                    'ou monte um em <b>Looks</b>.</div>', unsafe_allow_html=True)
        return

    pecas = lk["pecas"]
    labels = _slot_labels(len(pecas))
    cols = st.columns(len(pecas), gap="small")
    for col, peca, lab in zip(cols, pecas, labels):
        tone = D.tone_for(peca)
        col.markdown(f"""
        <div>
          <div style="width:100%;height:240px;background:linear-gradient(150deg,{tone} 0%,
               {C._darken(tone, .2)} 100%);border:1px solid var(--line);"></div>
          <div class="eyebrow" style="margin-top:14px;font-size:9.5px;">{lab}</div>
          <div style="font-size:13px;color:var(--ink);margin-top:5px;line-height:1.3;">{peca}</div>
        </div>
        """, unsafe_allow_html=True)


def _slot_labels(n: int):
    base = ["Base", "Meio", "Terceira peça", "Acabamento", "Extra"]
    if n <= len(base):
        labels = base[:n]
        labels[-1] = "Acabamento"
        return labels
    return base + ["Extra"] * (n - len(base))


# ── Emergência + dica (recolhido) ────────────────────────────────
def _emergencia_e_dica(perfil):
    col_e, col_d = st.columns([1.5, 1], gap="medium")

    with col_e:
        emg = D.emergencia()
        tiles = "".join(
            f'<div style="flex:1;aspect-ratio:3/4;background:'
            f'linear-gradient(150deg,{D.tone_for(p)} 0%,{C._darken(D.tone_for(p),.2)} 100%);'
            f'border:1px solid var(--line);"></div>'
            for p in emg["pecas"]
        )
        razoes = "".join(
            f'<div class="chk-item" style="margin-bottom:16px;">'
            f'<div class="chk-mark">◍</div><div class="chk-desc">{r}</div></div>'
            for r in emg["razoes"]
        )
        st.markdown(f"""
        <div style="padding:6px 6px 0;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
            <div>
              <div class="eyebrow" style="margin-bottom:8px;">Look de emergência</div>
              <div class="serif-md">{emg['titulo']}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);">Custo por uso</div>
              <div style="font-family:'Playfair Display',serif;font-size:20px;margin-top:2px;">{emg['custo']}</div>
            </div>
          </div>
          <div style="display:flex;gap:10px;margin-bottom:22px;">{tiles}</div>
          {razoes}
        </div>
        """, unsafe_allow_html=True)

    with col_d:
        st.markdown(f"""
        <div style="background:var(--black);color:#fff;padding:30px;height:100%;
             display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <div style="font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;
                 color:rgba(255,255,255,.6);margin-bottom:18px;">✦ Dica de autoridade</div>
            <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:21px;
                 line-height:1.4;">"{perfil['citacao']}"</div>
          </div>
          <div style="border-top:1px solid rgba(255,255,255,.2);padding-top:20px;margin-top:26px;">
            <div style="font-size:10px;letter-spacing:.16em;text-transform:uppercase;
                 color:rgba(255,255,255,.55);margin-bottom:6px;">Seu arquétipo</div>
            <div style="font-size:14px;font-weight:600;">{perfil['arquetipo']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
