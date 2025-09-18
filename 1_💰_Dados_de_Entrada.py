import streamlit as st
import pandas as pd
from babel.numbers import format_currency, format_decimal

# --- Configuração da Página ---
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
        word-wrap: break-word;
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

# --- Funções de Cálculo ---

def calcular_viabilidade(area_terreno, indice_aproveitamento, relacao_privativa_construida,
                         preco_medio_vendas, custo_direto_construcao_m2, custos_indiretos_percentuais_df,
                         custos_indiretos_monetarios_dict):
    """Calcula todas as métricas financeiras e de área do projeto."""
    # 1. Cálculos de Áreas
    area_privativa = area_terreno * indice_aproveitamento
    # Evita divisão por zero
    area_construida = area_privativa / relacao_privativa_construida if relacao_privativa_construida > 0 else 0
    
    # 2. VGV (Valor Geral de Vendas)
    vgv = preco_medio_vendas * area_privativa
    
    # 3. Custos Totais
    custo_direto_total = area_construida * custo_direto_construcao_m2
    
    # Soma dos custos indiretos percentuais
    total_percentual = custos_indiretos_percentuais_df['%'].sum()
    custos_indiretos_vgv_total = (total_percentual / 100) * vgv
    
    # Soma dos custos indiretos monetários
    custos_indiretos_monetarios_total = sum(custos_indiretos_monetarios_dict.values())
    custos_indiretos_total = custos_indiretos_vgv_total + custos_indiretos_monetarios_total
    
    custo_total = custo_direto_total + custos_indiretos_total
    
    # 4. Resultado Financeiro
    resultado_negocio = vgv - custo_total
    margem_lucro = (resultado_negocio / vgv) * 100 if vgv > 0 else 0
    
    return {
        'area_privativa': area_privativa,
        'area_construida': area_construida,
        'vgv': vgv,
        'custo_direto_total': custo_direto_total,
        'custos_indiretos_total': custos_indiretos_total,
        'custo_total': custo_total,
        'resultado_negocio': resultado_negocio,
        'margem_lucro': margem_lucro
    }

# --- Entrada de Dados (Interface do Usuário) ---

with st.expander("1. Terreno e Construção"):
    col1, col2, col3 = st.columns(3)
    with col1:
        area_terreno = st.number_input("Área do Terreno (m²)", min_value=0.0, key="area_terreno")
    with col2:
        indice_aproveitamento = st.slider(
            "Índice de Aproveitamento", min_value=1.00, max_value=4.00, value=1.00, step=0.01, key="indice_aproveitamento"
        )
    with col3:
        relacao_privativa_construida = st.slider(
            "Relação AP / AC", min_value=0.00, max_value=1.00, value=0.70, step=0.01, key="relacao_privativa"
        )

with st.expander("2. Vendas"):
    st.markdown("Os resultados da viabilidade serão atualizados com base nos custos e vendas inseridos.")
    preco_medio_vendas = st.number_input("Preço Médio de Vendas (R$/m²)", min_value=0.0, key="preco_medio_vendas")

with st.expander("3. Custos Diretos"):
    custo_direto_construcao_m2 = st.number_input("Custo Direto de Construção (R$/m²)", min_value=0.0, key="custo_direto_construcao")

