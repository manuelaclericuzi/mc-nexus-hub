"""
MC Atelier — Looks
"""
import streamlit as st
import components as C
import data as D


_OCC_TONE = {
    "Negócios": "#2f333b", "Câmera": "#a9855f",
    "Dia a dia": "#8a7a66", "Evento": "#1c2a3a", "Criativo": "#6f2530",
}


def render():
    C.topbar()

    C.sec_header(
        "Looks",
        subtitle="Combinações prontas por ocasião — o seu uniforme pessoal, montado.",
    )

    looks = st.session_state.looks
    for start in range(0, len(looks), 2):
        cols = st.columns(2, gap="large")
        for col, lk in zip(cols, looks[start:start+2]):
            with col:
                _look_card(lk)
                st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)


def _look_card(lk):
    tone = _OCC_TONE.get(lk["ocasiao"], "#2f333b")
    pecas = "".join(C.chip(pc, "soft") for pc in lk["pecas"])
    st.markdown(f"""
    <div style="background:var(--paper);border:1px solid var(--line);">
      <div style="position:relative;height:280px;overflow:hidden;
           background:linear-gradient(155deg,{tone} 0%, {C._darken(tone,.22)} 100%);">
        <div style="position:absolute;left:26px;bottom:24px;color:#fff;">
          <div style="font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
               opacity:.85;margin-bottom:8px;">{lk['ocasiao']}</div>
          <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:28px;">{lk['nome']}</div>
        </div>
      </div>
      <div style="padding:28px;">
        <div style="font-size:13.5px;color:var(--muted);line-height:1.6;margin-bottom:18px;">{lk['descricao']}</div>
        <div class="eyebrow" style="margin-bottom:12px;">{lk['nivel']}</div>
        <div>{pecas}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
