import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import random # Usado para simular taxas enquanto o scraper de detalhe não está ativo

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Radar EU | Fundos", page_icon="🇪🇺", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp header {background-color: transparent;}
    .projeto-titulo {font-size: 1.2rem; font-weight: 600; color: #1E3A8A;}
    .projeto-programa {font-size: 0.9rem; color: #6B7280; font-weight: bold;}
    .badge-aberto {background-color: #DEF7EC; color: #03543F; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;}
    .badge-taxa {background-color: #E0E7FF; color: #3730A3; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; margin-left: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- 1. FUNÇÃO REAL DE WEB SCRAPING (PRR) ---
@st.cache_data(ttl=3600) 
def extrair_avisos_prr():
    url_alvo = "https://recuperarportugal.gov.pt/candidaturas/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    avisos_extraidos = []
    
    try:
        resposta = requests.get(url_alvo, headers=headers, timeout=10)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, 'html.parser')
        artigos = soup.find_all('article')
        
        for artigo in artigos:
            link_tag = artigo.find('a')
            if not link_tag: continue
            
            titulo = link_tag.get_text(strip=True)
            link_exato = link_tag.get('href')
            if not titulo: continue
            
            estado = "Fechado" if any(x in titulo.lower() for x in ["encerrad", "suspens"]) else "Aberto"
            
            # SIMULAÇÃO DE TAXA: Como a taxa está no PDF, atribuímos um valor para o filtro funcionar.
            # No futuro, o "Análise IA" substituirá este valor pelo real.
            taxa_simulada = random.choice([40, 50, 70, 85, 100]) if estado == "Aberto" else 0
            
            avisos_extraidos.append({
                "titulo": titulo,
                "estado": estado,
                "programa": "PRR",
                "taxa": taxa_simulada,
                "links": [{"nome": "Página Oficial do Aviso", "url": link_exato}]
            })
    except Exception as e:
        st.sidebar.error(f"Erro ao ler PRR: {e}")
    return avisos_extraidos

# --- 2. FUNÇÃO DE RESUMO (IA) ---
@st.cache_data(ttl=3600)
def gerar_resumo_aviso(titulo, taxa):
    time.sleep(1)
    return {
        "Finalidades e objetivos": f"Investimentos estratégicos integrados no aviso {titulo}.",
        "Prazos e condições para as PME": "Consultar anexo técnico para prazos de submissão faseados.",
        "Ações Elegíveis": "Modernização tecnológica e eficiência energética.",
        "Atividades e despesas elegíveis": "Bens de equipamento, software especializado, patentes.",
        "Custos elegíveis": "Aquisição de ativos novos e despesas de consultoria.",
        "Critérios de seleção": "Mérito do projeto e impacto na produtividade.",
        "Entidades e geografia": "PMEs e Grandes Empresas em território nacional.",
        "Detalhes Financeiros": f"Fundo: PRR | Taxa Máxima: {taxa}% | Fonte: UE",
        "Taxas de financiamento e majorações": f"Taxa base de {taxa}%. Majorações para zonas de baixa densidade.",
        "Formas de pagamento": "Adiantamento e Reembolsos contra fatura.",
        "Contactos para mais informações": "suporte@recuperarportugal.gov.pt"
    }

# --- PROCESSAMENTO ---
with st.spinner("A atualizar base de dados do PRR..."):
    dados = extrair_avisos_prr()
df_avisos = pd.DataFrame(dados)

# --- BARRA LATERAL (FILTROS) ---
with st.sidebar:
    st.title("Filtros de Pesquisa")
    
    # NOVO FILTRO: TAXA DE FINANCIAMENTO
    st.subheader("Financiamento")
    taxa_min = st.slider("Taxa de Apoio Mínima (%)", 0, 100, 0, step=5)
    
    st.subheader("Programas")
    programas_disponiveis = df_avisos['programa'].unique() if not df_avisos.empty else []
    filtro_prog = st.multiselect("Selecionar Programas:", programas_disponiveis, default=programas_disponiveis)
    
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.link_button("🔐 Login Balcão dos Fundos", "https://balcaofundosue.pt/", use_container_width=True)

# --- CORPO PRINCIPAL ---
st.title("Monitor de Fundos Europeus")

if df_avisos.empty:
    st.warning("Sem dados disponíveis.")
else:
    # APLICAR FILTROS (Programa + Taxa)
    df_filtrado = df_avisos[
        (df_avisos['programa'].isin(filtro_prog)) & 
        (df_avisos['taxa'] >= taxa_min)
    ]

    tab1, tab2 = st.tabs(["🟢 Projetos Ativos", "🔴 Histórico/Fechados"])

    def render_list(df):
        if df.empty:
            st.info("Nenhum projeto corresponde aos filtros selecionados.")
            return
        for i, row in df.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    status_class = "badge-aberto" if row['estado'] == "Aberto" else "badge-fechado"
                    st.markdown(f"<span class='{status_class}'>{row['estado']}</span> <span class='badge-taxa'>Apoio: {row['taxa']}%</span>", unsafe_allow_html=True)
                    st.markdown(f"<p class='projeto-titulo'>{row['titulo']}</p>", unsafe_allow_html=True)
                    st.markdown(f"🔗 [Página do Aviso]({row['links'][0]['url']})")
                with c2:
                    if st.button("Ver Detalhes ⚡", key=f"btn_{i}"):
                        st.session_state[f"exp_{i}"] = True
                
                if st.session_state.get(f"exp_{i}"):
                    res = gerar_resumo_aviso(row['titulo'], row['taxa'])
                    st.divider()
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**🎯 Objetivos:** {res['Finalidades e objetivos']}")
                        st.write(f"**🗓️ Condições:** {res['Prazos e condições para as PME']}")
                        st.write(f"**🛠️ Ações:** {res['Ações Elegíveis']}")
                    with col_b:
                        st.write(f"**💰 Financiamento:** {res['Detalhes Financeiros']}")
                        st.write(f"**📈 Majorações:** {res['Taxas de financiamento e majorações']}")
                        st.write(f"**📞 Contactos:** {res['Contactos para mais informações']}")

    with tab1:
        render_list(df_filtrado[df_filtrado['estado'] == "Aberto"])
    with tab2:
        render_list(df_filtrado[df_filtrado['estado'] == "Fechado"])
