import streamlit as st

# Importa a função do módulo src
from src.calculos_financeiros import calcular_resultado_negocio

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
    st.write("Altere o preço de vendas para simular o impacto no resultado do negócio.")
    
    variacao_preco = st.slider(
        "Variação no Preço Médio de Vendas (%)",
        min_value=-20,
        max_value=20,
        value=0,
        step=1
    )
    
    # Aplica a variação ao preço de venda
    preco_ajustado = dados_projeto["preco_medio_vendas"] * (1 + variacao_preco / 100)

    # Recalcula os resultados com o novo preço
    resultados = calcular_resultado_negocio(
        area_terreno=dados_projeto["area_terreno"],
        indice_aproveitamento=dados_projeto["indice_aproveitamento"],
        custo_por_metro_quadrado=dados_projeto["custo_por_metro_quadrado"],
        relacao_privativa_construida=dados_projeto["relacao_privativa_construida"],
        preco_medio_vendas=preco_ajustado
    )
    
    st.markdown("---")
    
    # Exibe os indicadores-chave
    st.header("Indicadores-Chave")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Área Construída", f"{resultados['area_construida']:,.2f} m²")
    with col2:
        st.metric("Área Privativa", f"{resultados['area_privativa']:,.2f} m²")
    with col3:
        st.metric("V.G.V.", f"R$ {resultados['vgv']:,.2f}")

    st.markdown("---")
    
    st.header("Resumo Financeiro")
    
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Custo Total", f"R$ {resultados['custo_total']:,.2f}")
    with col5:
        st.metric("Resultado do Negócio", f"R$ {resultados['resultado_negocio']:,.2f}")
