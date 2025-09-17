# src/calculos_financeiros.py

def calcular_resultado_negocio(
    area_terreno: float,
    indice_aproveitamento: float,
    custo_por_metro_quadrado: float,
    relacao_privativa_construida: float,
    preco_medio_vendas: float
):
    """
    Calcula os indicadores financeiros chave do projeto.
    Retorna um dicionário com VGV, Custo Total e Resultado do Negócio.
    """
    # 1. Calcular a Área Construída com base no índice de aproveitamento
    area_construida = area_terreno * indice_aproveitamento
    
    # 2. Calcular a Área Privativa com base na relação
    area_privativa = area_construida * relacao_privativa_construida
    
    # 3. Calcular o Custo Total
    custo_total = area_construida * custo_por_metro_quadrado
    
    # 4. Calcular o Valor Geral de Vendas (V.G.V.)
    vgv = preco_medio_vendas * area_privativa
    
    # 5. Calcular o Resultado do Negócio
    resultado_negocio = vgv - custo_total
    
    return {
        "area_construida": area_construida,
        "area_privativa": area_privativa,
        "custo_total": custo_total,
        "vgv": vgv,
        "resultado_negocio": resultado_negocio,
    }
