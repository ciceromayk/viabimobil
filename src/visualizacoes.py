# src/visualizacoes.py

import pandas as pd
import plotly.express as px

def plotar_fluxo_de_caixa(fluxo_caixa_df: pd.DataFrame):
    """
    Cria e retorna um gráfico de barras interativo do fluxo de caixa.
    """
    # Calcula o fluxo de caixa acumulado
    fluxo_caixa_df["Fluxo de Caixa Acumulado"] = fluxo_caixa_df["Fluxo de Caixa"].cumsum()
    
    fig = px.bar(
        fluxo_caixa_df,
        x="Mes",
        y="Fluxo de Caixa",
        title="Fluxo de Caixa Mensal",
        labels={"Mes": "Mês do Projeto", "Fluxo de Caixa": "Valor (R$)"}
    )
    
    # Adiciona a linha do fluxo de caixa acumulado
    fig.add_trace(
        px.line(
            fluxo_caixa_df,
            x="Mes",
            y="Fluxo de Caixa Acumulado",
        ).data[0]
    )
    
    # Atualiza o layout do gráfico
    fig.update_traces(
        hovertemplate="Mês: %{x}<br>Fluxo de Caixa: R$ %{y:,.2f}<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Mês do Projeto",
        yaxis_title="Valor (R$)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title="",
            traceorder="reversed"
        ),
        showlegend=True
    )
    
    return fig
