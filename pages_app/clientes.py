"""Página: Gestão de Clientes"""
import streamlit as st
import pandas as pd
from components import gold_divider, section_title, status_badge


def _fmt_brl(v):
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render():
    section_title("Clientes", "Gestão da carteira de clientes")
    gold_divider()

    clientes = st.session_state.clientes

    # ── Filtros ─────────────────────────────────────────────────
    fcol1, fcol2, fcol3 = st.columns([3, 2, 1])
    with fcol1:
        busca = st.text_input("Buscar por nome ou e-mail", placeholder="Digite para filtrar...")
    with fcol2:
        status_f = st.selectbox("Status", ["Todos", "Ativo", "Inativo"])
    with fcol3:
        st.markdown("<br>", unsafe_allow_html=True)
        novo = st.button("+ Novo Cliente", use_container_width=True)

    # Filtragem
    filtrados = clientes
    if busca:
        busca_l = busca.lower()
        filtrados = [c for c in filtrados if busca_l in c["nome"].lower() or busca_l in c["email"].lower()]
    if status_f != "Todos":
        filtrados = [c for c in filtrados if c["status"] == status_f]

    gold_divider()

    # ── KPIs rápidos ────────────────────────────────────────────
    total    = len(clientes)
    ativos   = sum(1 for c in clientes if c["status"] == "Ativo")
    pat_tot  = sum(c["patrimonio"] for c in clientes)

    k1, k2, k3 = st.columns(3)
    k1.markdown(f"""<div class="metric-card"><div class="metric-label">Total Clientes</div>
    <div class="metric-value">{total}</div></div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="metric-card"><div class="metric-label">Clientes Ativos</div>
    <div class="metric-value">{ativos}</div></div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="metric-card"><div class="metric-label">Patrimônio Total</div>
    <div class="metric-value">{_fmt_brl(pat_tot)}</div></div>""", unsafe_allow_html=True)

    gold_divider()

    # ── Tabela ──────────────────────────────────────────────────
    st.markdown(f"<p style='color:#666;font-size:0.8rem;'>{len(filtrados)} cliente(s) encontrado(s)</p>",
                unsafe_allow_html=True)

    if not filtrados:
        st.info("Nenhum cliente encontrado com os filtros selecionados.")
        return

    # Renderiza com HTML para exibir badges
    rows_html = ""
    for c in filtrados:
        badge = status_badge(c["status"])
        rows_html += f"""
        <tr>
            <td style="padding:10px 14px;border-bottom:1px solid #1E1E1E;">{c['nome']}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #1E1E1E;color:#888;">{c['email']}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #1E1E1E;color:#888;">{c['telefone']}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #1E1E1E;color:#C9A84C;">{_fmt_brl(c['patrimonio'])}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #1E1E1E;">{badge}</td>
            <td style="padding:10px 14px;border-bottom:1px solid #1E1E1E;color:#555;font-size:0.8rem;">{c['data_cadastro']}</td>
        </tr>"""

    header_style = "padding:10px 14px;text-align:left;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#666;border-bottom:1px solid #2A2A2A;"
    table_html = f"""
    <div style="background:#111;border:1px solid #2A2A2A;border-radius:12px;overflow:hidden;margin-top:8px;">
    <table style="width:100%;border-collapse:collapse;">
        <thead>
            <tr style="background:#151515;">
                <th style="{header_style}">Nome</th>
                <th style="{header_style}">E-mail</th>
                <th style="{header_style}">Telefone</th>
                <th style="{header_style}">Patrimônio</th>
                <th style="{header_style}">Status</th>
                <th style="{header_style}">Cadastro</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>"""
    st.markdown(table_html, unsafe_allow_html=True)

    gold_divider()

    # ── Modal: Novo Cliente ─────────────────────────────────────
    if novo or st.session_state.get("show_form_cliente"):
        st.session_state["show_form_cliente"] = True
        st.markdown("<h3>Novo Cliente</h3>", unsafe_allow_html=True)
        with st.form("form_cliente", clear_on_submit=True):
            nc1, nc2 = st.columns(2)
            nome      = nc1.text_input("Nome completo *")
            email     = nc2.text_input("E-mail *")
            tel       = nc1.text_input("Telefone")
            patrimonio = nc2.number_input("Patrimônio (R$)", min_value=0.0, step=10_000.0)
            status    = nc1.selectbox("Status", ["Ativo", "Inativo"])
            submitted = st.form_submit_button("Salvar Cliente")

            if submitted:
                if not nome or not email:
                    st.error("Nome e e-mail são obrigatórios.")
                else:
                    novo_id = max(c["id"] for c in st.session_state.clientes) + 1
                    st.session_state.clientes.append({
                        "id": novo_id,
                        "nome": nome,
                        "email": email,
                        "telefone": tel,
                        "patrimonio": patrimonio,
                        "status": status,
                        "data_cadastro": str(pd.Timestamp.today().date()),
                    })
                    st.session_state["show_form_cliente"] = False
                    st.success(f"Cliente '{nome}' cadastrado com sucesso!")
                    st.rerun()
