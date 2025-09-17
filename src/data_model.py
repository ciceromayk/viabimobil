# src/data_model.py

from typing import Dict, Any

def get_empty_project_data() -> Dict[str, Any]:
    """Retorna um dicionário com a estrutura de dados do projeto."""
    return {
        "area_terreno": 0.0,
        "area_construida": 0.0,
        "custo_por_metro_quadrado": 0.0,
        "preco_venda_por_metro_quadrado": 0.0,
        "taxa_deducao_vendas": 0.0,
        "taxa_desconto": 0.0,
        "duracao_projeto": 0,
    }
