import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURAÇÃO DA PÁGINA (VISUAL INOVADOR) ---
st.set_page_config(page_title="Radar EU | Fundos", page_icon="🇪🇺", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (Para um visual mais limpo e profissional) ---
st.markdown("""
    <style>
    .stApp header {background-color: transparent;}
    .projeto-titulo {font-size: 1.2rem; font-weight: 600; color: #1E3A8A;}
    .projeto-programa {font-size: 0.9rem; color: #6B7280; font-weight: bold;}
    .badge-aberto {background-color: #DEF7EC; color: #03543F; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;}
    .badge-breve {background-color: #FEF08A; color: #854D0E; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;}
    .badge-fechado {background-color: #FDE8E8; color: #9B1C1C; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS COM CACHE (Simulação Realista) ---
@st.cache_data(ttl=3600) 
def extrair_avisos():
    time.sleep(1) # Simula o scraping
    return [
        {
            "titulo": "Inovação Produtiva - PME", 
            "estado": "Aberto", 
            "programa": "PT 2030", 
            "links": [
                {"nome": "Aviso N.º 01/COMPETE/2026", "url": "https://balcaofundosue.pt/avisos/aviso-01-compete-2026"},
                {"nome": "Anexos Técnicos", "url": "https://balcaofundosue.pt/avisos/anexos-01-compete"}
            ]
        },
        {
            "titulo": "Digitalização do Comércio Local", 
            "estado": "Brevemente", 
            "programa": "PRR", 
            "links": [
                {"nome": "Plano Anual de Avisos", "url": "https://recuperarportugal.gov.pt/plano-anual-avisos/"}
            ]
        },
        {
            "titulo": "Descarbonização da Indústria", 
            "estado": "Fechado", 
            "programa": "PRR", 
            "links": [
                {"nome": "Aviso N.º 03/C11-i01/2025", "url": "https://recuperarportugal.gov.pt/aviso-descarbonizacao/"}
            ]
        },
        {
            "titulo": "Apoio à Internacionalização", 
            "estado": "Fechado", 
            "programa": "PT 2030", 
            "links": [
                {"nome": "Aviso de Encerramento", "url": "https://balcaofundosue.pt/avisos/internacionalizacao-fechado"}
            ]
        }
    ]

@st.cache_data(ttl=3600)
def gerar_resumo_aviso(titulo):
    """Simulação da extração exata dos campos solicitados pelo utilizador."""
    time.sleep(1.5)
    return {
        "Finalidades e objetivos": "Apoiar operações de investimento que visem a inovação de produto e de processo, promovendo a alteração do perfil de especialização da economia portuguesa.",
        "Prazos e condições para as PME": "Candidaturas abertas até 30/06/2026. Obrigatório: PME certificada (IAPMEI), capitais próprios > 15%, sem dívidas SS/AT.",
        "Ações Elegíveis": "Criação de um novo estabelecimento, aumento de capacidade ou diversificação da produção.",
        "Atividades e despesas elegíveis": "CAEs da Indústria Transformadora. Máquinas, equipamentos, software e serviços de engenharia.",
        "Custos elegíveis": "Ativos corpóreos (máquinas), ativos incorpóreos (patentes até 20%) e custos com TOC/ROC até 5.000€.",
        "Critérios de seleção": "Grau de inovação (30%), Criação de emprego (20%), Viabilidade económico-financeira (50%).",
        "Entidades e geografia": "Micro, Pequenas e Médias Empresas. Portugal Continental.",
        "Detalhes Financeiros": "Fundo: FEDER | Dotação Fundo: 20M€ | Taxa Máx.: 40% | Dotação Nacional: 5M€ | Fonte de Financ. Nac.: Orçamento de Estado",
        "Taxas de financiamento e majorações": "Taxa base 30% a fundo perdido. Majorações: +10% territórios baixa densidade; +5% transição digital.",
        "Formas de pagamento": "Adiantamento de 20% com garantia bancária. Pedidos de reembolso trimestrais baseados em faturas pagas.",
        "Contactos para mais informações": "Linha dos Fundos: 800 104 114 | Email: suporte@balcaofundosue.pt"
    }

# --- MOTOR DA APLICAÇÃO ---
dados_avisos = extrair_avisos()
df_avisos = pd.DataFrame(dados_avisos)

# --- BARRA LATERAL (FILTROS E ATALHOS GLOBAIS) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg", width=50)
    st.title("Filtros Globais")
    
    filtro_programa = st.multiselect("Filtrar Programa:", options=df_avisos['programa'].unique(), default=df_avisos['programa'].unique())
    
    st.divider()
    
    # ATALHO DIRETO PARA O LOGIN DO BALCÃO DOS FUNDOS
    st.markdown("### 🔐 Área Restrita")
    link_login = "https://bfue-ids.balcaofundosue.pt/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DBalcao%252B%26redirect_uri%3Dhttps%253A%252F%252Fbalcaofundosue.pt%252Fsignin-oidc%26response_type%3Dcode%2520id_token%26scope%3Dopenid%2520profile%2520Balcao%252Bapi%26response_mode%3Dform_post%26nonce%3D639110087193244904.ZDllNmRjOTAtMDc5MS00NjM0LTgyMDAtYmYzODUzM2YyYzliZTExZTA2ZDMtNjI4Yi00YWM1LWE0Y2QtNzQ1ZDliMmQ2M2E2%26state%3DCfDJ8NLoVggsWu1Li3rXCtxGrmCKrKJy09Q3AY1KPjxZL5zsNU3ymCt5FaMvgIqR0dRqEDnUGcCh4llpzrXnHKYdd0E9ddzcE4hkl0oYhRF4JrXcqnWzryy0WVJM_p6UMQMtAakOkhb4w6pEpCu08scXZwzluLnWxfKWPrGnNkm-laM9RUHRdrAyOtIOfPrqBNUpMNZU2T_CGvzcwx8VPqfR_aSoYSPrGIUAe9sdIdLVXyc0BDGeL5J7_QtjF5ZuCoMxN1BO0C8h5ozkpptR968sV0bz5mw35zbfw-fyjhpPIs4wTKzDHzcITgsC6LXk59FiHw%26x-client-SKU%3DID_NETSTANDARD2_0%26x-client-ver%3D5.5.0.0"
    st.link_button("Submeter Candidaturas (Login) ↗", link_login, type="primary", use_container_width=True)

# --- CORPO PRINCIPAL ---
st.title("Monitor de Fundos Europeus")
st.markdown("Plataforma de agregação e análise inteligente de avisos PT2030 e PRR.")

df_filtrado = df_avisos[df_avisos['programa'].isin(filtro_programa)]

# Criação de Tabs (Separadores Inovadores)
tab1, tab2 = st.tabs(["🟢 Projetos Abertos & Brevemente", "🔴 Projetos Fechados / Histórico"])

# Função auxiliar para renderizar os cartões dos projetos
def renderizar_projetos(dataframe):
    if dataframe.empty:
        st.info("Nenhum aviso encontrado nesta categoria com os filtros atuais.")
        return

    for index, aviso in dataframe.iterrows():
        # Lógica de cores CSS
        if aviso['estado'] == "Aberto":
            badge = f"<span class='badge-aberto'>🟢 {aviso['estado'].upper()}</span>"
        elif aviso['estado'] == "Brevemente":
            badge = f"<span class='badge-breve'>🟡 {aviso['estado'].upper()}</span>"
        else:
            badge = f"<span class='badge-fechado'>🔴 {aviso['estado'].upper()}</span>"

        with st.container(border=True):
            col_info, col_action = st.columns([3, 1])
            
            with col_info:
                st.markdown(f"{badge} &nbsp; <span class='projeto-programa'>{aviso['programa']}</span>", unsafe_allow_html=True)
                st.markdown(f"<p class='projeto-titulo'>{aviso['titulo']}</p>", unsafe_allow_html=True)
                
                # Renderiza dinamicamente os atalhos exatos reais deste aviso
                urls_markdown = " | ".join([f"[{link['nome']}]({link['url']})" for link in aviso['links']])
                st.markdown(f"🔗 **Documentos Oficiais:** {urls_markdown}")
            
            with col_action:
                st.write("") # Espaçamento
                if st.button("Análise de IA ⚡", key=f"btn_{index}", use_container_width=True):
                    st.session_state[f"resumo_{index}"] = True
            
            # Área expandida após clique no botão
            if st.session_state.get(f"resumo_{index}", False):
                st.divider()
                with st.spinner("A processar e a estruturar a documentação do aviso..."):
                    resumo = gerar_resumo_aviso(aviso['titulo'])
                    
                    st.markdown("#### 📑 Resumo Estruturado do Apoio")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**🎯 Finalidades e Objetivos:**\n> {resumo['Finalidades e objetivos']}")
                        st.markdown(f"**🗓️ Prazos e Condições (PME):**\n> {resumo['Prazos e condições para as PME']}")
                        st.markdown(f"**🛠️ Ações Elegíveis:**\n> {resumo['Ações Elegíveis']}")
                        st.markdown(f"**💼 Atividades e Despesas:**\n> {resumo['Atividades e despesas elegíveis']}")
                        st.markdown(f"**🧾 Custos Elegíveis:**\n> {resumo['Custos elegíveis']}")
                        st.markdown(f"**⚖️ Critérios de Seleção:**\n> {resumo['Critérios de seleção']}")
                    with c2:
                        st.markdown(f"**🏦 Detalhes Financeiros:**\n> {resumo['Detalhes Financeiros']}")
                        st.markdown(f"**📈 Taxas e Majorações:**\n> {resumo['Taxas de financiamento e majorações']}")
                        st.markdown(f"**💳 Formas de Pagamento:**\n> {resumo['Formas de pagamento']}")
                        st.markdown(f"**📍 Entidades e Geografia:**\n> {resumo['Entidades e geografia']}")
                        st.markdown(f"**📞 Contactos:**\n> {resumo['Contactos para mais informações']}")

# Renderizar Tab 1 (Abertos e Brevemente)
with tab1:
    st.subheader("Oportunidades Atuais")
    df_abertos = df_filtrado[df_filtrado['estado'].isin(['Aberto', 'Brevemente'])]
    renderizar_projetos(df_abertos)

# Renderizar Tab 2 (Fechados)
with tab2:
    st.subheader("Histórico de Avisos")
    df_fechados = df_filtrado[df_filtrado['estado'] == 'Fechado']
    renderizar_projetos(df_fechados)
