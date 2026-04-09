"""
MC Nexus Hub — CSS fiel ao design system do nexus-capital_1.html
Paleta: Dark Navy/Blue + Green/Red/Amber  |  Fontes: Syne + DM Mono
"""

CSS = """
<style>
/* ── Google Fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;500;600;700;800&display=swap');

/* ── CSS Variables (idênticas ao HTML de referência) ─────── */
:root {
  --bg:    #07090d;
  --bg2:   #0d1117;
  --bg3:   #141923;
  --bg4:   #1a2030;
  --bg5:   #202840;
  --border:  #ffffff0a;
  --border2: #ffffff14;
  --border3: #ffffff20;
  --text:  #e2e8f4;
  --text2: #7a88a0;
  --text3: #3d4a5c;
  --green:  #00e09a;  --green2:  #00b37a;
  --green-bg: #00e09a10; --green-border: #00e09a25;
  --red:    #ff4466;  --red2:    #cc2244;
  --red-bg: #ff446610; --red-border: #ff446625;
  --blue:   #4da6ff;  --blue2:   #2288ee;
  --blue-bg:#4da6ff10; --blue-border:#4da6ff25;
  --amber:  #ffaa33;
  --amber-bg:#ffaa3310; --amber-border:#ffaa3325;
  --purple: #b388ff;  --purple-bg:#b388ff10;
  --radius:8px; --radius-lg:12px; --radius-xl:18px;
  --font:'Syne',sans-serif; --mono:'DM Mono',monospace;
}

/* ── Reset / base ─────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
  font-family: var(--font) !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border2) !important;
}
section[data-testid="stSidebar"] * { color: var(--text2) !important; }

/* ── Títulos ──────────────────────────────────────────────── */
h1, h2, h3 {
  font-family: var(--font) !important;
  font-weight: 700 !important;
  letter-spacing: -0.3px;
  color: var(--text) !important;
}
h1 { font-size: 1.5rem !important; }
h2 { font-size: 1.2rem !important; }
h3 { font-size: 1rem !important; }

/* ── Metric card (strip colorida no topo) ─────────────────── */
.metric-card {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: var(--radius-lg);
  padding: 16px;
  position: relative;
  overflow: hidden;
  min-width: 0;
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.metric-card.m-blue::before  { background: var(--blue2); }
.metric-card.m-green::before { background: var(--green2); }
.metric-card.m-red::before   { background: var(--red2); }
.metric-card.m-amber::before { background: var(--amber); }

.metric-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text3);
  letter-spacing: .5px;
  text-transform: uppercase;
  margin-bottom: 8px;
  line-height: 1.3;
}
.metric-value {
  font-size: 20px;
  font-weight: 700;
  font-family: var(--mono);
  letter-spacing: -1px;
  line-height: 1;
  color: var(--text);
}
.metric-delta {
  font-size: 11px;
  font-family: var(--mono);
  margin-top: 5px;
  color: var(--text3);
}
.metric-delta.pos { color: var(--green); }
.metric-delta.neg { color: var(--red); }

/* ── Cards ────────────────────────────────────────────────── */
.card {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: var(--radius-lg);
}
.card-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border2);
}
.card-title { font-size: 12px; font-weight: 700; color: var(--text); }
.card-body  { padding: 16px; }

.inner-card {
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: var(--radius-lg);
  padding: 16px;
}
.inner-card.green  { border-color: var(--green-border); }
.inner-card.blue   { border-color: var(--blue-border); }
.inner-card.amber  { border-color: var(--amber-border); }
.inner-card.red    { border-color: var(--red-border); }

/* ── Info-box (insight) ────────────────────────────────────── */
.info-box {
  background: var(--bg3);
  border-radius: var(--radius);
  padding: 10px 12px;
  font-size: 12px;
  color: var(--text2);
  line-height: 1.6;
}
.info-box.green { border-left: 3px solid var(--green); }
.info-box.amber { border-left: 3px solid var(--amber); }
.info-box.blue  { border-left: 3px solid var(--blue);  }
.info-box.red   { border-left: 3px solid var(--red);   }

/* ── Tabelas ──────────────────────────────────────────────── */
.stDataFrame thead th {
  background: var(--bg3) !important;
  color: var(--text3) !important;
  font-size: 10px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: .5px !important;
}
.stDataFrame tbody td { font-size: 12px !important; }
.stDataFrame tbody tr:hover td { background: var(--bg3) !important; }

/* ── Botões ────────────────────────────────────────────────── */
.stButton > button {
  background: var(--blue2) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-family: var(--font) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  padding: 7px 16px !important;
  transition: opacity .15s;
}
.stButton > button:hover { opacity: .85 !important; }

.btn-ghost > button {
  background: var(--bg3) !important;
  color: var(--text2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
}
.btn-ghost > button:hover {
  border-color: var(--border3) !important;
  color: var(--text) !important;
}

/* ── Inputs / selects ─────────────────────────────────────── */
input, textarea, select,
[data-baseweb="input"] input,
[data-baseweb="select"] div {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font) !important;
  font-size: 12px !important;
}
[data-baseweb="input"] input:focus {
  border-color: var(--blue2) !important;
  box-shadow: 0 0 0 3px var(--blue-bg) !important;
}
.stSelectbox label,
.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stSlider label {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: var(--text2) !important;
  letter-spacing: .3px !important;
}

/* ── Progress bar ─────────────────────────────────────────── */
.prog-wrap {
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  padding: 12px 14px;
  margin-bottom: 10px;
}
.prog-title {
  font-size: 12px;
  color: var(--text2);
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
}
.prog-bar-bg {
  height: 4px;
  background: var(--bg4);
  border-radius: 2px;
  overflow: hidden;
}
.prog-bar-fg {
  height: 100%;
  border-radius: 2px;
  transition: width .5s ease;
}

/* ── Alert row ────────────────────────────────────────────── */
.alert-row {
  display: flex;
  gap: 10px;
  padding: 12px;
  background: var(--bg3);
  border-radius: var(--radius);
  border-left: 3px solid;
  margin-bottom: 8px;
}
.al-info   { border-color: var(--blue); }
.al-warn   { border-color: var(--amber); }
.al-danger { border-color: var(--red); }
.al-ok     { border-color: var(--green); }

/* ── Status tags ──────────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 2px 7px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: .3px;
}
.badge-ativo   { background: var(--green-bg);  color: var(--green);  border: 1px solid var(--green-border); }
.badge-inativo { background: var(--bg4);        color: var(--text3);  border: 1px solid var(--border2); }

/* ── Sidebar nav ──────────────────────────────────────────── */
.nav-btn button {
  background: transparent !important;
  color: var(--text2) !important;
  border: 1px solid transparent !important;
  border-radius: var(--radius) !important;
  text-align: left !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  padding: 8px 10px !important;
  width: 100% !important;
  font-family: var(--font) !important;
  transition: background .12s, color .12s;
}
.nav-btn button:hover {
  background: var(--bg3) !important;
  color: var(--text) !important;
}
.nav-btn-active button {
  background: var(--blue-bg) !important;
  color: var(--blue) !important;
  border: 1px solid var(--blue-border) !important;
}

/* ── Sec header ───────────────────────────────────────────── */
.sec-head {
  display: flex; align-items: flex-start;
  justify-content: space-between;
}
.sec-title { font-size: 15px; font-weight: 700; color: var(--text); }
.sec-sub   { font-size: 11px; color: var(--text3); margin-top: 2px; }

/* ── Divider ──────────────────────────────────────────────── */
.divider { border: none; border-top: 1px solid var(--border2); margin: 16px 0; }

/* ── Mono helper ──────────────────────────────────────────── */
.mono { font-family: var(--mono) !important; }
.pos  { color: var(--green) !important; }
.neg  { color: var(--red) !important; }
.neu  { color: var(--text3) !important; }

/* ── Scrollbar ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border3); border-radius: 2px; }

/* ── Live pill ────────────────────────────────────────────── */
.live-pill {
  background: var(--green);
  color: #000;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;
  letter-spacing: .8px;
  animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.5} }

/* ── Topbar ───────────────────────────────────────────────── */
.topbar-custom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background: var(--bg2);
  border-bottom: 1px solid var(--border2);
  margin-bottom: 20px;
}
.logo-text {
  font-size: 16px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: var(--text);
}
.logo-text em { color: var(--blue); font-style: normal; }

/* ── Quote card ───────────────────────────────────────────── */
.qcard {
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: var(--radius-lg);
  padding: 12px;
  margin-bottom: 10px;
}
.qcard-ticker { font-family: var(--mono); font-size: 12px; font-weight: 600; color: var(--text); }
.qcard-price  { font-size: 18px; font-weight: 700; font-family: var(--mono); line-height: 1; }
.qcard-chg    { font-size: 11px; font-family: var(--mono); margin-top: 3px; }

/* ── Ticker / Category tags (Renda Variável) ─────────────── */
.ticker-tag {
  font-family: var(--mono);
  font-weight: 500;
  color: var(--text);
  background: var(--bg4);
  padding: 2px 6px;
  border-radius: 5px;
  border: 1px solid var(--border2);
  font-size: 11px;
  white-space: nowrap;
}
.cat-tag {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 20px;
  font-weight: 600;
  white-space: nowrap;
}
.ct-acao  { background: #4da6ff18; color: var(--blue); }
.ct-fii   { background: #00e09a18; color: var(--green); }
.ct-etf   { background: #b388ff18; color: var(--purple); }
.ct-bdr   { background: #ffaa3318; color: var(--amber); }
.ct-opcao { background: #ff446618; color: var(--red); }

/* ── Tabela de Renda Variável ─────────────────────────────── */
.rv-table {
  width: 100%;
  border-collapse: collapse;
}
.rv-table th {
  padding: 9px 14px;
  text-align: left;
  font-size: 10px;
  font-weight: 600;
  color: var(--text3);
  letter-spacing: .5px;
  text-transform: uppercase;
  border-bottom: 1px solid var(--border2);
  white-space: nowrap;
}
.rv-table th.r { text-align: right; }
.rv-table td {
  padding: 10px 14px;
  font-size: 12px;
  border-bottom: 1px solid var(--border);
  color: var(--text2);
  vertical-align: middle;
  white-space: nowrap;
}
.rv-table tr:last-child td { border-bottom: none; }
.rv-table tr:hover td { background: var(--bg3); }
.rv-table td.r { text-align: right; }
.vp { color: var(--green); font-family: var(--mono); }
.vn { color: var(--red);   font-family: var(--mono); }
.vq { color: var(--text2); font-family: var(--mono); }
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)
