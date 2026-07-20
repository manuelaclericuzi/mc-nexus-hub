"""
MC Atelier — Componentes editoriais reutilizáveis
"""
import datetime
import streamlit as st


# ── Topbar (data + marcações) ────────────────────────────────────
_MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
          "jul", "ago", "set", "out", "nov", "dez"]
_DIAS  = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def topbar():
    now = datetime.datetime.now()
    label = f"{_DIAS[now.weekday()]}, {now.day:02d} {_MESES[now.month-1]}".upper()
    st.markdown(f"""
    <div class="topbar">
      <div class="date">{label}</div>
      <div class="marks">✦ &nbsp; ◷</div>
    </div>
    """, unsafe_allow_html=True)


# ── Section header ───────────────────────────────────────────────
def sec_header(title: str, subtitle: str = "", link: str = ""):
    sub  = f'<div class="sec-sub">{subtitle}</div>' if subtitle else ""
    lnk  = f'<span class="sec-link">{link}</span>' if link else ""
    st.markdown(f"""
    <div class="sec-head" style="margin-bottom:26px;">
      <div>
        <div class="sec-title">{title}</div>
        {sub}
      </div>
      {lnk}
    </div>
    """, unsafe_allow_html=True)


# ── Eyebrow ──────────────────────────────────────────────────────
def eyebrow(text: str):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)


# ── Divider ──────────────────────────────────────────────────────
def divider():
    st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── Image placeholder tile (garment / look) ──────────────────────
def tile(tone: str, mono: str = "", badge: str = "", ratio: str = "3 / 4",
         photo: str = "") -> str:
    """
    Retorna HTML de um tile de imagem. Se `photo` (data URI) for informado,
    usa a foto real; senão, um placeholder tonal editorial.
    """
    badge_html = f'<div class="tile-badge">{badge}</div>' if badge else ""
    if photo:
        # Peça recortada (PNG com transparência) → mostra "flutuando" inteira
        # sobre um fundo suave; foto normal (JPEG) → preenche o tile.
        recortada = photo.startswith("data:image/png")
        size = "contain" if recortada else "cover"
        fundo = "background-color:var(--panel);" if recortada else ""
        pad = "padding:10px;" if recortada else ""
        return (f'<div class="tile" style="aspect-ratio:{ratio};{fundo}{pad}'
                f'background-image:url({photo});background-size:{size};'
                f'background-position:center;background-repeat:no-repeat;">'
                f'{badge_html}</div>')
    grad = f"linear-gradient(150deg, {tone} 0%, {_darken(tone, .18)} 100%)"
    mono_html = f'<div class="tile-mono">{mono}</div>' if mono else ""
    return (f'<div class="tile" style="aspect-ratio:{ratio};background:{grad};">'
            f'{badge_html}{mono_html}</div>')


def garment_card(brand: str, name: str, price: str = "",
                 tone: str = "#3a3c40", mono: str = "", badge: str = "", photo: str = ""):
    price_html = f'<div class="g-price">{price}</div>' if price else ""
    st.markdown(f"""
    <div>
      {tile(tone, mono, badge, photo=photo)}
      <div class="g-brand">{brand}</div>
      <div class="g-name">{name}</div>
      {price_html}
    </div>
    """, unsafe_allow_html=True)


# ── Checklist item ───────────────────────────────────────────────
def check_item(title: str, desc: str, filled: bool = True):
    mark = "●" if filled else "○"
    st.markdown(f"""
    <div class="chk-item">
      <div class="chk-mark">{mark}</div>
      <div>
        <div class="chk-title">{title}</div>
        <div class="chk-desc">{desc}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Chip ─────────────────────────────────────────────────────────
def chip(text: str, variant: str = "") -> str:
    cls = "chip" + (f" chip-{variant}" if variant else "")
    return f'<span class="{cls}">{text}</span>'


# ── Do / Don't row ───────────────────────────────────────────────
def dd_row(text: str, yes: bool = True) -> str:
    mark = "✓" if yes else "✕"
    cls  = "yes" if yes else "no"
    return (f'<div class="dd-row"><div class="dd-mark {cls}">{mark}</div>'
            f'<div class="dd-text">{text}</div></div>')


# ── Helpers de cor ───────────────────────────────────────────────
def _darken(hex_color: str, amount: float) -> str:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return "#" + hex_color
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    return f"#{r:02x}{g:02x}{b:02x}"
