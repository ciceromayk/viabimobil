import streamlit as st
import pandas as pd

# --- Configuração da Página e Conexão com o Banco ---
st.set_page_config(
    page_title="Abrir Viabilidade",
    page_icon="📁",
    layout="wide"
)

# Estabelece a conexão com o banco de dados
conn = st.connection("postgresql", type="sql")

st.title("📁 Abrir Viabilidade Existente")
st.write("Selecione uma viabilidade da lista abaixo para carregar os dados.")

# Carrega a lista de viabilidades do banco de dados
# O "conn.query" com cache (@st.cache_data) garante que a query só rode uma vez
# a menos que os parâmetros mudem.
@st.cache_data(ttl=600)  # Cache por 10 minutos
def get_viabilidades_from_db():
    return conn.query("SELECT id, nome_terreno, data_criacao FROM viabilidades;")

viabilidades_salvas = get_viabilidades_from_db()

if viabilidades_salvas.empty:
    st.info("Nenhuma viabilidade salva ainda. Crie uma na página 'Análise de Viabilidade Imobiliária'.")
else:
    # Cria uma lista de nomes para o selectbox
    nomes_viabilidades = viabilidades_salvas['nome_terreno'].tolist()
    
    viabilidade_selecionada = st.selectbox(
        "Escolha uma viabilidade para carregar:",
        options=nomes_viabilidades,
        index=None,
        placeholder="Selecione um projeto..."
    )

    if st.button("Carregar Viabilidade", type="primary"):
        if viabilidade_selecionada:
            # Busca a viabilidade completa pelo nome e carrega o JSON
            query = f"SELECT dados FROM viabilidades WHERE nome_terreno = '{viabilidade_selecionada}';"
            dados_viabilidade = conn.query(query).iloc[0]['dados']
            
            # Atualiza o estado da sessão com os dados do projeto carregado
            for key, value in dados_viabilidade.items():
                st.session_state[key] = value
            
            st.success(f"Viabilidade '{viabilidade_selecionada}' carregada com sucesso!")
            st.info("Volte para a página 'Análise de Viabilidade Imobiliária' para ver os dados e resultados atualizados.")
        else:
            st.warning("Por favor, selecione uma viabilidade para carregar.")
