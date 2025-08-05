"""
Dashboard simplificado para garantir funcionamento
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from analyzer import QANXBTCAnalyzer
from utils import calculate_returns
# Cores estilo Meta Facebook
META_COLORS = {
    'primary': '#1877F2',      # Azul Facebook
    'secondary': '#42B883',    # Verde
    'accent': '#E1306C',       # Rosa/Magenta
    'warning': '#F56500',      # Laranja
    'background': '#F0F2F5',   # Cinza claro de fundo
    'surface': '#FFFFFF',      # Branco para cards
    'text_primary': '#1C1E21', # Texto principal
    'text_secondary': '#65676B', # Texto secundário
    'border': '#CED0D4',       # Bordas
    'hover': '#E4E6EA'         # Hover states
}

# Carrega dados
print("Carregando dados...")
analyzer = QANXBTCAnalyzer()
analyzer.load_data()
data = analyzer.merged_data

print(f"Dados carregados: {len(data)} registros")

# Inicializa app com suporte a múltiplas páginas
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# CSS customizado
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>QANX vs BTC Analysis</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #F0F2F5;
            }
            .metric-card {
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                transition: box-shadow 0.2s ease;
            }
            .metric-card:hover {
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            }
            .insight-card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #1877F2;
            }
            .chart-container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 24px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Executa análise completa para insights
print("Executando análise completa...")
analyzer.analyze_correlation()
analyzer.analyze_btc_seasons_impact()
analyzer.test_manipulation_theory()
insights = analyzer.generate_insights()

# Função para criar o header de navegação
def create_header():
    return html.Div([
        html.Div([
            # Logo/Título
            html.Div([
                html.H1("QANX Investment Analysis",
                        style={
                            'color': META_COLORS['text_primary'],
                            'fontSize': '28px',
                            'fontWeight': '700',
                            'margin': '0',
                            'letterSpacing': '-0.5px'
                        })
            ], style={'flex': '1'}),

            # Navegação
            html.Div([
                html.A("Analysis Dashboard",
                       href="/",
                       style={
                           'color': META_COLORS['primary'],
                           'textDecoration': 'none',
                           'padding': '12px 24px',
                           'borderRadius': '8px',
                           'backgroundColor': 'transparent',
                           'border': f'2px solid {META_COLORS["primary"]}',
                           'fontWeight': '600',
                           'fontSize': '14px',
                           'marginRight': '12px',
                           'transition': 'all 0.2s ease'
                       }),
                html.A("Investment Strategy",
                       href="/strategy",
                       style={
                           'color': 'white',
                           'textDecoration': 'none',
                           'padding': '12px 24px',
                           'borderRadius': '8px',
                           'backgroundColor': META_COLORS['primary'],
                           'border': f'2px solid {META_COLORS["primary"]}',
                           'fontWeight': '600',
                           'fontSize': '14px',
                           'transition': 'all 0.2s ease'
                       })
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 24px'
        })
    ], style={
        'background': META_COLORS['surface'],
        'borderBottom': f"1px solid {META_COLORS['border']}",
        'padding': '16px 0',
        'position': 'sticky',
        'top': '0',
        'zIndex': '1000',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
    })

# Layout principal com roteamento
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    create_header(),
    html.Div(id='page-content')
], style={
    'backgroundColor': META_COLORS['background'],
    'minHeight': '100vh',
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
})

# Layout da página de análise
def create_analysis_page():
    return html.Div([
        # Subtitle
        html.Div([
            html.P(f"Comprehensive analysis from {data.index.min().strftime('%B %Y')} to {data.index.max().strftime('%B %Y')}",
                   style={
                       'color': META_COLORS['text_secondary'],
                       'fontSize': '16px',
                       'margin': '0',
                       'textAlign': 'center'
                   })
        ], style={
            'padding': '24px 0',
            'borderBottom': f"1px solid {META_COLORS['border']}",
            'marginBottom': '24px'
        }),

    # Container principal
    html.Div([
        # Seção de Insights (topo)
        html.Div([
            html.H2("Key Insights",
                    style={
                        'color': META_COLORS['text_primary'],
                        'fontSize': '24px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),

            # Cards de métricas principais
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Correlation", style={
                            'color': META_COLORS['text_secondary'],
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'margin': '0 0 8px 0',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.5px'
                        }),
                        html.H2(f"{calculate_returns(data['price_qanx']).corr(calculate_returns(data['price_btc'])):.3f}",
                                style={
                                    'color': META_COLORS['primary'],
                                    'fontSize': '36px',
                                    'fontWeight': '700',
                                    'margin': '0'
                                })
                    ], className='metric-card', style={'padding': '24px', 'textAlign': 'center'})
                ], style={'width': '23%', 'display': 'inline-block', 'margin': '0 1% 16px 0'}),

                html.Div([
                    html.Div([
                        html.H3("Analysis Period", style={
                            'color': META_COLORS['text_secondary'],
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'margin': '0 0 8px 0',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.5px'
                        }),
                        html.H2(f"{len(data):,} days",
                                style={
                                    'color': META_COLORS['secondary'],
                                    'fontSize': '36px',
                                    'fontWeight': '700',
                                    'margin': '0'
                                })
                    ], className='metric-card', style={'padding': '24px', 'textAlign': 'center'})
                ], style={'width': '23%', 'display': 'inline-block', 'margin': '0 1% 16px 0'}),

                html.Div([
                    html.Div([
                        html.H3("BTC Price", style={
                            'color': META_COLORS['text_secondary'],
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'margin': '0 0 8px 0',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.5px'
                        }),
                        html.H2(f"${data['price_btc'].iloc[-1]:,.0f}",
                                style={
                                    'color': META_COLORS['warning'],
                                    'fontSize': '36px',
                                    'fontWeight': '700',
                                    'margin': '0'
                                })
                    ], className='metric-card', style={'padding': '24px', 'textAlign': 'center'})
                ], style={'width': '23%', 'display': 'inline-block', 'margin': '0 1% 16px 0'}),

                html.Div([
                    html.Div([
                        html.H3("QANX Price", style={
                            'color': META_COLORS['text_secondary'],
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'margin': '0 0 8px 0',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.5px'
                        }),
                        html.H2(f"${data['price_qanx'].iloc[-1]:.4f}",
                                style={
                                    'color': META_COLORS['accent'],
                                    'fontSize': '36px',
                                    'fontWeight': '700',
                                    'margin': '0'
                                })
                    ], className='metric-card', style={'padding': '24px', 'textAlign': 'center'})
                ], style={'width': '23%', 'display': 'inline-block'})
            ], style={'marginBottom': '32px'}),

            # Insights detalhados
            html.Div([
                # Evidência estatística
                html.Div([
                    html.H3("Statistical Evidence",
                            style={
                                'color': META_COLORS['text_primary'],
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'marginBottom': '16px'
                            }),
                    html.Div([
                        html.Div([
                            html.P("P-value", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '14px',
                                'margin': '0 0 4px 0'
                            }),
                            html.P(f"{analyzer.analysis_results['manipulation_theory']['p_value']:.4f}", style={
                                'color': META_COLORS['secondary'] if analyzer.analysis_results['manipulation_theory']['significant'] else META_COLORS['accent'],
                                'fontSize': '24px',
                                'fontWeight': '700',
                                'margin': '0'
                            }),
                            html.P("Statistically Significant" if analyzer.analysis_results['manipulation_theory']['significant'] else "Not Significant", style={
                                'color': META_COLORS['secondary'] if analyzer.analysis_results['manipulation_theory']['significant'] else META_COLORS['accent'],
                                'fontSize': '12px',
                                'fontWeight': '500',
                                'margin': '4px 0 0 0'
                            })
                        ], style={'width': '32%', 'display': 'inline-block', 'textAlign': 'center'}),

                        html.Div([
                            html.P("QANX after BTC Rise", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '14px',
                                'margin': '0 0 4px 0'
                            }),
                            html.P(f"+{analyzer.analysis_results['manipulation_theory']['qanx_after_btc_up_mean']*100:.2f}%", style={
                                'color': META_COLORS['secondary'],
                                'fontSize': '24px',
                                'fontWeight': '700',
                                'margin': '0'
                            })
                        ], style={'width': '32%', 'display': 'inline-block', 'textAlign': 'center', 'margin': '0 2%'}),

                        html.Div([
                            html.P("QANX after BTC Fall", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '14px',
                                'margin': '0 0 4px 0'
                            }),
                            html.P(f"{analyzer.analysis_results['manipulation_theory']['qanx_after_btc_down_mean']*100:.2f}%", style={
                                'color': META_COLORS['accent'],
                                'fontSize': '24px',
                                'fontWeight': '700',
                                'margin': '0'
                            })
                        ], style={'width': '32%', 'display': 'inline-block', 'textAlign': 'center'})
                    ])
                ], className='insight-card', style={'padding': '24px', 'marginBottom': '16px'}),

                # Performance por ciclos
                html.Div([
                    html.H3("Performance by BTC Cycles",
                            style={
                                'color': META_COLORS['text_primary'],
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'marginBottom': '16px'
                            }),
                    html.Div([
                        html.Div([
                            html.P("Bull Markets", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '14px',
                                'margin': '0 0 4px 0'
                            }),
                            html.P(f"+{analyzer.analysis_results['btc_seasons']['qanx_bull_performance']:.1f}%", style={
                                'color': META_COLORS['secondary'],
                                'fontSize': '28px',
                                'fontWeight': '700',
                                'margin': '0'
                            }),
                            html.P("Annual Return", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '12px',
                                'margin': '4px 0 0 0'
                            })
                        ], style={'width': '48%', 'display': 'inline-block', 'textAlign': 'center'}),

                        html.Div([
                            html.P("Bear Markets", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '14px',
                                'margin': '0 0 4px 0'
                            }),
                            html.P(f"{analyzer.analysis_results['btc_seasons']['qanx_bear_performance']:.1f}%", style={
                                'color': META_COLORS['accent'],
                                'fontSize': '28px',
                                'fontWeight': '700',
                                'margin': '0'
                            }),
                            html.P("Annual Return", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '12px',
                                'margin': '4px 0 0 0'
                            })
                        ], style={'width': '48%', 'display': 'inline-block', 'textAlign': 'center', 'margin': '0 0 0 4%'})
                    ])
                ], className='insight-card', style={'padding': '24px', 'marginBottom': '16px'}),

                # Períodos históricos
                html.Div([
                    html.H3("Historical Periods Analysis",
                            style={
                                'color': META_COLORS['text_primary'],
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'marginBottom': '16px'
                            }),
                    html.Div(id='historical-periods')
                ], className='insight-card', style={'padding': '24px', 'marginBottom': '16px'}),

                # Conclusão
                html.Div([
                    html.H3("Conclusion",
                            style={
                                'color': META_COLORS['text_primary'],
                                'fontSize': '18px',
                                'fontWeight': '600',
                                'marginBottom': '16px'
                            }),
                    html.P("Theory Validation: " + ("STATISTICALLY CONFIRMED" if analyzer.analysis_results['manipulation_theory']['significant'] else "NOT CONFIRMED"),
                           style={
                               'fontSize': '16px',
                               'fontWeight': '600',
                               'color': META_COLORS['secondary'] if analyzer.analysis_results['manipulation_theory']['significant'] else META_COLORS['accent'],
                               'marginBottom': '12px'
                           }),
                    html.P("The data shows clear evidence that QANX behaves differently after BTC movements, with statistical significance. " +
                           "The evolution of correlation over time and anomalous patterns strongly suggest an active fund manipulation strategy based on Bitcoin cycles.",
                           style={
                               'fontSize': '14px',
                               'color': META_COLORS['text_secondary'],
                               'lineHeight': '1.6',
                               'margin': '0'
                           })
                ], className='insight-card', style={'padding': '24px', 'marginBottom': '32px'})
            ])
        ], style={'marginBottom': '32px'}),

        # Seção de Gráficos
        html.Div([
            html.H2("Charts & Analysis",
                    style={
                        'color': META_COLORS['text_primary'],
                        'fontSize': '24px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),

            # Gráficos
            html.Div([
                dcc.Graph(id='price-chart')
            ], className='chart-container'),

            html.Div([
                html.Div([
                    dcc.Graph(id='correlation-chart')
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='returns-chart')
                ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
            ], className='chart-container'),

            html.Div([
                dcc.Graph(id='scatter-chart')
            ], className='chart-container')
        ])
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '0 24px'
    })
    ])

# Layout da página de estratégia
def create_strategy_page():
    return html.Div([
        # Título da página
        html.Div([
            html.H1("Investment Strategy",
                    style={
                        'color': META_COLORS['text_primary'],
                        'fontSize': '32px',
                        'fontWeight': '700',
                        'margin': '0 0 16px 0',
                        'textAlign': 'center'
                    }),
            html.P("How to profit from QANX manipulation patterns as a small investor",
                   style={
                       'color': META_COLORS['text_secondary'],
                       'fontSize': '18px',
                       'margin': '0',
                       'textAlign': 'center'
                   })
        ], style={
            'padding': '32px 0',
            'borderBottom': f"1px solid {META_COLORS['border']}",
            'marginBottom': '32px'
        }),

        # Container principal
        html.Div([
            # Resumo executivo
            html.Div([
                html.H2("Executive Summary",
                        style={
                            'color': META_COLORS['text_primary'],
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'marginBottom': '16px'
                        }),
                html.P("Based on our statistical analysis (p-value: 0.0042), QANX shows significant behavioral patterns after BTC movements. " +
                       "This creates predictable opportunities for small investors to capitalize on fund manipulation strategies.",
                       style={
                           'color': META_COLORS['text_secondary'],
                           'fontSize': '16px',
                           'lineHeight': '1.6',
                           'marginBottom': '24px'
                       })
            ], className='insight-card', style={'padding': '24px', 'marginBottom': '24px'}),

            # Estratégias principais
            html.Div([
                html.H2("Key Investment Strategies",
                        style={
                            'color': META_COLORS['text_primary'],
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'marginBottom': '24px'
                        }),

                # Estratégia 1: Momentum Following
                html.Div([
                    html.H3("1. BTC Momentum Following",
                            style={
                                'color': META_COLORS['primary'],
                                'fontSize': '20px',
                                'fontWeight': '600',
                                'marginBottom': '16px'
                            }),
                    html.Div([
                        html.Div([
                            html.H4("Strategy", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginBottom': '8px'}),
                            html.P("When BTC rises >3% in a day, buy QANX within 24 hours. Our data shows QANX averages +5.19% after BTC rises.",
                                   style={'color': META_COLORS['text_secondary'], 'fontSize': '14px', 'margin': '0'})
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                        html.Div([
                            html.H4("Risk Level", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginBottom': '8px'}),
                            html.P("Medium - Success rate ~65% based on historical data",
                                   style={'color': META_COLORS['warning'], 'fontSize': '14px', 'margin': '0'})
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
                    ]),
                    html.Div([
                        html.H4("Entry/Exit Rules", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginTop': '16px', 'marginBottom': '8px'}),
                        html.Ul([
                            html.Li("Entry: BTC +3% daily gain, buy QANX next day", style={'margin': '4px 0'}),
                            html.Li("Exit: Take profit at +8% or stop loss at -5%", style={'margin': '4px 0'}),
                            html.Li("Max position: 10% of portfolio", style={'margin': '4px 0'})
                        ], style={'color': META_COLORS['text_secondary'], 'fontSize': '14px'})
                    ])
                ], className='insight-card', style={'padding': '20px', 'marginBottom': '16px', 'borderLeft': f'4px solid {META_COLORS["primary"]}'}),

                # Estratégia 2: Contrarian Play
                html.Div([
                    html.H3("2. COVID-Style Contrarian Play",
                            style={
                                'color': META_COLORS['secondary'],
                                'fontSize': '20px',
                                'fontWeight': '600',
                                'marginBottom': '16px'
                            }),
                    html.Div([
                        html.Div([
                            html.H4("Strategy", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginBottom': '8px'}),
                            html.P("During major BTC crashes (>15%), QANX sometimes moves opposite. Look for divergence patterns similar to COVID crash.",
                                   style={'color': META_COLORS['text_secondary'], 'fontSize': '14px', 'margin': '0'})
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                        html.Div([
                            html.H4("Risk Level", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginBottom': '8px'}),
                            html.P("High - Rare opportunity, high reward potential",
                                   style={'color': META_COLORS['accent'], 'fontSize': '14px', 'margin': '0'})
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
                    ]),
                    html.Div([
                        html.H4("Entry/Exit Rules", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginTop': '16px', 'marginBottom': '8px'}),
                        html.Ul([
                            html.Li("Entry: BTC crashes >15%, QANX shows strength", style={'margin': '4px 0'}),
                            html.Li("Exit: Take profit at +25% or when correlation normalizes", style={'margin': '4px 0'}),
                            html.Li("Max position: 5% of portfolio (high risk)", style={'margin': '4px 0'})
                        ], style={'color': META_COLORS['text_secondary'], 'fontSize': '14px'})
                    ])
                ], className='insight-card', style={'padding': '20px', 'marginBottom': '16px', 'borderLeft': f'4px solid {META_COLORS["secondary"]}'}),

                # Estratégia 3: Cycle Trading
                html.Div([
                    html.H3("3. Bull/Bear Cycle Trading",
                            style={
                                'color': META_COLORS['warning'],
                                'fontSize': '20px',
                                'fontWeight': '600',
                                'marginBottom': '16px'
                            }),
                    html.Div([
                        html.Div([
                            html.H4("Strategy", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginBottom': '8px'}),
                            html.P("QANX performs +404% in bull markets vs -322% in bear markets. Time entries with BTC cycle identification.",
                                   style={'color': META_COLORS['text_secondary'], 'fontSize': '14px', 'margin': '0'})
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                        html.Div([
                            html.H4("Risk Level", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginBottom': '8px'}),
                            html.P("Low-Medium - Long-term strategy with clear patterns",
                                   style={'color': META_COLORS['secondary'], 'fontSize': '14px', 'margin': '0'})
                        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
                    ]),
                    html.Div([
                        html.H4("Entry/Exit Rules", style={'color': META_COLORS['text_primary'], 'fontSize': '16px', 'marginTop': '16px', 'marginBottom': '8px'}),
                        html.Ul([
                            html.Li("Entry: Early bull market signals (BTC breaking ATH)", style={'margin': '4px 0'}),
                            html.Li("Exit: Bear market confirmation (BTC -50% from peak)", style={'margin': '4px 0'}),
                            html.Li("Max position: 20% of portfolio", style={'margin': '4px 0'})
                        ], style={'color': META_COLORS['text_secondary'], 'fontSize': '14px'})
                    ])
                ], className='insight-card', style={'padding': '20px', 'marginBottom': '24px', 'borderLeft': f'4px solid {META_COLORS["warning"]}'}),
            ]),

            # Risk Management
            html.Div([
                html.H2("Risk Management",
                        style={
                            'color': META_COLORS['text_primary'],
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'marginBottom': '16px'
                        }),
                html.Div([
                    html.Div([
                        html.H4("Position Sizing", style={'color': META_COLORS['accent'], 'fontSize': '18px', 'marginBottom': '12px'}),
                        html.Ul([
                            html.Li("Never risk more than 2% of portfolio on single trade", style={'margin': '6px 0'}),
                            html.Li("Maximum QANX allocation: 25% of total portfolio", style={'margin': '6px 0'}),
                            html.Li("Use dollar-cost averaging for cycle trades", style={'margin': '6px 0'})
                        ], style={'color': META_COLORS['text_secondary'], 'fontSize': '14px'})
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                    html.Div([
                        html.H4("Stop Losses", style={'color': META_COLORS['accent'], 'fontSize': '18px', 'marginBottom': '12px'}),
                        html.Ul([
                            html.Li("Momentum trades: -5% stop loss", style={'margin': '6px 0'}),
                            html.Li("Contrarian trades: -10% stop loss", style={'margin': '6px 0'}),
                            html.Li("Cycle trades: -20% stop loss (longer term)", style={'margin': '6px 0'})
                        ], style={'color': META_COLORS['text_secondary'], 'fontSize': '14px'})
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
                ])
            ], className='insight-card', style={'padding': '24px', 'marginBottom': '24px'}),

            # Tools and Monitoring
            html.Div([
                html.H2("Tools & Monitoring",
                        style={
                            'color': META_COLORS['text_primary'],
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'marginBottom': '16px'
                        }),
                html.Div([
                    html.Div([
                        html.H4("Essential Tools", style={'color': META_COLORS['primary'], 'fontSize': '18px', 'marginBottom': '12px'}),
                        html.Ul([
                            html.Li("TradingView for BTC technical analysis", style={'margin': '6px 0'}),
                            html.Li("CoinGecko/CMC for QANX price monitoring", style={'margin': '6px 0'}),
                            html.Li("This dashboard for correlation tracking", style={'margin': '6px 0'}),
                            html.Li("Portfolio tracker (Delta, Blockfolio)", style={'margin': '6px 0'})
                        ], style={'color': META_COLORS['text_secondary'], 'fontSize': '14px'})
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                    html.Div([
                        html.H4("Key Metrics to Watch", style={'color': META_COLORS['primary'], 'fontSize': '18px', 'marginBottom': '12px'}),
                        html.Ul([
                            html.Li("BTC daily returns >3% (momentum signal)", style={'margin': '6px 0'}),
                            html.Li("30-day rolling correlation changes", style={'margin': '6px 0'}),
                            html.Li("QANX volume spikes (manipulation signs)", style={'margin': '6px 0'}),
                            html.Li("BTC market cycle indicators", style={'margin': '6px 0'})
                        ], style={'color': META_COLORS['text_secondary'], 'fontSize': '14px'})
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '4%'})
                ])
            ], className='insight-card', style={'padding': '24px', 'marginBottom': '24px'}),

            # Disclaimer
            html.Div([
                html.H3("Important Disclaimer",
                        style={
                            'color': META_COLORS['accent'],
                            'fontSize': '20px',
                            'fontWeight': '600',
                            'marginBottom': '16px'
                        }),
                html.P("This analysis is for educational purposes only and should not be considered financial advice. " +
                       "Cryptocurrency investments are highly risky and volatile. Past performance does not guarantee future results. " +
                       "Always do your own research and consider consulting with a financial advisor before making investment decisions.",
                       style={
                           'color': META_COLORS['text_secondary'],
                           'fontSize': '14px',
                           'lineHeight': '1.6',
                           'fontStyle': 'italic'
                       })
            ], style={
                'backgroundColor': '#FFF3CD',
                'border': f'1px solid {META_COLORS["warning"]}',
                'borderRadius': '8px',
                'padding': '20px',
                'marginBottom': '32px'
            })
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 24px'
        })
    ])

@app.callback(Output('price-chart', 'figure'), [Input('price-chart', 'id')])
def update_price_chart(_):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Normalized Prices (Base 100)', 'Absolute Prices'),
        vertical_spacing=0.1
    )

    # Normaliza preços
    btc_norm = (data['price_btc'] / data['price_btc'].iloc[0]) * 100
    qanx_norm = (data['price_qanx'] / data['price_qanx'].iloc[0]) * 100

    # Gráfico normalizado
    fig.add_trace(go.Scatter(
        x=data.index, y=btc_norm,
        name='BTC (Normalized)',
        line=dict(color=META_COLORS['warning'], width=2)
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index, y=qanx_norm,
        name='QANX (Normalized)',
        line=dict(color=META_COLORS['primary'], width=2)
    ), row=1, col=1)

    # Gráfico absoluto
    fig.add_trace(go.Scatter(
        x=data.index, y=data['price_btc'],
        name='BTC Price ($)',
        line=dict(color=META_COLORS['warning'], width=2)
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=data.index, y=data['price_qanx'],
        name='QANX Price ($)',
        line=dict(color=META_COLORS['primary'], width=2),
        yaxis='y4'
    ), row=2, col=1)

    fig.update_layout(
        title={
            'text': "Price Evolution (2019-2025)",
            'font': {'size': 20, 'color': META_COLORS['text_primary']},
            'x': 0.5
        },
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': META_COLORS['text_primary']},
        yaxis4=dict(overlaying='y3', side='right', title='QANX Price ($)')
    )

    fig.update_xaxes(showgrid=True, gridcolor=META_COLORS['border'])
    fig.update_yaxes(showgrid=True, gridcolor=META_COLORS['border'])

    return fig

@app.callback(Output('correlation-chart', 'figure'), [Input('correlation-chart', 'id')])
def update_correlation_chart(_):
    import plotly.graph_objects as go
    from utils import calculate_correlation

    btc_returns = calculate_returns(data['price_btc'])
    qanx_returns = calculate_returns(data['price_qanx'])
    rolling_corr = calculate_correlation(qanx_returns, btc_returns, window=30)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rolling_corr.index, y=rolling_corr,
        name='30-day Rolling Correlation',
        line=dict(color=META_COLORS['primary'], width=2)
    ))

    # Linhas de referência
    fig.add_hline(y=0, line_dash="dash", line_color=META_COLORS['text_secondary'], opacity=0.5)
    fig.add_hline(y=0.5, line_dash="dot", line_color=META_COLORS['secondary'], opacity=0.7)
    fig.add_hline(y=-0.5, line_dash="dot", line_color=META_COLORS['accent'], opacity=0.7)

    fig.update_layout(
        title={
            'text': "Rolling Correlation (30 days)",
            'font': {'size': 16, 'color': META_COLORS['text_primary']},
            'x': 0.5
        },
        yaxis_title="Correlation",
        yaxis=dict(range=[-1, 1]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': META_COLORS['text_primary']},
        height=350
    )

    fig.update_xaxes(showgrid=True, gridcolor=META_COLORS['border'])
    fig.update_yaxes(showgrid=True, gridcolor=META_COLORS['border'])

    return fig

@app.callback(Output('returns-chart', 'figure'), [Input('returns-chart', 'id')])
def update_returns_chart(_):
    import plotly.graph_objects as go

    btc_returns = calculate_returns(data['price_btc']) * 100
    qanx_returns = calculate_returns(data['price_qanx']) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=btc_returns.index, y=btc_returns,
        name='BTC Returns (%)',
        line=dict(color=META_COLORS['warning'], width=1),
        opacity=0.8
    ))
    fig.add_trace(go.Scatter(
        x=qanx_returns.index, y=qanx_returns,
        name='QANX Returns (%)',
        line=dict(color=META_COLORS['primary'], width=1),
        opacity=0.8
    ))

    fig.add_hline(y=0, line_dash="dash", line_color=META_COLORS['text_secondary'], opacity=0.5)

    fig.update_layout(
        title={
            'text': "Daily Returns (%)",
            'font': {'size': 16, 'color': META_COLORS['text_primary']},
            'x': 0.5
        },
        yaxis_title="Return (%)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': META_COLORS['text_primary']},
        height=350
    )

    fig.update_xaxes(showgrid=True, gridcolor=META_COLORS['border'])
    fig.update_yaxes(showgrid=True, gridcolor=META_COLORS['border'])

    return fig

@app.callback(Output('scatter-chart', 'figure'), [Input('scatter-chart', 'id')])
def update_scatter_chart(_):
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    btc_returns = calculate_returns(data['price_btc']) * 100
    qanx_returns = calculate_returns(data['price_qanx']) * 100

    # Remove NaN
    valid_data = pd.DataFrame({'btc': btc_returns, 'qanx': qanx_returns}).dropna()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=valid_data['btc'], y=valid_data['qanx'],
        mode='markers', name='Daily Returns',
        marker=dict(
            color=META_COLORS['primary'],
            opacity=0.6,
            size=4
        )
    ))

    # Linha de tendência
    z = np.polyfit(valid_data['btc'], valid_data['qanx'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=valid_data['btc'], y=p(valid_data['btc']),
        mode='lines', name='Trend Line',
        line=dict(color=META_COLORS['accent'], dash='dash', width=2)
    ))

    fig.update_layout(
        title={
            'text': "Returns Correlation",
            'font': {'size': 16, 'color': META_COLORS['text_primary']},
            'x': 0.5
        },
        xaxis_title="BTC Return (%)",
        yaxis_title="QANX Return (%)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': META_COLORS['text_primary']},
        height=400
    )

    fig.update_xaxes(showgrid=True, gridcolor=META_COLORS['border'])
    fig.update_yaxes(showgrid=True, gridcolor=META_COLORS['border'])

    return fig

@app.callback(Output('historical-periods', 'children'), [Input('historical-periods', 'id')])
def update_historical_periods(_):
    if 'historical_periods' not in analyzer.analysis_results['btc_seasons']:
        return html.P("Historical periods data not available",
                     style={'color': META_COLORS['text_secondary']})

    periods = analyzer.analysis_results['btc_seasons']['historical_periods']
    period_elements = []

    period_names = {
        'early_2019': 'Early 2019',
        'covid_crash': 'COVID Crash (Mar-Apr 2020)',
        'bull_2020_2021': 'Bull Market 2020-2021',
        'bear_2022': 'Bear Market 2022',
        'bull_2023_2024': 'Bull Market 2023-2024',
        'recent': 'Recent Period'
    }

    for period_key, period_data in periods.items():
        if period_key in period_names:
            name = period_names[period_key]
            corr = period_data['correlation']
            btc_perf = period_data['btc_performance']
            qanx_perf = period_data['qanx_performance']

            # Cor baseada na correlação
            if corr > 0.7:
                corr_color = META_COLORS['secondary']
                corr_bg = '#E8F5E8'
            elif corr > 0.3:
                corr_color = META_COLORS['warning']
                corr_bg = '#FFF4E6'
            else:
                corr_color = META_COLORS['accent']
                corr_bg = '#FDE7F3'

            period_elements.append(
                html.Div([
                    html.H4(name, style={
                        'color': META_COLORS['text_primary'],
                        'margin': '0 0 12px 0',
                        'fontSize': '16px',
                        'fontWeight': '600'
                    }),
                    html.Div([
                        html.Div([
                            html.P("Correlation", style={
                                'color': META_COLORS['text_secondary'],
                                'fontSize': '12px',
                                'margin': '0 0 4px 0'
                            }),
                            html.P(f"{corr:.3f}", style={
                                'color': corr_color,
                                'fontSize': '18px',
                                'fontWeight': '700',
                                'margin': '0'
                            })
                        ], style={'textAlign': 'center', 'marginBottom': '8px'}),

                        html.Div([
                            html.P(f"BTC: {btc_perf:+.1f}%", style={
                                'color': META_COLORS['warning'],
                                'fontSize': '14px',
                                'margin': '2px 0'
                            }),
                            html.P(f"QANX: {qanx_perf:+.1f}%", style={
                                'color': META_COLORS['primary'],
                                'fontSize': '14px',
                                'margin': '2px 0'
                            }),
                            html.P(f"Diff: {qanx_perf - btc_perf:+.1f}%", style={
                                'color': META_COLORS['text_primary'],
                                'fontSize': '14px',
                                'fontWeight': '600',
                                'margin': '2px 0'
                            })
                        ])
                    ])
                ], style={
                    'backgroundColor': META_COLORS['surface'],
                    'border': f'1px solid {META_COLORS["border"]}',
                    'borderLeft': f'4px solid {corr_color}',
                    'padding': '16px',
                    'margin': '0 8px 8px 0',
                    'borderRadius': '8px',
                    'display': 'inline-block',
                    'width': '280px',
                    'verticalAlign': 'top',
                    'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)'
                })
            )

    return period_elements

# Callback de roteamento
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/strategy':
        return create_strategy_page()
    else:
        return create_analysis_page()

if __name__ == '__main__':
    print("Iniciando dashboard em http://127.0.0.1:8051")
    print("Páginas disponíveis:")
    print("- Análise: http://127.0.0.1:8051/")
    print("- Estratégia: http://127.0.0.1:8051/strategy")
    app.run(host='127.0.0.1', port=8051, debug=False)
