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
</style>
""", unsafe_allow_html=True)

st.title("💰 Análise de Viabilidade Imobiliária")
st.write("Insira os parâmetros para a análise de viabilidade do seu projeto imobiliário.")

st.subheader("1. Terreno e Construção")
col1, col2, col3, col4 = st.columns(4)
with col1:
    area_terreno = st.number_input("Área do Terreno (m²)", min_value=0.0)
with col2:
    indice_aproveitamento = st.slider(
        "Índice de Aproveitamento",
        min_value=1.00,
        max_value=4.00,
        value=1.00,
        step=0.01,
    )
with col3:
    custo_direto_construcao_m2 = st.number_input("Custo Direto de Construção (R$/m²)", min_value=0.0)
with col4:
    relacao_privativa_construida = st.slider(
        "Relação AP / AC",
        min_value=0.00,
        max_value=1.00,
        value=0.70,
        step=0.01,
    )

st.subheader("2. Vendas")
col5, col6 = st.columns(2)
with col5:
    preco_medio_vendas = st.number_input("Preço Médio de Vendas (R$/m²)", min_value=0.0)

# Expansor para Custos Indiretos
st.markdown("---")
st.subheader("3. Custos Indiretos")
with st.expander("Configurar Custos Indiretos", expanded=False):
    st.write("Selecione a forma de cálculo:")
    modo_calculo = st.radio(" ", ["Percentual sobre VGV", "Valor Absoluto (R$)"], key="custo_indireto_mode", horizontal=True)

    custos_indiretos_percentual = 0.0
    custos_indiretos_absoluto = 0.0

    if modo_calculo == "Percentual sobre VGV":
        col_irpj, col_corretagem, col_publicidade = st.columns(3)
        with col_irpj:
            irpj = st.number_input("IRPJ/CS/PIS/COFINS (%)", min_value=0.0, value=4.00)
            manutencao = st.number_input("Manutenção (%)", min_value=0.0, value=0.50)
            outorga = st.number_input("Outorga Onerosa (%)", min_value=0.0, value=0.00)
            iptu = st.number_input("IPTU (%)", min_value=0.0, value=0.07)
        with col_corretagem:
            corretagem = st.number_input("Corretagem (%)", min_value=0.0, value=3.61)
            custo_fixo = st.number_input("Custo Fixo IDIBRA (%)", min_value=0.0, value=4.00)
            condominio = st.number_input("Condomínio (%)", min_value=0.0, value=0.00)
        with col_publicidade:
            publicidade = st.number_input("Publicidade (%)", min_value=0.0, value=0.90)
            assessoria = st.number_input("Assessoria Técnica (%)", min_value=0.0, value=0.70)
            projetos = st.number_input("Projetos (%)", min_value=0.0, value=0.52)
            licenciamento = st.number_input("Licenciamento e Incorporação (%)", min_value=0.0, value=0.20)
            preparacao_terreno = st.number_input("Preparação do Terreno (%)", min_value=0.0, value=0.33)
            financiamento = st.number_input("Financiamento Bancário (%)", min_value=0.0, value=1.90)

        custos_indiretos_percentual = iptu + corretagem + publicidade + manutencao + custo_fixo + assessoria + projetos + licenciamento + outorga + condominio + preparacao_terreno + financiamento
        st.metric("Total de Custos Indiretos (%)", f"{custos_indiretos_percentual:,.2f}%")
    else:
        custos_indiretos_absoluto = st.number_input("Custo Indireto Total (R$)", min_value=0.0)

# Recalcula os resultados com base nos parâmetros
resultados = calcular_resultado_negocio(
    area_terreno=area_terreno,
    indice_aproveitamento=indice_aproveitamento,
    custo_direto_construcao_m2=custo_direto_construcao_m2,
    relacao_privativa_construida=relacao_privativa_construida,
    preco_medio_vendas=preco_medio_vendas,
    custos_indiretos_percentual=custos_indiretos_percentual,
    custos_indiretos_absoluto=custos_indiretos_absoluto
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
        <div class="card-metric">{resultados['area_construida']:,.2f} m²</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Área Privativa</div>
        <div class="card-metric">{resultados['area_privativa']:,.2f} m²</div>
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

# Resumo de Custos
st.header("Resumo de Custos")
col_custos_1, col_custos_2, col_custos_3 = st.columns(3)
with col_custos_1:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Custos Diretos</div>
        <div class="card-metric">R$ {resultados['custo_direto_total']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with col_custos_2:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Custos Indiretos</div>
        <div class="card-metric">R$ {resultados['custos_indiretos_total']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with col_custos_3:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Custo Total</div>
        <div class="card-metric">R$ {resultados['custo_total']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Resumo Financeiro
st.header("Resumo Financeiro")
col6, col7, col8 = st.columns(3)
with col6:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">V.G.V.</div>
        <div class="card-metric">R$ {resultados['vgv']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with col7:
    resultado_negocio = resultados['resultado_negocio']
    card_class = "positive" if resultado_negocio > 0 else "negative" if resultado_negocio < 0 else "neutral"
    st.markdown(f"""
    <div class="card {card_class}">
        <div class="card-title">Resultado do Negócio</div>
        <div class="card-metric">R$ {resultado_negocio:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with col8:
    margem_lucro = (resultados['resultado_negocio'] / resultados['vgv']) * 100 if resultados['vgv'] != 0 else 0
    card_class = "positive" if margem_lucro > 0 else "negative" if margem_lucro < 0 else "neutral"
    st.markdown(f"""
    <div class="card {card_class}">
        <div class="card-title">Margem de Lucro</div>
        <div class="card-metric">{margem_lucro:,.2f}%</div>
    </div>
    """, unsafe_allow_html=True)
