"""Página: Metas"""
import streamlit as st
from components import gold_divider, section_title, progress_bar


def _fmt_brl(v):
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_num(v):
    return f"{v:,.0f}".replace(",", ".")


META_CONFIG = {
    "receita_bruta":  {"label": "Receita Bruta Mensal",  "fmt": _fmt_brl,     "cor": "#C9A84C",  "icone": "💰"},
    "novos_clientes": {"label": "Novos Clientes",         "fmt": _fmt_num,     "cor": "#5ED68A",  "icone": "👤"},
    "captacao":       {"label": "Captação Bruta",         "fmt": _fmt_brl,     "cor": "#6AB8D4",  "icone": "📈"},
    "aum":            {"label": "AUM Total",               "fmt": _fmt_brl,     "cor": "#A78BFA",  "icone": "🏦"},
}


def render():
    section_title("Metas", "Acompanhamento de metas e performance")
    gold_divider()

    metas = st.session_state.metas

    # ── Barras de progresso ─────────────────────────────────────
    for key, cfg in META_CONFIG.items():
        m = metas[key]
        progress_bar(
            title     = f"{cfg['icone']}  {cfg['label']}",
            realizado = m["realizado"],
            meta      = m["meta"],
            fmt_fn    = cfg["fmt"],
            color     = cfg["cor"],
        )

    gold_divider()

    # ── Resumo scorecard ────────────────────────────────────────
    st.markdown("<h3>Scorecard Resumido</h3>", unsafe_allow_html=True)

    rows_html = ""
    for key, cfg in META_CONFIG.items():
        m   = metas[key]
        pct = m["realizado"] / m["meta"] * 100 if m["meta"] else 0
        cor = "#5ED68A" if pct >= 80 else "#C9A84C" if pct >= 50 else "#E05A5A"
        status = "No prazo" if pct >= 80 else "Atenção" if pct >= 50 else "Crítico"
        rows_html += f"""
        <tr>
            <td style="padding:12px 16px;border-bottom:1px solid #1A1A1A;">{cfg['icone']}  {cfg['label']}</td>
            <td style="padding:12px 16px;border-bottom:1px solid #1A1A1A;color:#C9A84C;">{cfg['fmt'](m['realizado'])}</td>
            <td style="padding:12px 16px;border-bottom:1px solid #1A1A1A;color:#666;">{cfg['fmt'](m['meta'])}</td>
            <td style="padding:12px 16px;border-bottom:1px solid #1A1A1A;color:{cor};font-weight:600;">{pct:.1f}%</td>
            <td style="padding:12px 16px;border-bottom:1px solid #1A1A1A;">
                <span style="background:{cor}22;color:{cor};border:1px solid {cor}44;padding:2px 10px;border-radius:50px;font-size:0.72rem;">{status}</span>
            </td>
        </tr>"""

    th = "padding:10px 16px;text-align:left;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#555;border-bottom:1px solid #2A2A2A;"
    st.markdown(f"""
    <div style="background:#111;border:1px solid #2A2A2A;border-radius:12px;overflow:hidden;">
    <table style="width:100%;border-collapse:collapse;">
        <thead><tr style="background:#151515;">
            <th style="{th}">Indicador</th>
            <th style="{th}">Realizado</th>
            <th style="{th}">Meta</th>
            <th style="{th}">Progresso</th>
            <th style="{th}">Status</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Editar metas ────────────────────────────────────────────
    with st.expander("Editar Metas do Mês"):
        with st.form("form_metas"):
            cols = st.columns(2)
            novos = {}
            for i, (key, cfg) in enumerate(META_CONFIG.items()):
                col = cols[i % 2]
                m   = metas[key]
                novos[key] = {
                    "meta":      col.number_input(f"Meta — {cfg['label']}", value=float(m["meta"]),      step=1000.0, key=f"meta_{key}"),
                    "realizado": col.number_input(f"Realizado — {cfg['label']}", value=float(m["realizado"]), step=1000.0, key=f"real_{key}"),
                }
            if st.form_submit_button("Salvar Metas"):
                st.session_state.metas = novos
                st.success("Metas atualizadas com sucesso!")
                st.rerun()
