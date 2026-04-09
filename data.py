"""
MC Nexus Hub — Camada de dados (in-memory com session_state)
"""
import streamlit as st
from datetime import date, timedelta
import random
import requests

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _init_clientes():
    return [
        {"id": 1, "nome": "Ana Beatriz Souza",     "email": "ana@email.com",    "telefone": "(11) 99001-2345", "patrimonio": 850_000,  "status": "Ativo",   "data_cadastro": "2023-03-15"},
        {"id": 2, "nome": "Carlos Mendes",          "email": "carlos@email.com", "telefone": "(21) 98765-4321", "patrimonio": 2_300_000,"status": "Ativo",   "data_cadastro": "2022-07-22"},
        {"id": 3, "nome": "Fernanda Lima",          "email": "fe@email.com",     "telefone": "(31) 97654-3210", "patrimonio": 410_000,  "status": "Inativo", "data_cadastro": "2023-11-01"},
        {"id": 4, "nome": "Roberto Alves",          "email": "rob@email.com",    "telefone": "(41) 96543-2109", "patrimonio": 1_750_000,"status": "Ativo",   "data_cadastro": "2021-05-18"},
        {"id": 5, "nome": "Patrícia Gomes",         "email": "pat@email.com",    "telefone": "(51) 95432-1098", "patrimonio": 630_000,  "status": "Ativo",   "data_cadastro": "2024-01-10"},
        {"id": 6, "nome": "Marcelo Ferreira",       "email": "mf@email.com",     "telefone": "(61) 94321-0987", "patrimonio": 3_100_000,"status": "Ativo",   "data_cadastro": "2020-09-05"},
        {"id": 7, "nome": "Juliana Costa",          "email": "ju@email.com",     "telefone": "(71) 93210-9876", "patrimonio": 920_000,  "status": "Ativo",   "data_cadastro": "2023-06-28"},
        {"id": 8, "nome": "Eduardo Nunes",          "email": "edu@email.com",    "telefone": "(81) 92109-8765", "patrimonio": 275_000,  "status": "Inativo", "data_cadastro": "2024-02-14"},
    ]


def _init_receitas():
    return [
        {"id": 1, "cliente": "Carlos Mendes",    "produto": "Renda Fixa",   "valor_aplicacao": 500_000, "roa": 1.2, "repasse": 0.35, "data": "2024-03-01"},
        {"id": 2, "cliente": "Roberto Alves",    "produto": "Multimercado", "valor_aplicacao": 800_000, "roa": 1.8, "repasse": 0.40, "data": "2024-03-05"},
        {"id": 3, "cliente": "Ana Beatriz",      "produto": "Renda Variável","valor_aplicacao": 300_000, "roa": 2.5, "repasse": 0.45, "data": "2024-03-12"},
        {"id": 4, "cliente": "Marcelo Ferreira", "produto": "Previdência",  "valor_aplicacao": 1_000_000,"roa": 0.9,"repasse": 0.30, "data": "2024-03-18"},
        {"id": 5, "cliente": "Patrícia Gomes",   "produto": "Renda Fixa",   "valor_aplicacao": 200_000, "roa": 1.1, "repasse": 0.35, "data": "2024-03-22"},
        {"id": 6, "cliente": "Juliana Costa",    "produto": "FII",          "valor_aplicacao": 450_000, "roa": 1.5, "repasse": 0.40, "data": "2024-03-28"},
    ]


def _init_metas():
    return {
        "receita_bruta":   {"meta": 50_000,   "realizado": 36_800},
        "novos_clientes":  {"meta": 10,        "realizado": 7},
        "captacao":        {"meta": 5_000_000, "realizado": 3_750_000},
        "aum":             {"meta": 20_000_000,"realizado": 15_200_000},
    }


def _init_operacoes():
    return [
        {"id": 1, "client_id": 1, "tipo": "Compra", "ticker": "PETR4",  "cat": "Ação", "qty": 100.0, "price": 34.50, "date": "2024-01-15", "obs": ""},
        {"id": 2, "client_id": 1, "tipo": "Compra", "ticker": "VALE3",  "cat": "Ação", "qty":  50.0, "price": 67.20, "date": "2024-01-22", "obs": ""},
        {"id": 3, "client_id": 2, "tipo": "Compra", "ticker": "HGLG11", "cat": "FII",  "qty":  30.0, "price":163.00, "date": "2024-02-05", "obs": ""},
        {"id": 4, "client_id": 2, "tipo": "Compra", "ticker": "PETR4",  "cat": "Ação", "qty": 200.0, "price": 36.80, "date": "2024-02-10", "obs": ""},
        {"id": 5, "client_id": 1, "tipo": "Venda",  "ticker": "PETR4",  "cat": "Ação", "qty":  50.0, "price": 38.20, "date": "2024-03-01", "obs": "Parcial"},
        {"id": 6, "client_id": 4, "tipo": "Compra", "ticker": "BOVA11", "cat": "ETF",  "qty":  80.0, "price":118.50, "date": "2024-02-20", "obs": ""},
        {"id": 7, "client_id": 4, "tipo": "Compra", "ticker": "ITUB4",  "cat": "Ação", "qty": 150.0, "price": 32.10, "date": "2024-03-05", "obs": ""},
        {"id": 8, "client_id": 6, "tipo": "Compra", "ticker": "BBAS3",  "cat": "Ação", "qty": 300.0, "price": 53.40, "date": "2024-01-30", "obs": ""},
        {"id": 9, "client_id": 6, "tipo": "Compra", "ticker": "XPML11", "cat": "FII",  "qty": 100.0, "price":101.20, "date": "2024-02-15", "obs": ""},
    ]


