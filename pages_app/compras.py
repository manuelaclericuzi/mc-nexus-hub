"""
MC Atelier — Compras · Lista de Compras Estratégica (versão enxuta)
"""
import streamlit as st
import components as C
import data as D


_PRIO_ORDER = {"Alta": 0, "Média": 1, "Baixa": 2}


def _brl(v: float) -> str:
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def render():
    C.topbar()

    C.sec_header(
        "Lista de Compras Estratégica",
        subtitle="Cada peça é um investimento na sua imagem. Compre com intenção, não por impulso.",
    )

    compras = sorted(
        st.session_state.compras,
        key=lambda c: (c["comprado"], _PRIO_ORDER.get(c["prioridade"], 3)),
    )
    pendentes = [c for c in compras if not c["comprado"]]
    total = D.total_compras()

    # ── Barra-resumo enxuta ──────────────────────────────────────
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
         border-top:1px solid var(--ink);border-bottom:1px solid var(--line);padding:16px 2px;margin-bottom:24px;">
      <span class="eyebrow">{len(pendentes):02d} lacunas · prioridade por impacto</span>
      <span style="font-size:13px;color:var(--muted);">Investimento previsto
        <b style="font-family:'Playfair Display',serif;font-size:18px;color:var(--ink);margin-left:8px;">{_brl(total)}</b></span>
    </div>
    """, unsafe_allow_html=True)

    # ── Lista (foco) ─────────────────────────────────────────────
    for c in compras:
        _lacuna(c)

    # ── Secundário recolhido ─────────────────────────────────────
    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

    with st.expander("💡  Guia de investimento — como decidir uma compra"):
        st.markdown("""
        <div style="padding:6px 4px 4px;">
          <div style="font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:8px;">Custo por uso (CPW)</div>
          <div style="font-size:13.5px;color:var(--muted);line-height:1.65;margin-bottom:18px;">
            Preço ÷ Vezes usado = Valor Real. Um blazer caro usado 200 vezes custa menos que uma peça barata usada 5.</div>
          <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:17px;color:var(--ink);margin-bottom:6px;">"Qualidade é lembrada muito depois que o preço é esquecido."</div>
          <div class="eyebrow" style="margin-bottom:20px;">— Sir Henry Royce</div>
          <div style="font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:8px;">Regra dos 3 looks</div>
          <div style="font-size:13.5px;color:var(--muted);line-height:1.65;">
            Nunca adquira uma peça que não combine com pelo menos 3 itens que você já possui no guarda-roupa.</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("✦  Sugestões curadas para você"):
        rows = ""
        for nome, tag, tone in st.session_state.sugestoes:
            rows += (
                f'<div style="display:flex;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line);">'
                f'<div style="width:48px;height:48px;flex:none;background:linear-gradient(150deg,{tone},#111);"></div>'
                f'<div><div style="font-family:\'Playfair Display\',serif;font-size:15px;">{nome}</div>'
                f'<div style="font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);margin-top:4px;">{tag}</div>'
                f'</div></div>'
            )
        st.markdown(f'<div style="padding:4px;">{rows}</div>', unsafe_allow_html=True)

    with st.expander("＋  Adicionar lacuna personalizada"):
        with st.form("add_compra", clear_on_submit=True):
            a, b = st.columns([2, 1])
            item = a.text_input("Item")
            prio = b.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
            motivo = st.text_input("Por que entra na cápsula")
            d, e = st.columns(2)
            preco = d.number_input("Investimento estimado (R$)", min_value=0.0, step=50.0, value=0.0)
            tagv  = e.text_input("Versatilidade / nota", value="")
            if st.form_submit_button("Adicionar à lista"):
                if item.strip():
                    nid = max([c["id"] for c in st.session_state.compras], default=0) + 1
                    tags = [("Custo por uso", "—")]
                    if tagv.strip():
                        tags.append(("Versatilidade", tagv.strip()))
                    st.session_state.compras.append({
                        "id": nid, "item": item.strip(), "prioridade": prio,
                        "motivo": motivo.strip(), "tags": tags, "preco": float(preco),
                        "tone": "#3a3c40", "comprado": False,
                    })
                    st.rerun()


def _lacuna(c):
    prio_color = {"Alta": "var(--ink)", "Média": "var(--muted)", "Baixa": "var(--faint)"}
    color   = prio_color.get(c["prioridade"], "var(--faint)")
    opacity = "opacity:.5;" if c["comprado"] else ""
    strike  = "text-decoration:line-through;" if c["comprado"] else ""
    tags = "".join(
        f'<span style="border:1px solid var(--line2);padding:5px 10px;font-size:10px;'
        f'font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);'
        f'margin-right:8px;">{k}: {v}</span>'
        for k, v in c["tags"]
    )
    col_card, col_btn = st.columns([9, 1])
    with col_card:
        st.markdown(f"""
        <div style="background:var(--paper);border:1px solid var(--line);
             border-left:3px solid {color};padding:24px 28px;{opacity}">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;">
            <div style="flex:1;">
              <span style="border:1px solid var(--ink);padding:4px 9px;font-size:9.5px;font-weight:700;
                    letter-spacing:.12em;text-transform:uppercase;">{c['prioridade']} prioridade</span>
              <div style="font-family:'Playfair Display',serif;font-size:22px;margin:14px 0 10px;{strike}">{c['item']}</div>
              <div style="font-size:13px;color:var(--muted);line-height:1.55;max-width:70ch;margin-bottom:16px;">{c['motivo']}</div>
              <div>{tags}</div>
            </div>
            <div style="text-align:right;flex:none;">
              <div class="eyebrow">Investimento est.</div>
              <div style="font-family:'Playfair Display',serif;font-size:22px;margin-top:6px;">{_brl(c['preco'])}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    with col_btn:
        label = "↺" if c["comprado"] else "✓"
        if st.button(label, key=f"buy_{c['id']}", type="secondary", use_container_width=True):
            for it in st.session_state.compras:
                if it["id"] == c["id"]:
                    it["comprado"] = not it["comprado"]
            st.rerun()
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
