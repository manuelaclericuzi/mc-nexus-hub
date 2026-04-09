"""Página: Receitas"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components import gold_divider, section_title, metric_card
from data import calcular_receita, IR_FIXO


def _fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


FAIXAS_REPASSE = {
    "20% (Básico)":   0.20,
    "25%":            0.25,
    "30%":            0.30,
    "35% (Padrão)":   0.35,
    "40%":            0.40,
    "45%":            0.45,
    "50% (Premium)":  0.50,
}

PRODUTOS = ["Renda Fixa", "Multimercado", "Renda Variável", "Previdência", "FII", "COE", "Estruturado"]


def render():
    section_title("Receitas", "Controle de receitas e comissionamento")
    gold_divider()

    receitas = st.session_state.receitas

    # ── Totalizadores ───────────────────────────────────────────
    total_bruta = total_repasse = total_ir = total_liq = 0.0
    for r in receitas:
        c = calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])
        total_bruta   += c["receita_bruta"]
        total_repasse += c["repasse_valor"]
        total_ir      += c["ir"]
        total_liq     += c["receita_liquida"]

    k1, k2, k3, k4 = st.columns(4)
    with k1: metric_card("Receita Bruta",   _fmt_brl(total_bruta))
    with k2: metric_card("Repasse Total",   _fmt_brl(total_repasse))
    with k3: metric_card("IR (19,5%)",      _fmt_brl(total_ir), negative=True)
    with k4: metric_card("Receita Líquida", _fmt_brl(total_liq), "▲ 8,1% vs mês ant.")

    gold_divider()

    # ── Botão nova receita ───────────────────────────────────────
    col_btn, _ = st.columns([2, 5])
    with col_btn:
        nova = st.button("+ Nova Receita", use_container_width=True)

    # ── Modal: Nova Receita ─────────────────────────────────────
    if nova or st.session_state.get("show_form_receita"):
        st.session_state["show_form_receita"] = True
        st.markdown("<h3>Nova Receita</h3>", unsafe_allow_html=True)

        with st.form("form_receita", clear_on_submit=True):
            nomes_clientes = [c["nome"] for c in st.session_state.clientes]

            fc1, fc2 = st.columns(2)
            cliente  = fc1.selectbox("Cliente *", nomes_clientes)
            produto  = fc2.selectbox("Produto *", PRODUTOS)

            fc3, fc4, fc5 = st.columns(3)
            valor_aplic = fc3.number_input("Valor de Aplicação (R$) *", min_value=0.0, step=10_000.0, value=100_000.0)
            roa         = fc4.number_input("ROA (% ao ano) *", min_value=0.0, max_value=20.0, step=0.1, value=1.2)
            repasse_key = fc5.selectbox("Repasse *", list(FAIXAS_REPASSE.keys()), index=3)

            repasse_frac = FAIXAS_REPASSE[repasse_key]
            calc = calcular_receita(valor_aplic, roa, repasse_frac)

            # Preview em tempo real
            st.markdown(f"""
            <div style="background:#161610;border:1px solid #2A2A2A;border-radius:10px;padding:16px 20px;margin:12px 0;">
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#666;margin-bottom:12px;">Preview de Receita</div>
                <div style="display:flex;gap:32px;flex-wrap:wrap;">
                    <div><div style="color:#555;font-size:0.72rem;">Receita Bruta</div>
                         <div style="color:#C9A84C;font-size:1.1rem;font-weight:600;">{_fmt_brl(calc['receita_bruta'])}</div></div>
                    <div><div style="color:#555;font-size:0.72rem;">Repasse ({repasse_key})</div>
                         <div style="color:#C9A84C;font-size:1.1rem;font-weight:600;">{_fmt_brl(calc['repasse_valor'])}</div></div>
                    <div><div style="color:#555;font-size:0.72rem;">IR (19,5%)</div>
                         <div style="color:#E05A5A;font-size:1.1rem;font-weight:600;">- {_fmt_brl(calc['ir'])}</div></div>
                    <div><div style="color:#555;font-size:0.72rem;">Receita Líquida</div>
                         <div style="color:#5ED68A;font-size:1.3rem;font-weight:700;">{_fmt_brl(calc['receita_liquida'])}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            data_op = st.date_input("Data da operação")
            submitted = st.form_submit_button("Registrar Receita")

            if submitted:
                if valor_aplic <= 0 or roa <= 0:
                    st.error("Valor de aplicação e ROA devem ser maiores que zero.")
                else:
                    novo_id = max(r["id"] for r in st.session_state.receitas) + 1 if st.session_state.receitas else 1
                    st.session_state.receitas.append({
                        "id":             novo_id,
                        "cliente":        cliente,
                        "produto":        produto,
                        "valor_aplicacao": valor_aplic,
                        "roa":            roa,
                        "repasse":        repasse_frac,
                        "data":           str(data_op),
                    })
                    st.session_state["show_form_receita"] = False
                    st.success(f"Receita registrada! Líquido: {_fmt_brl(calc['receita_liquida'])}")
                    st.rerun()

    gold_divider()

    # ── Tabela de receitas ──────────────────────────────────────
    st.markdown("<h3>Histórico de Receitas</h3>", unsafe_allow_html=True)
    rows = []
    for r in reversed(receitas):
        c = calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])
        rows.append({
            "Cliente":       r["cliente"],
            "Produto":       r["produto"],
            "Aplic. (R$)":   _fmt_brl(r["valor_aplicacao"]),
            "ROA %":         f"{r['roa']:.1f}%",
            "Repasse":       f"{r['repasse']*100:.0f}%",
            "Bruta (R$)":    _fmt_brl(c["receita_bruta"]),
            "IR (R$)":       _fmt_brl(c["ir"]),
            "Líquida (R$)":  _fmt_brl(c["receita_liquida"]),
            "Data":          r["data"],
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    gold_divider()

    # ── Gráfico receita por produto ─────────────────────────────
    st.markdown("<h3>Receita Líquida por Produto</h3>", unsafe_allow_html=True)
    prod_dict: dict[str, float] = {}
    for r in receitas:
        c = calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])
        prod_dict[r["produto"]] = prod_dict.get(r["produto"], 0) + c["receita_liquida"]

    fig = go.Figure(go.Bar(
        x=list(prod_dict.keys()),
        y=list(prod_dict.values()),
        marker_color="#C9A84C",
        text=[_fmt_brl(v) for v in prod_dict.values()],
        textposition="outside",
        textfont=dict(color="#888", size=10),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#888"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=250,
        xaxis=dict(showgrid=False, color="#555"),
        yaxis=dict(showgrid=True, gridcolor="#1E1E1E", color="#555"),
    )
    st.plotly_chart(fig, use_container_width=True)
