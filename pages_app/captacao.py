"""Página: Captação"""
import streamlit as st
import plotly.graph_objects as go
from components import gold_divider, section_title, metric_card


def _fmt_brl(v):
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render():
    section_title("Captação", "Fluxo de captação mensal")
    gold_divider()

    captacoes = st.session_state.captacoes
    meses  = [c["mes"] for c in captacoes]
    valores = [c["valor"] for c in captacoes]

    total_ano    = sum(valores)
    media_mensal = total_ano / len(valores)
    melhor_mes   = max(captacoes, key=lambda x: x["valor"])

    k1, k2, k3 = st.columns(3)
    with k1: metric_card("Captação Total (Ano)", _fmt_brl(total_ano))
    with k2: metric_card("Média Mensal",          _fmt_brl(media_mensal))
    with k3: metric_card("Melhor Mês",            f"{melhor_mes['mes']}: {_fmt_brl(melhor_mes['valor'])}")

    gold_divider()

    # ── Gráfico linha + área ────────────────────────────────────
    st.markdown("<h3>Evolução de Captação</h3>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses, y=valores,
        mode="lines+markers",
        fill="tozeroy",
        line=dict(color="#C9A84C", width=2.5),
        fillcolor="rgba(201,168,76,0.10)",
        marker=dict(color="#C9A84C", size=7),
        text=[_fmt_brl(v) for v in valores],
        hovertemplate="%{x}: %{text}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#888"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=300,
        xaxis=dict(showgrid=False, color="#555"),
        yaxis=dict(showgrid=True, gridcolor="#1A1A1A", color="#555"),
    )
    st.plotly_chart(fig, use_container_width=True)

    gold_divider()

    # ── Tabela mensal ───────────────────────────────────────────
    st.markdown("<h3>Detalhamento Mensal</h3>", unsafe_allow_html=True)
    rows_html = ""
    acumulado = 0.0
    for c in captacoes:
        acumulado += c["valor"]
        var = ""
        rows_html += f"""
        <tr>
            <td style="padding:10px 14px;border-bottom:1px solid #1A1A1A;color:#888;">{c['mes']}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #1A1A1A;color:#C9A84C;">{_fmt_brl(c['valor'])}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #1A1A1A;color:#666;">{_fmt_brl(acumulado)}</td>
        </tr>"""

    th = "padding:10px 14px;text-align:left;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#555;border-bottom:1px solid #2A2A2A;"
    st.markdown(f"""
    <div style="background:#111;border:1px solid #2A2A2A;border-radius:12px;overflow:hidden;">
    <table style="width:100%;border-collapse:collapse;">
        <thead><tr style="background:#151515;">
            <th style="{th}">Mês</th>
            <th style="{th}">Captação</th>
            <th style="{th}">Acumulado</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Adicionar captação manual ───────────────────────────────
    st.markdown("<h3>Registrar Captação</h3>", unsafe_allow_html=True)
    with st.form("form_captacao"):
        ac1, ac2 = st.columns(2)
        mes_sel = ac1.selectbox("Mês", meses)
        valor_novo = ac2.number_input("Valor (R$)", min_value=0.0, step=10_000.0)
        if st.form_submit_button("Atualizar"):
            for c in st.session_state.captacoes:
                if c["mes"] == mes_sel:
                    c["valor"] = valor_novo
            st.success(f"Captação de {mes_sel} atualizada para {_fmt_brl(valor_novo)}!")
            st.rerun()
