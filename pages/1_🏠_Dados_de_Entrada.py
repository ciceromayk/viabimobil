import streamlit as st
import pandas as pd
from babel.numbers import format_currency, format_decimal
from sqlalchemy import create_engine, text

# --- Configuração da página ---
st.set_page_config(
    page_title="Análise de Viabilidade Imobiliária",
    page_icon="🏠",
    layout="wide"
)

# --- Conexão com o banco usando secrets.toml ---
try:
    DATABASE_URL = st.secrets["connections"]["postgresql"]["url"]
except KeyError:
    st.error("Não foi possível obter a URL de conexão em secrets.toml.")
    st.stop()

engine = create_engine(DATABASE_URL)

# --- Criação da tabela 'viabilidades' se não existir ---
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS viabilidades (
            id SERIAL PRIMARY KEY,
            nome_terreno VARCHAR(255) UNIQUE,
            dados JSONB,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))

# --- CSS personalizado para os cards ---
st.markdown("""
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #f8f9fa;
    }
    .card {
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
        text-align: center;
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
    .card-title { font-size: 0.9em; color: #6c757d; margin-bottom: 5px; }
    .card-metric { font-size: 1.5em; font-weight: 700; color: #495057; }
    .card.positive { background-color: #e6f7ea; border-color: #c8e6c9; color: #28a745; }
    .card.negative { background-color: #fcebeb; border-color: #f5c6cb; color: #dc3545; }
    .card.neutral  { background-color: #f8f9fa; border-color: #e9ecef; color: #343a40; }
    h1, h2, h3 { color: #343a40; font-weight: 600; }
    .stDataFrame { box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("💰 Análise de Viabilidade Imobiliária")
st.write("Insira os parâmetros para a análise de viabilidade do seu projeto imobiliário.")

# --- Funções de Cálculo e Banco de Dados ---

def calcular_viabilidade(
    nome_terreno,
    area_terreno,
    indice_aproveitamento,
    relacao_privativa_construida,
    preco_medio_vendas,
    custo_direto_construcao_m2,
    custos_indiretos_percentuais_df,
    custos_indiretos_monetarios_dict
):
    """Calcula métricas de área e financeiras do projeto."""
    area_privativa = area_terreno * indice_aproveitamento
    area_construida = (area_privativa / relacao_privativa_construida
                       if relacao_privativa_construida > 0 else 0)
    vgv = preco_medio_vendas * area_privativa
    custo_direto_total = area_construida * custo_direto_construcao_m2

    total_perc = custos_indiretos_percentuais_df['%'].sum()
    custos_vgv = (total_perc / 100) * vgv
    custos_monet = sum(custos_indiretos_monetarios_dict.values())
    custos_indiretos_total = custos_vgv + custos_monet

    custo_total = custo_direto_total + custos_indiretos_total
    resultado_negocio = vgv - custo_total
    margem_lucro = (resultado_negocio / vgv) * 100 if vgv > 0 else 0

    return {
        'nome_terreno': nome_terreno,
        'area_terreno': area_terreno,
        'area_privativa': area_privativa,
        'area_construida': area_construida,
        'vgv': vgv,
        'custo_direto_total': custo_direto_total,
        'custos_indiretos_total': custos_indiretos_total,
        'custo_total': custo_total,
        'resultado_negocio': resultado_negocio,
        'margem_lucro': margem_lucro
    }

def salvar_viabilidade(viabilidade):
    """Salva a viabilidade calculada no banco de dados."""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO viabilidades (nome_terreno, dados) VALUES (:nome, :dados);"),
                {"nome": viabilidade['nome_terreno'], "dados": viabilidade}
            )
        st.success("Viabilidade salva com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar a viabilidade: {e}")

# --- Entrada de Dados (Interface) ---

with st.expander("1. Terreno e Construção"):
    if 'nome_terreno' not in st.session_state:
        st.session_state.nome_terreno = ''
    nome_terreno = st.text_input("Nome do Terreno", key="nome_terreno")

    col1, col2, col3 = st.columns(3)
    with col1:
        if 'area_terreno' not in st.session_state:
            st.session_state.area_terreno = 0.0
        area_terreno = st.number_input(
            "Área do Terreno (m²)",
            min_value=0.0,
            key="area_terreno",
            format="%.2f"
        )
    with col2:
        if 'indice_aproveitamento' not in st.session_state:
            st.session_state.indice_aproveitamento = 1.00
        indice_aproveitamento = st.slider(
            "Índice de Aproveitamento",
            min_value=1.00,
            max_value=4.00,
            value=st.session_state.indice_aproveitamento,
            step=0.01,
            key="indice_aproveitamento"
        )
    with col3:
        if 'relacao_privativa_construida' not in st.session_state:
            st.session_state.relacao_privativa_construida = 0.70
        relacao_privativa_construida = st.slider(
            "Relação AP / AC",
            min_value=0.00,
            max_value=1.00,
            value=st.session_state.relacao_privativa_construida,
            step=0.01,
            key="relacao_privativa_construida"
        )

with st.expander("2. Vendas"):
    if 'preco_medio_vendas' not in st.session_state:
        st.session_state.preco_medio_vendas = 0.0
    preco_medio_vendas = st.number_input(
        "Preço Médio de Vendas (R$/m²)",
        min_value=0.0,
        key="preco_medio_vendas",
        format="%.2f"
    )

with st.expander("3. Custos Diretos"):
    if 'custo_direto_construcao_m2' not in st.session_state:
        st.session_state.custo_direto_construcao_m2 = 0.0
    custo_direto_construcao_m2 = st.number_input(
        "Custo Direto de Construção (R$/m²)",
        min_value=0.0,
        key="custo_direto_construcao_m2",
        format="%.2f"
    )

with st.expander("4. Custos Indiretos"):
    # Tabela padrão de custos indiretos (% do VGV)
    if 'custos_indiretos_padrao' not in st.session_state:
        st.session_state.custos_indiretos_padrao = pd.DataFrame([
            {'Custo': 'IRPJ/CS/PIS/COFINS', '%': 4.00},
            {'Custo': 'Corretagem', '%': 3.61},
            {'Custo': 'Publicidade', '%': 0.90},
            {'Custo': 'Manutenção', '%': 0.50},
            {'Custo': 'Custo Fixo IDIBRA', '%': 4.00},
            {'Custo': 'Assessoria Técnica', '%': 0.70},
            {'Custo': 'Projetos', '%': 0.52},
            {'Custo': 'Licenciamento e Incorporação', '%': 0.20},
        ])

    # Calcula VGV temporário
    area_privativa_temp = area_terreno * indice_aproveitamento
    vgv_temp = preco_medio_vendas * area_privativa_temp

    # Prepara DataFrame e edita
    df_custos = st.session_state.custos_indiretos_padrao.copy()
    df_custos['%'] = pd.to_numeric(df_custos['%'])
    df_custos['Valor (R$)'] = df_custos['%'] * (vgv_temp / 100)

    altura = 35
    cabec = 39
    total_h = len(df_custos) * altura + cabec

    custos_indiretos_editavel = st.data_editor(
        df_custos,
        column_config={
            "Custo": st.column_config.TextColumn("Custo", disabled=True),
            "%": st.column_config.NumberColumn("Percentual (%)", min_value=0.0, format="%.2f"),
            "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", disabled=True, format="R$ %.2f"),
        },
        hide_index=True,
        num_rows="fixed",
        height=total_h,
        key="data_editor_custos"
    )
    st.session_state.custos_indiretos_padrao = custos_indiretos_editavel[['Custo', '%']]

    # Custos monetários adicionais
    st.subheader("Custos relacionados ao Terreno / Produto")
    col4, col5, col6, col7, col8 = st.columns(5)
    with col4:
        if 'outorga_onerosa' not in st.session_state:
            st.session_state.outorga_onerosa = 0.0
        outorga_onerosa = st.number_input(
            "Outorga Onerosa (R$)",
            min_value=0.0,
            key="outorga_onerosa",
            format="%.2f"
        )
    with col5:
        if 'condominio' not in st.session_state:
            st.session_state.condominio = 0.0
        condominio = st.number_input(
            "Condomínio (R$)",
            min_value=0.0,
            key="condominio",
            format="%.2f"
        )
    with col6:
        if 'iptu' not in st.session_state:
            st.session_state.iptu = 0.0
        iptu = st.number_input(
            "IPTU (R$)",
            min_value=0.0,
            key="iptu",
            format="%.2f"
        )
    with col7:
        if 'preparacao_terreno' not in st.session_state:
            st.session_state.preparacao_terreno = 0.0
        preparacao_terreno = st.number_input(
            "Preparação do Terreno (R$)",
            min_value=0.0,
            key="preparacao_terreno",
            format="%.2f"
        )
    with col8:
        if 'financiamento_bancario' not in st.session_state:
            st.session_state.financiamento_bancario = 0.0
        financiamento_bancario = st.number_input(
            "Financiamento Bancário (R$)",
            min_value=0.0,
            key="financiamento_bancario",
            format="%.2f"
        )

# --- Execução do Cálculo ---
custos_indiretos_monetarios = {
    'outorga_onerosa': outorga_onerosa,
    'condominio': condominio,
    'iptu': iptu,
    'preparacao_terreno': preparacao_terreno,
    'financiamento_bancario': financiamento_bancario
}

resultados = calcular_viabilidade(
    st.session_state.nome_terreno,
    st.session_state.area_terreno,
    st.session_state.indice_aproveitamento,
    st.session_state.relacao_privativa_construida,
    st.session_state.preco_medio_vendas,
    st.session_state.custo_direto_construcao_m2,
    st.session_state.custos_indiretos_padrao,
    custos_indiretos_monetarios
)

# --- Botão de Salvar Viabilidade ---
st.markdown("---")
if st.button("💾 Salvar Viabilidade", type="primary"):
    if st.session_state.nome_terreno:
        salvar_viabilidade(resultados)
    else:
        st.warning("Digite o nome do terreno antes de salvar.")

# --- Exibição de Resultados ---
st.markdown("---")
st.header("Resumo de Custos")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Custos Diretos</div>
          <div class="card-metric">{format_currency(resultados['custo_direto_total'], 'BRL', locale='pt_BR')}</div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Custos Indiretos</div>
          <div class="card-metric">{format_currency(resultados['custos_indiretos_total'], 'BRL', locale='pt_BR')}</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Custo Total</div>
          <div class="card-metric">{format_currency(resultados['custo_total'], 'BRL', locale='pt_BR')}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.header("Resumo Financeiro")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">V.G.V.</div>
          <div class="card-metric">{format_currency(resultados['vgv'], 'BRL', locale='pt_BR')}</div>
        </div>
    """, unsafe_allow_html=True)