def _init_alertas():
    return []


def _init_captacoes():
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    base = [320, 480, 560, 390, 620, 700, 510, 680, 730, 590, 810, 950]
    return [{"mes": m, "valor": v * 1000} for m, v in zip(meses, base)]


# ---------------------------------------------------------------------------
# Inicialização do estado global
# ---------------------------------------------------------------------------

def init_state():
    if "clientes" not in st.session_state:
        st.session_state.clientes = _init_clientes()
    if "receitas" not in st.session_state:
        st.session_state.receitas = _init_receitas()
    if "metas" not in st.session_state:
        st.session_state.metas = _init_metas()
    if "captacoes" not in st.session_state:
        st.session_state.captacoes = _init_captacoes()
    if "operacoes" not in st.session_state:
        st.session_state.operacoes = _init_operacoes()
    if "alertas" not in st.session_state:
        st.session_state.alertas = _init_alertas()
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Dashboard"


# ---------------------------------------------------------------------------
# Cálculo de receita
# ---------------------------------------------------------------------------

IR_FIXO = 0.195  # 19,5 %

def calcular_receita(valor_aplicacao: float, roa: float, repasse: float) -> dict:
    """
    Retorna dict com receita_bruta, repasse_valor, ir, receita_liquida.
    roa em % ao ano  →  receita_bruta = valor_aplicacao * roa / 100
    repasse em fração (ex: 0.35)
    """
    receita_bruta   = valor_aplicacao * roa / 100
    repasse_valor   = receita_bruta * repasse
    ir              = repasse_valor * IR_FIXO
    receita_liquida = repasse_valor - ir
    return {
        "receita_bruta":   receita_bruta,
        "repasse_valor":   repasse_valor,
        "ir":              ir,
        "receita_liquida": receita_liquida,
    }


# ---------------------------------------------------------------------------
# Renda Variável — posições e cotações
# Port direto de buildPositions / enrichPositions do nexus-capital_1.html
# ---------------------------------------------------------------------------

BRAPI_BASE  = "https://brapi.dev/api"
BRAPI_TOKEN = "2jou51P6VahKzY5uHZMyW7"  # token padrão do protótipo HTML


def build_positions(ops: list, client_id=None) -> list:
    """
    Agrega operações em posições abertas por (client_id, ticker).
    Retorna lista de dicts com qty, total_cost, realized_pl.
    """
    if client_id is not None:
        ops = [o for o in ops if o["client_id"] == client_id]
    pos_map: dict = {}
    for o in ops:
        k = f"{o['client_id']}_{o['ticker']}"
        if k not in pos_map:
            pos_map[k] = {
                "client_id":   o["client_id"],
                "ticker":      o["ticker"],
                "cat":         o["cat"],
                "qty":         0.0,
                "total_cost":  0.0,
                "realized_pl": 0.0,
            }
        p = pos_map[k]
        if o["tipo"] == "Compra":
            p["qty"]       += o["qty"]
            p["total_cost"] += o["qty"] * o["price"]
        else:
            pm = p["total_cost"] / p["qty"] if p["qty"] > 0 else 0.0
            p["realized_pl"] += (o["price"] - pm) * o["qty"]
            p["qty"]         -= o["qty"]
            p["total_cost"]  -= pm * o["qty"]
    return [p for p in pos_map.values() if p["qty"] > 0.001]


def enrich_positions(positions: list, quote_cache: dict) -> list:
    """
    Adiciona preço médio, cotação atual e P&L a cada posição.
    quote_cache: {ticker: {"price": float, "change_pct": float}}
    """
    enriched = []
    for p in positions:
        pm      = p["total_cost"] / p["qty"] if p["qty"] > 0 else 0.0
        q       = quote_cache.get(p["ticker"])
        current = q["price"] if q else pm
        unreal  = (current - pm) * p["qty"]
        enriched.append({
            **p,
            "pm":        pm,
            "current":   current,
            "unreal":    unreal,
            "unreal_pct": ((current - pm) / pm * 100) if pm > 0 else 0.0,
            "quote":     q,
        })
    return enriched


@st.cache_data(ttl=300)
def fetch_quotes(tickers: tuple) -> dict:
    """
    Busca cotações na Brapi (B3). Cache de 5 min.
    Retorna {ticker: {"price": float, "change_pct": float}} ou {} em caso de erro.
    """
    if not tickers:
        return {}
    symbols = ",".join(tickers)
    url = f"{BRAPI_BASE}/quote/{symbols}?token={BRAPI_TOKEN}&fundamental=false"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return {}
        data = r.json()
        result = {}
        for item in data.get("results", []):
            sym   = item.get("symbol", "")
            price = item.get("regularMarketPrice", 0)
            chg   = item.get("regularMarketChangePercent", 0)
            if sym and price:
                result[sym] = {"price": float(price), "change_pct": float(chg or 0)}
        return result
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Receitas
# ---------------------------------------------------------------------------

def resumo_receitas() -> dict:
    total_bruta   = 0.0
    total_liquida = 0.0
    for r in st.session_state.receitas:
        calc = calcular_receita(r["valor_aplicacao"], r["roa"], r["repasse"])
        total_bruta   += calc["receita_bruta"]
        total_liquida += calc["receita_liquida"]
    return {"bruta": total_bruta, "liquida": total_liquida}
