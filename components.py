"""
MC Nexus Hub — Componentes reutilizáveis
Design system fiel ao nexus-capital_1.html
"""
import streamlit as st


# ── Metric card com strip colorida ──────────────────────────────
def metric_card(label: str, value: str, delta: str = "",
                color: str = "blue", negative: bool = False):
    """
    color: 'blue' | 'green' | 'red' | 'amber'
    negative: se True, força color='red'
    """
    if negative:
        color = "red"
    delta_cls  = ""
    delta_html = ""
    if delta:
        if delta.startswith("▲") or delta.startswith("+"):
            delta_cls = "pos"
        elif delta.startswith("▼") or delta.startswith("-"):
            delta_cls = "neg"
        else:
            delta_cls = "neu"
        delta_html = f'<div class="metric-delta {delta_cls}">{delta}</div>'

    st.markdown(f"""
    <div class="metric-card m-{color}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# ── Divider ──────────────────────────────────────────────────────
def divider():
    st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── Section header ───────────────────────────────────────────────
def sec_header(title: str, subtitle: str = ""):
    sub = f'<div class="sec-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="sec-head" style="margin-bottom:16px;">
      <div>
        <div class="sec-title">{title}</div>
        {sub}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Progress bar ─────────────────────────────────────────────────
def progress_bar(title: str, realizado: float, meta: float,
                 fmt_fn=None, color: str = "#2288ee"):
    pct    = min(realizado / meta * 100, 100) if meta > 0 else 0
    fmt    = fmt_fn or (lambda v: f"{v:,.0f}")
    status_color = (
        "var(--green)" if pct >= 80
        else "var(--amber)" if pct >= 50
        else "var(--red)"
    )
    st.markdown(f"""
    <div class="prog-wrap">
      <div class="prog-title">
        <span style="color:var(--text2);">{title}</span>
        <span style="font-family:var(--mono);font-size:11px;color:{status_color};">{pct:.1f}%</span>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:11px;
                  font-family:var(--mono);color:var(--text3);margin-bottom:8px;">
        <span>{fmt(realizado)}</span>
        <span>meta {fmt(meta)}</span>
      </div>
      <div class="prog-bar-bg">
        <div class="prog-bar-fg" style="width:{pct}%;background:{color};"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Info box (insight / alerta) ──────────────────────────────────
def info_box(text: str, variant: str = "blue"):
    """variant: blue | green | amber | red"""
    st.markdown(f'<div class="info-box {variant}">{text}</div>',
                unsafe_allow_html=True)


# ── Alert row ────────────────────────────────────────────────────
def alert_row(icon: str, text: str, variant: str = "info"):
    """variant: info | warn | danger | ok"""
    cls_map = {"info": "al-info", "warn": "al-warn",
               "danger": "al-danger", "ok": "al-ok"}
    cls = cls_map.get(variant, "al-info")
    st.markdown(f"""
    <div class="alert-row {cls}">
      <span style="font-size:16px;flex-shrink:0;margin-top:1px;">{icon}</span>
      <p style="font-size:12px;color:var(--text2);line-height:1.6;margin:0;">{text}</p>
    </div>
    """, unsafe_allow_html=True)


# ── Status badge ─────────────────────────────────────────────────
def status_badge(status: str) -> str:
    css = "badge-ativo" if status == "Ativo" else "badge-inativo"
    return f'<span class="badge {css}">{status}</span>'


# ── Topbar (logo + live pill) ─────────────────────────────────────
def topbar(page_name: str = ""):
    import datetime
    hora = datetime.datetime.now().strftime("%H:%M")
    right = f'<span style="font-family:var(--mono);font-size:11px;color:var(--text3);">{hora}</span>'
    if page_name:
        right = f'<span style="font-size:12px;color:var(--text2);">{page_name}</span>&nbsp;&nbsp;' + right
    st.markdown(f"""
    <div class="topbar-custom">
      <div style="display:flex;align-items:center;gap:12px;">
        <div class="logo-text">NEXUS <em>Hub</em></div>
        <div class="live-pill">LIVE</div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">{right}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Insight card (tag + texto) ───────────────────────────────────
def insight_card(tag: str, text: str):
    tag_colors = {
        "Retenção":            ("var(--blue-bg)",   "var(--blue)",   "var(--blue-border)"),
        "Rentabilidade":       ("var(--green-bg)",  "var(--green)",  "var(--green-border)"),
        "Alerta de Meta":      ("var(--red-bg)",    "var(--red)",    "var(--red-border)"),
        "Oportunidade":        ("var(--green-bg)",  "var(--green)",  "var(--green-border)"),
        "Risco de Concentração":("var(--amber-bg)", "var(--amber)",  "var(--amber-border)"),
        "Boas Práticas":       ("var(--blue-bg)",   "var(--blue)",   "var(--blue-border)"),
    }
    bg, color, border = tag_colors.get(tag, ("var(--blue-bg)", "var(--blue)", "var(--blue-border)"))
    st.markdown(f"""
    <div style="background:var(--bg3);border:1px solid var(--border2);border-radius:var(--radius-lg);
                padding:14px 16px;margin-bottom:10px;display:flex;gap:12px;align-items:flex-start;">
      <span style="background:{bg};color:{color};border:1px solid {border};padding:2px 8px;
                   border-radius:20px;font-size:10px;font-weight:700;white-space:nowrap;
                   margin-top:1px;flex-shrink:0">{tag}</span>
      <p style="font-size:12px;color:var(--text2);line-height:1.7;margin:0">{text}</p>
    </div>""", unsafe_allow_html=True)


# ── Aliases para compatibilidade com pages existentes ────────────
def gold_divider():
    """Alias de divider() — mantido para compatibilidade."""
    st.markdown('<hr class="divider">', unsafe_allow_html=True)


def section_title(title: str, subtitle: str = ""):
    """Alias de sec_header() — mantido para compatibilidade."""
    sec_header(title, subtitle)


# ── Ticker tag (badge mono com borda) ─────────────────────────────
def ticker_tag(ticker: str) -> str:
    return f'<span class="ticker-tag">{ticker}</span>'


# ── Category tag (badge colorido por tipo) ───────────────────────
_CAT_CLS = {
    "Ação": "ct-acao", "FII": "ct-fii", "ETF": "ct-etf",
    "BDR": "ct-bdr",   "Opção": "ct-opcao",
}

def cat_tag(cat: str) -> str:
    cls = _CAT_CLS.get(cat, "ct-acao")
    return f'<span class="cat-tag {cls}">{cat}</span>'


# ── Tabela HTML customizada ───────────────────────────────────────
def html_table(headers: list[str], rows: list[list[str]],
               right_cols: list[int] | None = None):
    right_cols = right_cols or []
    th_style = ("padding:9px 14px;text-align:left;font-size:10px;font-weight:600;"
                "color:var(--text3);letter-spacing:.5px;text-transform:uppercase;"
                "border-bottom:1px solid var(--border2);white-space:nowrap;")
    td_style = ("padding:10px 14px;font-size:12px;border-bottom:1px solid var(--border);"
                "color:var(--text2);vertical-align:middle;white-space:nowrap;")

    ths = "".join(
        f'<th style="{th_style}{"text-align:right;" if i in right_cols else ""}">{h}</th>'
        for i, h in enumerate(headers)
    )
    trs = ""
    for row in rows:
        tds = "".join(
            f'<td style="{td_style}{"text-align:right;" if i in right_cols else ""}">{cell}</td>'
            for i, cell in enumerate(row)
        )
        trs += f'<tr onmouseover="this.style.background=\'var(--bg3)\'" onmouseout="this.style.background=\'\'">{tds}</tr>'

    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border2);
                border-radius:var(--radius-lg);overflow:hidden;">
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead><tr style="background:var(--bg2);">{ths}</tr></thead>
          <tbody>{trs}</tbody>
        </table>
      </div>
    </div>
    """, unsafe_allow_html=True)
