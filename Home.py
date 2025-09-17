import streamlit as st

st.set_page_config(
    page_title="Viabilidade Imobiliária",
    page_icon="🏠",
)

st.title("🏠 Análise de Viabilidade Imobiliária")

st.write(
    """
    Bem-vindo ao aplicativo de análise de viabilidade imobiliária!
    Use este aplicativo para avaliar a viabilidade financeira de projetos de desenvolvimento imobiliário de forma rápida e intuitiva.
    
    Navegue pelas páginas no menu lateral para:
    
    1.  **Dados de Entrada**: Insira todas as informações do seu projeto.
    2.  **Resultados**: Visualize os indicadores-chave de viabilidade.
    
    A análise é baseada em indicadores como o Valor Geral de Vendas (V.G.V.), o Custo Total do projeto e o Resultado do Negócio.
    """
)

st.info("💡 **Dica:** Utilize o menu lateral para alternar entre as páginas da aplicação.")

st.markdown("---")

st.header("Sobre o Projeto")
st.write(
    """
    Este projeto foi desenvolvido com Streamlit para combinar uma interface de usuário intuitiva com uma lógica financeira robusta, permitindo 
    a simulação de diferentes cenários para a tomada de decisões estratégicas.
    """
)
