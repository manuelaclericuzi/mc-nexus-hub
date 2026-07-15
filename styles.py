"""
MC Atelier — Design system editorial
Baseado nas telas "Atelier Digital" (Google Stitch).
Paleta: Bone / Preto / Champagne  |  Fontes: Playfair Display + Hanken Grotesk
"""

CSS = """
<style>
/* ── Fonts ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap');

/* ── Tokens ────────────────────────────────────────────────── */
:root {
  --bone:      #f9f9f9;
  --paper:     #ffffff;
  --panel:     #f3f3f4;
  --ink:       #1a1c1c;
  --muted:     #44474d;
  --faint:     #75777e;
  --line:      #e2e2e2;
  --line2:     #c5c6cd;
  --line-soft: #eeeeee;
  --black:     #000000;
  --navy:      #0d1c32;
  --gold:      #8a6a1f;
  --gold-soft: #fed488;
  --serif: 'Playfair Display', Georgia, serif;
  --sans:  'Hanken Grotesk', system-ui, -apple-system, sans-serif;
}

/* ── Base ──────────────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
  font-family: var(--sans) !important;
  background-color: var(--bone) !important;
  color: var(--ink) !important;
}
.stApp { background: var(--bone) !important; }

/* Hide Streamlit chrome for an app feel */
#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] {
  background: transparent !important;
  height: 0 !important;
}
[data-testid="stToolbar"] { right: 8px; }

/* Main content width / padding */
.block-container {
  max-width: 1360px !important;
  padding: 28px 40px 64px !important;
}

/* ── Typography ────────────────────────────────────────────── */
h1, h2, h3, h4 {
  font-family: var(--serif) !important;
  color: var(--ink) !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em;
}
p, span, div, label, li { font-family: var(--sans); }

/* Editorial helpers */
.eyebrow {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--faint);
}
.serif-xl { font-family: var(--serif); font-size: 44px; line-height: 1.05; font-weight: 700; letter-spacing: -0.02em; }
.serif-lg { font-family: var(--serif); font-size: 30px; line-height: 1.15; font-weight: 600; }
.serif-md { font-family: var(--serif); font-size: 22px; line-height: 1.25; font-weight: 600; }
.italic   { font-style: italic; }
.mono-num { font-variant-numeric: tabular-nums; }

/* ── Sidebar ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--paper) !important;
  border-right: 1px solid var(--line) !important;
  width: 264px !important;
}
section[data-testid="stSidebar"] > div { padding-top: 8px; }

.side-brand {
  font-family: var(--serif);
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--black);
  line-height: 1.1;
  text-transform: uppercase;
}
.side-tag {
  font-family: var(--sans);
  font-size: 9.5px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--faint);
  margin-top: 6px;
}
.side-label {
  font-family: var(--sans);
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--faint);
  padding: 4px 6px 6px;
}

/* Sidebar nav buttons */
section[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  color: var(--muted) !important;
  border: none !important;
  border-left: 2px solid transparent !important;
  border-radius: 0 !important;
  text-align: left !important;
  font-family: var(--sans) !important;
  font-size: 12.5px !important;
  font-weight: 600 !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  padding: 9px 12px !important;
  width: 100% !important;
  transition: color .15s, border-color .15s, background .15s;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  color: var(--black) !important;
  background: var(--bone) !important;
}
/* Active nav (primary) */
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  color: var(--black) !important;
  font-weight: 700 !important;
  border-left: 2px solid var(--black) !important;
  background: transparent !important;
}

/* ── Buttons (main content) ────────────────────────────────── */
.stButton > button {
  background: var(--black) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 0 !important;
  font-family: var(--sans) !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  padding: 12px 26px !important;
  transition: opacity .15s, background .15s;
}
.stButton > button:hover { opacity: .82 !important; }
.stButton > button[kind="secondary"] {
  background: transparent !important;
  color: var(--ink) !important;
  border: 1px solid var(--line2) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: var(--black) !important;
  opacity: 1 !important;
}

/* ── Cards / surfaces ──────────────────────────────────────── */
.card {
  background: var(--paper);
  border: 1px solid var(--line);
  padding: 32px;
}
.card-flush { background: var(--paper); border: 1px solid var(--line); }
.panel-dark { background: var(--black); color: #fff; }
.panel-soft { background: var(--panel); border: 1px solid var(--line); }

.hr-line { border: none; border-top: 1px solid var(--line); margin: 0; }
.divider { border: none; border-top: 1px solid var(--line); margin: 20px 0; }

/* ── Section header ────────────────────────────────────────── */
.sec-head { display:flex; align-items:flex-end; justify-content:space-between; gap:18px; }
.sec-title { font-family: var(--serif); font-size: 30px; font-weight: 600; color: var(--ink); letter-spacing: -0.01em; }
.sec-sub  { font-family: var(--sans); font-size: 13px; color: var(--muted); margin-top: 8px; max-width: 62ch; line-height: 1.6; }
.sec-link { font-family: var(--sans); font-size: 11px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--ink); border-bottom: 1px solid var(--ink); padding-bottom: 3px; }

/* ── Topbar ────────────────────────────────────────────────── */
.topbar {
  display:flex; align-items:center; justify-content:space-between;
  border-bottom: 1px solid var(--line);
  padding: 0 2px 16px;
  margin-bottom: 32px;
}
.topbar .date { font-family: var(--sans); font-size: 11px; letter-spacing: 0.24em; text-transform: uppercase; color: var(--faint); }
.topbar .marks { display:flex; gap:18px; color: var(--faint); font-size: 18px; }

/* ── Checklist item ────────────────────────────────────────── */
.chk-item { display:flex; gap:14px; align-items:flex-start; margin-bottom: 22px; }
.chk-mark { flex:none; width:20px; height:20px; color: var(--black); font-size: 18px; line-height:1; }
.chk-title { font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink); margin-bottom: 4px; }
.chk-desc  { font-family: var(--sans); font-size: 13px; color: var(--muted); line-height: 1.55; }

/* ── Garment / image placeholder tile ─────────────────────── */
.tile {
  position: relative;
  width: 100%;
  aspect-ratio: 3 / 4;
  display: grid;
  place-items: center;
  overflow: hidden;
  border: 1px solid var(--line);
}
.tile-mono { font-family: var(--serif); font-size: 30px; font-style: italic; color: #ffffff; opacity: .92; letter-spacing: .04em; }
.tile-badge {
  position:absolute; top:14px; right:14px;
  background: rgba(255,255,255,.92); color: var(--ink);
  font-size: 9.5px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase;
  padding: 5px 10px;
}
.g-brand { font-family: var(--sans); font-size: 10.5px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--ink); margin-top: 16px; }
.g-name  { font-family: var(--sans); font-size: 13px; color: var(--muted); margin-top: 4px; }
.g-price { font-family: var(--sans); font-size: 13px; font-weight: 700; color: var(--ink); margin-top: 8px; }

/* ── Agenda row ────────────────────────────────────────────── */
.agenda-row { display:flex; align-items:center; gap:20px; padding: 20px 0; border-top: 1px solid var(--line); }
.agenda-time { font-family: var(--serif); font-size: 18px; color: var(--muted); width: 74px; font-variant-numeric: tabular-nums; }
.agenda-title { font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink); }
.agenda-meta  { font-family: var(--sans); font-size: 13px; font-style: italic; color: var(--muted); margin-top: 3px; }

/* ── Swatch ────────────────────────────────────────────────── */
.sw-grid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.sw { border: 1px solid var(--line); }
.sw-color { height: 64px; }
.sw-meta { padding: 10px 12px; }
.sw-name { font-family: var(--sans); font-size: 12px; font-weight: 600; color: var(--ink); }
.sw-hex  { font-family: var(--sans); font-size: 10.5px; color: var(--faint); margin-top: 2px; letter-spacing: .04em; }

/* ── Chips / tags ──────────────────────────────────────────── */
.chip {
  display:inline-block;
  font-family: var(--sans); font-size: 10px; font-weight: 600;
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 4px 10px; border: 1px solid var(--ink); color: var(--ink);
  margin: 0 6px 6px 0;
}
.chip-soft { border-color: var(--line2); color: var(--muted); }
.chip-gold { border-color: var(--gold); color: var(--gold); }

/* ── Do / Don't lists ──────────────────────────────────────── */
.dd-row { display:flex; gap:12px; align-items:flex-start; margin-bottom: 14px; }
.dd-mark { flex:none; font-family: var(--serif); font-size: 16px; line-height: 1.3; width: 16px; }
.dd-mark.yes { color: var(--ink); }
.dd-mark.no  { color: var(--faint); }
.dd-text { font-family: var(--sans); font-size: 13.5px; color: var(--muted); line-height: 1.55; }

/* ── Occasion table ────────────────────────────────────────── */
.occ-table { width:100%; border-collapse: collapse; }
.occ-table th {
  text-align:left; font-family: var(--sans); font-size: 10px; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase; color: var(--faint);
  padding: 0 16px 14px; border-bottom: 1px solid var(--ink);
}
.occ-table td {
  padding: 18px 16px; font-family: var(--sans); font-size: 13.5px; color: var(--muted);
  border-bottom: 1px solid var(--line); vertical-align: top; line-height: 1.55;
}
.occ-table td b { color: var(--ink); font-weight: 600; }

/* ── Stat ──────────────────────────────────────────────────── */
.stat-num { font-family: var(--serif); font-size: 46px; font-weight: 700; line-height: 1; letter-spacing: -0.02em; }
.stat-lab { font-family: var(--sans); font-size: 10px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; }

/* ── Inputs ────────────────────────────────────────────────── */
input, textarea, select,
[data-baseweb="input"] input, [data-baseweb="select"] div, [data-baseweb="textarea"] textarea {
  background: var(--paper) !important;
  border-radius: 0 !important;
  color: var(--ink) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
}
[data-baseweb="input"], [data-baseweb="textarea"] {
  background: var(--paper) !important;
  border: none !important;
  border-bottom: 1px solid var(--line2) !important;
  border-radius: 0 !important;
}
[data-baseweb="select"] > div {
  background: var(--paper) !important;
  border: none !important;
  border-bottom: 1px solid var(--line2) !important;
  border-radius: 0 !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stTextArea label, .stMultiSelect label, .stDateInput label {
  font-family: var(--sans) !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: var(--faint) !important;
}

/* ── Scrollbar ─────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bone); }
::-webkit-scrollbar-thumb { background: var(--line); }

.blk { margin-bottom: 20px; }

/* ── Tabs (editorial) ──────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  gap: 34px;
  border-bottom: 1px solid var(--line) !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: var(--sans) !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: var(--faint) !important;
  padding: 4px 0 16px !important;
  background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--ink) !important; }
.stTabs [aria-selected="true"] { color: var(--ink) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--ink) !important; height: 2px !important; }
.stTabs [data-baseweb="tab-border"] { background: transparent !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 34px; }

/* ── Expander (seção recolhível) ───────────────────────────── */
[data-testid="stExpander"] {
  border: 1px solid var(--line) !important;
  border-radius: 0 !important;
  background: var(--paper) !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] details > summary {
  font-family: var(--sans) !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: var(--ink) !important;
  padding: 16px 20px !important;
}
[data-testid="stExpander"] summary:hover { color: var(--muted) !important; }

/* ── Extra breathing room ──────────────────────────────────── */
.block-container { padding-top: 24px !important; }
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)