with f2:
    neg = resultados['resultado_negocio']
    cls = "positive" if neg > 0 else "negative" if neg < 0 else "neutral"
    st.markdown(f"""
        <div class="card {cls}">
          <div class="card-title">Resultado do Negócio</div>
          <div class="card-metric">{format_currency(neg, 'BRL', locale='pt_BR')}</div>
        </div>
    """, unsafe_allow_html=True)
with f3:
    mg = resultados['margem_lucro']
    cls = "positive" if mg > 0 else "negative" if mg < 0 else "neutral"
    st.markdown(f"""
        <div class="card {cls}">
          <div class="card-title">Margem de Lucro</div>
          <div class="card-metric">{format_decimal(mg, locale='pt_BR')}%</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.header("Resumo do Projeto")
p1, p2, p3, p4, p5 = st.columns(5)
with p1:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Área do Terreno</div>
          <div class="card-metric">{format_decimal(resultados['area_terreno'], locale='pt_BR')} m²</div>
        </div>
    """, unsafe_allow_html=True)
with p2:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Índice de Aproveitamento</div>
          <div class="card-metric">{format_decimal(st.session_state.indice_aproveitamento, locale='pt_BR')}</div>
        </div>
    """, unsafe_allow_html=True)
with p3:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Área Construída</div>
          <div class="card-metric">{format_decimal(resultados['area_construida'], locale='pt_BR')} m²</div>
        </div>
    """, unsafe_allow_html=True)
with p4:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Área Privativa</div>
          <div class="card-metric">{format_decimal(resultados['area_privativa'], locale='pt_BR')} m²</div>
        </div>
    """, unsafe_allow_html=True)
with p5:
    st.markdown(f"""
        <div class="card neutral">
          <div class="card-title">Relação AP/AC</div>
          <div class="card-metric">{format_decimal(st.session_state.relacao_privativa_construida, locale='pt_BR')}</div>
        </div>
    """, unsafe_allow_html=True)
