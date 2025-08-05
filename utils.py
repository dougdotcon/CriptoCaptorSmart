"""
Funções utilitárias para análise QANX vs BTC
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from config import DATA_DIR

def ensure_data_dir():
    """Garante que o diretório de dados existe"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def calculate_returns(prices):
    """Calcula retornos percentuais"""
    return prices.pct_change().dropna()

def calculate_volatility(prices, window=14):
    """Calcula volatilidade móvel"""
    returns = calculate_returns(prices)
    return returns.rolling(window=window).std() * np.sqrt(365)

def calculate_correlation(series1, series2, window=30):
    """Calcula correlação móvel entre duas séries"""
    return series1.rolling(window=window).corr(series2)

def identify_btc_seasons(btc_prices, threshold=0.2):
    """
    Identifica períodos de alta (bull) e baixa (bear) do BTC
    threshold: mudança percentual mínima para considerar uma tendência
    """
    returns = calculate_returns(btc_prices)
    cumulative_returns = (1 + returns).cumprod()
    
    # Identifica picos e vales
    rolling_max = cumulative_returns.rolling(window=30, min_periods=1).max()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    
    seasons = []
    current_season = None
    
    for date, price in btc_prices.items():
        dd = drawdown.loc[date] if date in drawdown.index else 0
        
        if dd > -0.2 and current_season != 'bull':
            current_season = 'bull'
            seasons.append({'date': date, 'season': 'bull', 'price': price})
        elif dd <= -0.2 and current_season != 'bear':
            current_season = 'bear'
            seasons.append({'date': date, 'season': 'bear', 'price': price})
    
    return pd.DataFrame(seasons)

def calculate_performance_metrics(prices):
    """Calcula métricas de performance"""
    returns = calculate_returns(prices)
    
    metrics = {
        'total_return': (prices.iloc[-1] / prices.iloc[0] - 1) * 100,
        'annualized_return': ((prices.iloc[-1] / prices.iloc[0]) ** (365 / len(prices)) - 1) * 100,
        'volatility': returns.std() * np.sqrt(365) * 100,
        'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(365) if returns.std() > 0 else 0,
        'max_drawdown': ((prices / prices.expanding().max()) - 1).min() * 100,
        'win_rate': (returns > 0).mean() * 100
    }
    
    return metrics

def format_currency(value, symbol='$'):
    """Formata valores monetários"""
    if value >= 1e9:
        return f"{symbol}{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"{symbol}{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"{symbol}{value/1e3:.2f}K"
    else:
        return f"{symbol}{value:.2f}"

def save_data(data, filename):
    """Salva dados em CSV"""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    data.to_csv(filepath, index=True)
    print(f"Dados salvos em: {filepath}")

def load_data(filename):
    """Carrega dados de CSV"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath, index_col=0, parse_dates=True)
    return None
