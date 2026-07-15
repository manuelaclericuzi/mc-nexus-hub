"""
MC Atelier — Persistência simples em JSON + utilitário de imagem.

Os dados do usuário (perfil, guarda-roupa, looks, compras) são gravados
num arquivo JSON local. Isso mantém tudo salvo entre recarregamentos e
navegações. Observação: em hospedagem efêmera (ex.: Streamlit Cloud), o
arquivo é reiniciado quando o container reinicia — para persistência
permanente na nuvem seria necessário um banco externo.
"""
import base64
import io
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "atelier_data.json")

# Chaves de estado que são persistidas
KEYS = ["perfil", "guarda_roupa", "looks", "compras", "sugestoes",
        "agenda", "look_of_day"]


def load() -> dict:
    """Carrega os dados salvos; retorna {} se não houver ou em erro."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save(data: dict) -> None:
    """Grava os dados no arquivo JSON (silencioso em caso de erro)."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


def encode_image(uploaded_file, max_size=(560, 780)) -> str:
    """
    Converte um arquivo enviado (st.file_uploader) numa data URI base64,
    redimensionando para caber em max_size quando o Pillow está disponível.
    """
    raw = uploaded_file.read()
    mime = getattr(uploaded_file, "type", None) or "image/jpeg"
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(raw))
        img = img.convert("RGB")
        img.thumbnail(max_size)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=82)
        raw = buf.getvalue()
        mime = "image/jpeg"
    except Exception:
        pass
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"
