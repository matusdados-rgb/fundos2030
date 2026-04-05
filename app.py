import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Radar de Fundos EU", page_icon="🇪🇺", layout="wide")

# --- FUNÇÕES DE DADOS COM CACHE ---
@st.cache_data(ttl=3600) 
def extrair_avisos():
    """
    Simulação dos dados raspados. 
    Notar a nova estrutura de 'links' que suporta múltiplos ficheiros/URLs por projeto.
    """
    time.sleep(1.5) # Simula o tempo de ligação
    
    return [
        {
            "titulo": "Inovação Produtiva - PME", 
            "estado": "Aberto", 
            "programa": "PT 2030", 
            "links": [
                {"nome": "Aviso N.º 01/COMPETE/2026", "url": "https://exemplo.pt/aviso_principal.pdf"},
                {"nome": "Anexos Técnicos", "url": "https://exemplo.pt/anexos.pdf"}
            ]
        },
        {
            "titulo": "Qualificação de Recursos Humanos", 
            "estado": "Brevemente", 
            "programa": "Norte 2030", 
            "links": [
                {"nome": "Plano Anual de Avisos (Pág. 12)", "url": "https://exemplo.pt/plano.pdf"}
            ]
        },
        {
            "titulo": "Descarbonização da Indústria", 
            "estado": "Aberto", 
            "programa": "PRR", 
            "links": [
                {"nome": "Aviso N.º 03/C11-i01/2026", "url": "https://exemplo.pt/aviso_prr.pdf"}
            ]
        }
    ]

@st.cache_data(ttl=3600)
def gerar_resumo_aviso(titulo):
    """
    Simula a extração inteligente (ex: via IA) de um PDF longo, 
    mapeando as regras para os teus campos específicos.
    """
    time.sleep(1) # Simula tempo de processamento/IA
    
    return {
        "Prazos e condições para as PME": "Candidaturas até 30 de Junho de 2026. Necessário ter contabilidade organizada, capitais próprios positivos e não ter dívidas à AT/SS.",
        "Ações Elegíveis": "Criação de um novo estabelecimento, aumento da capacidade de um estabelecimento existente ou diversificação da produção.",
        "Atividades e despesas elegíveis": "Atividades da indústria transformadora e turismo. Despesas com máquinas, equipamentos, software e serviços de engenharia.",
        "Custos elegíveis": "Ativos corpóreos (maquinaria), ativos incorpóreos (patentes, software até 20% do total) e TOC/ROC até 5.000€.",
        "Financiamento": "Apoio misto (subvenção não reembolsável + empréstimo bancário sem juros). Fundo FEDER e PRR.",
        "Taxas de financiamento e majorações": "Taxa base de 30% a fundo perdido. Majorações: +10% para investimentos no interior, +5% para Indústria 4.0 (Máximo de 40%).",
        "Critérios de seleção": "Grau de inovação do projeto (30%), Criação de emprego qualificado (20%), Viabilidade económico-financeira (50%).",
        "Entidades e geografia": "PME (Micro, Pequenas e Médias Empresas). Abrange Portugal Continental (Norte, Centro, Alentejo têm dotações específicas)."
    }

# --- INTERFACE WEB ---

st.title("🇪🇺 Radar de Fundos Europeus")
st.markdown("Monitorização diária de avisos PT2030 e PRR.")

try:
    dados_avisos = extrair_avisos()
    df_avisos = pd.DataFrame(dados_avisos)
except Exception as e:
    st.error(f"Erro ao ligar aos portais: {e}")
    st.stop()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("🔍 Filtros")
filtro_estado = st.sidebar.multiselect(
    "Estado do Aviso:",
    options=df_avisos['estado'].unique(),
    default=["Aberto", "Brevemente"]
)

filtro_programa = st.sidebar.multiselect(
    "Programa:",
    options=df_avisos['programa'].unique(),
    default=df_avisos['programa'].unique()
)

if st.sidebar.button("🔄 Forçar Atualização"):
    st.cache_data.clear()
    st.rerun()

# --- APLICAR FILTROS ---
df_filtrado = df_avisos[
    (df_avisos['estado'].isin(filtro_estado)) & 
    (df_avisos['programa'].isin(filtro_programa))
]

# --- MÉTRICAS GERAIS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total de Avisos", len(df_filtrado))
col2.metric("Avisos Abertos", len(df_filtrado[df_filtrado['estado'] == 'Aberto']))
col3.metric("Última Verificação", datetime.now().strftime('%H:%M'))

st.divider()

# --- APRESENTAÇÃO DOS DADOS ---
if df_filtrado.empty:
    st.warning("Nenhum aviso encontrado com os filtros atuais.")
else:
    for index, aviso in df_filtrado.iterrows():
        
        cor_estado = "🟢" if aviso['estado'] == "Aberto" else "🟡" if aviso['estado'] == "Brevemente" else "🔴"
        
        with st.expander(f"{cor_estado} {aviso['programa']} | {aviso['titulo']}"):
            
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.write(f"**Estado:** {aviso['estado']}")
                
                # Renderiza dinamicamente os links exatos de cada aviso
                st.markdown("**Documentos Oficiais:**")
                for link in aviso['links']:
                    st.markdown(f"🔗 [{link['nome']}]({link['url']})")
                
                st.write("") # Espaço vazio
                if st.button("Ler e Resumir Aviso", key=f"btn_{index}"):
                    st.session_state[f"resumo_{index}"] = True
            
            with c2:
                if st.session_state.get(f"resumo_{index}", False):
                    with st.spinner("A processar a documentação do aviso..."):
                        resumo = gerar_resumo_aviso(aviso['titulo'])
                        
                        st.markdown("### 📋 Análise Detalhada do Apoio")
                        
                        # Organização em bullet points para fácil leitura
                        st.markdown(f"**🗓️ Prazos e Condições PME:**\n> {resumo['Prazos e condições para as PME']}")
                        st.markdown(f"**🎯 Ações Elegíveis:**\n> {resumo['Ações Elegíveis']}")
                        st.markdown(f"**💼 Atividades e Despesas Elegíveis:**\n> {resumo['Atividades e despesas elegíveis']}")
                        st.markdown(f"**💰 Custos Elegíveis:**\n> {resumo['Custos elegíveis']}")
                        st.markdown(f"**🏦 Financiamento:**\n> {resumo['Financiamento']}")
                        st.markdown(f"**📈 Taxas e Majorações:**\n> {resumo['Taxas de financiamento e majorações']}")
                        st.markdown(f"**⚖️ Critérios de Seleção:**\n> {resumo['Critérios de seleção']}")
                        st.markdown(f"**📍 Entidades e Geografia:**\n> {resumo['Entidades e geografia']}")
