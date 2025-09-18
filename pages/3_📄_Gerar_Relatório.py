import streamlit as st

st.set_page_config(
    page_title="Gerar Relatório PDF",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Gerar Relatório em PDF")
st.write("Esta página é dedicada à geração e exportação de relatórios.")

st.info("Esta é uma funcionalidade futura. O botão abaixo é apenas um placeholder.")

st.button("Gerar e Baixar Relatório (PDF)")

st.write("---")

if 'resultados_viabilidade' in st.session_state:
    st.subheader("Dados Atuais da Viabilidade")
    st.json(st.session_state['resultados_viabilidade'])
