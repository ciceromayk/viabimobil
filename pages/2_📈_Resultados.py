import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from numpy.lib.financial import npv, irr

# Importa as funções do módulo src
from src.calculos_financieros import calcular_fluxo_de_caixa_projetado
from src.visualizacoes import plotar_fluxo_de_caixa

st.set_page_config(
    page_title="Resultados",
    page_icon="📈",
)

st.title("📈 Análise de Resultados")

# Verifica se os dados foram salvos na página de entrada
if "dados_projeto" not in st.session_state:
    st.warning("Por favor, preencha os dados na página 'Dados de Entrada' primeiro.")
else:
    dados_projeto = st.session_state["dados_projeto"]

    # Simulação de Cenários com slider (Análise de Sensibilidade)
    st.header("Simulação de Cenários")
    st.write("Altere as variáveis abaixo para simular o impacto nos resultados.")
    
    variacao_preco = st.slider(
        "Variação no Preço de Venda (%)",
        min_value=-20, max_value=20, value=0, step=1
    )
    
    # Aplica a variação ao preço de venda
    preco_ajustado = dados_projeto["preco_venda_por_metro_quadrado"] * (1 + variacao_preco / 100)

    # Recalcula o fluxo de caixa com o novo preço
    fluxo_caixa_df = calcular_fluxo_de_caixa_projetado(
        duracao_projeto=dados_projeto["duracao_projeto"],
        area_construida=dados_projeto["area_construida"],
        custo_por_metro_quadrado=dados_projeto["custo_por_metro_quadrado"],
        preco_venda_por_metro_quadrado=preco_ajustado,
        taxa_deducao_vendas=dados_projeto["taxa_deducao_vendas"]
    )
    
    # Calcula VPL e TIR
    taxa_desconto_mensal = (1 + dados_projeto["taxa_desconto"])**(1/12) - 1
    vpl = npv(taxa_desconto_mensal, fluxo_caixa_df["Fluxo de Caixa"].values)
    tir = irr(fluxo_caixa_df["Fluxo de Caixa"].values)

    st.markdown("---")
    
    # Exibe os indicadores-chave
    st.header("Indicadores-Chave")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("VPL", f"R$ {vpl:,.2f}")
    with col2:
        st.metric("TIR", f"{tir * 100:,.2f}%")
    with col3:
        margem_lucro = (vpl / abs(fluxo_caixa_df["Fluxo de Caixa"].iloc[0])) * 100 if vpl > 0 else 0
        st.metric("Margem de Lucro", f"{margem_lucro:,.2f}%")

    st.markdown("---")

    # Exibe o gráfico do fluxo de caixa
    st.header("Gráfico do Fluxo de Caixa")
    fig = plotar_fluxo_de_caixa(fluxo_caixa_df)
    st.plotly_chart(fig)
