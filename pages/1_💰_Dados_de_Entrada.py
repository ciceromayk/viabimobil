import streamlit as st
import pandas as pd

# Importa a função do módulo de cálculos para uso futuro
# from src.calculos_financeiros import calcular_vpl_tir

st.set_page_config(
    page_title="Dados de Entrada",
    page_icon="💰",
)

st.title("💰 Dados de Entrada do Projeto")

st.header("Informações do Terreno e da Obra")
area_terreno = st.number_input("Área Total do Terreno (m²)", min_value=0.0)
area_construida = st.number_input("Área Construída (m²)", min_value=0.0)
custo_por_metro_quadrado = st.number_input("Custo Médio de Construção (R$/m²)", min_value=0.0)

st.header("Condições de Venda")
preco_venda_por_metro_quadrado = st.number_input("Preço de Venda por m² (R$/m²)", min_value=0.0)
taxa_deducao_vendas = st.slider("Deduções sobre Vendas (%)", min_value=0, max_value=100, value=15)

st.header("Outras Informações")
taxa_desconto = st.number_input("Taxa de Desconto Anual (%)", min_value=0.0)
duracao_projeto = st.number_input("Duração do Projeto (meses)", min_value=1)

# Botão para salvar os dados no Session State para uso em outras páginas
if st.button("Salvar Dados"):
    st.session_state["dados_projeto"] = {
        "area_terreno": area_terreno,
        "area_construida": area_construida,
        "custo_por_metro_quadrado": custo_por_metro_quadrado,
        "preco_venda_por_metro_quadrado": preco_venda_por_metro_quadrado,
        "taxa_deducao_vendas": taxa_deducao_vendas / 100, # Convertendo para decimal
        "taxa_desconto": taxa_desconto / 100, # Convertendo para decimal
        "duracao_projeto": duracao_projeto,
    }
    st.success("Dados salvos com sucesso! Agora você pode ir para a página de Resultados.")
