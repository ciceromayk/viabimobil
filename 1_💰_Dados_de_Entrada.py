import streamlit as st
import pandas as pd

# Importa a função do módulo src
from src.calculos_financeiros import calcular_resultado_negocio

st.set_page_config(
    page_title="Viabilidade Imobiliária",
    page_icon="🏠",
    layout="wide"
)

# Adiciona CSS para o estilo dos cards
st.markdown("""
<style>
    .card {
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.1);
        transition: 0.3s;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin: 5px;
    }
    .card-title {
        font-size: 0.8em;
        font-weight: bold;
        margin-bottom: 3px;
        color: #262626;
    }
    .card-metric {
        font-size: 1.2em;
        font-weight: bold;
        color: #4d94ff;
        word-wrap: break-word; /* Garante que os números se quebrem se forem muito longos */
    }
    .card.positive {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .card.negative {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
    .card.neutral {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
    }
    /* Ajusta a barra lateral para ser mais compacta */
    .st-emotion-cache-1cypcdb {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ----- Sidebar para Parâmetros de Entrada -----
with st.sidebar:
    st.header("Análise de Viabilidade")
    st.subheader("Parâmetros do Projeto")
    st.markdown("---")
    
    st.subheader("1. Terreno e Construção")
    area_terreno = st.number_input("Área do Terreno (m²)", min_value=0.0)
    indice_aproveitamento = st.slider(
        "Índice de Aproveitamento",
        min_value=1.00,
        max_value=4.00,
        value=1.00,
        step=0.01,
    )
    custo_por_metro_quadrado = st.number_input("Custo de Área Construída (R$/m²)", min_value=0.0)
    relacao_privativa_construida = st.slider(
        "Relação Área Privativa / Área Construída",
        min_value=0.00,
        max_value=1.00,
        value=0.70,
        step=0.01,
    )
    
    st.markdown("---")

    st.subheader("2. Vendas")
    preco_medio_vendas = st.number_input("Preço Médio de Vendas (R$/m²)", min_value=0.0)

# ----- Main Content (Conteúdo Principal) -----
st.title("💰 Análise de Viabilidade Imobiliária")
st.write("Insira os parâmetros no menu lateral para a análise de viabilidade do seu projeto imobiliário.")

# Seção de Resultados (agora em tempo real)
st.header("Análise de Cenários")
st.write("Altere os parâmetros acima para simular o impacto no resultado do negócio.")
    
# Slider para controlar a variação do preço
variacao_preco = st.slider(
    "Variação no Preço (%)",
    min_value=-20,
    max_value=20,
    value=0,
    step=1
)
    
preco_ajustado = preco_medio_vendas * (1 + variacao_preco / 100)
    
# Cards de preço
col_preco_original, col_preco_ajustado = st.columns(2)
    
with col_preco_original:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Preço Original (R$/m²)</div>
        <div class="card-metric">R$ {preco_medio_vendas:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
with col_preco_ajustado:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Preço Ajustado (R$/m²)</div>
        <div class="card-metric">R$ {preco_ajustado:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# Recalcula os resultados com o novo preço ajustado
resultados_ajustados = calcular_resultado_negocio(
    area_terreno=area_terreno,
    indice_aproveitamento=indice_aproveitamento,
    custo_por_metro_quadrado=custo_por_metro_quadrado,
    relacao_privativa_construida=relacao_privativa_construida,
    preco_medio_vendas=preco_ajustado
)

st.markdown("---")
    
# Resumo do Projeto
st.header("Resumo do Projeto")
col1, col2, col3, col4, col5 = st.columns(5)
    
with col1:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Área do Terreno</div>
        <div class="card-metric">{area_terreno:,.2f} m²</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Índice de Aproveitamento</div>
        <div class="card-metric">{indice_aproveitamento:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Área Construída</div>
        <div class="card-metric">{resultados_ajustados['area_construida']:,.2f} m²</div>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Área Privativa</div>
        <div class="card-metric">{resultados_ajustados['area_privativa']:,.2f} m²</div>
    </div>
    """, unsafe_allow_html=True)
    
with col5:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Relação AP/AC</div>
        <div class="card-metric">{relacao_privativa_construida:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Resumo Financeiro
st.header("Resumo Financeiro")
col6, col7, col8, col9 = st.columns(4)
    
with col6:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">V.G.V.</div>
        <div class="card-metric">R$ {resultados_ajustados['vgv']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Custo Total</div>
        <div class="card-metric">R$ {resultados_ajustados['custo_total']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
with col8:
    # Lógica para colorir o card de Resultado do Negócio
    resultado_negocio = resultados_ajustados['resultado_negocio']
    card_class = "positive" if resultado_negocio > 0 else "negative" if resultado_negocio < 0 else "neutral"

    st.markdown(f"""
    <div class="card {card_class}">
        <div class="card-title">Resultado do Negócio</div>
        <div class="card-metric">R$ {resultado_negocio:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col9:
    # Lógica para colorir o card de Margem de Lucro
    margem_lucro = (resultados_ajustados['resultado_negocio'] / resultados_ajustados['vgv']) * 100 if resultados_ajustados['vgv'] != 0 else 0
    card_class = "positive" if margem_lucro > 0 else "negative" if margem_lucro < 0 else "neutral"
    st.markdown(f"""
    <div class="card {card_class}">
        <div class="card-title">Margem de Lucro</div>
        <div class="card-metric">{margem_lucro:,.2f}%</div>
    </div>
    """, unsafe_allow_html=True)