with st.expander("4. Custos Indiretos"):
    # Define os valores padrão da tabela de custos indiretos
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
    
    st.subheader("Custos indiretos baseados no VGV")
    
    # A variável 'vgv' precisa ser calculada aqui para exibir na tabela de forma dinâmica
    area_privativa_temp = area_terreno * indice_aproveitamento
    vgv_temp = preco_medio_vendas * area_privativa_temp
    
    # Cria uma cópia da tabela para exibição e permite a edição
    df_custos = st.session_state.custos_indiretos_padrao.copy()
    df_custos['Valor (R$)'] = df_custos['%'] * (vgv_temp / 100)
    
    custos_indiretos_editavel = st.data_editor(
        df_custos,
        column_config={
            "Custo": st.column_config.TextColumn("Custo", disabled=True),
            "%": st.column_config.NumberColumn("Percentual (%)", min_value=0.0, format="%.2f"),
            "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", disabled=True, format="R$ %.2f")
        },
        hide_index=True,
        num_rows="fixed",
        height=300,
        key="data_editor_custos"
    )
    st.session_state.custos_indiretos_padrao = custos_indiretos_editavel[['Custo', '%']]

    st.subheader("Custos relacionados ao Terreno / Produto")
    col4, col5 = st.columns(2)
    with col4:
        outorga_onerosa = st.number_input("Outorga Onerosa (R$)", min_value=0.0, key="outorga_onerosa")
        condominio = st.number_input("Condomínio (R$)", min_value=0.0, key="condominio")
        iptu = st.number_input("IPTU (R$)", min_value=0.0, key="iptu")
    with col5:
        preparacao_terreno = st.number_input("Preparação do Terreno (R$)", min_value=0.0, key="preparacao_terreno")
        financiamento_bancario = st.number_input("Financiamento Bancário (R$)", min_value=0.0, key="financiamento_bancario")

# --- Execução do Cálculo e Exibição de Resultados ---
# Reúne os custos monetários em um dicionário para a função de cálculo
custos_indiretos_monetarios_dict = {
    'outorga_onerosa': outorga_onerosa,
    'condominio': condominio,
    'iptu': iptu,
    'preparacao_terreno': preparacao_terreno,
    'financiamento_bancario': financiamento_bancario
}

# Chama a função principal de cálculo
resultados = calcular_viabilidade(
    area_terreno,
    indice_aproveitamento,
    relacao_privativa_construida,
    preco_medio_vendas,
    custo_direto_construcao_m2,
    st.session_state.custos_indiretos_padrao,
    custos_indiretos_monetarios_dict
)

# --- Exibição de Resultados ---
st.markdown("---")

# Resumo do Projeto
st.header("Resumo do Projeto")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Área do Terreno</div>
        <div class="card-metric">{format_decimal(area_terreno, locale='pt_BR')} m²</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Índice de Aproveitamento</div>
        <div class="card-metric">{format_decimal(indice_aproveitamento, locale='pt_BR')}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Área Construída</div>
        <div class="card-metric">{format_decimal(resultados['area_construida'], locale='pt_BR')} m²</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Área Privativa</div>
        <div class="card-metric">{format_decimal(resultados['area_privativa'], locale='pt_BR')} m²</div>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Relação AP/AC</div>
        <div class="card-metric">{format_decimal(relacao_privativa_construida, locale='pt_BR')}</div>
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
        <div class="card-metric">{format_currency(resultados['custo_direto_total'], 'BRL', locale='pt_BR')}</div>
    </div>
    """, unsafe_allow_html=True)
with col_custos_2:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Custos Indiretos</div>
        <div class="card-metric">{format_currency(resultados['custos_indiretos_total'], 'BRL', locale='pt_BR')}</div>
    </div>
    """, unsafe_allow_html=True)
with col_custos_3:
    st.markdown(f"""
    <div class="card neutral">
        <div class="card-title">Custo Total</div>
        <div class="card-metric">{format_currency(resultados['custo_total'], 'BRL', locale='pt_BR')}</div>
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
        <div class="card-metric">{format_currency(resultados['vgv'], 'BRL', locale='pt_BR')}</div>
    </div>
    """, unsafe_allow_html=True)
with col7:
    resultado_negocio = resultados['resultado_negocio']
    card_class = "positive" if resultado_negocio > 0 else "negative" if resultado_negocio < 0 else "neutral"
    st.markdown(f"""
    <div class="card {card_class}">
        <div class="card-title">Resultado do Negócio</div>
        <div class="card-metric">{format_currency(resultado_negocio, 'BRL', locale='pt_BR')}</div>
    </div>
    """, unsafe_allow_html=True)
with col8:
    margem_lucro = resultados['margem_lucro']
    card_class = "positive" if margem_lucro > 0 else "negative" if margem_lucro < 0 else "neutral"
    st.markdown(f"""
    <div class="card {card_class}">
        <div class="card-title">Margem de Lucro</div>
        <div class="card-metric">{format_decimal(margem_lucro, locale='pt_BR')}%</div>
    </div>
    """, unsafe_allow_html=True)
