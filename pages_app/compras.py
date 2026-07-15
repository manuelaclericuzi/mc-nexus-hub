"""
MC Atelier — Compras · Lista de Compras Estratégica
"""
import streamlit as st
import components as C
import data as D


_PRIO_ORDER = {"Alta": 0, "Média": 1, "Baixa": 2}


def _brl(v: float) -> str:
    s = f"{v:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def render():
    C.topbar()

    st.markdown("""
    <div style="margin-bottom:36px;">
      <div style="font-family:'Playfair Display',serif;font-size:28px;margin-bottom:8px;">Lista de Compras Estratégica</div>
      <div style="font-size:14px;color:var(--muted);line-height:1.6;max-width:66ch;">
        Construa autoridade através de aquisições curadas. Cada peça é um investimento na sua
        imagem profissional e expressão de excelência.</div>
    </div>
    """, unsafe_allow_html=True)

    col_list, col_side = st.columns([2.1, 1], gap="large")

    # ── Lacunas identificadas ────────────────────────────────────
    with col_list:
        compras = sorted(
            st.session_state.compras,
            key=lambda c: (c["comprado"], _PRIO_ORDER.get(c["prioridade"], 3)),
        )
        pendentes = [c for c in compras if not c["comprado"]]
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
             border-bottom:1px solid var(--ink);padding-bottom:14px;margin-bottom:8px;">
          <span class="eyebrow">Lacunas identificadas ({len(pendentes):02d})</span>
          <span class="eyebrow">Prioridade por impacto</span>
        </div>
        """, unsafe_allow_html=True)

        for c in compras:
            _lacuna(c)

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

    # ── Rail direita ─────────────────────────────────────────────
    with col_side:
        _guia_investimento()
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        _planejamento()
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        _sugestoes()


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
    col_card, col_btn = st.columns([7, 1])
    with col_card:
        st.markdown(f"""
        <div style="background:var(--panel);border:1px solid var(--line);padding:26px;{opacity}">
          <div style="display:flex;gap:22px;">
            <div style="flex:none;width:78px;">{C.tile(c['tone'], mono=c['item'][:1].upper(), ratio='3 / 4')}</div>
            <div style="flex:1;">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;">
                <div>
                  <span style="border:1px solid var(--ink);padding:4px 9px;font-size:9.5px;font-weight:700;
                        letter-spacing:.12em;text-transform:uppercase;">{c['prioridade']} prioridade</span>
                  <div style="font-family:'Playfair Display',serif;font-size:22px;margin-top:14px;{strike}">{c['item']}</div>
                </div>
                <div style="text-align:right;flex:none;">
                  <div class="eyebrow">Investimento est.</div>
                  <div style="font-family:'Playfair Display',serif;font-size:20px;margin-top:4px;">{_brl(c['preco'])}</div>
                </div>
              </div>
              <div style="font-size:13px;color:var(--muted);line-height:1.55;margin:14px 0 16px;">{c['motivo']}</div>
              <div>{tags}</div>
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


def _guia_investimento():
    st.markdown("""
    <div style="background:var(--black);color:#fff;padding:30px;">
      <div style="font-family:'Playfair Display',serif;font-size:22px;border-bottom:1px solid rgba(255,255,255,.18);
           padding-bottom:16px;margin-bottom:20px;">Guia de Investimento</div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#e0b25f;margin-bottom:10px;">Custo por uso (CPW)</div>
      <div style="font-size:13px;color:rgba(255,255,255,.82);line-height:1.6;margin-bottom:22px;">
        Preço ÷ Vezes usado = Valor Real. Um blazer caro usado 200 vezes custa menos que uma peça barata usada 5.</div>
      <div style="border:1px solid rgba(255,255,255,.18);padding:20px;margin-bottom:22px;">
        <div style="font-family:'Playfair Display',serif;font-style:italic;font-size:16px;line-height:1.5;margin-bottom:12px;">"Qualidade é lembrada muito depois que o preço é esquecido."</div>
        <div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.55);text-align:right;">— Sir Henry Royce</div>
      </div>
      <div style="font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#e0b25f;margin-bottom:10px;">Regra dos 3 looks</div>
      <div style="font-size:13px;color:rgba(255,255,255,.82);line-height:1.6;">
        Nunca adquira uma peça que não combine com pelo menos 3 itens que você já possui no guarda-roupa.</div>
    </div>
    """, unsafe_allow_html=True)


def _planejamento():
    total = D.total_compras()
    altas = sum(c["preco"] for c in st.session_state.compras
                if not c["comprado"] and c["prioridade"] == "Alta")
    pct = round(altas / total * 100) if total else 0
    st.markdown(f"""
    <div style="background:var(--panel);border:1px solid var(--line);padding:30px;">
      <div class="eyebrow" style="margin-bottom:20px;">Planejamento financeiro</div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;
           border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:12px;">
        <span style="font-size:13px;color:var(--muted);">Investimento total previsto</span>
        <span style="font-family:'Playfair Display',serif;font-size:20px;">{_brl(total)}</span>
      </div>
      <div style="font-size:12px;color:var(--faint);font-style:italic;margin-bottom:20px;">{pct}% alocado em peças de Alta Prioridade</div>
      <div style="background:var(--ink);color:#fff;text-align:center;padding:14px;
           font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;">Exportar para concierge</div>
    </div>
    """, unsafe_allow_html=True)


def _sugestoes():
    rows = ""
    for nome, tag, tone in st.session_state.sugestoes:
        rows += (
            f'<div style="display:flex;gap:14px;align-items:center;padding:14px 0;border-top:1px solid var(--line);">'
            f'<div style="width:52px;height:52px;flex:none;background:linear-gradient(150deg,{tone},#111);"></div>'
            f'<div><div style="font-family:\'Playfair Display\',serif;font-size:15px;">{nome}</div>'
            f'<div style="font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);margin-top:4px;">{tag}</div>'
            f'</div></div>'
        )
    html = (
        '<div style="background:var(--paper);border:1px solid var(--line);padding:30px;">'
        '<div class="eyebrow" style="margin-bottom:8px;">Sugestões curadas</div>'
        f'{rows}'
        '<div style="margin-top:16px;"><span class="sec-link">Ver todas as sugestões</span></div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
