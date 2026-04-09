"""Página: Dashboard"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from components import metric_card, gold_divider, section_title
from data import resumo_receitas, calcular_receita


def _fmt_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render():
    section_title("Dashboard", "Visão geral do escritório")
    gold_divider()

    clientes   = st.session_state.clientes
    receitas   = st.session_state.receitas
    captacoes  = st.session_state.captacoes
    metas      = st.session_state.metas
    resumo     = resumo_receitas()

    ativos    = sum(1 for c in clientes if c["status"] == "Ativo")
    patrimonio = sum(c["patrimonio"] for c in clientes)
    captacao_total = sum(c["valor"] for c in captacoes[-3:])  # últimos 3 meses

    # ── KPI cards ──────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Clientes Ativos", str(ativos), "▲ 2 este mês")
    with c2:
        metric_card("AUM Total", _fmt_brl(patrimonio), "▲ 4,2%")
    with c3:
        metric_card("Receita Líquida", _fmt_brl(resumo["liquida"]), "▲ 8,1%")
    with c4:
        pct_meta = metas["receita_bruta"]["realizado"] / metas["receita_bruta"]["meta"] * 100
        metric_card("Meta Receita", f"{pct_meta:.0f}%", f"R$ {metas['receita_bruta']['realizado']:,.0f} / R$ {metas['receita_bruta']['meta']:,.0f}")

    gold_divider()

    # ── Gráficos ────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("<h3>Captação Mensal</h3>", unsafe_allow_html=True)
        meses  = [c["mes"] for c in captacoes]
        valores = [c["valor"] / 1000 for c in captacoes]
        fig = go.Figure(go.Bar(
            x=meses, y=valores,
            marker_color=["#C9A84C" if i >= 9 else "#2A2A2A" for i in range(12)],
            text=[f"R${v:.0f}k" for v in valores],
            textposition="outside",
            textfont=dict(color="#888", size=10),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#888", size=11),
            margin=dict(l=0, r=0, t=10, b=0),
            height=260,
            showlegend=False,
            xaxis=dict(showgrid=False, color="#555"),
            yaxis=dict(showgrid=True, gridcolor="#1E1E1E", color="#555"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("<h3>Distribuição AUM</h3>", unsafe_allow_html=True)
        labels = ["Renda Fixa", "Multimercado", "R. Variável", "Prev.", "FII"]
        values = [40, 25, 18, 10, 7]
        colors = ["#C9A84C", "#A8863A", "#8A6D30", "#6B5326", "#4D3A1C"]
        fig2 = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color="#0D0D0D", width=2)),
            textinfo="percent",
            textfont=dict(color="#E8E8E8", size=11),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#888"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=260,
            showlegend=True,
            legend=dict(font=dict(color="#888", size=10), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    gold_divider()

    # ── Últimas receitas ────────────────────────────────────────
    st.markdown("<h3>Últimas Receitas Lançadas</h3>", unsafe_allow_html=True)
    rows = []
    for r in reversed(st.session_state.receitas[-5:]):
        calc = calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])
        rows.append({
            "Cliente":        r["cliente"],
            "Produto":        r["produto"],
            "Valor Aplic.":   _fmt_brl(r["valor_aplicacao"]),
            "ROA (%)":        f"{r['roa']:.1f}%",
            "Repasse":        f"{r['repasse']*100:.0f}%",
            "Rec. Líquida":   _fmt_brl(calc["receita_liquida"]),
            "Data":           r["data"],
        })
    import pandas as pd
    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
    )
