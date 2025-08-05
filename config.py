"""
Configurações para análise QANX vs BTC
"""

# APIs de dados
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINMARKETCAP_API_BASE = "https://pro-api.coinmarketcap.com/v1"

# IDs dos tokens
QANX_ID = "qanplatform"  # ID do QANX no CoinGecko
BTC_ID = "bitcoin"       # ID do BTC no CoinGecko

# Configurações de análise
CORRELATION_WINDOW = 30  # Janela para correlação móvel (dias)
VOLATILITY_WINDOW = 14   # Janela para cálculo de volatilidade

# Configurações do dashboard
DASH_HOST = "127.0.0.1"
DASH_PORT = 8050
DASH_DEBUG = True

# Diretórios
DATA_DIR = "data"
CHARTS_DIR = "charts"

# Cores para gráficos
COLORS = {
    'qanx': '#00D4FF',
    'btc': '#F7931A',
    'background': '#1E1E1E',
    'text': '#FFFFFF',
    'grid': '#404040'
}
