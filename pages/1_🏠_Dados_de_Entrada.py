import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# --- Configuração da Página ---
st.set_page_config(
    page_title="Análise de Viabilidade Imobiliária",
    page_icon="🏠",
    layout="wide"
)

# --- Estabelecendo conexão com o banco --- #
# Use sua string de conexão PostgreSQL aqui:
# Exemplo: "postgresql://usuario:senha@host:porta/nome_do_banco"
DATABASE_URL = "sua_string_de_conexao_aqui"

# Criando engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Conectar-se ao banco de dados
with engine.connect() as conn:
    # Cria a tabela se ela não existir
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS viabilidades (
            id SERIAL PRIMARY KEY,
            nome_terreno VARCHAR(255) UNIQUE,
            dados JSONB,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

# --- Estilo CSS para os cards --- #
st.markdown(
    """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            background-color: #f8f9fa;
        }
        .card {
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin: 10px;
            border: 1px solid rgba(0,0,0,0.05);
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }
        .card-title {
            font-size: 0.9em;
            font-weight: 500;
            margin-bottom: 5px;
            color: #6c757d;
        }
        .card-metric {
            font-size: 1.5em;
            font-weight: 700;
            color: #495057;
        }
        .card.positive {
            background-color: #e6f7ea;
            color: #28a745;
            border-color: #c8e6c9;
        }
        .card.positive .card-metric {
            color: #28a745;
        }
        .card.negative {
            background-color: #fcebeb;
            color: #dc3545;
            border-color: #f5c6cb;
        }
        .card.negative .card-metric {
            color: #dc3545;
        }
        .card.neutral {
            background-color: #f8f9fa;
            color: #343a40;
            border-color: #e9ecef;
        }
        .card.neutral .card-metric {
            color: #495057;
        }
        h1, h2, h3 {
            color: #343a40;
            font-weight: 600;
        }
        .stDataFrame {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True
)

st.title("💰 Análise de Viabilidade Imobiliária")
st.write("Insira os parâmetros para a análise de viabilidade do seu projeto imobiliário.")

# --- Funções de operação no banco de dados ---

def criar_tabela():
    """Cria a tabela no banco se ela não existir."""
    with engine.connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS viabilidades (
                id SERIAL PRIMARY KEY,
                nome_terreno VARCHAR(255) UNIQUE,
                dados JSONB,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

def salvar_viabilidade(viabilidade):
    """Salva uma nova viabilidade no banco."""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO viabilidades (nome_terreno, dados) VALUES (:nome, :dados);"),
                {"nome": viabilidade['nome_terreno'], "dados": viabilidade}
            )
        st.success("Viabilidade salva com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar a viabilidade: {e}")

def get_viabilidades():
    """Recupera todas as viabilidades salvas."""
    with engine.connect() as conn:
        result = conn.execute("SELECT id, nome_terreno, data_criacao FROM viabilidades;")
        return pd.DataFrame(result.fetchall(), columns=['id', 'nome_terreno', 'data_criacao'])

# Carregar lista de viabilidades existentes
viabilidades_salvas = get_viabilidades()

# --- Interface para selecionar ou criar nova viabilidade ---
if viabilidades_salvas.empty:
    st.info("Nenhuma viabilidade salva ainda. Crie uma na página 'Análise de Viabilidade Imobiliária'.")
else:
    nomes_viabilidades = viabilidades_salvas['nome_terreno'].tolist()
    viabilidade_selecionada = st.selectbox(
        "Escolha uma viabilidade para carregar:",
        options=nomes_viabilidades,
        placeholder="Selecione um projeto..."
    )

    if st.button("Carregar Viabilidade"):
        if viabilidade_selecionada:
            # Carregar detalhes da viabilidade
            with engine.connect() as conn:
                resultado = conn.execute(
                    text("SELECT dados FROM viabilidades WHERE nome_terreno = :nome;"),
                    {"nome": viabilidade_selecionada}
                ).fetchone()
            if resultado:
                st.session_state['dados_viabilidade'] = resultado['dados']
                st.success(f"Viabilidade '{viabilidade_selecionada}' carregada.")
        else:
            st.warning("Por favor, selecione uma viabilidade.")

# --- Continuação do seu código: inputs e cálculos ---
# Aqui você pode continuar com seu restante de código, acessando os dados carregados em st.session_state['dados_viabilidade']

# Exemplo de uso
# if 'dados_viabilidade' in st.session_state:
#     # use os dados carregados
#     pass
