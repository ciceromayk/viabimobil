import streamlit as st

# Importa a função do módulo src
from src.calculos_financeiros import calcular_resultado_negocio

st.set_page_config(
    page_title="Resultados",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Análise de Resultados")

# Adiciona CSS para o estilo dos cards
st.markdown("""
<style>
    .card {
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        background-color: #f0f2f6;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin: 10px;
    }
    .card-title {
        font-size: 0.9em;
        font-weight: bold;
        margin-bottom: 5px;
        color: #262626;
    }
    .card-metric {
        font-size: 1.5em;
        font-weight: bold;
        color: #4d94ff;
        word-wrap: break-word; /* Garante que os números se quebrem se forem muito longos */
    }
</style>
""", unsafe_allow_html=True)

# Verifica se os dados foram salvos na página de entrada
if "dados_projeto" not in st.session_state:
    st.warning("Por favor, preencha os dados na página 'Dados de Entrada' primeiro.")
else:
    dados_projeto = st.session_state["dados_projeto"]

    # Simulação de Cenários: Preço Médio de Vendas
    st.header("Análise de Cenários")
    st.write("Altere o preço de vendas para simular o impacto no resultado do negócio.")

    col_preco, col_slider = st.columns([1, 2])
    
    with col_preco:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Preço Médio de Vendas (R$/m²)</div>
            <div class="card-metric">R$ {dados_projeto['preco_medio_vendas']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_slider:
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
    
    st.header("Resumo do Projeto")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Área Construída</div>
            <div class="card-metric">{resultados['area_construida']:,.2f} m²</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Área Privativa</div>
            <div class="card-metric">{resultados['area_privativa']:,.2f} m²</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">V.G.V.</div>
            <div class="card-metric">R$ {resultados['vgv']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Custo Total</div>
            <div class="card-metric">R$ {resultados['custo_total']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Resultado do Negócio</div>
            <div class="card-metric">R$ {resultados['resultado_negocio']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        margem_lucro = (resultados['resultado_negocio'] / resultados['vgv']) * 100 if resultados['vgv'] != 0 else 0
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Margem de Lucro</div>
            <div class="card-metric">{margem_lucro:,.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
