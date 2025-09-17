# src/calculos_financeiros.py
def calcular_resultado_negocio(
    area_terreno: float,
    indice_aproveitamento: float,
    custo_direto_construcao_m2: float,
    relacao_privativa_construida: float,
    preco_medio_vendas: float,
    custos_indiretos_data: list
) -> dict:
    """
    Calcula a viabilidade financeira de um projeto imobiliário.

    Args:
        area_terreno: Área total do terreno em m².
        indice_aproveitamento: Índice de aproveitamento do terreno.
        custo_direto_construcao_m2: Custo direto de construção por m².
        relacao_privativa_construida: Relação entre área privativa e área construída.
        preco_medio_vendas: Preço médio de vendas por m² de área privativa.
        custos_indiretos_data: Lista de dicionários com os custos indiretos (percentuais).
    
    Returns:
        Um dicionário contendo os resultados financeiros do projeto.
    """
    if relacao_privativa_construida <= 0:
        area_construida = 0
        area_privativa = 0
    else:
        area_privativa = area_terreno * indice_aproveitamento
        area_construida = area_privativa / relacao_privativa_construida

    vgv = preco_medio_vendas * area_privativa
    
    custo_direto_total = area_construida * custo_direto_construcao_m2
    
    # Novo cálculo: agora somamos os percentuais para obter o total dos custos indiretos
    total_percentual_custos_indiretos = sum(item['%'] for item in custos_indiretos_data)
    custos_indiretos_total = (total_percentual_custos_indiretos / 100) * vgv
    
    custo_total = custo_direto_total + custos_indiretos_total
    
    resultado_negocio = vgv - custo_total
    
    return {
        'area_privativa': area_privativa,
        'area_construida': area_construida,
        'vgv': vgv,
        'custo_direto_total': custo_direto_total,
        'custos_indiretos_total': custos_indiretos_total,
        'custo_total': custo_total,
        'resultado_negocio': resultado_negocio
    }
