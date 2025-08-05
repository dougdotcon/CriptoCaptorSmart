"""
🔥 CriptoCaptorSmart - Analisador Universal 🔥
Analisador de correlação e padrões para qualquer criptomoeda
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import ta
from crypto_config import (
    CORRELATION_WINDOW, VOLATILITY_WINDOW, TREND_WINDOW,
    RSI_WINDOW, MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BULL_MARKET_THRESHOLD, BEAR_MARKET_THRESHOLD,
    HIGH_CORRELATION_THRESHOLD, LOW_CORRELATION_THRESHOLD
)

class UniversalCryptoAnalyzer:
    def __init__(self):
        self.crypto1_data = None
        self.crypto2_data = None
        self.merged_data = None
        self.analysis_results = {}
        
    def load_data(self, crypto1_data, crypto2_data=None, crypto1_name="Crypto1", crypto2_name="Crypto2"):
        """Carrega dados para análise"""
        self.crypto1_data = crypto1_data.copy()
        self.crypto1_name = crypto1_name
        
        if crypto2_data is not None:
            self.crypto2_data = crypto2_data.copy()
            self.crypto2_name = crypto2_name
            self._merge_data()
        else:
            self.crypto2_data = None
            self.crypto2_name = None
            
        print(f"✅ Dados carregados: {crypto1_name}" + (f" vs {crypto2_name}" if crypto2_data is not None else ""))

    def _merge_data(self):
        """Combina dados de duas criptomoedas"""
        if self.crypto2_data is None:
            return
            
        # Garante que os índices são datetime
        if not isinstance(self.crypto1_data.index, pd.DatetimeIndex):
            self.crypto1_data.index = pd.to_datetime(self.crypto1_data.index)
        if not isinstance(self.crypto2_data.index, pd.DatetimeIndex):
            self.crypto2_data.index = pd.to_datetime(self.crypto2_data.index)

        # Remove dados nulos
        self.crypto1_data = self.crypto1_data.dropna()
        self.crypto2_data = self.crypto2_data.dropna()

        # Encontra período comum
        start_date = max(self.crypto1_data.index.min(), self.crypto2_data.index.min())
        end_date = min(self.crypto1_data.index.max(), self.crypto2_data.index.max())

        # Filtra para período comum
        crypto1_filtered = self.crypto1_data[start_date:end_date]
        crypto2_filtered = self.crypto2_data[start_date:end_date]

        # Combina dados
        self.merged_data = pd.DataFrame({
            f'price_{self.crypto1_name.lower()}': crypto1_filtered['price'],
            f'volume_{self.crypto1_name.lower()}': crypto1_filtered['volume'],
            f'price_{self.crypto2_name.lower()}': crypto2_filtered['price'],
            f'volume_{self.crypto2_name.lower()}': crypto2_filtered['volume']
        })

        self.merged_data = self.merged_data.dropna()
        print(f"📊 Dados combinados: {len(self.merged_data)} registros de {start_date.date()} a {end_date.date()}")

    def calculate_technical_indicators(self, data, price_col='price'):
        """Calcula indicadores técnicos"""
        if price_col not in data.columns:
            print(f"❌ Coluna {price_col} não encontrada")
            return data
            
        df = data.copy()
        prices = df[price_col]
        
        # Médias móveis
        df['sma_20'] = ta.trend.sma_indicator(prices, window=20)
        df['sma_50'] = ta.trend.sma_indicator(prices, window=50)
        df['ema_12'] = ta.trend.ema_indicator(prices, window=12)
        df['ema_26'] = ta.trend.ema_indicator(prices, window=26)
        
        # RSI
        df['rsi'] = ta.momentum.rsi(prices, window=RSI_WINDOW)
        
        # MACD
        df['macd'] = ta.trend.macd_diff(prices, window_slow=MACD_SLOW, window_fast=MACD_FAST, window_sign=MACD_SIGNAL)
        df['macd_signal'] = ta.trend.macd_signal(prices, window_slow=MACD_SLOW, window_fast=MACD_FAST, window_sign=MACD_SIGNAL)
        
        # Bollinger Bands
        df['bb_upper'] = ta.volatility.bollinger_hband(prices)
        df['bb_lower'] = ta.volatility.bollinger_lband(prices)
        df['bb_middle'] = ta.volatility.bollinger_mavg(prices)
        
        # Volatilidade
        df['returns'] = prices.pct_change()
        df['volatility'] = df['returns'].rolling(window=VOLATILITY_WINDOW).std() * np.sqrt(365)
        
        # Suporte e Resistência (simplificado)
        df['resistance'] = prices.rolling(window=20).max()
        df['support'] = prices.rolling(window=20).min()
        
        return df

    def analyze_single_crypto(self):
        """Análise de uma única criptomoeda"""
        if self.crypto1_data is None:
            print("❌ Nenhum dado carregado")
            return
            
        print(f"\n🔍 Analisando {self.crypto1_name}...")
        
        # Adiciona indicadores técnicos
        data_with_indicators = self.calculate_technical_indicators(self.crypto1_data)
        
        # Análise de performance
        prices = data_with_indicators['price']
        returns = data_with_indicators['returns'].dropna()
        
        performance = {
            'total_return': ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100,
            'annualized_return': (((prices.iloc[-1] / prices.iloc[0]) ** (365 / len(prices))) - 1) * 100,
            'volatility': returns.std() * np.sqrt(365) * 100,
            'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(365) if returns.std() > 0 else 0,
            'max_drawdown': ((prices / prices.expanding().max()) - 1).min() * 100,
            'win_rate': (returns > 0).mean() * 100,
            'current_price': prices.iloc[-1],
            'price_change_24h': ((prices.iloc[-1] / prices.iloc[-2]) - 1) * 100 if len(prices) > 1 else 0
        }
        
        # Análise técnica atual
        current_data = data_with_indicators.iloc[-1]
        technical_analysis = {
            'rsi': current_data['rsi'],
            'rsi_signal': 'Sobrecomprado' if current_data['rsi'] > 70 else 'Sobrevendido' if current_data['rsi'] < 30 else 'Neutro',
            'macd_signal': 'Bullish' if current_data['macd'] > current_data['macd_signal'] else 'Bearish',
            'bb_position': 'Acima' if current_data['price'] > current_data['bb_upper'] else 'Abaixo' if current_data['price'] < current_data['bb_lower'] else 'Dentro',
            'trend': 'Alta' if current_data['sma_20'] > current_data['sma_50'] else 'Baixa'
        }
        
        self.analysis_results['single_crypto'] = {
            'performance': performance,
            'technical': technical_analysis,
            'data_with_indicators': data_with_indicators
        }
        
        return self.analysis_results['single_crypto']

    def analyze_correlation(self):
        """Análise de correlação entre duas criptomoedas"""
        if self.merged_data is None or self.crypto2_data is None:
            print("❌ Dados de duas criptomoedas necessários para análise de correlação")
            return
            
        print(f"\n🔍 Analisando correlação {self.crypto1_name} vs {self.crypto2_name}...")
        
        price1_col = f'price_{self.crypto1_name.lower()}'
        price2_col = f'price_{self.crypto2_name.lower()}'
        
        # Calcula retornos
        returns1 = self.merged_data[price1_col].pct_change().dropna()
        returns2 = self.merged_data[price2_col].pct_change().dropna()
        
        # Correlações
        price_correlation = self.merged_data[price1_col].corr(self.merged_data[price2_col])
        returns_correlation = returns1.corr(returns2)
        rolling_correlation = returns1.rolling(window=CORRELATION_WINDOW).corr(returns2)
        
        # Análise de lag
        lag_correlations = {}
        for lag in range(-10, 11):
            if lag == 0:
                lag_corr = returns_correlation
            elif lag > 0:
                lag_corr = returns1.corr(returns2.shift(lag))
            else:
                lag_corr = returns1.shift(-lag).corr(returns2)
            lag_correlations[lag] = lag_corr
        
        best_lag = max(lag_correlations.items(), key=lambda x: abs(x[1]))
        
        correlation_analysis = {
            'price_correlation': price_correlation,
            'returns_correlation': returns_correlation,
            'rolling_correlation': rolling_correlation,
            'correlation_strength': 'Alta' if abs(returns_correlation) > HIGH_CORRELATION_THRESHOLD else 'Baixa' if abs(returns_correlation) < LOW_CORRELATION_THRESHOLD else 'Média',
            'best_lag': best_lag[0],
            'best_lag_correlation': best_lag[1],
            'lag_analysis': lag_correlations
        }
        
        self.analysis_results['correlation'] = correlation_analysis
        return correlation_analysis

    def identify_market_cycles(self, crypto_name=None):
        """Identifica ciclos de mercado (bull/bear)"""
        if crypto_name is None:
            crypto_name = self.crypto1_name
            
        if self.merged_data is not None and f'price_{crypto_name.lower()}' in self.merged_data.columns:
            prices = self.merged_data[f'price_{crypto_name.lower()}']
        elif crypto_name.lower() == self.crypto1_name.lower():
            prices = self.crypto1_data['price']
        else:
            print(f"❌ Dados não encontrados para {crypto_name}")
            return
            
        returns = prices.pct_change().dropna()
        rolling_returns = returns.rolling(window=TREND_WINDOW).mean()
        
        cycles = []
        current_cycle = None
        
        for date, ret in rolling_returns.items():
            if ret > BULL_MARKET_THRESHOLD / 365 and current_cycle != 'bull':
                current_cycle = 'bull'
                cycles.append({'date': date, 'cycle': 'bull', 'price': prices.loc[date]})
            elif ret < BEAR_MARKET_THRESHOLD / 365 and current_cycle != 'bear':
                current_cycle = 'bear'
                cycles.append({'date': date, 'cycle': 'bear', 'price': prices.loc[date]})
        
        cycles_df = pd.DataFrame(cycles)
        
        # Estatísticas dos ciclos
        if not cycles_df.empty:
            bull_periods = cycles_df[cycles_df['cycle'] == 'bull']
            bear_periods = cycles_df[cycles_df['cycle'] == 'bear']
            
            cycle_stats = {
                'total_cycles': len(cycles_df),
                'bull_periods': len(bull_periods),
                'bear_periods': len(bear_periods),
                'current_cycle': current_cycle,
                'cycles_data': cycles_df
            }
        else:
            cycle_stats = {
                'total_cycles': 0,
                'bull_periods': 0,
                'bear_periods': 0,
                'current_cycle': 'indefinido',
                'cycles_data': cycles_df
            }
        
        self.analysis_results['market_cycles'] = cycle_stats
        return cycle_stats

    def generate_insights(self):
        """Gera insights baseados na análise"""
        insights = []
        
        # Insights de crypto única
        if 'single_crypto' in self.analysis_results:
            perf = self.analysis_results['single_crypto']['performance']
            tech = self.analysis_results['single_crypto']['technical']
            
            insights.append(f"{self.crypto1_name} teve retorno total de {perf['total_return']:.1f}%")
            insights.append(f"Volatilidade anualizada: {perf['volatility']:.1f}%")
            insights.append(f"RSI atual: {tech['rsi']:.1f} ({tech['rsi_signal']})")
            insights.append(f"Tendência: {tech['trend']} (SMA 20 vs SMA 50)")
            
        # Insights de correlação
        if 'correlation' in self.analysis_results:
            corr = self.analysis_results['correlation']
            
            insights.append(f"Correlação de retornos: {corr['returns_correlation']:.3f} ({corr['correlation_strength']})")
            
            if abs(corr['best_lag_correlation']) > abs(corr['returns_correlation']):
                insights.append(f"Melhor correlação com lag de {corr['best_lag']} dias: {corr['best_lag_correlation']:.3f}")
                
        # Insights de ciclos
        if 'market_cycles' in self.analysis_results:
            cycles = self.analysis_results['market_cycles']
            insights.append(f"Ciclo atual: {cycles['current_cycle']}")
            insights.append(f"Total de ciclos identificados: {cycles['total_cycles']}")
            
        return insights

    def run_full_analysis(self):
        """Executa análise completa"""
        results = {}
        
        # Análise de crypto única
        if self.crypto1_data is not None:
            results['single'] = self.analyze_single_crypto()
            results['cycles'] = self.identify_market_cycles()
        
        # Análise de correlação se houver duas cryptos
        if self.crypto2_data is not None:
            results['correlation'] = self.analyze_correlation()
            
        # Gera insights
        results['insights'] = self.generate_insights()
        
        return results

def main():
    """Função principal para teste"""
    print("🔥 Testando Analisador Universal...")
    
    # Aqui você pode adicionar dados de teste
    # analyzer = UniversalCryptoAnalyzer()
    # analyzer.load_data(crypto1_data, crypto2_data, "BTC", "ETH")
    # results = analyzer.run_full_analysis()
    
    print("✅ Analisador Universal pronto!")

if __name__ == "__main__":
    main()
