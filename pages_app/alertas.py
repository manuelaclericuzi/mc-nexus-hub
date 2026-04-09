"""Página: Alertas de Preço — Monitoramento de níveis de entrada/saída"""
import streamlit as st
from components import gold_divider, section_title, ticker_tag
from data import fetch_quotes


def _fmt_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _th(label: str, right: bool = False) -> str:
    align = "right" if right else "left"
    return (
        f'<th style="padding:9px 14px;text-align:{align};font-size:10px;font-weight:600;'
        f'color:var(--text3);letter-spacing:.5px;text-transform:uppercase;'
        f'border-bottom:1px solid var(--border2);white-space:nowrap">{label}</th>'
    )


def _check_alertas(alertas: list, quotes: dict) -> None:
    """Marca alertas como disparados conforme cotações atuais."""
    for a in alertas:
        if a.get("triggered"):
            continue
        q = quotes.get(a["ticker"])
        if not q:
            continue
        price = q["price"]
        if a["direcao"] == "Acima de" and price >= a["preco_alvo"]:
            a["triggered"] = True
        elif a["direcao"] == "Abaixo de" and price <= a["preco_alvo"]:
            a["triggered"] = True


def render():
    section_title("Alertas de Preço", "Monitoramento de níveis de entrada e saída")
    gold_divider()

    alertas  = st.session_state.alertas
    clientes = st.session_state.clientes

    # ── KPIs ──────────────────────────────────────────────────────
    n_ativos    = sum(1 for a in alertas if not a.get("triggered"))
    n_disparados = sum(1 for a in alertas if a.get("triggered"))

    k1, k2, k3 = st.columns(3)
    k1.markdown(f"""<div class="metric-card m-blue">
        <div class="metric-label">Alertas Ativos</div>
        <div class="metric-value">{n_ativos}</div>
    </div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="metric-card m-amber">
        <div class="metric-label">Disparados</div>
        <div class="metric-value">{n_disparados}</div>
    </div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="metric-card">
        <div class="metric-label">Total</div>
        <div class="metric-value">{len(alertas)}</div>
    </div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Novo Alerta ───────────────────────────────────────────────
    col_btn, _ = st.columns([2, 5])
    with col_btn:
        novo = st.button("+ Novo Alerta", use_container_width=True)

    if novo or st.session_state.get("show_form_alerta"):
        st.session_state["show_form_alerta"] = True
        st.markdown("<h3>Criar Alerta</h3>", unsafe_allow_html=True)

        with st.form("form_alerta", clear_on_submit=True):
            fc1, fc2, fc3 = st.columns(3)
            ticker     = fc1.text_input("Ticker *", placeholder="ex: PETR4").upper().strip()
            direcao    = fc2.selectbox("Disparar quando", ["Acima de", "Abaixo de"])
            preco_alvo = fc3.number_input("Preço Alvo (R$) *", min_value=0.01, step=0.01, format="%.2f")

            nomes_c   = ["— Nenhum —"] + [c["nome"] for c in clientes]
            cliente_s = st.selectbox("Cliente relacionado (opcional)", nomes_c)
            obs       = st.text_input("Observação", placeholder="Opcional")

            submitted = st.form_submit_button("Criar Alerta")
            if submitted:
                if not ticker or preco_alvo <= 0:
                    st.error("Ticker e preço alvo são obrigatórios.")
                else:
                    novo_id = max((a["id"] for a in alertas), default=0) + 1
                    cid     = None
                    if cliente_s != "— Nenhum —":
                        cid = next((c["id"] for c in clientes if c["nome"] == cliente_s), None)
                    st.session_state.alertas.append({
                        "id":         novo_id,
                        "ticker":     ticker,
                        "direcao":    direcao,
                        "preco_alvo": preco_alvo,
                        "client_id":  cid,
                        "obs":        obs,
                        "triggered":  False,
                    })
                    st.session_state.pop("show_form_alerta", None)
                    dir_sym = "▲" if direcao == "Acima de" else "▼"
                    st.success(f"Alerta criado: {ticker} {dir_sym} {_fmt_brl(preco_alvo)}")
                    st.rerun()

    gold_divider()

    # ── Checar cotações e atualizar status ────────────────────────
    if alertas:
        tks_ativos = tuple(sorted({a["ticker"] for a in alertas if not a.get("triggered")}))
        if tks_ativos:
            quotes = fetch_quotes(tks_ativos)
            _check_alertas(alertas, quotes)

    # ── Tabela ─────────────────────────────────────────────────────
    st.markdown("<h3>Alertas Configurados</h3>", unsafe_allow_html=True)

    if not alertas:
        st.markdown("""<div style="text-align:center;padding:40px;color:var(--text3)">
            <div style="font-size:28px;opacity:.3">◎</div>
            <div style="font-size:12px;margin-top:8px">Nenhum alerta configurado.</div>
        </div>""", unsafe_allow_html=True)
        return

    # Cotações para todos os alertas (para exibir preço atual)
    all_tks = tuple(sorted({a["ticker"] for a in alertas}))
    quotes  = fetch_quotes(all_tks) if all_tks else {}

    cl_map = {c["id"]: c["nome"] for c in clientes}
    rows   = ""
    for a in reversed(alertas):
        q           = quotes.get(a["ticker"])
        preco_atual = (
            f'<span class="vq">{_fmt_brl(q["price"])}</span>'
            if q else '<span style="color:var(--text3)">—</span>'
        )
        if a.get("triggered"):
            status_html = (
                '<span style="background:var(--amber-bg);color:var(--amber);'
                'border:1px solid var(--amber-border);padding:2px 8px;'
                'border-radius:20px;font-size:10px;font-weight:600">DISPARADO</span>'
            )
        else:
            status_html = (
                '<span style="background:var(--blue-bg);color:var(--blue);'
                'border:1px solid var(--blue-border);padding:2px 8px;'
                'border-radius:20px;font-size:10px;font-weight:600">ATIVO</span>'
            )
        dir_cls = "vp" if a["direcao"] == "Acima de" else "vn"
        dir_sym = "▲" if a["direcao"] == "Acima de" else "▼"

        rows += f"""<tr>
            <td>{ticker_tag(a['ticker'])}</td>
            <td class="{dir_cls}">{dir_sym} {a['direcao']}</td>
            <td class="r vq">{_fmt_brl(a['preco_alvo'])}</td>
            <td class="r">{preco_atual}</td>
            <td style="color:var(--text2)">{cl_map.get(a.get('client_id'), '—')}</td>
            <td style="color:var(--text3);font-size:11px">{a.get('obs', '')}</td>
            <td>{status_html}</td>
        </tr>"""

    headers = [
        ("Ticker", False), ("Condição", False),
        ("Preço Alvo", True), ("Cotação", True),
        ("Cliente", False), ("Obs", False), ("Status", False),
    ]
    ths = "".join(_th(h, r) for h, r in headers)

    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border2);border-radius:var(--radius-lg);overflow:hidden;">
      <div style="overflow-x:auto;">
        <table class="rv-table"><thead><tr>{ths}</tr></thead><tbody>{rows}</tbody></table>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Limpar disparados ─────────────────────────────────────────
    if n_disparados:
        gold_divider()
        rc1, _ = st.columns([2, 5])
        with rc1:
            if st.button(f"Limpar {n_disparados} alerta(s) disparado(s)", use_container_width=True):
                st.session_state.alertas = [a for a in st.session_state.alertas if not a.get("triggered")]
                st.rerun()
