import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- FUNÇÕES DE DADOS (Simulação) ---
def extrair_avisos():
    # Simulação dos dados raspados
    return [
        {
            "titulo": "Inovação Produtiva - PME",
            "estado": "Aberto",
            "programa": "Portugal 2030 / COMPETE 2030",
            "link_detalhe": "https://exemplo.pt/aviso1"
        },
        {
            "titulo": "Qualificação de Recursos Humanos",
            "estado": "A abrir brevemente",
            "programa": "Norte 2030",
            "link_detalhe": "https://exemplo.pt/aviso2"
        },
        {
            "titulo": "Descarbonização da Indústria",
            "estado": "Aberto",
            "programa": "PRR",
            "link_detalhe": "https://exemplo.pt/aviso3"
        }
    ]

def gerar_resumo_aviso(titulo):
    # Simulação da extração/resumo de um PDF ou página de detalhe
    return {
        "Data de Início": "01/05/2026",
        "Data de Fim": "30/06/2026",
        "Taxa de Apoio": "Até 40% a fundo perdido",
        "Apoio (Mín - Máx)": "100k€ - 5M€",
        "Despesas Elegíveis": "Maquinaria, Software, Construção civil (parcial)",
        "Tipo de Empresas": "PME, Small Mid Cap",
        "Zona": "Norte, Centro, Alentejo",
        "Majorações": "Majoração de 10% para zonas de baixa densidade."
    }

# --- INTERFACE WEB (Streamlit) ---
st.set_page_config(page_title="Radar de Fundos EU", layout="wide")

st.title("🇪🇺 Radar de Fundos Europeus (PT2030 & PRR)")
st.write(f"Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")

st.divider()

# Botão para atualizar dados
if st.button("🔄 Atualizar Avisos (Scraping)"):
    with st.spinner("A procurar novos avisos nos portais oficiais..."):
        time.sleep(1) # Simula o tempo de scraping
        st.session_state['avisos'] = extrair_avisos()
        st.success("Dados atualizados com sucesso!")

# Carregar dados iniciais se não existirem
if 'avisos' not in st.session_state:
    st.session_state['avisos'] = extrair_avisos()

avisos = st.session_state['avisos']

# --- APRESENTAÇÃO DOS DADOS ---
st.subheader("📋 Lista de Concursos")

# Mostramos a lista em formato de grelha onde podes clicar para expandir
for aviso in avisos:
    # Cria uma caixa expansível para cada projeto
    with st.expander(f"{aviso['estado'].upper()} | {aviso['programa']} - {aviso['titulo']}"):
        
        # Dividir o ecrã em duas colunas para ficar organizado
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write(f"**Estado:** {aviso['estado']}")
            st.write(f"**Programa:** {aviso['programa']}")
            st.markdown(f"[🔗 Link para o Aviso Oficial]({aviso['link_detalhe']})")
            
            # Botão para acionar o resumo gerado
            if st.button(f"Gerar Resumo Detalhado", key=aviso['titulo']):
                st.session_state[f"resumo_{aviso['titulo']}"] = gerar_resumo_aviso(aviso['titulo'])
        
        with col2:
            # Se o botão de resumo foi clicado, mostra a informação
            if f"resumo_{aviso['titulo']}" in st.session_state:
                resumo = st.session_state[f"resumo_{aviso['titulo']}"]
                st.write("### 📝 Resumo do Projeto")
                
                # Apresentar os dados estruturados de forma elegante
                for chave, valor in resumo.items():
                    st.write(f"**{chave}:** {valor}")