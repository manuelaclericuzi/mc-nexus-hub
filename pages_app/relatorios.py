"""Página: Relatórios"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from components import gold_divider, section_title
from data import calcular_receita


def _fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render():
    section_title("Relatórios", "Análises consolidadas e exportações")
    gold_divider()

    # ── Seletor de período ──────────────────────────────────────
    rc1, rc2, _ = st.columns([2, 2, 3])
    tipo = rc1.selectbox("Tipo de Relatório", ["Receitas", "Clientes", "Captação", "Consolidado"])
    periodo = rc2.selectbox("Período", ["Último Mês", "Último Trimestre", "Ano Atual", "Todos"])

    gold_divider()

    if tipo == "Receitas":
        _relatorio_receitas()
    elif tipo == "Clientes":
        _relatorio_clientes()
    elif tipo == "Captação":
        _relatorio_captacao()
    else:
        _relatorio_consolidado()


def _relatorio_receitas():
    st.markdown("<h3>Relatório de Receitas</h3>", unsafe_allow_html=True)
    receitas = st.session_state.receitas
    rows = []
    for r in receitas:
        c = calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])
        rows.append({
            "Cliente":      r["cliente"],
            "Produto":      r["produto"],
            "Aplic.":       _fmt_brl(r["valor_aplicacao"]),
            "ROA%":         f"{r['roa']:.1f}%",
            "Repasse%":     f"{r['repasse']*100:.0f}%",
            "Rec. Bruta":   _fmt_brl(c["receita_bruta"]),
            "IR":           _fmt_brl(c["ir"]),
            "Rec. Líquida": _fmt_brl(c["receita_liquida"]),
            "Data":         r["data"],
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Totais
    total_liq = sum(calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])["receita_liquida"] for r in receitas)
    st.markdown(f"""
    <div style="background:#1A1A0E;border:1px solid #C9A84C33;border-radius:10px;padding:14px 20px;margin-top:12px;text-align:right;">
        <span style="color:#666;font-size:0.8rem;">Total Receita Líquida: </span>
        <span style="color:#C9A84C;font-size:1.3rem;font-weight:700;">{_fmt_brl(total_liq)}</span>
    </div>""", unsafe_allow_html=True)


def _relatorio_clientes():
    st.markdown("<h3>Relatório de Clientes</h3>", unsafe_allow_html=True)
    clientes = st.session_state.clientes

    # Pizza status
    ativos   = sum(1 for c in clientes if c["status"] == "Ativo")
    inativos = len(clientes) - ativos

    col1, col2 = st.columns([2, 3])
    with col1:
        fig = go.Figure(go.Pie(
            labels=["Ativos", "Inativos"],
            values=[ativos, inativos],
            hole=0.55,
            marker=dict(colors=["#C9A84C", "#2A2A2A"], line=dict(color="#0D0D0D", width=2)),
            textinfo="percent+value",
            textfont=dict(color="#E8E8E8", size=12),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#888"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=220,
            legend=dict(font=dict(color="#888", size=10), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        rows = [{
            "Nome":        c["nome"],
            "Patrimônio":  _fmt_brl(c["patrimonio"]),
            "Status":      c["status"],
            "Cadastro":    c["data_cadastro"],
        } for c in sorted(clientes, key=lambda x: x["patrimonio"], reverse=True)]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _relatorio_captacao():
    st.markdown("<h3>Relatório de Captação</h3>", unsafe_allow_html=True)
    captacoes = st.session_state.captacoes
    meses  = [c["mes"] for c in captacoes]
    valores = [c["valor"] for c in captacoes]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=meses, y=valores,
        marker_color="#C9A84C",
        name="Captação",
    ))
    # Meta fictícia
    meta_val = 600_000
    fig.add_hline(y=meta_val, line_dash="dash", line_color="#E05A5A", annotation_text=f"Meta: {_fmt_brl(meta_val)}")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#888"),
        margin=dict(l=0, r=0, t=20, b=0),
        height=320,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1A1A1A"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    df = pd.DataFrame({
        "Mês":       meses,
        "Captação":  [_fmt_brl(v) for v in valores],
        "Acum.":     [_fmt_brl(sum(valores[:i+1])) for i in range(len(valores))],
        "vs Meta":   ["✅" if v >= meta_val else "❌" for v in valores],
    })
    st.dataframe(df, use_container_width=True, hide_index=True)


def _relatorio_consolidado():
    st.markdown("<h3>Relatório Consolidado</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666;font-size:0.83rem;'>Visão executiva unificada.</p>", unsafe_allow_html=True)

    clientes  = st.session_state.clientes
    receitas  = st.session_state.receitas
    captacoes = st.session_state.captacoes
    metas     = st.session_state.metas

    total_liq = sum(calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])["receita_liquida"] for r in receitas)
    aum       = sum(c["patrimonio"] for c in clientes)
    cap_total = sum(c["valor"] for c in captacoes)

    rows = [
        {"Indicador": "Clientes Ativos",       "Valor": str(sum(1 for c in clientes if c["status"] == "Ativo"))},
        {"Indicador": "AUM Total",              "Valor": _fmt_brl(aum)},
        {"Indicador": "Captação Anual",         "Valor": _fmt_brl(cap_total)},
        {"Indicador": "Receita Líquida Total",  "Valor": _fmt_brl(total_liq)},
        {"Indicador": "Meta Receita (%)",        "Valor": f"{metas['receita_bruta']['realizado']/metas['receita_bruta']['meta']*100:.1f}%"},
        {"Indicador": "Meta Captação (%)",       "Valor": f"{metas['captacao']['realizado']/metas['captacao']['meta']*100:.1f}%"},
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
