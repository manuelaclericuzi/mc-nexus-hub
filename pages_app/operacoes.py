"""Página: Operações — Registro de compras e vendas de ativos"""
import streamlit as st
from datetime import date
from components import gold_divider, section_title, ticker_tag, cat_tag

CATEGORIAS = ["Ação", "FII", "ETF", "BDR", "Opção"]


def _fmt_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _th(label: str, right: bool = False) -> str:
    align = "right" if right else "left"
    return (
        f'<th style="padding:9px 14px;text-align:{align};font-size:10px;font-weight:600;'
        f'color:var(--text3);letter-spacing:.5px;text-transform:uppercase;'
        f'border-bottom:1px solid var(--border2);white-space:nowrap">{label}</th>'
    )


def render():
    section_title("Operações", "Registro de compras e vendas de ativos")
    gold_divider()

    operacoes = st.session_state.operacoes
    clientes  = st.session_state.clientes

    # ── KPIs ─────────────────────────────────────────────────────
    total_ops     = len(operacoes)
    vol_compras   = sum(o["qty"] * o["price"] for o in operacoes if o["tipo"] == "Compra")
    vol_vendas    = sum(o["qty"] * o["price"] for o in operacoes if o["tipo"] == "Venda")
    saldo         = vol_compras - vol_vendas

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""<div class="metric-card m-blue">
        <div class="metric-label">Total Operações</div>
        <div class="metric-value">{total_ops}</div>
    </div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="metric-card m-green">
        <div class="metric-label">Volume Compras</div>
        <div class="metric-value">{_fmt_brl(vol_compras)}</div>
    </div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="metric-card m-red">
        <div class="metric-label">Volume Vendas</div>
        <div class="metric-value">{_fmt_brl(vol_vendas)}</div>
    </div>""", unsafe_allow_html=True)
    k4.markdown(f"""<div class="metric-card m-amber">
        <div class="metric-label">Saldo (C − V)</div>
        <div class="metric-value">{_fmt_brl(saldo)}</div>
    </div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Nova Operação ─────────────────────────────────────────────
    col_btn, _ = st.columns([2, 5])
    with col_btn:
        nova = st.button("+ Nova Operação", use_container_width=True)

    if nova or st.session_state.get("show_form_operacao"):
        st.session_state["show_form_operacao"] = True
        st.markdown("<h3>Registrar Operação</h3>", unsafe_allow_html=True)

        nomes = {c["nome"]: c["id"] for c in clientes}
        with st.form("form_operacao", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            cliente_nome = fc1.selectbox("Cliente *", list(nomes.keys()))
            tipo         = fc2.selectbox("Tipo *", ["Compra", "Venda"])

            fc3, fc4 = st.columns(2)
            ticker = fc3.text_input("Código do Ativo *", placeholder="ex: PETR4").upper().strip()
            cat    = fc4.selectbox("Categoria *", CATEGORIAS)

            fc5, fc6, fc7 = st.columns(3)
            qty   = fc5.number_input("Quantidade *", min_value=1, step=1, value=100)
            price = fc6.number_input("Preço (R$) *", min_value=0.01, step=0.01, value=30.00, format="%.2f")
            dt    = fc7.date_input("Data *", value=date.today())

            obs = st.text_input("Observação", placeholder="Opcional")

            if ticker:
                total_op = qty * price
                cor_tipo = "var(--green)" if tipo == "Compra" else "var(--red)"
                st.markdown(f"""<div class="info-box blue">
                    <span style="color:{cor_tipo};font-weight:700">{tipo}</span>
                    &nbsp;{ticker}&nbsp;·&nbsp;{cat}&nbsp;·&nbsp;
                    {qty:,} × {_fmt_brl(price)} =
                    <strong style="color:var(--blue)">{_fmt_brl(total_op)}</strong>
                </div>""", unsafe_allow_html=True)

            submitted = st.form_submit_button("Registrar Operação")
            if submitted:
                if not ticker:
                    st.error("Código do ativo é obrigatório.")
                else:
                    novo_id = max((o["id"] for o in operacoes), default=0) + 1
                    st.session_state.operacoes.append({
                        "id":        novo_id,
                        "client_id": nomes[cliente_nome],
                        "tipo":      tipo,
                        "ticker":    ticker,
                        "cat":       cat,
                        "qty":       float(qty),
                        "price":     float(price),
                        "date":      str(dt),
                        "obs":       obs,
                    })
                    st.session_state.pop("show_form_operacao", None)
                    st.success(f"Operação registrada: {tipo} {qty}x {ticker} @ {_fmt_brl(price)}")
                    st.rerun()

    gold_divider()

    # ── Filtros ───────────────────────────────────────────────────
    st.markdown("<h3>Histórico de Operações</h3>", unsafe_allow_html=True)
    fcol1, fcol2, fcol3 = st.columns([3, 2, 2])
    busca     = fcol1.text_input("Buscar ticker", placeholder="ex: PETR4", label_visibility="visible")
    tipo_f    = fcol2.selectbox("Tipo", ["Todos", "Compra", "Venda"])
    cliente_f = fcol3.selectbox("Cliente", ["Todos"] + [c["nome"] for c in clientes])

    ops_f = list(reversed(operacoes))
    if busca:
        ops_f = [o for o in ops_f if busca.upper() in o["ticker"]]
    if tipo_f != "Todos":
        ops_f = [o for o in ops_f if o["tipo"] == tipo_f]
    if cliente_f != "Todos":
        cid = next((c["id"] for c in clientes if c["nome"] == cliente_f), None)
        if cid:
            ops_f = [o for o in ops_f if o["client_id"] == cid]

    if not ops_f:
        st.markdown("""<div style="text-align:center;padding:40px;color:var(--text3)">
            <div style="font-size:32px;opacity:.3">⇄</div>
            <div style="font-size:12px;margin-top:8px">Nenhuma operação encontrada.</div>
        </div>""", unsafe_allow_html=True)
        return

    cl_map = {c["id"]: c["nome"] for c in clientes}
    rows   = ""
    for o in ops_f:
        tipo_cls = "vp" if o["tipo"] == "Compra" else "vn"
        tipo_sym = "▲" if o["tipo"] == "Compra" else "▼"
        rows += f"""<tr>
            <td style="color:var(--text2)">{cl_map.get(o['client_id'], '—')}</td>
            <td>{ticker_tag(o['ticker'])}</td>
            <td>{cat_tag(o['cat'])}</td>
            <td class="{tipo_cls}">{tipo_sym} {o['tipo']}</td>
            <td class="r vq">{o['qty']:,.0f}</td>
            <td class="r vq">{_fmt_brl(o['price'])}</td>
            <td class="r vq">{_fmt_brl(o['qty'] * o['price'])}</td>
            <td style="color:var(--text3)">{o['date']}</td>
            <td style="color:var(--text3);font-size:11px">{o.get('obs', '')}</td>
        </tr>"""

    headers = [
        ("Cliente", False), ("Ticker", False), ("Cat", False), ("Tipo", False),
        ("Qtd", True), ("Preço", True), ("Total", True), ("Data", False), ("Obs", False),
    ]
    ths = "".join(_th(h, r) for h, r in headers)

    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border2);border-radius:var(--radius-lg);overflow:hidden;margin-top:8px;">
      <div style="overflow-x:auto;">
        <table class="rv-table"><thead><tr>{ths}</tr></thead><tbody>{rows}</tbody></table>
      </div>
    </div>""", unsafe_allow_html=True)
