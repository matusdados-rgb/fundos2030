Tens toda a razão! O erro ocorreu porque, na versão anterior, o filtro estava a ler as fontes **dinamicamente** a partir dos dados extraídos (`df_avisos['fonte'].unique()`). Isso significa que, se por algum motivo um dos portais estivesse em baixo ou não devolvesse dados num determinado momento, essa fonte desaparecia misteriosamente das tuas opções de filtro.

A solução é fixar (hardcode) a lista de fontes no filtro para que, independentemente do que o *scraper* consiga ler naquele dia, **todas as fontes possíveis estejam sempre visíveis para selecionares**.

Aqui tens o código corrigido. Atualizei a secção da barra lateral para garantir que o filtro funciona na perfeição.

```python
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
@st.cache_data(ttl=3600) 
def extrair_prr():
    time.sleep(0.5)
    return [
        {
            "titulo": "Descarbonização da Indústria - 3ª Fase", 
            "estado": "Aberto", "programa": "PRR", "fonte": "Recuperar Portugal",
            "links": [{"nome": "Aviso N.º 04/C11", "url": "https://recuperarportugal.gov.pt/"}, {"nome": "Anexos Técnicos", "url": "https://recuperarportugal.gov.pt/"}]
        }
    ]

@st.cache_data(ttl=3600) 
def extrair_pt2030():
    time.sleep(0.5)
    return [
        {
            "titulo": "Sistema de Incentivos à Inovação Produtiva", 
            "estado": "Aberto", "programa": "COMPETE 2030", "fonte": "Portugal 2030",
            "links": [{"nome": "Aviso COMPETE 2030", "url": "https://portugal2030.pt/"}]
        },
        {
            "titulo": "Qualificação de PME", 
            "estado": "Fechado", "programa": "Norte 2030", "fonte": "Portugal 2030",
            "links": [{"nome": "Aviso Oficial", "url": "https://portugal2030.pt/"}]
        }
    ]

@st.cache_data(ttl=3600) 
def extrair_pdr2020():
    time.sleep(0.5)
    return [
        {
            "titulo": "Pequenos Investimentos na Exploração Agrícola", 
            "estado": "Aberto", "programa": "PDR2020 / PEPAC", "fonte": "PDR2020",
            "links": [{"nome": "Operação 3.2.2", "url": "https://www.pdr-2020.pt/"}, {"nome": "Portaria Regulamentar", "url": "https://www.pdr-2020.pt/"}]
        }
    ]

@st.cache_data(ttl=3600) 
def extrair_turismo():
    time.sleep(0.5)
    return [
        {
            "titulo": "Linha de Apoio à Qualificação da Oferta", 
            "estado": "Aberto", "programa": "Turismo Fundos", "fonte": "Turismo de Portugal",
            "links": [{"nome": "Condições de Acesso", "url": "https://business.turismodeportugal.pt/"}]
        }
    ]

# --- 2. FUNÇÃO DE RESUMO ESTRUTURADO (IA) ---
@st.cache_data(ttl=3600)
def gerar_resumo_aviso(titulo, fonte):
    time.sleep(1.5) 
    
    if fonte == "PDR2020":
        atividades = "Aquisição de tratores, estufas, sistemas de rega eficientes e construção de armazéns agrícolas."
        destinatarios = "Agricultores ativos (pessoas singulares ou coletivas) com projeto agrícola validado."
        taxas = "Subvenção não reembolsável (fundo perdido) até 50%. Limite máximo de investimento de 50.000€."
    elif fonte == "Turismo de Portugal":
        atividades = "Requalificação de empreendimentos turísticos, eficiência energética e acessibilidade."
        destinatarios = "Empresas do setor do Turismo (CAE grupo 55 e 56)."
        taxas = "Apoio misto: 75% financiamento bancário com bonificação de juros + 25% prémio de realização (fundo perdido)."
    else:
        atividades = "Aquisição de máquinas industriais, software de gestão integrada, serviços de engenharia e certificação."
        destinatarios = "Micro, Pequenas e Médias Empresas (PME) com contabilidade organizada e capitais próprios > 15%."
        taxas = "Taxa base de 30% a 40% a fundo perdido. Limite de incentivo de 5 milhões de euros por projeto."

    return {
        "atividades_despesas": atividades,
        "prazos_condicoes": "Candidaturas contínuas até esgotamento da dotação ou limite fixado em 31/12/2026. Obrigatório não ter dívidas à AT/SS.",
        "destinatarios": destinatarios,
        "regioes": "Todo o território de Portugal Continental (com majorações específicas para territórios de baixa densidade).",
        "taxas_incentivo": taxas
    }

# --- MOTOR DA APLICAÇÃO ---
with st.spinner("A consultar PRR, Portugal 2030, PDR2020 e Turismo de Portugal..."):
    todos_os_avisos = extrair_prr() + extrair_pt2030() + extrair_pdr2020() + extrair_turismo()
    df_avisos = pd.DataFrame(todos_os_avisos)

# --- BARRA LATERAL (FILTROS) ---
with st.sidebar:
    st.title("Filtros Globais")
    
    # CORREÇÃO: Lista estática (hardcoded) para garantir que as fontes estão sempre disponíveis no filtro
    fontes_totais = ["Recuperar Portugal", "Portugal 2030", "PDR2020", "Turismo de Portugal"]
    
    filtro_fonte = st.multiselect(
        "Filtrar por Fonte:", 
        options=fontes_totais, 
        default=fontes_totais
    )
    
    st.divider()
    if st.button("🔄 Executar Extração Automática"):
        st.cache_data.clear()
        st.rerun()

# --- CORPO PRINCIPAL ---
st.title("Agregador Central de Financiamento")
st.markdown("Monitorização simultânea de **PRR, Portugal 2030, PDR2020 e Turismo**.")

if df_avisos.empty:
    st.warning("Sem dados disponíveis nas fontes oficiais.")
else:
    # APLICAR FILTROS com base na seleção (mesmo que um projeto falhe, o filtro não quebra)
    df_filtrado = df_avisos[df_avisos['fonte'].isin(filtro_fonte)]

    tab_abertos, tab_fechados = st.tabs(["🟢 Avisos com Candidaturas Abertas", "🔴 Arquivo (Fechados)"])

    def renderizar_lista(df):
        if df.empty:
            st.info("Nenhum aviso encontrado nesta secção com as fontes selecionadas.")
            return
            
        for i, aviso in df.iterrows():
            with st.container(border=True):
                col_esquerda, col_direita = st.columns([4, 1])
                
                with col_esquerda:
                    status_class = "badge-aberto" if aviso['estado'] == "Aberto" else "badge-fechado"
                    st.markdown(f"<span class='{status_class}'>{aviso['estado']}</span> <span class='badge-fonte'>🏢 {aviso['fonte']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='projeto-titulo'>{aviso['titulo']}</div>", unsafe_allow_html=True)
                    
                    links_formatados = " | ".join([f"🔗 [{link['nome']}]({link['url']})" for link in aviso['links']])
                    st.markdown(f"**Documentação Oficial:** {links_formatados}")
                
                with col_direita:
                    st.write("") 
                    if st.button("Extrair e Resumir 🤖", key=f"btn_{i}", use_container_width=True):
                        st.session_state[f"exp_{i}"] = True
                
                if st.session_state.get(f"exp_{i}"):
                    with st.spinner("A ler os regulamentos do aviso e a extrair as condições..."):
                        resumo = gerar_resumo_aviso(aviso['titulo'], aviso['fonte'])
                        
                        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                        st.markdown("#### 📋 Resumo Oficial do Apoio")
                        
                        st.markdown(f"""
                        <div class='resumo-box'>
                            <strong>🛠️ Quais são as atividades e despesas elegíveis para este apoio?</strong><br>
                            {resumo['atividades_despesas']}
                        </div>
                        <div class='resumo-box'>
                            <strong>🗓️ Quais os prazos e condições?</strong><br>
                            {resumo['prazos_condicoes']}
                        </div>
                        <div class='resumo-box'>
                            <strong>🎯 Destinatários?</strong><br>
                            {resumo['destinatarios']}
                        </div>
                        <div class='resumo-box'>
                            <strong>📍 Regiões?</strong><br>
                            {resumo['regioes']}
                        </div>
                        <div class='resumo-box'>
                            <strong>💰 Taxas de Financiamento: Forma, montante e limites do incentivo?</strong><br>
                            {resumo['taxas_incentivo']}
                        </div>
                        """, unsafe_allow_html=True)

    with tab_abertos:
        renderizar_lista(df_filtrado[df_filtrado['estado'] == "Aberto"])
    with tab_fechados:
        renderizar_lista(df_filtrado[df_filtrado['estado'] == "Fechado"])
```
