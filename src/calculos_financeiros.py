# src/calculos_financeiros.py

def calcular_resultado_negocio(
    area_terreno: float,
    indice_aproveitamento: float,
    custo_direto_construcao_m2: float,
    relacao_privativa_construida: float,
    preco_medio_vendas: float,
    custos_indiretos_data: list
):
    """
    Calcula os indicadores financeiros chave do projeto, incluindo custos diretos e indiretos
    de uma tabela editável.
    Retorna um dicionário com VGV, Custo Total e Resultado do Negócio.
    """
    
    # 1. Calcular a Área Privativa
    area_privativa = area_terreno * indice_aproveitamento
    
    # 2. Calcular a Área Construída com base na relação AP/AC
    if relacao_privativa_construida == 0:
        area_construida = 0
    else:
        area_construida = area_privativa / relacao_privativa_construida
    
    # 3. Calcular o Valor Geral de Vendas (V.G.V.)
    vgv = preco_medio_vendas * area_privativa
    
    # 4. Calcular o Custo Direto
    custo_direto_total = area_construida * custo_direto_construcao_m2

    # 5. Calcular os Custos Indiretos totais a partir da tabela
    custos_indiretos_total = 0
    if custos_indiretos_data:
        for custo in custos_indiretos_data:
            if custo['Tipo'] == '%':
                custos_indiretos_total += vgv * (custo['Valor'] / 100)
            else: # Tipo 'R$'
                custos_indiretos_total += custo['Valor']
    
    # 6. Calcular o Custo Total
    custo_total = custo_direto_total + custos_indiretos_total
    
    # 7. Calcular o Resultado do Negócio
    resultado_negocio = vgv - custo_total
    
    return {
        "area_construida": area_construida,
        "area_privativa": area_privativa,
        "custo_direto_total": custo_direto_total,
        "custos_indiretos_total": custos_indiretos_total,
        "custo_total": custo_total,
        "vgv": vgv,
        "resultado_negocio": resultado_negocio,
    }
