"""
MC Atelier — Looks
Meus looks (salvos) + Sugeridos pelo acervo (montados automaticamente).
"""
import streamlit as st
import components as C
import data as D


_OCC_TONE = {
    "Negócios": "#2f333b", "Câmera": "#a9855f",
    "Dia a dia": "#8a7a66", "Evento": "#1c2a3a", "Criativo": "#6f2530",
    "Versátil": "#4a4038",
}


def render():
    C.topbar()

    C.sec_header(
        "Looks",
        subtitle="Combinações prontas por ocasião — e novas montadas com o seu acervo.",
    )

    tab_meus, tab_auto = st.tabs(["  Meus looks  ", "  Sugeridos pelo acervo  "])

    with tab_meus:
        _meus_looks()

    with tab_auto:
        _sugeridos()


# ── Meus looks (salvos) ──────────────────────────────────────────
def _meus_looks():
    looks = st.session_state.looks
    if not looks:
        st.markdown('<div style="background:var(--panel);border:1px dashed var(--line2);'
                    'padding:44px;text-align:center;color:var(--faint);font-size:13px;">'
                    'Você ainda não salvou nenhum look. Vá em <b>Sugeridos pelo acervo</b> '
                    'e salve os que gostar.</div>', unsafe_allow_html=True)
        return

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    for start in range(0, len(looks), 2):
        cols = st.columns(2, gap="large")
        for col, lk in zip(cols, looks[start:start+2]):
            with col:
                _look_card(lk)
                if st.button("Remover", key=f"del_{lk['id']}", type="secondary",
                             use_container_width=True):
                    st.session_state.looks = [l for l in st.session_state.looks
                                              if l["id"] != lk["id"]]
                    D.persist()
                    st.rerun()
                st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)


# ── Sugeridos pelo acervo (auto) ─────────────────────────────────
def _sugeridos():
    st.markdown("""
    <div style="background:var(--panel);border:1px solid var(--line);padding:20px 24px;
         margin:8px 0 22px;">
      <div style="font-size:13px;color:var(--muted);line-height:1.6;">
        O MC Atelier combina as peças do seu <b>Guarda-roupa</b> em looks completos,
        seguindo a sua paleta Outono Quente, a coluna monocromática e o seu ponto de
        ouro. Quanto mais peças você cadastra, mais opções ele monta.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtro de ocasião a partir das ocasiões reais das peças
    occs = sorted({p.get("ocasiao") for p in st.session_state.guarda_roupa
                   if p.get("ocasiao") and p.get("ocasiao") != "Todas"})
    f1, f2 = st.columns([2, 1])
    alvo = f1.selectbox("Para qual ocasião?", ["Todas as ocasiões"] + occs,
                        key="auto_occ", label_visibility="collapsed")
    gerar = f2.button("Montar looks", type="primary", use_container_width=True)

    if gerar or st.session_state.get("_auto_gerados") is None:
        alvo_arg = None if alvo == "Todas as ocasiões" else alvo
        st.session_state["_auto_gerados"] = D.montar_looks(n=6, ocasiao=alvo_arg)

    gerados = st.session_state.get("_auto_gerados") or []
    if not gerados:
        st.markdown('<div style="background:var(--panel);border:1px dashed var(--line2);'
                    'padding:44px;text-align:center;color:var(--faint);font-size:13px;">'
                    'Poucas peças para combinar. Adicione ao menos um topo e uma base '
                    'no <b>Guarda-roupa</b>.</div>', unsafe_allow_html=True)
        return

    salvos = {frozenset(l["pecas"]) for l in st.session_state.looks}
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    for start in range(0, len(gerados), 2):
        cols = st.columns(2, gap="large")
        for i, (col, lk) in enumerate(zip(cols, gerados[start:start+2])):
            with col:
                _auto_card(lk)
                ja = frozenset(lk["pecas"]) in salvos
                if ja:
                    st.button("✓ Já está nos meus looks", key=f"saved_{start+i}",
                              disabled=True, use_container_width=True)
                elif st.button("＋ Salvar nos meus looks", key=f"save_{start+i}",
                               type="secondary", use_container_width=True):
                    D.salvar_look(lk)
                    st.toast(f"“{lk['nome']}” salvo nos seus looks.")
                    st.rerun()
                st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)


# ── Cartões ──────────────────────────────────────────────────────
def _look_card(lk):
    tone = _OCC_TONE.get(lk["ocasiao"], "#2f333b")
    pecas = "".join(C.chip(pc, "soft") for pc in lk["pecas"])
    st.markdown(f"""
    <div style="background:var(--paper);border:1px solid var(--line);">
      <div style="position:relative;height:260px;overflow:hidden;
           background:linear-gradient(155deg,{tone} 0%, {C._darken(tone,.22)} 100%);">
        <div style="position:absolute;left:26px;bottom:24px;color:#fff;">
          <div style="font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
               opacity:.85;margin-bottom:8px;">{lk['ocasiao']}</div>
          <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:26px;">{lk['nome']}</div>
        </div>
      </div>
      <div style="padding:26px;">
        <div style="font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:16px;">{lk['descricao']}</div>
        <div class="eyebrow" style="margin-bottom:12px;">{lk['nivel']}</div>
        <div>{pecas}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def _auto_card(lk):
    tones = [D.tone_for(pc) for pc in lk["pecas"]]
    faixa = "".join(
        f'<div style="flex:1;background:linear-gradient(150deg,{t} 0%,'
        f'{C._darken(t,.2)} 100%);"></div>' for t in tones
    )
    chips = "".join(C.chip(pc, "soft") for pc in lk["pecas"])
    motivos = "".join(
        f'<div style="display:flex;gap:8px;margin-bottom:8px;">'
        f'<span style="color:var(--gold);font-size:12px;">◍</span>'
        f'<span style="font-size:12px;color:var(--muted);line-height:1.5;">{m}</span></div>'
        for m in lk.get("motivos", [])
    )
    st.markdown(f"""
    <div style="background:var(--paper);border:1px solid var(--line);">
      <div style="display:flex;height:200px;">{faixa}</div>
      <div style="padding:24px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">
          <div>
            <div class="eyebrow" style="margin-bottom:6px;">{lk['ocasiao']}</div>
            <div style="font-family:'Playfair Display',serif;font-size:22px;">{lk['nome']}</div>
          </div>
        </div>
        <div style="margin-bottom:16px;">{chips}</div>
        {motivos}
      </div>
    </div>
    """, unsafe_allow_html=True)
