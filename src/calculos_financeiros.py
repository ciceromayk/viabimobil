# src/calculos_financeiros.py

import pandas as pd
import numpy as np

def calcular_fluxo_de_caixa_projetado(
    duracao_projeto: int,
    area_construida: float,
    custo_por_metro_quadrado: float,
    preco_venda_por_metro_quadrado: float,
    taxa_deducao_vendas: float
) -> pd.DataFrame:
    """
    Calcula o fluxo de caixa projetado do projeto imobiliário.
    """
    
    # Cria um DataFrame para o fluxo de caixa
    fluxo_caixa = pd.DataFrame({
        "Mes": range(duracao_projeto + 1),
        "Receita": 0.0,
        "Custo": 0.0,
        "Fluxo de Caixa": 0.0
    })

    # Custo inicial (mês 0)
    custo_total_obra = area_construida * custo_por_metro_quadrado
    fluxo_caixa.loc[0, "Custo"] = custo_total_obra
    fluxo_caixa.loc[0, "Fluxo de Caixa"] = -custo_total_obra

    # Receita de vendas (distribuída ao longo do tempo, simplificado para o exemplo)
    receita_total_vendas = area_construida * preco_venda_por_metro_quadrado * (1 - taxa_deducao_vendas)
    
    # Distribui a receita de forma linear ao longo do projeto
    receita_mensal = receita_total_vendas / duracao_projeto
    fluxo_caixa.loc[1:, "Receita"] = receita_mensal
    
    # Atualiza o fluxo de caixa mensal (Receita - Custo)
    fluxo_caixa.loc[1:, "Fluxo de Caixa"] = fluxo_caixa.loc[1:, "Receita"] - fluxo_caixa.loc[1:, "Custo"]
    
    return fluxo_caixa
