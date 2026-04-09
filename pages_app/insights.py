"""Página: Insights IA"""
import streamlit as st
from components import gold_divider, section_title, insight_card
from data import calcular_receita


def _fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _gerar_insights() -> list[dict]:
    """Gera insights dinâmicos baseados nos dados reais do session_state."""
    insights = []

    clientes  = st.session_state.clientes
    receitas  = st.session_state.receitas
    metas     = st.session_state.metas
    captacoes = st.session_state.captacoes

    # 1. Clientes inativos
    inativos = [c for c in clientes if c["status"] == "Inativo"]
    if inativos:
        nomes = ", ".join(c["nome"] for c in inativos[:3])
        insights.append({
            "tag":  "Retenção",
            "text": f"{len(inativos)} cliente(s) inativo(s) detectado(s): {nomes}. "
                    "Considere uma abordagem de reativação com nova proposta de alocação.",
        })

    # 2. ROA médio
    if receitas:
        roa_med = sum(r["roa"] for r in receitas) / len(receitas)
        if roa_med < 1.5:
            insights.append({
                "tag":  "Rentabilidade",
                "text": f"ROA médio da carteira está em {roa_med:.2f}% a.a. — abaixo do benchmark de 1,5%. "
                        "Revise alocações em produtos de menor remuneração.",
            })
        else:
            insights.append({
                "tag":  "Rentabilidade",
                "text": f"ROA médio saudável: {roa_med:.2f}% a.a. Carteira bem posicionada em relação ao benchmark.",
            })

    # 3. Meta receita
    m_rec = metas["receita_bruta"]
    pct   = m_rec["realizado"] / m_rec["meta"] * 100
    if pct < 70:
        falta = m_rec["meta"] - m_rec["realizado"]
        insights.append({
            "tag":  "Alerta de Meta",
            "text": f"Meta de receita bruta com {pct:.0f}% de execução. "
                    f"Faltam {_fmt_brl(falta)} para atingir o objetivo do mês. "
                    "Priorize operações com ROA mais elevado.",
        })

    # 4. Captação — tendência
    ultimos = captacoes[-3:]
    if ultimos[2]["valor"] > ultimos[1]["valor"] > ultimos[0]["valor"]:
        insights.append({
            "tag":  "Oportunidade",
            "text": "Captação em tendência crescente nos últimos 3 meses consecutivos. "
                    "Momento favorável para ampliar prospecção e metas de AUM.",
        })

    # 5. Concentração de carteira
    if clientes:
        pats     = sorted(clientes, key=lambda c: c["patrimonio"], reverse=True)
        top1_pat = pats[0]["patrimonio"]
        total    = sum(c["patrimonio"] for c in clientes)
        if total > 0 and top1_pat / total > 0.35:
            insights.append({
                "tag":  "Risco de Concentração",
                "text": f"Cliente '{pats[0]['nome']}' representa {top1_pat/total*100:.0f}% do AUM total. "
                        "Alta concentração pode ser um risco operacional — diversifique a carteira.",
            })

    # Insight fixo — boas práticas
    insights.append({
        "tag":  "Boas Práticas",
        "text": "Revisões semestrais de política de investimento (IPS) aumentam a aderência do cliente em até 40%. "
                "Agende reuniões de rebalanceamento com os 3 maiores clientes este mês.",
    })

    return insights


def render():
    section_title("Insights IA", "Análises e recomendações inteligentes")
    gold_divider()

    st.markdown("""
    <p style="color:#666;font-size:0.85rem;margin-top:-8px;margin-bottom:20px;">
    Os insights abaixo são gerados automaticamente com base nos seus dados cadastrados.
    Atualizam em tempo real conforme você registra receitas, clientes e metas.
    </p>""", unsafe_allow_html=True)

    insights = _gerar_insights()

    for ins in insights:
        insight_card(ins["tag"], ins["text"])

    gold_divider()

    # ── Simulador de receita ────────────────────────────────────
    st.markdown("<h3>Simulador de Receita</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666;font-size:0.83rem;'>Simule cenários sem salvar no sistema.</p>",
                unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    s_valor  = sc1.number_input("Valor de Aplicação (R$)", min_value=0.0, step=10_000.0, value=500_000.0, key="sim_val")
    s_roa    = sc2.number_input("ROA (% ao ano)",          min_value=0.0, max_value=20.0, step=0.1,      value=1.5,     key="sim_roa")
    s_rep    = sc3.slider("Repasse (%)", min_value=20, max_value=50, value=35, step=5, key="sim_rep")

    calc = calcular_receita(s_valor, s_roa, s_rep / 100)
    st.markdown(f"""
    <div style="background:#161610;border:1px solid #C9A84C33;border-radius:12px;padding:20px 24px;margin-top:12px;">
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.12em;color:#666;margin-bottom:16px;">Resultado da Simulação</div>
        <div style="display:flex;gap:40px;flex-wrap:wrap;align-items:center;">
            <div>
                <div style="color:#555;font-size:0.72rem;">Receita Bruta</div>
                <div style="color:#C9A84C;font-size:1.4rem;font-weight:600;">{_fmt_brl(calc['receita_bruta'])}</div>
            </div>
            <div style="color:#2A2A2A;font-size:1.5rem;">→</div>
            <div>
                <div style="color:#555;font-size:0.72rem;">Repasse ({s_rep}%)</div>
                <div style="color:#C9A84C;font-size:1.4rem;font-weight:600;">{_fmt_brl(calc['repasse_valor'])}</div>
            </div>
            <div style="color:#2A2A2A;font-size:1.5rem;">−</div>
            <div>
                <div style="color:#555;font-size:0.72rem;">IR (19,5%)</div>
                <div style="color:#E05A5A;font-size:1.4rem;font-weight:600;">{_fmt_brl(calc['ir'])}</div>
            </div>
            <div style="color:#2A2A2A;font-size:1.5rem;">=</div>
            <div>
                <div style="color:#555;font-size:0.72rem;">Receita Líquida</div>
                <div style="color:#5ED68A;font-size:1.7rem;font-weight:700;">{_fmt_brl(calc['receita_liquida'])}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
