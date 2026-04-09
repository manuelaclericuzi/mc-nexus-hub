"""
MC Nexus Hub — Aplicação principal
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "pages_app"))

import streamlit as st

st.set_page_config(
    page_title="MC Nexus Hub",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

from styles import inject_css
from data   import init_state

inject_css()
init_state()

# ── Importa páginas ───────────────────────────────────────────
from pages_app import (
    dashboard, clientes, receitas, captacao, metas, insights, relatorios,
    operacoes, posicoes, cotacoes, alertas,
)

# ── Navegação ─────────────────────────────────────────────────
NAV_ASSESSORIA = [
    ("◈  Dashboard",   "Dashboard"),
    ("◉  Clientes",    "Clientes"),
    ("◈  Receitas",    "Receitas"),
    ("◉  Captação",    "Captação"),
    ("◈  Metas",       "Metas"),
    ("◉  Insights IA", "Insights IA"),
    ("◈  Relatórios",  "Relatórios"),
]

NAV_RV = [
    ("⇄  Operações",  "Operações"),
    ("▦  Posições",   "Posições"),
    ("◉  Cotações",   "Cotações"),
    ("◎  Alertas",    "Alertas"),
]

with st.sidebar:
    # Logo / branding
    st.markdown("""
    <div style="padding:28px 16px 20px;border-bottom:1px solid #2A2A2A;margin-bottom:20px;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.55rem;color:#C9A84C;font-weight:700;letter-spacing:0.06em;">
            MC Nexus Hub
        </div>
        <div style="font-size:0.68rem;color:#555;text-transform:uppercase;letter-spacing:0.16em;margin-top:4px;">
            Gestão de Patrimônio
        </div>
    </div>
    """, unsafe_allow_html=True)

    pagina_atual = st.session_state.get("pagina", "Dashboard")

    # ── Seção Assessoria ──────────────────────────────────────────
    st.markdown(
        '<div style="font-size:9px;font-weight:700;color:#3d4a5c;letter-spacing:1.2px;'
        'text-transform:uppercase;padding:6px 10px 4px">Assessoria</div>',
        unsafe_allow_html=True,
    )
    for label, key in NAV_ASSESSORIA:
        active = pagina_atual == key
        btn_class = "nav-btn-active" if active else "nav-btn"
        st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.pagina = key
            st.session_state.pop("show_form_cliente",   None)
            st.session_state.pop("show_form_receita",   None)
            st.session_state.pop("show_form_operacao",  None)
            st.session_state.pop("show_form_alerta",    None)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Seção Renda Variável ──────────────────────────────────────
    st.markdown(
        '<div style="font-size:9px;font-weight:700;color:#3d4a5c;letter-spacing:1.2px;'
        'text-transform:uppercase;padding:14px 10px 4px">Renda Variável</div>',
        unsafe_allow_html=True,
    )
    for label, key in NAV_RV:
        active = pagina_atual == key
        btn_class = "nav-btn-active" if active else "nav-btn"
        st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.pagina = key
            st.session_state.pop("show_form_operacao", None)
            st.session_state.pop("show_form_alerta",   None)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:24px;left:0;width:220px;padding:0 16px;">
        <div style="border-top:1px solid #2A2A2A;padding-top:14px;">
            <div style="font-size:0.68rem;color:#444;text-transform:uppercase;letter-spacing:0.12em;">Assessor</div>
            <div style="color:#888;font-size:0.82rem;margin-top:2px;">MC Assessoria</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Roteamento de páginas ─────────────────────────────────────
pagina = st.session_state.get("pagina", "Dashboard")

if   pagina == "Dashboard":   dashboard.render()
elif pagina == "Clientes":    clientes.render()
elif pagina == "Receitas":    receitas.render()
elif pagina == "Captação":    captacao.render()
elif pagina == "Metas":       metas.render()
elif pagina == "Insights IA": insights.render()
elif pagina == "Relatórios":  relatorios.render()
elif pagina == "Operações":   operacoes.render()
elif pagina == "Posições":    posicoes.render()
elif pagina == "Cotações":    cotacoes.render()
elif pagina == "Alertas":     alertas.render()
