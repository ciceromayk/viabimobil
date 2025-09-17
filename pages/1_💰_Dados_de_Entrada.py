import streamlit as st

st.set_page_config(
    page_title="Dados de Entrada",
    page_icon="💰",
)

st.title("💰 Dados de Entrada do Projeto")

st.header("Informações do Terreno e Construção")
area_terreno = st.number_input("Área do Terreno (m²)", min_value=0.0)
indice_aproveitamento = st.slider(
    "Índice de Aproveitamento",
    min_value=1.00,
    max_value=4.00,
    value=1.00,
    step=0.01,
)

st.header("Custos e Vendas")
custo_por_metro_quadrado = st.number_input("Custo de Área Construída (R$/m²)", min_value=0.0)
relacao_privativa_construida = st.slider(
    "Relação Área Privativa / Área Construída",
    min_value=0.00,
    max_value=1.00,
    value=0.70,
    step=0.01,
)
preco_medio_vendas = st.number_input("Preço Médio de Vendas (R$/m²)", min_value=0.0)

# Botão para salvar os dados no Session State para uso em outras páginas
if st.button("Salvar Dados"):
    st.session_state["dados_projeto"] = {
        "area_terreno": area_terreno,
        "indice_aproveitamento": indice_aproveitamento,
        "custo_por_metro_quadrado": custo_por_metro_quadrado,
        "relacao_privativa_construida": relacao_privativa_construida,
        "preco_medio_vendas": preco_medio_vendas,
    }
    st.success("Dados salvos com sucesso! Agora você pode ir para a página de Resultados.")
