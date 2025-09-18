import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Abrir Viabilidade",
    page_icon="📁",
    layout="wide"
)

st.title("📁 Abrir Viabilidade Existente")
st.write("Aqui você poderá selecionar e carregar uma viabilidade salva.")

st.info("Esta é uma funcionalidade futura. Por enquanto, a lista abaixo é apenas um exemplo.")

# Exemplo de dados de projetos salvos
projetos_salvos = pd.DataFrame([
    {"Projeto": "Terreno A", "Data": "15/09/2025", "Status": "Em Andamento"},
    {"Projeto": "Terreno B - Loteamento", "Data": "10/09/2025", "Status": "Concluído"},
    {"Projeto": "Viabilidade Centro", "Data": "01/09/2025", "Status": "Em Andamento"},
])

st.subheader("Projetos Salvos (Exemplo)")
st.table(projetos_salvos)

st.write("---")
st.button("Carregar Projeto Selecionado")
