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
    .resumo-box {background-color: #F8FAFC; padding: 12px 15px; border-left: 4px solid #3B82F6; border-radius: 4px; margin-bottom: 8px; font-size: 0.95rem; line-height: 1.5;}
    .resumo-box strong {color: #1E40AF;}
    </style>
""", unsafe_allow_html=True)

# --- 1. FUNÇÕES DE EXTRAÇÃO DE DADOS ---
@st.cache_data(ttl=60)
def extrair_dados():
    time.sleep(0.5)
    return [
        {"titulo": "Descarbonização da Indústria", "estado": "Aberto", "programa": "PRR", "fonte": "Recuperar Portugal", "links": [{"nome": "Aviso Oficial", "url": "https://recuperarportugal.gov.pt/"}]},
        {"titulo": "Inovação Produtiva", "estado": "Aberto", "programa": "COMPETE 2030", "fonte": "Portugal 2030", "links": [{"nome": "Aviso Oficial", "url": "https://portugal2030.pt/"}]},
        {"titulo": "Qualificação de PME", "estado": "Fechado", "programa": "Norte 2030", "fonte": "Portugal 2030", "links": [{"nome": "Aviso Oficial", "url": "https://portugal2030.pt/"}]},
        {"titulo": "Pequenos Investimentos Agrícolas", "estado": "Aberto", "programa": "PDR2020", "fonte": "PDR2020", "links": [{"nome": "Aviso Oficial", "url": "https://www.pdr-2020.pt/"}]},
        {"titulo": "Qualificação da Oferta", "estado": "Aberto", "programa": "Turismo Fundos", "fonte": "Turismo de Portugal", "links": [{"nome": "Aviso Oficial", "url": "https://business.turismodeportugal.pt/"}]},
        # NOVA FONTE: IEFP
        {"titulo": "Compromisso Emprego Sustentável", "estado": "Aberto", "programa": "Medidas de Emprego", "fonte": "IEFP", "links": [{"nome": "Aviso Oficial IEFP", "url": "https://www.iefp.pt/"}]}
    ]

# --- 2. FUNÇÃO DE RESUMO ESTRUTURADO (IA - 11 PONTOS) ---
def gerar_resumo_aviso(titulo, fonte):
    if fonte == "PDR2020":
        return {
            "1_areas": "Modernização do setor agroflorestal, eficiência hídrica e melhoria da capacidade produtiva e de armazenamento.",
            "2_financiamento_prazos": "Duração máxima da execução física e financeira do projeto: 18 meses após a assinatura do Termo de Aceitação.",
            "3_montantes_regiao": "Min: 5.000€ | Max: 50.000€ por operação. Aplicável de igual forma em todo o território continental.",
            "4_criterios_eleg": "Viabilidade económica comprovada; titularidade da exploração agrícola; inexistência de dívidas à Autoridade Tributária e Segurança Social.",
            "5_publico_alvo": "Pessoas Singulares ou Coletivas que exerçam atividade agrícola.",
            "6_cae": "CAE Secção A (Agricultura, Produção Animal, Caça, Floresta e Pesca), especificamente divisões 01 a 03.",
            "7_montantes_invest": "Dotação orçamental global do aviso: 15 Milhões de Euros.",
            "8_taxas": "Incentivo não reembolsável (Fundo Perdido). Taxa base de 40%, com majorações até 50% para Jovens Agricultores ou Zonas Desfavorecidas.",
            "9_despesas": "Aquisição de máquinas e equipamentos novos (ex: tratores), sistemas de rega, construção/adaptação de instalações e estudos técnicos (até 5%).",
            "10_entidades": "Agricultores ativos, Cooperativas agrícolas e Sociedades Agropecuárias.",
            "11_prazos": "Submissões abertas de 01/05/2026 a 30/09/2026. Análise das candidaturas efetuada de forma contínua."
        }
    elif fonte == "Turismo de Portugal":
        return {
            "1_areas": "Transição digital, eficiência energética, economia circular e acessibilidade nos empreendimentos turísticos.",
            "2_financiamento_prazos": "Carência de capital até 24 meses; amortização em 7 anos (projetos gerais) ou 10 anos (projetos sustentáveis).",
            "3_montantes_regiao": "Min: 150.000€ | Max: 3.000.000€. Territórios de Baixa Densidade têm dotação específica cativada.",
            "4_criterios_eleg": "Licenciamento turístico regularizado; Autonomia Financeira pré-projeto >= 15%; Registo Nacional de Turismo ativo.",
            "5_publico_alvo": "Empresas com operação turística ativa (Micro, Pequenas, Médias e Grandes Empresas).",
            "6_cae": "CAE 55 (Alojamento), 56 (Restauração), 77210 (Aluguer de bens recreativos), 93 (Atividades desportivas e de diversão).",
            "7_montantes_invest": "Dotação global: 100 Milhões de Euros (provenientes de capitais próprios do Turismo de Portugal e Banca protocolada).",
            "8_taxas": "Apoio Misto: Até 75% do investimento elegível garantido por financiamento bancário, com prémio de desempenho (fundo perdido) até 20% do valor do empréstimo.",
            "9_despesas": "Obras de requalificação, aquisição de equipamentos eco-eficientes, software de gestão turística e formação de RH associada ao investimento.",
            "10_entidades": "Sociedades comerciais legalmente constituídas com sede em Portugal.",
            "11_prazos": "Aviso de regime aberto (submissão contínua) até ao esgotamento da dotação orçamental."
        }
    elif fonte == "IEFP":
        return {
            "1_areas": "Apoios à contratação sem termo, estágios profissionais (ATIVAR) e programas de criação do próprio emprego.",
            "2_financiamento_prazos": "Pagamento efetuado em prestações (ex: 60% no início, 40% no mês 13). Obrigação de manutenção do contrato de trabalho por 24 meses.",
            "3_montantes_regiao": "Apoio base indexado ao IAS (Indexante dos Apoios Sociais). Majorações de +25% para contratações em territórios do Interior.",
            "4_criterios_eleg": "Criação líquida de emprego comprovada. Inexistência de despedimentos coletivos ou por extinção de posto de trabalho nos últimos 3 meses.",
            "5_publico_alvo": "Desempregados inscritos no IEFP, com foco em jovens (<35 anos), desempregados de longa duração e públicos sub-representados.",
            "6_cae": "Aplicável à generalidade dos CAEs (PMEs e Grandes Empresas), exceto subsetores financeiros, seguros e entidades públicas.",
            "7_montantes_invest": "Dotação gerida diretamente pelo IEFP, frequentemente cofinanciada pelo Fundo Social Europeu Mais (FSE+).",
            "8_taxas": "Prémio financeiro direto (Subsídio não reembolsável) por cada trabalhador contratado, acrescido de isenção ou redução de 50% na TSU.",
            "9_despesas": "Apoio para comparticipação dos salários base dos colaboradores contratados no âmbito da medida.",
            "10_entidades": "Pessoas singulares ou coletivas de natureza privada, com ou sem fins lucrativos.",
            "11_prazos": "Candidaturas em regime aberto ou sujeitas a períodos de aviso específicos publicados no portal IEFPonline."
        }
    else: # PRR e PT2030 (Genérico Industrial/Inovação)
        return {
            "1_areas": "Inovação tecnológica (Indústria 4.0), diversificação da produção e transição climática (redução de pegada carbónica).",
            "2_financiamento_prazos": "Conclusão da operação num prazo máximo de 24 meses. Pedidos de pagamento intercalares permitidos a cada 3 meses.",
            "3_montantes_regiao": "Norte, Centro e Alentejo: Max 5M€. Lisboa e Algarve: Max 1.5M€ (condicionado às regras de auxílio de estado de minimis).",
            "4_criterios_eleg": "Autonomia Financeira > 15% (ou 10% se startup < 1 ano); sem projetos por concluir da mesma tipologia do PT2020; Certificação PME.",
            "5_publico_alvo": "Micro, Pequenas e Médias Empresas (PME) e, excecionalmente, Small Mid Caps (até 500 colaboradores).",
            "6_cae": "CAE 10 a 33 (Indústrias Transformadoras), CAE 62 (Atividades de Informática) e CAE 72 (I&D).",
            "7_montantes_invest": "Investimento mínimo elegível: 250.000€. Dotação total do concurso: 250 Milhões de Euros.",
            "8_taxas": "Subvenção Não Reembolsável (Fundo perdido) com taxa base de 30%. Majorações: +10% Baixa Densidade; +10% Indústria 4.0. Limite máximo global: 50%.",
            "9_despesas": "Máquinas e equipamentos produtivos, patentes e licenças, serviços de engenharia e certificações de qualidade/ambiente.",
            "10_entidades": "Empresas sob a forma de sociedades comerciais (S.A., Lda., Unipessoal Lda.).",
            "11_prazos": "Fase 1: Até 30/06/2026. Fase 2: Até 31/10/2026. Fase 3 (sujeito a dotação sobrante): 31/12/2026."
        }

# --- MOTOR DA APLICAÇÃO ---
with st.spinner("A consultar bases de dados..."):
    dados_brutos = extrair_dados()
    if not dados_brutos:
        df_avisos = pd.DataFrame(columns=["titulo", "estado", "programa", "fonte", "links"])
    else:
        df_avisos = pd.DataFrame(dados_brutos)

# --- BARRA LATERAL (FILTROS E ATALHOS) ---
with st.sidebar:
    st.title("Filtros Globais")
    
    # Adicionada a nova fonte IEFP à lista base
    fontes_totais = ["Recuperar Portugal", "Portugal 2030", "PDR2020", "Turismo de Portugal", "IEFP"]
    filtro_fonte = st.multiselect("Filtrar por Fonte:", options=fontes_totais, default=fontes_totais)
    
    st.divider()
    
    # Botão de atualização visível (Forçar limpeza)
    if st.button("🔄 Forçar Atualização dos Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # ATALHOS RÁPIDOS
    st.markdown("### 🔗 Links Oficiais Rápidos")
    st.link_button("Balcão dos Fundos ↗", "https://balcaofundosue.pt/", use_container_width=True)
    st.link_button("Portal das Finanças (AT) ↗", "https://www.portaldasfinancas.gov.pt/", use_container_width=True)
    st.link_button("IEFP Online ↗", "https://iefponline.iefp.pt/", use_container_width=True)

# --- CORPO PRINCIPAL ---
st.title("Agregador Central de Financiamento")

if df_avisos.empty:
    st.warning("A base de dados encontra-se atualmente vazia.")
else:
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
                    st.markdown("#### 📑 Síntese Técnica do Aviso")
                    
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.markdown(f"<div class='resumo-box'><strong>1. Áreas de Intervenção:</strong><br>{resumo['1_areas']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>3. Investimento por Região (Min/Max):</strong><br>{resumo['3_montantes_regiao']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>5. Público-Alvo:</strong><br>{resumo['5_publico_alvo']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>7. Montantes Globais de Investimento:</strong><br>{resumo['7_montantes_invest']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>9. Despesas Elegíveis:</strong><br>{resumo['9_despesas']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>11. Prazos de Candidatura:</strong><br>{resumo['11_prazos']}</div>", unsafe_allow_html=True)

                    with c2:
                        st.markdown(f"<div class='resumo-box'><strong>2. Financiamento e Prazos de Execução:</strong><br>{resumo['2_financiamento_prazos']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>4. Critérios de Elegibilidade:</strong><br>{resumo['4_criterios_eleg']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>6. CAE Elegíveis:</strong><br>{resumo['6_cae']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>8. Taxas de Financiamento:</strong><br>{resumo['8_taxas']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='resumo-box'><strong>10. Entidades Elegíveis:</strong><br>{resumo['10_entidades']}</div>", unsafe_allow_html=True)

    with tab_abertos:
        renderizar_lista(df_filtrado[df_filtrado['estado'] == "Aberto"])
    with tab_fechados:
        renderizar_lista(df_filtrado[df_filtrado['estado'] == "Fechado"])
