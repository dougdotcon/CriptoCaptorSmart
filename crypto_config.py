"""
🔥 CriptoCaptorSmart - Configurações Cyberpunk 🔥
Configurações centralizadas para análise universal de criptomoedas
"""

import os
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 CONFIGURAÇÕES DE APIs
# ═══════════════════════════════════════════════════════════════════════════════

# APIs de dados de criptomoedas
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINMARKETCAP_API_BASE = "https://pro-api.coinmarketcap.com/v1"
BINANCE_API_BASE = "https://api.binance.com/api/v3"

# Chaves de API (opcionais - usar variáveis de ambiente)
COINGECKO_API_KEY = os.environ.get('COINGECKO_API_KEY', '')
COINMARKETCAP_API_KEY = os.environ.get('COINMARKETCAP_API_KEY', '')

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 CONFIGURAÇÕES DE ANÁLISE
# ═══════════════════════════════════════════════════════════════════════════════

# Janelas de análise (em dias)
CORRELATION_WINDOW = 30      # Janela para correlação móvel
VOLATILITY_WINDOW = 14       # Janela para cálculo de volatilidade
TREND_WINDOW = 50           # Janela para identificação de tendências
RSI_WINDOW = 14             # Janela para RSI
MACD_FAST = 12              # MACD linha rápida
MACD_SLOW = 26              # MACD linha lenta
MACD_SIGNAL = 9             # MACD sinal

# Períodos de análise disponíveis
ANALYSIS_PERIODS = {
    '7d': 7,
    '30d': 30,
    '90d': 90,
    '180d': 180,
    '1y': 365,
    '2y': 730,
    'max': 2000
}

# Thresholds para análise
BULL_MARKET_THRESHOLD = 0.2    # 20% de alta para bull market
BEAR_MARKET_THRESHOLD = -0.2   # 20% de queda para bear market
HIGH_CORRELATION_THRESHOLD = 0.7
LOW_CORRELATION_THRESHOLD = 0.3

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 CONFIGURAÇÕES VISUAIS CYBERPUNK
# ═══════════════════════════════════════════════════════════════════════════════

# Cores cyberpunk para terminal
CYBERPUNK_COLORS = {
    'primary': '#00FF41',      # Verde Matrix
    'secondary': '#FF0080',    # Rosa neon
    'accent': '#00D4FF',       # Ciano
    'warning': '#FFD700',      # Dourado
    'error': '#FF4444',        # Vermelho
    'success': '#00FF41',      # Verde
    'info': '#00D4FF',         # Ciano
    'text': '#FFFFFF',         # Branco
    'background': '#000000',   # Preto
    'border': '#333333'        # Cinza escuro
}

