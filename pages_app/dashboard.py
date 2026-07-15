"""
MC Atelier — Dashboard (Command Center)
Visão da semana + look de hoje + look de emergência + dica de autoridade.
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
    hoje_i = datetime.datetime.now().weekday()          # 0 = segunda
    hoje_i = min(hoje_i, len(semana) - 1)

    # ── Saudação ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:30px;">
      <div style="font-family:'Playfair Display',serif;font-size:46px;font-weight:700;
           line-height:1.02;letter-spacing:-.02em;">Olá, Manuela!</div>
      <div style="font-size:13px;color:var(--muted);margin-top:10px;letter-spacing:.02em;">
           Seu comando de estilo da semana — {semana[hoje_i]['ocasiao']} hoje.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Weekly Overview ──────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-bottom:16px;">Visão da semana</div>',
                unsafe_allow_html=True)

    cols = st.columns(7, gap="small")
    for i, (col, dia) in enumerate(zip(cols, semana)):
        col.markdown(_day_card(dia, today=(i == hoje_i)), unsafe_allow_html=True)

    st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)

    # ── Fórmula visual: look de hoje ─────────────────────────────
    _formula_hoje(semana[hoje_i])

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    n1, n2, _ = st.columns([1, 1, 3])
    if n1.button("Ver closet completo", key="dash_closet", use_container_width=True):
        st.session_state.pagina = "Guarda-roupa"; st.rerun()
    if n2.button("Editar a semana", key="dash_semana", type="secondary", use_container_width=True):
        st.session_state.pagina = "Calendário"; st.rerun()

    st.markdown('<div style="height:34px;"></div>', unsafe_allow_html=True)

    # ── Emergência + Dica de autoridade ──────────────────────────
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
        <div style="background:var(--paper);border:1px solid var(--line);padding:32px;height:100%;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:22px;">
            <div>
              <div class="eyebrow" style="margin-bottom:8px;">Look de emergência</div>
              <div class="serif-md">{emg['titulo']}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);">Custo por uso</div>
              <div style="font-family:'Playfair Display',serif;font-size:20px;margin-top:2px;">{emg['custo']}</div>
            </div>
          </div>
          <div style="display:flex;gap:10px;margin-bottom:24px;">{tiles}</div>
          {razoes}
        </div>
        """, unsafe_allow_html=True)

    with col_d:
        st.markdown(f"""
        <div style="background:var(--black);color:#fff;padding:32px;height:100%;
             display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <div style="font-size:11px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;
                 color:rgba(255,255,255,.6);margin-bottom:20px;">✦ Dica de autoridade</div>
            <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:22px;
                 line-height:1.4;">"{perfil['citacao']}"</div>
          </div>
          <div style="border-top:1px solid rgba(255,255,255,.2);padding-top:22px;margin-top:28px;">
            <div style="font-size:10px;letter-spacing:.16em;text-transform:uppercase;
                 color:rgba(255,255,255,.55);margin-bottom:6px;">Seu arquétipo</div>
            <div style="font-size:14px;font-weight:600;">{perfil['arquetipo']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)


# ── Componentes internos ─────────────────────────────────────────
def _day_card(dia: dict, today: bool = False) -> str:
    lk = D.look_by_id(dia.get("look_id"))
    clima = _CLIMA.get(dia.get("clima", ""), "")

    if lk and lk.get("pecas"):
        tone = D.tone_for(lk["pecas"][0])
        img = (f'background:linear-gradient(150deg,{tone} 0%,'
               f'{C._darken(tone, .2)} 100%);')
        inner = ""
    else:
        img = "background:var(--panel);"
        inner = ('<div style="position:absolute;inset:0;display:grid;place-items:center;'
                 'font-family:\'Playfair Display\',serif;font-size:22px;color:var(--line2);">+</div>')

    border = "2px solid var(--ink)" if today else "1px solid var(--line)"
    bg = "var(--bone)" if today else "var(--paper)"
    daycolor = "var(--ink)" if today else "var(--faint)"

    return (
        f'<div style="border:{border};background:{bg};padding:12px 12px 14px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
        f'<span style="font-size:10px;font-weight:700;letter-spacing:.14em;color:{daycolor};">{dia["dia"]}</span>'
        f'<span style="font-size:12px;color:var(--faint);">{clima}</span></div>'
        f'<div style="position:relative;width:100%;aspect-ratio:3/4;{img}'
        f'border:1px solid var(--line);margin-bottom:12px;">{inner}</div>'
        f'<div style="font-size:11px;font-weight:700;color:var(--ink);line-height:1.25;">{dia["ocasiao"]}</div>'
        f'<div style="font-size:10.5px;color:var(--faint);margin-top:3px;line-height:1.3;">{dia["tag"]}</div>'
        f'</div>'
    )


def _formula_hoje(dia: dict):
    lk = D.look_by_id(dia.get("look_id"))

    st.markdown(f"""
    <div style="display:flex;align-items:flex-end;justify-content:space-between;
         border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:26px;">
      <div>
        <div class="eyebrow" style="margin-bottom:8px;">Fórmula visual · Look de hoje</div>
        <div class="serif-lg">{lk['nome'] if lk else 'Dia livre'}</div>
      </div>
      <div style="font-size:11px;font-style:italic;color:var(--muted);text-align:right;max-width:34ch;">
        {lk['descricao'] if lk else 'Nenhum look planejado — que tal o de emergência abaixo?'}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not lk or not lk.get("pecas"):
        st.markdown('<div style="background:var(--panel);border:1px dashed var(--line2);'
                    'padding:44px;text-align:center;color:var(--faint);font-size:13px;">'
                    'Sem look para hoje. Planeje na aba <b>Calendário</b>.</div>',
                    unsafe_allow_html=True)
        return

    pecas = lk["pecas"]
    labels = _slot_labels(len(pecas))
    cols = st.columns(len(pecas), gap="small")
    for col, peca, lab in zip(cols, pecas, labels):
        tone = D.tone_for(peca)
        col.markdown(f"""
        <div>
          <div style="width:100%;height:260px;background:linear-gradient(150deg,{tone} 0%,
               {C._darken(tone, .2)} 100%);border:1px solid var(--line);"></div>
          <div class="eyebrow" style="margin-top:14px;font-size:9.5px;">{lab}</div>
          <div style="font-size:13px;color:var(--ink);margin-top:5px;line-height:1.3;">{peca}</div>
        </div>
        """, unsafe_allow_html=True)


def _slot_labels(n: int):
    """Rótulos editoriais conforme o número de peças do look."""
    base = ["Base", "Meio", "Terceira peça", "Acabamento", "Extra"]
    if n <= len(base):
        labels = base[:n]
        labels[-1] = "Acabamento"      # último sempre é o "final touch"
        return labels
    return base + ["Extra"] * (n - len(base))
