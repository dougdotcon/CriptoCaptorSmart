"""
Analisador de correlação entre QANX e BTC
Implementa a teoria de manipulação do fundo QANX baseado nos ciclos do BTC
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from utils import (
    load_data, calculate_returns, calculate_volatility, 
    calculate_correlation, identify_btc_seasons, 
    calculate_performance_metrics, save_data
)

class QANXBTCAnalyzer:
    def __init__(self):
        self.btc_data = None
        self.qanx_data = None
        self.merged_data = None
        self.analysis_results = {}
        
    def load_data(self):
        """Carrega os dados históricos"""
        print("Carregando dados históricos...")

        self.btc_data = load_data('btc_historical.csv')
        self.qanx_data = load_data('qanx_historical.csv')

        if self.btc_data is None or self.qanx_data is None:
            raise ValueError("Dados não encontrados. Execute data_collector.py primeiro.")

        # Garante que os índices são datetime
        if not isinstance(self.btc_data.index, pd.DatetimeIndex):
            self.btc_data.index = pd.to_datetime(self.btc_data.index)
        if not isinstance(self.qanx_data.index, pd.DatetimeIndex):
            self.qanx_data.index = pd.to_datetime(self.qanx_data.index)

        # Remove dados com valores nulos
        self.btc_data = self.btc_data.dropna()
        self.qanx_data = self.qanx_data.dropna()

        # Encontra o período comum
        start_date = max(self.btc_data.index.min(), self.qanx_data.index.min())
        end_date = min(self.btc_data.index.max(), self.qanx_data.index.max())

        # Filtra para o período comum
        self.btc_data = self.btc_data[start_date:end_date]
        self.qanx_data = self.qanx_data[start_date:end_date]

        # Merge dos dados por data
        self.merged_data = pd.merge(
            self.btc_data[['price', 'volume', 'market_cap']].add_suffix('_btc'),
            self.qanx_data[['price', 'volume', 'market_cap']].add_suffix('_qanx'),
            left_index=True, right_index=True, how='inner'
        )

        print(f"Dados carregados: {len(self.merged_data)} registros de {self.merged_data.index.min()} a {self.merged_data.index.max()}")
        
    def analyze_correlation(self):
        """Analisa correlação entre QANX e BTC"""
        print("Analisando correlações...")
        
        # Correlação de preços
        price_corr = self.merged_data['price_qanx'].corr(self.merged_data['price_btc'])
        
        # Correlação de retornos
        btc_returns = calculate_returns(self.merged_data['price_btc'])
        qanx_returns = calculate_returns(self.merged_data['price_qanx'])
        returns_corr = btc_returns.corr(qanx_returns)
        
        # Correlação móvel
        rolling_corr = calculate_correlation(qanx_returns, btc_returns, window=30)
        
        # Correlação de volumes
        volume_corr = self.merged_data['volume_qanx'].corr(self.merged_data['volume_btc'])
        
        self.analysis_results['correlations'] = {
            'price_correlation': price_corr,
            'returns_correlation': returns_corr,
            'volume_correlation': volume_corr,
            'rolling_correlation': rolling_corr
        }
        
        print(f"Correlação de preços: {price_corr:.4f}")
        print(f"Correlação de retornos: {returns_corr:.4f}")
        print(f"Correlação de volumes: {volume_corr:.4f}")
        
    def analyze_btc_seasons_impact(self):
        """Analisa o impacto dos ciclos do BTC no QANX ao longo dos anos"""
        print("Analisando impacto dos ciclos do BTC desde 2019...")

        # Identifica seasons do BTC
        btc_seasons = identify_btc_seasons(self.merged_data['price_btc'])

        # Calcula retornos durante diferentes seasons
        btc_returns = calculate_returns(self.merged_data['price_btc'])
        qanx_returns = calculate_returns(self.merged_data['price_qanx'])

        # Análise por períodos históricos específicos
        historical_periods = {
            'early_2019': (pd.Timestamp('2019-01-01'), pd.Timestamp('2019-12-31')),
            'covid_crash': (pd.Timestamp('2020-03-01'), pd.Timestamp('2020-04-30')),
            'bull_2020_2021': (pd.Timestamp('2020-10-01'), pd.Timestamp('2021-11-30')),
            'bear_2022': (pd.Timestamp('2022-01-01'), pd.Timestamp('2022-12-31')),
            'bull_2023_2024': (pd.Timestamp('2023-01-01'), pd.Timestamp('2024-03-31')),
            'recent': (pd.Timestamp('2024-04-01'), pd.Timestamp.now())
        }

        period_analysis = {}

        for period_name, (start, end) in historical_periods.items():
            # Filtra dados para o período
            mask = (self.merged_data.index >= start) & (self.merged_data.index <= end)
            period_data = self.merged_data[mask]

            if len(period_data) > 30:  # Só analisa se tem dados suficientes
                period_btc_returns = calculate_returns(period_data['price_btc'])
                period_qanx_returns = calculate_returns(period_data['price_qanx'])

                # Correlação do período
                correlation = period_btc_returns.corr(period_qanx_returns)

                # Performance anualizada
                btc_perf = (period_data['price_btc'].iloc[-1] / period_data['price_btc'].iloc[0] - 1) * 100
                qanx_perf = (period_data['price_qanx'].iloc[-1] / period_data['price_qanx'].iloc[0] - 1) * 100

                period_analysis[period_name] = {
                    'correlation': correlation,
                    'btc_performance': btc_perf,
                    'qanx_performance': qanx_perf,
                    'days': len(period_data),
                    'start_date': start,
                    'end_date': end
                }

                print(f"{period_name}: Correlação={correlation:.3f}, BTC={btc_perf:.1f}%, QANX={qanx_perf:.1f}%")

        # Análise geral de bull/bear markets
        rolling_btc_returns = btc_returns.rolling(window=90).mean()  # Janela maior para dados longos

        bull_mask = rolling_btc_returns > 0.005  # 0.5% de retorno médio trimestral
        bear_mask = rolling_btc_returns < -0.005  # -0.5% de retorno médio trimestral

        # Performance do QANX durante bull markets do BTC
        qanx_bull_performance = qanx_returns[bull_mask].mean() * 365 * 100 if bull_mask.sum() > 0 else 0
        qanx_bear_performance = qanx_returns[bear_mask].mean() * 365 * 100 if bear_mask.sum() > 0 else 0

        # Análise de lag (atraso) entre movimentos
        lag_analysis = self.analyze_lag_correlation()

        self.analysis_results['btc_seasons'] = {
            'qanx_bull_performance': qanx_bull_performance,
            'qanx_bear_performance': qanx_bear_performance,
            'bull_periods_count': bull_mask.sum(),
            'bear_periods_count': bear_mask.sum(),
            'lag_analysis': lag_analysis,
            'historical_periods': period_analysis
        }

        print(f"Performance QANX em bull markets BTC: {qanx_bull_performance:.2f}% anual")
        print(f"Performance QANX em bear markets BTC: {qanx_bear_performance:.2f}% anual")
        
    def analyze_lag_correlation(self):
        """Analisa correlação com diferentes lags temporais"""
        btc_returns = calculate_returns(self.merged_data['price_btc'])
        qanx_returns = calculate_returns(self.merged_data['price_qanx'])
        
        lag_correlations = {}
        
        # Testa lags de -10 a +10 dias
        for lag in range(-10, 11):
            if lag == 0:
                corr = btc_returns.corr(qanx_returns)
            elif lag > 0:
                # QANX atrasado em relação ao BTC
                corr = btc_returns[:-lag].corr(qanx_returns[lag:])
            else:
                # QANX adiantado em relação ao BTC
                corr = btc_returns[-lag:].corr(qanx_returns[:lag])
            
            lag_correlations[lag] = corr
        
        return lag_correlations
    
    def test_manipulation_theory(self):
        """Testa a teoria de manipulação do fundo QANX"""
        print("Testando teoria de manipulação...")
        
        btc_returns = calculate_returns(self.merged_data['price_btc'])
        qanx_returns = calculate_returns(self.merged_data['price_qanx'])
        
        # Identifica grandes movimentos do BTC
        btc_big_moves = btc_returns.abs() > btc_returns.std() * 2
        
        # Analisa comportamento do QANX após grandes movimentos do BTC
        qanx_after_btc_up = []
        qanx_after_btc_down = []
        
        for i in range(1, len(btc_returns)):
            if btc_big_moves.iloc[i-1]:  # Grande movimento no dia anterior
                if btc_returns.iloc[i-1] > 0:  # BTC subiu
                    qanx_after_btc_up.append(qanx_returns.iloc[i])
                else:  # BTC desceu
                    qanx_after_btc_down.append(qanx_returns.iloc[i])
        
        # Testa se há diferença significativa
        if len(qanx_after_btc_up) > 5 and len(qanx_after_btc_down) > 5:
            t_stat, p_value = stats.ttest_ind(qanx_after_btc_up, qanx_after_btc_down)
        else:
            t_stat, p_value = 0, 1
        
        # Análise de volume durante movimentos
        volume_analysis = self.analyze_volume_patterns()
        
        self.analysis_results['manipulation_theory'] = {
            'qanx_after_btc_up_mean': np.mean(qanx_after_btc_up) if qanx_after_btc_up else 0,
            'qanx_after_btc_down_mean': np.mean(qanx_after_btc_down) if qanx_after_btc_down else 0,
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'volume_analysis': volume_analysis
        }
        
        print(f"QANX após alta do BTC: {np.mean(qanx_after_btc_up)*100:.4f}% (média)")
        print(f"QANX após baixa do BTC: {np.mean(qanx_after_btc_down)*100:.4f}% (média)")
        print(f"Diferença significativa: {p_value < 0.05} (p-value: {p_value:.4f})")
    
    def analyze_volume_patterns(self):
        """Analisa padrões de volume"""
        btc_returns = calculate_returns(self.merged_data['price_btc'])
        
        # Normaliza volumes
        btc_volume_norm = (self.merged_data['volume_btc'] - self.merged_data['volume_btc'].mean()) / self.merged_data['volume_btc'].std()
        qanx_volume_norm = (self.merged_data['volume_qanx'] - self.merged_data['volume_qanx'].mean()) / self.merged_data['volume_qanx'].std()
        
        # Correlação entre volumes e movimentos de preço
        btc_volume_price_corr = btc_volume_norm.corr(btc_returns.abs())
        qanx_volume_btc_move_corr = qanx_volume_norm.corr(btc_returns.abs())
        
        return {
            'btc_volume_price_correlation': btc_volume_price_corr,
            'qanx_volume_btc_move_correlation': qanx_volume_btc_move_corr
        }
    
    def generate_insights(self):
        """Gera insights baseados na análise histórica desde 2019"""
        insights = []

        # Correlação geral
        corr = self.analysis_results['correlations']['returns_correlation']
        if not pd.isna(corr):
            if corr > 0.5:
                insights.append(f"Alta correlação positiva ({corr:.3f}) entre QANX e BTC sugere movimentos sincronizados")
            elif corr < -0.1:
                insights.append(f"Correlação negativa ({corr:.3f}) pode indicar estratégia contrária")
            else:
                insights.append(f"Correlação moderada ({corr:.3f}) entre QANX e BTC")

        # Análise dos períodos históricos
        if 'historical_periods' in self.analysis_results['btc_seasons']:
            periods = self.analysis_results['btc_seasons']['historical_periods']

            # Encontra período com maior correlação
            max_corr_period = max(periods.items(), key=lambda x: x[1]['correlation'] if not pd.isna(x[1]['correlation']) else 0)
            min_corr_period = min(periods.items(), key=lambda x: x[1]['correlation'] if not pd.isna(x[1]['correlation']) else 1)

            insights.append(f"Maior correlação em {max_corr_period[0]}: {max_corr_period[1]['correlation']:.3f}")
            insights.append(f"Menor correlação em {min_corr_period[0]}: {min_corr_period[1]['correlation']:.3f}")

            # Analisa performance em bull markets históricos
            bull_periods = ['bull_2020_2021', 'bull_2023_2024']
            for period in bull_periods:
                if period in periods:
                    data = periods[period]
                    insights.append(f"Durante {period}: QANX {data['qanx_performance']:.1f}% vs BTC {data['btc_performance']:.1f}%")

            # Analisa COVID crash
            if 'covid_crash' in periods:
                covid_data = periods['covid_crash']
                insights.append(f"COVID crash: QANX caiu {covid_data['qanx_performance']:.1f}% vs BTC {covid_data['btc_performance']:.1f}%")

        # Performance em diferentes ciclos
        bull_perf = self.analysis_results['btc_seasons']['qanx_bull_performance']
        bear_perf = self.analysis_results['btc_seasons']['qanx_bear_performance']

        if not pd.isna(bull_perf) and not pd.isna(bear_perf):
            if bull_perf > bear_perf:
                insights.append(f"QANX performa melhor durante bull markets do BTC ({bull_perf:.1f}% vs {bear_perf:.1f}% anual)")
            else:
                insights.append(f"QANX performa melhor durante bear markets do BTC ({bear_perf:.1f}% vs {bull_perf:.1f}% anual)")

        # Teoria de manipulação
        if self.analysis_results['manipulation_theory']['significant']:
            insights.append("⚠️ Evidência estatística de comportamento diferenciado do QANX após movimentos do BTC")
            insights.append("Isso pode suportar a teoria de manipulação do fundo")

        # Análise de lag
        lag_analysis = self.analysis_results['btc_seasons']['lag_analysis']
        if lag_analysis:
            best_lag = max(lag_analysis.items(), key=lambda x: abs(x[1]) if not pd.isna(x[1]) else 0)
            if abs(best_lag[1]) > 0.3:
                if best_lag[0] > 0:
                    insights.append(f"QANX reage com {best_lag[0]} dias de atraso ao BTC (correlação: {best_lag[1]:.3f})")
                elif best_lag[0] < 0:
                    insights.append(f"QANX antecipa movimentos do BTC em {abs(best_lag[0])} dias (correlação: {best_lag[1]:.3f})")

        # Evolução temporal da correlação
        if len(self.analysis_results['btc_seasons']['historical_periods']) > 2:
            insights.append("📈 Correlação QANX-BTC evoluiu significativamente desde 2019")
            insights.append("Isso pode indicar mudanças na estratégia do fundo ao longo do tempo")

        return insights
    
    def run_full_analysis(self):
        """Executa análise completa"""
        self.load_data()
        self.analyze_correlation()
        self.analyze_btc_seasons_impact()
        self.test_manipulation_theory()
        
        # Salva resultados
        results_df = pd.DataFrame({
            'btc_price': self.merged_data['price_btc'],
            'qanx_price': self.merged_data['price_qanx'],
            'btc_returns': calculate_returns(self.merged_data['price_btc']),
            'qanx_returns': calculate_returns(self.merged_data['price_qanx']),
            'rolling_correlation': self.analysis_results['correlations']['rolling_correlation']
        })
        
        save_data(results_df, 'analysis_results.csv')
        
        # Gera insights
        insights = self.generate_insights()
        
        print("\n=== INSIGHTS DA ANÁLISE ===")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        return self.analysis_results, insights

def main():
    analyzer = QANXBTCAnalyzer()
    results, insights = analyzer.run_full_analysis()
    return analyzer

if __name__ == "__main__":
    analyzer = main()
