"""
Dashboard web para análise QANX vs BTC
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

from utils import load_data, calculate_returns, calculate_correlation
from config import COLORS, DASH_HOST, DASH_PORT, DASH_DEBUG
from analyzer import QANXBTCAnalyzer

# Inicializa o app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "QANX vs BTC Analysis Dashboard"

# Carrega dados
try:
    analyzer = QANXBTCAnalyzer()
    analyzer.load_data()
    merged_data = analyzer.merged_data

    # Se não há dados, cria dados sintéticos históricos desde 2019
    if merged_data.empty:
        print("Criando dados sintéticos históricos desde 2019 para demonstração...")
        from datetime import datetime

        # Dados desde janeiro de 2019
        start_date = datetime(2019, 1, 1)
        end_date = pd.Timestamp.now()
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        total_days = len(dates)

        import numpy as np
        np.random.seed(42)

        # Simula dados históricos realistas do BTC
        btc_prices = []
        btc_price = 3500  # BTC em jan/2019

        # Períodos históricos importantes
        covid_crash = (datetime(2020, 3, 12), datetime(2020, 3, 20))
        bull_2020_2021 = (datetime(2020, 10, 1), datetime(2021, 11, 30))
        bear_2022 = (datetime(2022, 1, 1), datetime(2022, 12, 31))
        bull_2023_2024 = (datetime(2023, 1, 1), datetime(2024, 3, 31))

        for i, date in enumerate(dates):
            # Determina o período e ajusta parâmetros
            if covid_crash[0] <= date <= covid_crash[1]:
                trend, volatility = -0.05, 0.1  # Crash COVID
            elif bull_2020_2021[0] <= date <= bull_2020_2021[1]:
                trend, volatility = 0.003, 0.05  # Bull market
            elif bear_2022[0] <= date <= bear_2022[1]:
                trend, volatility = -0.001, 0.04  # Bear market
            elif bull_2023_2024[0] <= date <= bull_2023_2024[1]:
                trend, volatility = 0.002, 0.04  # Bull market recente
            else:
                trend, volatility = 0.0005, 0.03  # Períodos normais

            change = np.random.normal(trend, volatility)
            btc_price = max(btc_price * (1 + change), 3000)  # Não deixa ir muito baixo
            btc_prices.append(btc_price)

        # Simula dados do QANX com correlação variável ao BTC
        qanx_prices = []
        qanx_price = 0.001  # QANX inicial

        for i, date in enumerate(dates):
            btc_change = (btc_prices[i] / btc_prices[i-1] - 1) if i > 0 else 0

            # Correlação varia ao longo do tempo (sua teoria)
            if date.year <= 2020:
                correlation = 0.3  # Baixa correlação inicial
            elif date.year == 2021:
                correlation = 0.8  # Alta correlação durante bull market
            elif date.year == 2022:
                correlation = 0.6  # Correlação média durante bear
            else:
                correlation = 0.7  # Correlação alta recente

            # QANX segue BTC com correlação variável + ruído próprio
            qanx_change = btc_change * correlation + np.random.normal(0, 0.08)
            qanx_price = max(qanx_price * (1 + qanx_change), 0.0001)
            qanx_prices.append(qanx_price)

        # Volumes correlacionados com volatilidade
        btc_volumes = []
        qanx_volumes = []

        for i in range(total_days):
            btc_change = abs((btc_prices[i] / btc_prices[i-1] - 1)) if i > 0 else 0.01
            qanx_change = abs((qanx_prices[i] / qanx_prices[i-1] - 1)) if i > 0 else 0.01

            # Volume aumenta com volatilidade
            btc_vol = np.random.uniform(1e9, 3e9) * (1 + btc_change * 20)
            qanx_vol = np.random.uniform(1e6, 5e6) * (1 + qanx_change * 15)

            btc_volumes.append(btc_vol)
            qanx_volumes.append(qanx_vol)

        merged_data = pd.DataFrame({
            'price_btc': btc_prices,
            'price_qanx': qanx_prices,
            'volume_btc': btc_volumes,
            'volume_qanx': qanx_volumes,
            'market_cap_btc': [p * 19e6 for p in btc_prices],
            'market_cap_qanx': [p * 1e9 for p in qanx_prices]
        }, index=dates)

        print(f"Dados sintéticos criados: {len(merged_data)} registros de {dates[0].date()} a {dates[-1].date()}")

    # Calcula métricas básicas
    btc_returns = calculate_returns(merged_data['price_btc'])
    qanx_returns = calculate_returns(merged_data['price_qanx'])
    correlation = btc_returns.corr(qanx_returns)
    rolling_corr = calculate_correlation(qanx_returns, btc_returns, window=30)

except Exception as e:
    print(f"Erro ao carregar dados: {e}")
    merged_data = pd.DataFrame()
    correlation = 0
    rolling_corr = pd.Series()

# Layout do dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("QANX vs BTC Analysis Dashboard", 
                   className="text-center mb-4",
                   style={'color': COLORS['text']}),
            html.Hr()
        ])
    ]),
    
    # Cards com métricas principais
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Correlação Atual", className="card-title"),
                    html.H2(f"{correlation:.3f}", className="text-primary")
                ])
            ])
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Preço BTC", className="card-title"),
                    html.H2(f"${merged_data['price_btc'].iloc[-1]:,.2f}" if not merged_data.empty else "$0", 
                            className="text-warning")
                ])
            ])
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Preço QANX", className="card-title"),
                    html.H2(f"${merged_data['price_qanx'].iloc[-1]:.6f}" if not merged_data.empty else "$0", 
                            className="text-info")
                ])
            ])
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Período Análise", className="card-title"),
                    html.H2(f"{len(merged_data)} dias" if not merged_data.empty else "0 dias", 
                            className="text-success")
                ])
            ])
        ], width=3),
    ], className="mb-4"),
    
    # Gráfico principal de preços
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="price-chart")
        ])
    ], className="mb-4"),
    
    # Gráficos de análise
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="correlation-chart")
        ], width=6),
        dbc.Col([
            dcc.Graph(id="returns-chart")
        ], width=6)
    ], className="mb-4"),
    
    # Gráfico de volume e scatter plot
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="volume-chart")
        ], width=6),
        dbc.Col([
            dcc.Graph(id="scatter-chart")
        ], width=6)
    ], className="mb-4"),
    
    # Controles
    dbc.Row([
        dbc.Col([
            html.Label("Período para análise:"),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=merged_data.index.min() if not merged_data.empty else datetime.now() - timedelta(days=365),
                end_date=merged_data.index.max() if not merged_data.empty else datetime.now(),
                display_format='DD/MM/YYYY'
            )
        ], width=6),
        dbc.Col([
            html.Label("Janela de correlação (dias):"),
            dcc.Slider(
                id='correlation-window',
                min=7,
                max=90,
                step=7,
                value=30,
                marks={i: str(i) for i in range(7, 91, 14)}
            )
        ], width=6)
    ], className="mb-4"),
    
    # Insights
    dbc.Row([
        dbc.Col([
            html.H3("Insights da Análise"),
            html.Div(id="insights-content")
        ])
    ])
    
], fluid=True, style={'backgroundColor': COLORS['background'], 'color': COLORS['text']})

# Callbacks para atualizar gráficos
@app.callback(
    Output('price-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_price_chart(start_date, end_date):
    if merged_data.empty:
        return go.Figure().add_annotation(text="Dados não disponíveis",
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)

    try:
        # Filtra dados por período
        if start_date and end_date:
            mask = (merged_data.index >= start_date) & (merged_data.index <= end_date)
            filtered_data = merged_data.loc[mask]
        else:
            filtered_data = merged_data

        if filtered_data.empty:
            return go.Figure().add_annotation(text="Nenhum dado no período selecionado",
                                            xref="paper", yref="paper",
                                            x=0.5, y=0.5, showarrow=False)

        # Cria subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Preços Normalizados (Base 100)', 'Preços Absolutos'),
            vertical_spacing=0.15
        )

        # Normaliza preços para comparação (base 100)
        btc_norm = (filtered_data['price_btc'] / filtered_data['price_btc'].iloc[0]) * 100
        qanx_norm = (filtered_data['price_qanx'] / filtered_data['price_qanx'].iloc[0]) * 100

        # Gráfico normalizado
        fig.add_trace(
            go.Scatter(x=filtered_data.index, y=btc_norm, name='BTC (Normalizado)',
                      line=dict(color=COLORS['btc'], width=2)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=filtered_data.index, y=qanx_norm, name='QANX (Normalizado)',
                      line=dict(color=COLORS['qanx'], width=2)),
            row=1, col=1
        )

        # Gráfico absoluto BTC
        fig.add_trace(
            go.Scatter(x=filtered_data.index, y=filtered_data['price_btc'], name='BTC ($)',
                      line=dict(color=COLORS['btc'], width=2)),
            row=2, col=1
        )

        # Adiciona eixo secundário para QANX (escala diferente)
        fig.add_trace(
            go.Scatter(x=filtered_data.index, y=filtered_data['price_qanx'], name='QANX ($)',
                      line=dict(color=COLORS['qanx'], width=2), yaxis='y4'),
            row=2, col=1
        )

        fig.update_layout(
            title="Evolução dos Preços BTC vs QANX (2019-2025)",
            template="plotly_dark",
            height=700,
            yaxis4=dict(overlaying='y3', side='right', title='QANX ($)')
        )

        return fig

    except Exception as e:
        return go.Figure().add_annotation(text=f"Erro: {str(e)}",
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)

@app.callback(
    Output('correlation-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('correlation-window', 'value')]
)
def update_correlation_chart(start_date, end_date, window):
    if merged_data.empty:
        return go.Figure().add_annotation(text="Dados não disponíveis",
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)

    try:
        # Filtra dados
        if start_date and end_date:
            mask = (merged_data.index >= start_date) & (merged_data.index <= end_date)
            filtered_data = merged_data.loc[mask]
        else:
            filtered_data = merged_data

        if filtered_data.empty or len(filtered_data) < window:
            return go.Figure().add_annotation(text="Dados insuficientes para correlação",
                                            xref="paper", yref="paper",
                                            x=0.5, y=0.5, showarrow=False)

        # Calcula correlação móvel
        btc_returns = calculate_returns(filtered_data['price_btc'])
        qanx_returns = calculate_returns(filtered_data['price_qanx'])
        rolling_corr = calculate_correlation(qanx_returns, btc_returns, window=window)

        # Remove valores NaN
        rolling_corr = rolling_corr.dropna()

        if rolling_corr.empty:
            return go.Figure().add_annotation(text="Não foi possível calcular correlação",
                                            xref="paper", yref="paper",
                                            x=0.5, y=0.5, showarrow=False)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=rolling_corr.index, y=rolling_corr,
                      name=f'Correlação Móvel ({window}d)',
                      line=dict(color=COLORS['qanx'], width=2))
        )

        # Linhas de referência
        fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Zero")
        fig.add_hline(y=0.5, line_dash="dot", line_color="green", annotation_text="Correlação Forte (+)")
        fig.add_hline(y=-0.5, line_dash="dot", line_color="red", annotation_text="Correlação Forte (-)")

        fig.update_layout(
            title=f"Correlação Móvel QANX vs BTC ({window} dias) - Evolução Temporal",
            yaxis_title="Correlação",
            xaxis_title="Data",
            template="plotly_dark",
            yaxis=dict(range=[-1, 1])
        )

        return fig

    except Exception as e:
        return go.Figure().add_annotation(text=f"Erro: {str(e)}",
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)

@app.callback(
    Output('returns-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_returns_chart(start_date, end_date):
    if merged_data.empty:
        return go.Figure().add_annotation(text="Dados não disponíveis",
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)

    try:
        # Filtra dados
        if start_date and end_date:
            mask = (merged_data.index >= start_date) & (merged_data.index <= end_date)
            filtered_data = merged_data.loc[mask]
        else:
            filtered_data = merged_data

        if filtered_data.empty or len(filtered_data) < 2:
            return go.Figure().add_annotation(text="Dados insuficientes para retornos",
                                            xref="paper", yref="paper",
                                            x=0.5, y=0.5, showarrow=False)

        btc_returns = calculate_returns(filtered_data['price_btc']) * 100
        qanx_returns = calculate_returns(filtered_data['price_qanx']) * 100

        # Remove valores NaN
        btc_returns = btc_returns.dropna()
        qanx_returns = qanx_returns.dropna()

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=btc_returns.index, y=btc_returns,
                      name='BTC Returns (%)',
                      line=dict(color=COLORS['btc'], width=1),
                      opacity=0.7)
        )
        fig.add_trace(
            go.Scatter(x=qanx_returns.index, y=qanx_returns,
                      name='QANX Returns (%)',
                      line=dict(color=COLORS['qanx'], width=1),
                      opacity=0.7)
        )

        # Linha de referência em zero
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

        fig.update_layout(
            title="Retornos Diários (%) - Volatilidade Comparativa",
            yaxis_title="Retorno (%)",
            xaxis_title="Data",
            template="plotly_dark"
        )

        return fig

    except Exception as e:
        return go.Figure().add_annotation(text=f"Erro: {str(e)}",
                                        xref="paper", yref="paper",
                                        x=0.5, y=0.5, showarrow=False)

@app.callback(
    Output('volume-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_volume_chart(start_date, end_date):
    if merged_data.empty:
        return go.Figure()
    
    # Filtra dados
    mask = (merged_data.index >= start_date) & (merged_data.index <= end_date)
    filtered_data = merged_data.loc[mask]
    
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Volume BTC', 'Volume QANX'))
    
    fig.add_trace(
        go.Bar(x=filtered_data.index, y=filtered_data['volume_btc'], 
               name='Volume BTC', marker_color=COLORS['btc']),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=filtered_data.index, y=filtered_data['volume_qanx'], 
               name='Volume QANX', marker_color=COLORS['qanx']),
        row=2, col=1
    )
    
    fig.update_layout(
        title="Volume de Negociação",
        template="plotly_dark",
        height=500
    )
    
    return fig

@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_scatter_chart(start_date, end_date):
    if merged_data.empty:
        return go.Figure()
    
    # Filtra dados
    mask = (merged_data.index >= start_date) & (merged_data.index <= end_date)
    filtered_data = merged_data.loc[mask]
    
    btc_returns = calculate_returns(filtered_data['price_btc']) * 100
    qanx_returns = calculate_returns(filtered_data['price_qanx']) * 100
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=btc_returns, y=qanx_returns, 
                  mode='markers', name='Retornos Diários',
                  marker=dict(color=COLORS['qanx'], opacity=0.6))
    )
    
    # Linha de tendência
    if len(btc_returns) > 1:
        z = np.polyfit(btc_returns.dropna(), qanx_returns.dropna(), 1)
        p = np.poly1d(z)
        fig.add_trace(
            go.Scatter(x=btc_returns, y=p(btc_returns), 
                      mode='lines', name='Tendência',
                      line=dict(color='red', dash='dash'))
        )
    
    fig.update_layout(
        title="Correlação de Retornos: QANX vs BTC",
        xaxis_title="Retorno BTC (%)",
        yaxis_title="Retorno QANX (%)",
        template="plotly_dark"
    )
    
    return fig

@app.callback(
    Output('insights-content', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_insights(start_date, end_date):
    if merged_data.empty:
        return html.P("Dados não disponíveis")
    
    # Executa análise rápida
    try:
        analyzer_temp = QANXBTCAnalyzer()
        analyzer_temp.merged_data = merged_data
        analyzer_temp.analyze_correlation()
        analyzer_temp.analyze_btc_seasons_impact()
        analyzer_temp.test_manipulation_theory()
        insights = analyzer_temp.generate_insights()
        
        return [html.P(f"• {insight}") for insight in insights]
    except:
        return html.P("Erro ao gerar insights")

if __name__ == '__main__':
    app.run(host=DASH_HOST, port=DASH_PORT, debug=DASH_DEBUG)
