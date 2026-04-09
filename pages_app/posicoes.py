"""Página: Posições Abertas — Carteira consolidada com P&L"""
import streamlit as st
from components import gold_divider, section_title, ticker_tag, cat_tag
from data import build_positions, enrich_positions, fetch_quotes


def _fmt_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _pl_html(v: float) -> str:
    cls = "vp" if v >= 0 else "vn"
    return f'<span class="{cls}">{_fmt_brl(v)}</span>'


def _pct_html(v: float) -> str:
    cls = "vp" if v >= 0 else "vn"
    sym = "▲" if v >= 0 else "▼"
    return f'<span class="{cls}">{sym} {abs(v):.2f}%</span>'


def _th(label: str, right: bool = False) -> str:
    align = "right" if right else "left"
    return (
        f'<th style="padding:9px 14px;text-align:{align};font-size:10px;font-weight:600;'
        f'color:var(--text3);letter-spacing:.5px;text-transform:uppercase;'
        f'border-bottom:1px solid var(--border2);white-space:nowrap">{label}</th>'
    )


def render():
    section_title("Posições Abertas", "Carteira consolidada com cotações ao vivo")
    gold_divider()

    clientes  = st.session_state.clientes
    operacoes = st.session_state.operacoes

    # ── Controles ─────────────────────────────────────────────────
    fcol1, fcol2, _ = st.columns([2, 2, 3])
    cliente_f   = fcol1.selectbox("Filtrar por cliente", ["Todos"] + [c["nome"] for c in clientes])
    atualizar   = fcol2.button("⟳ Atualizar Cotações", use_container_width=True)

    if atualizar:
        fetch_quotes.clear()

    cid = None
    if cliente_f != "Todos":
        cid = next((c["id"] for c in clientes if c["nome"] == cliente_f), None)

    # ── Build + enrich ────────────────────────────────────────────
    positions = build_positions(operacoes, client_id=cid)

    if not positions:
        st.info("Nenhuma posição aberta. Registre operações na página Operações.")
        return

    tickers     = tuple(sorted({p["ticker"] for p in positions}))
    quote_cache = fetch_quotes(tickers)
    enriched    = enrich_positions(positions, quote_cache)

    # ── KPIs ──────────────────────────────────────────────────────
    total_exp    = sum(p["current"] * p["qty"] for p in enriched)
    total_custo  = sum(p["pm"]      * p["qty"] for p in enriched)
    total_unreal = sum(p["unreal"]             for p in enriched)
    unreal_pct   = (total_unreal / total_custo * 100) if total_custo > 0 else 0.0

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""<div class="metric-card m-blue">
        <div class="metric-label">Posições Abertas</div>
        <div class="metric-value">{len(enriched)}</div>
    </div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="metric-card m-blue">
        <div class="metric-label">Exposição Total</div>
        <div class="metric-value">{_fmt_brl(total_exp)}</div>
    </div>""", unsafe_allow_html=True)
    pl_color = "m-green" if total_unreal >= 0 else "m-red"
    pl_cls   = "pos"     if total_unreal >= 0 else "neg"
    k3.markdown(f"""<div class="metric-card {pl_color}">
        <div class="metric-label">P&amp;L Não Realizado</div>
        <div class="metric-value {pl_cls}">{_fmt_brl(total_unreal)}</div>
    </div>""", unsafe_allow_html=True)
    k4.markdown(f"""<div class="metric-card {pl_color}">
        <div class="metric-label">P&amp;L %</div>
        <div class="metric-value {pl_cls}">{unreal_pct:+.2f}%</div>
    </div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Tabela ────────────────────────────────────────────────────
    cl_map = {c["id"]: c["nome"] for c in clientes}
    rows   = ""
    for p in sorted(enriched, key=lambda x: abs(x["unreal"]), reverse=True):
        cotacao_html = (
            f'<span class="vq">{_fmt_brl(p["current"])}</span>'
            if p["quote"]
            else '<span style="color:var(--text3)">N/D</span>'
        )
        rows += f"""<tr>
            <td style="color:var(--text2)">{cl_map.get(p['client_id'], '—')}</td>
            <td>{ticker_tag(p['ticker'])}</td>
            <td>{cat_tag(p['cat'])}</td>
            <td class="r vq">{p['qty']:,.0f}</td>
            <td class="r vq">{_fmt_brl(p['pm'])}</td>
            <td class="r">{cotacao_html}</td>
            <td class="r vq">{_fmt_brl(p['current'] * p['qty'])}</td>
            <td class="r">{_pl_html(p['unreal'])}</td>
            <td class="r">{_pct_html(p['unreal_pct'])}</td>
        </tr>"""

    headers = [
        ("Cliente", False), ("Ticker", False), ("Cat", False),
        ("Qtd", True), ("Preço Médio", True), ("Cotação", True),
        ("Exposição", True), ("P&L R$", True), ("P&L %", True),
    ]
    ths = "".join(_th(h, r) for h, r in headers)

    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border2);border-radius:var(--radius-lg);overflow:hidden;">
      <div style="overflow-x:auto;">
        <table class="rv-table"><thead><tr>{ths}</tr></thead><tbody>{rows}</tbody></table>
      </div>
    </div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Alocação por categoria ────────────────────────────────────
    st.markdown("<h3>Alocação por Categoria</h3>", unsafe_allow_html=True)
    cat_exp: dict[str, float] = {}
    for p in enriched:
        cat_exp[p["cat"]] = cat_exp.get(p["cat"], 0.0) + p["current"] * p["qty"]

    cat_colors = {
        "Ação":  "var(--blue2)",
        "FII":   "var(--green2)",
        "ETF":   "var(--purple)",
        "BDR":   "var(--amber)",
        "Opção": "var(--red2)",
    }
    for cat, exp in sorted(cat_exp.items(), key=lambda x: x[1], reverse=True):
        pct   = exp / total_exp * 100 if total_exp > 0 else 0.0
        color = cat_colors.get(cat, "var(--blue2)")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:6px 0">
          <div style="width:60px;font-size:11px;color:var(--text2)">{cat}</div>
          <div style="flex:1;height:5px;background:var(--bg4);border-radius:3px;overflow:hidden">
            <div style="width:{pct:.1f}%;height:100%;background:{color};border-radius:3px"></div>
          </div>
          <div style="width:44px;text-align:right;font-size:11px;font-family:var(--mono);color:var(--text2)">{pct:.1f}%</div>
          <div style="width:110px;text-align:right;font-size:11px;font-family:var(--mono);color:var(--text3)">{_fmt_brl(exp)}</div>
        </div>""", unsafe_allow_html=True)
