"""Página: Cotações — Preços ao vivo via Brapi"""
import streamlit as st
from components import gold_divider, section_title
from data import fetch_quotes

_DEFAULT_WATCHLIST = ["PETR4", "VALE3", "ITUB4", "BBAS3", "BOVA11", "HGLG11", "XPML11", "WEGE3"]


def _fmt_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render():
    section_title("Cotações", "Preços ao vivo via Brapi — B3")
    gold_divider()

    if "watchlist" not in st.session_state:
        st.session_state.watchlist = list(_DEFAULT_WATCHLIST)

    # ── Controles ─────────────────────────────────────────────────
    wc1, wc2, wc3 = st.columns([3, 1, 1])
    novo_ticker = wc1.text_input(
        "Adicionar ticker", placeholder="ex: MGLU3",
        label_visibility="collapsed",
    ).upper().strip()
    add_btn     = wc2.button("Adicionar", use_container_width=True)
    refresh_btn = wc3.button("⟳ Atualizar", use_container_width=True)

    if add_btn and novo_ticker:
        if novo_ticker not in st.session_state.watchlist:
            st.session_state.watchlist.append(novo_ticker)
            fetch_quotes.clear()
            st.rerun()
        else:
            st.warning(f"{novo_ticker} já está na watchlist.")

    if refresh_btn:
        fetch_quotes.clear()
        st.rerun()

    # ── Busca ─────────────────────────────────────────────────────
    tickers = tuple(st.session_state.watchlist)
    quotes  = fetch_quotes(tickers) if tickers else {}

    n_ok  = sum(1 for t in tickers if t in quotes)
    n_err = len(tickers) - n_ok
    status_txt = f"{n_ok} com dados"
    if n_err:
        status_txt += f" · {n_err} sem resposta"
    st.markdown(
        f"<p style='color:var(--text3);font-size:11px;margin:4px 0 12px'>"
        f"{len(tickers)} ativos monitorados &nbsp;·&nbsp; {status_txt}</p>",
        unsafe_allow_html=True,
    )

    # ── Cards em grid de 4 ────────────────────────────────────────
    row_size = 4
    for i in range(0, len(tickers), row_size):
        chunk = tickers[i: i + row_size]
        cols  = st.columns(row_size)
        for j, ticker in enumerate(chunk):
            q = quotes.get(ticker)
            if q:
                chg     = q["change_pct"]
                chg_cls = "vp" if chg >= 0 else "vn"
                chg_sym = "▲" if chg >= 0 else "▼"
                price_s = _fmt_brl(q["price"])
                chg_s   = f"{chg_sym} {abs(chg):.2f}%"
            else:
                chg_cls = "neu"
                price_s = "—"
                chg_s   = "Sem dados"

            cols[j].markdown(f"""
            <div class="qcard">
              <div class="qcard-ticker">{ticker}</div>
              <div class="qcard-price">{price_s}</div>
              <div class="qcard-chg {chg_cls}">{chg_s}</div>
            </div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Gerenciar watchlist ───────────────────────────────────────
    st.markdown("<h3>Gerenciar Watchlist</h3>", unsafe_allow_html=True)
    remover = st.multiselect(
        "Selecionar tickers para remover",
        options=list(tickers),
        label_visibility="collapsed",
    )
    rc1, _ = st.columns([2, 5])
    with rc1:
        if st.button("Remover Selecionados", use_container_width=True) and remover:
            st.session_state.watchlist = [t for t in st.session_state.watchlist if t not in remover]
            fetch_quotes.clear()
            st.rerun()
