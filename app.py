"""
MC Atelier — Aplicação principal
Plataforma pessoal de imagem & estilo.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "pages_app"))

import streamlit as st

st.set_page_config(
    page_title="MC Atelier",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

from styles import inject_css
from data   import init_state
import store

inject_css()
init_state()

from pages_app import dashboard, guia, guarda_roupa, looks, compras, planner

# ── Navegação ─────────────────────────────────────────────────
NAV = [
    ("Dashboard",       "Dashboard"),
    ("Calendário",      "Calendário"),
    ("Guarda-roupa",    "Guarda-roupa"),
    ("Looks",           "Looks"),
    ("Guia de Estilo",  "Guia de Estilo"),
    ("Compras",         "Compras"),
]

with st.sidebar:
    st.markdown("""
    <div style="padding:22px 12px 26px;border-bottom:1px solid var(--line);margin-bottom:22px;">
      <div class="side-brand">MC Atelier</div>
      <div class="side-tag">Imagem &amp; Estilo</div>
    </div>
    """, unsafe_allow_html=True)

    pagina_atual = st.session_state.get("pagina", "Dashboard")

    st.markdown('<div class="side-label">Navegação</div>', unsafe_allow_html=True)
    for label, key in NAV:
        active = pagina_atual == key
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.pagina = key
            st.rerun()

    with st.expander("⚙️  Armazenamento"):
        modo = "Nuvem (Supabase)" if store.using_cloud() else "Local (temporário)"
        st.caption(f"Modo atual: **{modo}**")
        if st.button("Testar conexão com a nuvem", use_container_width=True):
            h = store.health()
            if h["cloud"]:
                st.success("Conexão OK — dados salvos na nuvem. ✅")
            elif h["secrets"]:
                st.error("Secrets encontrados, mas a nuvem falhou:")
                st.code(h["error"] or "erro desconhecido")
            else:
                st.warning(h["error"] or "Secrets do Supabase não encontrados.")

    p = st.session_state.perfil
    st.markdown(f"""
    <div style="position:fixed;bottom:26px;left:0;width:264px;padding:0 24px;">
      <div style="border-top:1px solid var(--line);padding-top:16px;display:flex;
           align-items:center;gap:12px;">
        <div style="width:38px;height:38px;background:var(--ink);color:#fff;
             display:grid;place-items:center;font-family:'Playfair Display',serif;
             font-style:italic;font-size:16px;">M</div>
        <div>
          <div style="font-size:12px;font-weight:600;color:var(--ink);letter-spacing:.04em;">Meu perfil</div>
          <div style="font-size:10px;color:var(--faint);text-transform:uppercase;letter-spacing:.12em;">{p['arquetipo']}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Roteamento ────────────────────────────────────────────────
pagina = st.session_state.get("pagina", "Dashboard")

if   pagina == "Dashboard":      dashboard.render()
elif pagina == "Calendário":     planner.render()
elif pagina == "Guarda-roupa":   guarda_roupa.render()
elif pagina == "Looks":          looks.render()
elif pagina == "Guia de Estilo": guia.render()
elif pagina == "Compras":        compras.render()
else:                            dashboard.render()
