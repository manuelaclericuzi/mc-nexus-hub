"""
MC Atelier — Calendário Semanal de Estilo (Style Planner)
Sete dias planejáveis + banco de looks. Cada dia recebe um look salvo;
edição via formulário, persistida na nuvem/arquivo.
"""
import datetime
import streamlit as st
import components as C
import data as D

_CLIMA = {"sol": "☀", "nuvem": "☁", "chuva": "☂"}
_SEM_PLANO = "— sem plano —"


def render():
    C.topbar()

    semana = st.session_state.semana
    hoje_i = min(datetime.datetime.now().weekday(), len(semana) - 1)
    datas  = _week_dates()

    # ── Cabeçalho ────────────────────────────────────────────────
    inicio, fim = datas[0], datas[-1]
    st.markdown(f"""
    <div style="display:flex;align-items:flex-end;justify-content:space-between;
         border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:30px;">
      <div>
        <div class="eyebrow" style="margin-bottom:12px;">Style Planner</div>
        <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;
             letter-spacing:-.02em;line-height:1;">Calendário Semanal</div>
      </div>
      <div style="font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);">
        {inicio} — {fim}
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_cal, col_bank = st.columns([2.5, 1], gap="large")

    # ── Dias da semana ───────────────────────────────────────────
    with col_cal:
        for i, dia in enumerate(semana):
            _day_row(i, dia, datas[i], today=(i == hoje_i))

    # ── Look Bank ────────────────────────────────────────────────
    with col_bank:
        _look_bank()


# ── Linha de um dia ──────────────────────────────────────────────
def _day_row(i: int, dia: dict, data_lbl: str, today: bool = False):
    lk = D.look_by_id(dia.get("look_id"))
    clima = _CLIMA.get(dia.get("clima", ""), "")
    accent = "var(--ink)" if today else "var(--line)"

    if lk and lk.get("pecas"):
        chips = "".join(
            f'<span style="display:inline-block;font-size:11px;color:var(--muted);'
            f'border:1px solid var(--line);padding:4px 10px;margin:0 6px 6px 0;">{p}</span>'
            for p in lk["pecas"]
        )
        corpo = (
            f'<div style="font-family:\'Playfair Display\',serif;font-size:20px;'
            f'margin-bottom:12px;">{lk["nome"]}</div>'
            f'<div style="font-size:12px;color:var(--muted);font-style:italic;'
            f'line-height:1.5;margin-bottom:14px;max-width:60ch;">{lk["descricao"]}</div>'
            f'<div>{chips}</div>'
        )
        badge = (f'<span style="font-size:9.5px;font-weight:700;letter-spacing:.14em;'
                 f'text-transform:uppercase;color:var(--ink);border:1px solid var(--ink);'
                 f'padding:4px 10px;">{dia["ocasiao"]}</span>')
    else:
        corpo = ('<div style="font-size:13px;color:var(--faint);font-style:italic;'
                 'padding:8px 0;">Sem plano para este dia — atribua um look abaixo.</div>')
        badge = (f'<span style="font-size:9.5px;font-weight:700;letter-spacing:.14em;'
                 f'text-transform:uppercase;color:var(--faint);border:1px dashed var(--line2);'
                 f'padding:4px 10px;">{dia["ocasiao"]}</span>')

    st.markdown(f"""
    <div style="border-top:2px solid {accent};padding:22px 0 10px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
        <div style="display:flex;align-items:baseline;gap:14px;">
          <span style="font-family:'Playfair Display',serif;font-size:22px;">{dia['dia']}</span>
          <span style="font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);">{data_lbl}</span>
          <span style="font-size:13px;color:var(--faint);">{clima}</span>
        </div>
        {badge}
      </div>
      {corpo}
    </div>
    """, unsafe_allow_html=True)

    _day_editor(i, dia)


def _day_editor(i: int, dia: dict):
    looks = st.session_state.looks
    opcoes = [_SEM_PLANO] + [lk["nome"] for lk in looks]
    atual = D.look_by_id(dia.get("look_id"))
    idx = opcoes.index(atual["nome"]) if atual else 0

    with st.expander("Editar este dia"):
        with st.form(f"day_{i}"):
            escolha = st.selectbox("Look do dia", opcoes, index=idx, key=f"look_sel_{i}")
            ocasiao = st.text_input("Ocasião", value=dia.get("ocasiao", ""), key=f"occ_{i}")
            if st.form_submit_button("Salvar dia"):
                novo_id = None
                for lk in looks:
                    if lk["nome"] == escolha:
                        novo_id = lk["id"]
                        break
                st.session_state.semana[i]["look_id"] = novo_id
                st.session_state.semana[i]["ocasiao"] = ocasiao.strip() or dia.get("ocasiao", "")
                D.persist()
                st.rerun()


# ── Look Bank ────────────────────────────────────────────────────
def _look_bank():
    st.markdown("""
    <div style="border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:20px;">
      <div style="font-family:'Playfair Display',serif;font-size:20px;">Look Bank</div>
      <div style="font-size:11px;letter-spacing:.14em;text-transform:uppercase;
           color:var(--faint);margin-top:6px;">Looks prontos</div>
    </div>
    """, unsafe_allow_html=True)

    for lk in st.session_state.looks:
        tone = D.tone_for(lk["pecas"][0]) if lk.get("pecas") else "#3a3c40"
        st.markdown(f"""
        <div style="margin-bottom:22px;">
          <div style="width:100%;aspect-ratio:4/3;background:linear-gradient(150deg,{tone} 0%,
               {C._darken(tone, .2)} 100%);border:1px solid var(--line);margin-bottom:10px;"></div>
          <div style="font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
               color:var(--ink);">{lk['nome']}</div>
          <div style="font-size:12px;color:var(--muted);font-style:italic;margin-top:4px;">{lk['ocasiao']}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Criar novo look", key="bank_new", type="secondary", use_container_width=True):
        st.session_state.pagina = "Looks"
        st.rerun()


# ── Datas da semana atual (segunda a domingo) ────────────────────
_MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
          "jul", "ago", "set", "out", "nov", "dez"]


def _week_dates():
    hoje = datetime.date.today()
    seg = hoje - datetime.timedelta(days=hoje.weekday())
    out = []
    for k in range(7):
        d = seg + datetime.timedelta(days=k)
        out.append(f"{d.day:02d} {_MESES[d.month - 1]}")
    return out
