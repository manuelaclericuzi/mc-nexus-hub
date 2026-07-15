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
        "agenda", "look_of_day", "semana"]

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


def health() -> dict:
    """Testa de verdade a conexão com o Supabase e retorna um diagnóstico."""
    info = {"secrets": False, "cloud": False, "error": ""}
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
    except Exception as e:
        info["error"] = f"Não achei os secrets ({type(e).__name__})."
        return info
    info["secrets"] = bool(url and key)
    if not info["secrets"]:
        faltando = []
        if not url:
            faltando.append("SUPABASE_URL")
        if not key:
            faltando.append("SUPABASE_KEY")
        info["error"] = "Faltando nos secrets: " + ", ".join(faltando)
        return info
    try:
        from supabase import create_client
    except Exception as e:
        info["error"] = f"Biblioteca supabase não instalada: {e}"
        return info
    try:
        c = create_client(url, key)
        c.table(_TABLE).upsert({"id": "__health__", "data": {"ok": True}}).execute()
        res = c.table(_TABLE).select("data").eq("id", "__health__").execute()
        info["cloud"] = bool(res.data)
        if not info["cloud"]:
            info["error"] = "Gravou mas não conseguiu ler de volta."
    except Exception as e:
        info["error"] = f"{type(e).__name__}: {e}"
    return info


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
