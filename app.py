import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Radar de Financiamento PT", page_icon="🇵🇹", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp header {background-color: transparent;}
    .projeto-titulo {font-size: 1.3rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem;}
    .badge-aberto {background-color: #DEF7EC; color: #03543F; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;}
    .badge-fechado {background-color: #FDE8E8; color: #9B1C1C; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;}
    .badge-fonte {background-color: #F3F4F6; color: #374151; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #D1D5DB; margin-left: 8px;}
    .resumo-box {background-color: #F8FAFC; padding: 15px; border-left: 4px solid #3B82F6; border-radius: 4px; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- 1. FUNÇÕES DE EXTRAÇÃO DE DADOS ---
@st.cache_data(ttl=60) # Reduzido para 1 minuto para facilitar testes
def extrair_dados():
    time.sleep(0.5)
    return [
        {"titulo": "Descarbonização da Indústria", "estado": "Aberto", "programa": "PRR", "fonte": "Recuperar Portugal", "links": [{"nome": "Aviso Oficial", "url": "https://recuperarportugal.gov.pt/"}]},
        {"titulo": "Inovação Produtiva", "estado": "Aberto", "programa": "COMPETE 2030", "fonte": "Portugal 2030", "links": [{"nome": "Aviso Oficial", "url": "https://portugal2030.pt/"}]},
        {"titulo": "Qualificação de PME", "estado": "Fechado", "programa": "Norte 2030", "fonte": "Portugal 2030", "links": [{"nome": "Aviso Oficial", "url": "https://portugal2030.pt/"}]},
        {"titulo": "Pequenos Investimentos Agrícolas", "estado": "Aberto", "programa": "PDR2020", "fonte": "PDR2020", "links": [{"nome": "Aviso Oficial", "url": "https://www.pdr-2020.pt/"}]},
        {"titulo": "Qualificação da Oferta", "estado": "Aberto", "programa": "Turismo Fundos", "fonte": "Turismo de Portugal", "links": [{"nome": "Aviso Oficial", "url": "https://business.turismodeportugal.pt/"}]}
    ]

# --- 2. FUNÇÃO DE RESUMO ESTRUTURADO (IA) ---
def gerar_resumo_aviso(titulo, fonte):
    # Simulação rápida sem cache para não bloquear
    if fonte == "PDR2020":
        atividades = "Aquisição de tratores, estufas e sistemas de rega."
        destinatarios = "Agricultores ativos."
        taxas = "Fundo perdido até 50%."
    elif fonte == "Turismo de Portugal":
        atividades = "Requalificação de empreendimentos turísticos."
        destinatarios = "Empresas de Turismo."
        taxas = "Apoio misto (bancário + fundo perdido)."
    else:
        atividades = "Máquinas industriais e software."
        destinatarios = "PME."
        taxas = "Taxa base de 30% a 40% a fundo perdido."

    return {
        "atividades_despesas": atividades,
        "prazos_condicoes": "Candidaturas até 31/12/2026. Sem dívidas à AT/SS.",
        "destinatarios": destinatarios,
        "regioes": "Portugal Continental.",
        "taxas_incentivo": taxas
    }

# --- MOTOR DA APLICAÇÃO ---
with st.spinner("A consultar bases de dados..."):
    dados_brutos = extrair_dados()
    
    # PROGRAMAÇÃO DEFENSIVA: Garantir que as colunas existem sempre, mesmo se os dados vierem vazios
    if not dados_brutos:
        df_avisos = pd.DataFrame(columns=["titulo", "estado", "programa", "fonte", "links"])
    else:
        df_avisos = pd.DataFrame(dados_brutos)

# --- BARRA LATERAL (FILTROS) ---
with st.sidebar:
    st.title("Filtros Globais")
    
    # LISTA FIXA DE FONTES
    fontes_totais = ["Recuperar Portugal", "Portugal 2030", "PDR2020", "Turismo de Portugal"]
    
    filtro_fonte = st.multiselect(
        "Filtrar por Fonte:", 
        options=fontes_totais, 
        default=fontes_totais
    )
    
    st.divider()
    # Limpeza explícita de cache
    if st.button("🔄 Forçar Limpeza e Atualizar"):
        st.cache_data.clear()
        st.rerun()

# --- CORPO PRINCIPAL ---
st.title("Agregador Central de Financiamento")

if df_avisos.empty:
    st.warning("A base de dados encontra-se atualmente vazia.")
else:
    # FILTRO APLICADO AQUI
    df_filtrado = df_avisos[df_avisos['fonte'].isin(filtro_fonte)]

    tab_abertos, tab_fechados = st.tabs(["🟢 Avisos Abertos", "🔴 Histórico"])

    def renderizar_lista(df):
        if df.empty:
            st.info("Nenhum aviso corresponde às fontes selecionadas.")
            return
            
        for i, aviso in df.iterrows():
            with st.container(border=True):
                col_esquerda, col_direita = st.columns([4, 1])
                
                with col_esquerda:
                    status_class = "badge-aberto" if aviso['estado'] == "Aberto" else "badge-fechado"
                    st.markdown(f"<span class='{status_class}'>{aviso['estado']}</span> <span class='badge-fonte'>🏢 {aviso['fonte']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='projeto-titulo'>{aviso['titulo']}</div>", unsafe_allow_html=True)
                    st.markdown(f"🔗 [{aviso['links'][0]['nome']}]({aviso['links'][0]['url']})")
                
                with col_direita:
                    st.write("") 
                    if st.button("Extrair e Resumir 🤖", key=f"btn_{i}", use_container_width=True):
                        st.session_state[f"exp_{i}"] = True
                
                if st.session_state.get(f"exp_{i}"):
                    resumo = gerar_resumo_aviso(aviso['titulo'], aviso['fonte'])
                    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class='resumo-box'><strong>🛠️ Atividades:</strong> {resumo['atividades_despesas']}</div>
                    <div class='resumo-box'><strong>🗓️ Prazos:</strong> {resumo['prazos_condicoes']}</div>
                    <div class='resumo-box'><strong>🎯 Destinatários:</strong> {resumo['destinatarios']}</div>
                    <div class='resumo-box'><strong>📍 Regiões:</strong> {resumo['regioes']}</div>
                    <div class='resumo-box'><strong>💰 Taxas:</strong> {resumo['taxas_incentivo']}</div>
                    """, unsafe_allow_html=True)

    with tab_abertos:
        renderizar_lista(df_filtrado[df_filtrado['estado'] == "Aberto"])
    with tab_fechados:
        renderizar_lista(df_filtrado[df_filtrado['estado'] == "Fechado"])