# Cores para gráficos
CHART_COLORS = {
    'bitcoin': '#F7931A',      # Laranja Bitcoin
    'ethereum': '#627EEA',     # Azul Ethereum
    'crypto1': '#00FF41',      # Verde neon
    'crypto2': '#FF0080',      # Rosa neon
    'crypto3': '#00D4FF',      # Ciano
    'crypto4': '#FFD700',      # Dourado
    'crypto5': '#9D4EDD',      # Roxo
    'background': '#0A0A0A',   # Preto suave
    'grid': '#1A1A1A',        # Cinza muito escuro
    'text': '#FFFFFF'          # Branco
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🖥️ CONFIGURAÇÕES DO DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

# Configurações do servidor web
DASH_HOST = "127.0.0.1"
DASH_PORT = 8050
DASH_DEBUG = True

# Configurações de atualização
AUTO_REFRESH_INTERVAL = 60000  # 60 segundos em millisegundos
CHART_UPDATE_INTERVAL = 30000  # 30 segundos

# ═══════════════════════════════════════════════════════════════════════════════
# 📁 CONFIGURAÇÕES DE DIRETÓRIOS
# ═══════════════════════════════════════════════════════════════════════════════

# Diretórios do projeto
DATA_DIR = "data"
CHARTS_DIR = "charts"
LOGS_DIR = "logs"
CACHE_DIR = "cache"

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 CONFIGURAÇÕES TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════════

# Configurações de cache
CACHE_DURATION_MINUTES = 15    # Cache de dados por 15 minutos
MAX_CACHE_SIZE_MB = 100        # Máximo 100MB de cache

# Configurações de rate limiting
API_RATE_LIMIT_CALLS = 100     # Máximo 100 calls por minuto
API_RATE_LIMIT_WINDOW = 60     # Janela de 60 segundos

# Configurações de timeout
REQUEST_TIMEOUT = 30           # Timeout de 30 segundos para requests
CONNECTION_TIMEOUT = 10        # Timeout de conexão de 10 segundos

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 CRIPTOMOEDAS POPULARES PRÉ-CONFIGURADAS
# ═══════════════════════════════════════════════════════════════════════════════

POPULAR_CRYPTOS = {
    'bitcoin': {
        'symbol': 'BTC',
        'name': 'Bitcoin',
        'coingecko_id': 'bitcoin',
        'color': '#F7931A'
    },
    'ethereum': {
        'symbol': 'ETH', 
        'name': 'Ethereum',
        'coingecko_id': 'ethereum',
        'color': '#627EEA'
    },
    'qanplatform': {
        'symbol': 'QANX',
        'name': 'QAN Platform',
        'coingecko_id': 'qanplatform',
        'color': '#00D4FF'
    },
    'cardano': {
        'symbol': 'ADA',
        'name': 'Cardano',
        'coingecko_id': 'cardano',
        'color': '#0033AD'
    },
    'solana': {
        'symbol': 'SOL',
        'name': 'Solana',
        'coingecko_id': 'solana',
        'color': '#9945FF'
    },
    'polkadot': {
        'symbol': 'DOT',
        'name': 'Polkadot',
        'coingecko_id': 'polkadot',
        'color': '#E6007A'
    },
    'chainlink': {
        'symbol': 'LINK',
        'name': 'Chainlink',
        'coingecko_id': 'chainlink',
        'color': '#375BD2'
    },
    'polygon': {
        'symbol': 'MATIC',
        'name': 'Polygon',
        'coingecko_id': 'matic-network',
        'color': '#8247E5'
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🎮 CONFIGURAÇÕES DA INTERFACE CYBERPUNK
# ═══════════════════════════════════════════════════════════════════════════════

# ASCII Art e símbolos
CYBERPUNK_SYMBOLS = {
    'loading': ['▓', '▒', '░'],
    'bullet': '►',
    'success': '✓',
    'error': '✗',
    'warning': '⚠',
    'info': 'ℹ',
    'crypto': '₿',
    'trend_up': '↗',
    'trend_down': '↘',
    'trend_flat': '→'
}

# Configurações de animação
ANIMATION_SPEED = 0.1          # Velocidade das animações em segundos
LOADING_FRAMES = 20            # Número de frames para loading

# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 CONFIGURAÇÕES DE SEGURANÇA
# ═══════════════════════════════════════════════════════════════════════════════

# Configurações de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "crypto_captor.log"

# Configurações de backup
AUTO_BACKUP = True
BACKUP_INTERVAL_HOURS = 24
MAX_BACKUP_FILES = 7

def ensure_directories():
    """Garante que todos os diretórios necessários existem"""
    directories = [DATA_DIR, CHARTS_DIR, LOGS_DIR, CACHE_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Diretório criado: {directory}")

def get_crypto_info(crypto_id):
    """Retorna informações de uma criptomoeda"""
    return POPULAR_CRYPTOS.get(crypto_id.lower(), {
        'symbol': crypto_id.upper(),
        'name': crypto_id.title(),
        'coingecko_id': crypto_id.lower(),
        'color': CHART_COLORS['crypto1']
    })

def validate_config():
    """Valida as configurações"""
    ensure_directories()
    
    # Validações básicas
    assert CORRELATION_WINDOW > 0, "CORRELATION_WINDOW deve ser positivo"
    assert VOLATILITY_WINDOW > 0, "VOLATILITY_WINDOW deve ser positivo"
    assert DASH_PORT > 0, "DASH_PORT deve ser positivo"
    
    print("✅ Configurações validadas com sucesso!")

if __name__ == "__main__":
    validate_config()
