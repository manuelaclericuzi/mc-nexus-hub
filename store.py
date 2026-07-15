"""
MC Atelier — Persistência com Supabase (permanente) + fallback local (JSON).

Se as credenciais do Supabase estiverem configuradas em st.secrets
(SUPABASE_URL / SUPABASE_KEY), os dados são gravados numa tabela permanente
na nuvem. Caso contrário, cai automaticamente para um arquivo JSON local —
o app continua funcionando no computador, sem nuvem.

Estrutura no Supabase (rodar uma vez no SQL editor):
    create table if not exists atelier_state (
        id text primary key,
        data jsonb
    );
Use a chave service_role (o RLS é ignorado) — ela fica só nos secrets do
servidor, nunca é exposta ao navegador.
"""
import base64
import io
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "atelier_data.json")

# Chaves de estado que são persistidas
KEYS = ["perfil", "guarda_roupa", "looks", "compras", "sugestoes",
        "agenda", "look_of_day"]

_TABLE = "atelier_state"
_ROW_ID = "default"


# ── Supabase ─────────────────────────────────────────────────────
def _client():
    """Retorna um cliente Supabase se houver credenciais; senão None."""
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if not url or not key:
            return None
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None


def using_cloud() -> bool:
    return _client() is not None


# ── API pública ──────────────────────────────────────────────────
def load() -> dict:
    client = _client()
    if client is not None:
        try:
            res = client.table(_TABLE).select("data").eq("id", _ROW_ID).execute()
            if res.data:
                return res.data[0].get("data") or {}
            return {}
        except Exception:
            pass  # cai para o arquivo local
    return _load_file()


def save(data: dict) -> None:
    client = _client()
    if client is not None:
        try:
            client.table(_TABLE).upsert({"id": _ROW_ID, "data": data}).execute()
            return
        except Exception:
            pass  # cai para o arquivo local
    _save_file(data)


# ── Fallback em arquivo ──────────────────────────────────────────
def _load_file() -> dict:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_file(data: dict) -> None:
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


# ── Imagem → data URI (redimensionada) ───────────────────────────
def encode_image(uploaded_file, max_size=(560, 780)) -> str:
    raw = uploaded_file.read()
    mime = getattr(uploaded_file, "type", None) or "image/jpeg"
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        img.thumbnail(max_size)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=82)
        raw = buf.getvalue()
        mime = "image/jpeg"
    except Exception:
        pass
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"
