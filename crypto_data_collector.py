"""
🔥 CriptoCaptorSmart - Coletor Universal de Dados 🔥
Coletor de dados históricos para qualquer criptomoeda
"""

import requests
import pandas as pd
import time
import ccxt
import yfinance as yf
from datetime import datetime, timedelta
import json
import numpy as np
from tqdm import tqdm
from crypto_config import (
    COINGECKO_API_BASE, POPULAR_CRYPTOS, DATA_DIR,
    CACHE_DURATION_MINUTES, REQUEST_TIMEOUT, API_RATE_LIMIT_CALLS
)
import os

class UniversalCryptoCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CriptoCaptorSmart/1.0 (https://github.com/crypto-analysis)'
        })
        self.cache = {}
        self.rate_limit_calls = 0
        self.rate_limit_reset = time.time() + 60

        # Inicializa exchanges do CCXT
        self.exchanges = {}
        try:
            self.exchanges['binance'] = ccxt.binance()
        except:
            pass
        try:
            self.exchanges['coinbase'] = ccxt.coinbase()
        except:
            pass
        try:
            self.exchanges['kraken'] = ccxt.kraken()
        except:
            pass

    def _check_rate_limit(self):
        """Verifica e respeita rate limits"""
        current_time = time.time()

        if current_time > self.rate_limit_reset:
            self.rate_limit_calls = 0
            self.rate_limit_reset = current_time + 60

        if self.rate_limit_calls >= API_RATE_LIMIT_CALLS:
            sleep_time = self.rate_limit_reset - current_time
            if sleep_time > 0:
                print(f"⏳ Rate limit atingido. Aguardando {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                self.rate_limit_calls = 0
                self.rate_limit_reset = time.time() + 60

        self.rate_limit_calls += 1

    def search_crypto(self, query):
        """Busca criptomoedas por nome ou símbolo"""
        self._check_rate_limit()

        try:
            url = f"{COINGECKO_API_BASE}/search"
            params = {'query': query}

            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                data = response.json()
                coins = data.get('coins', [])

                results = []
                for coin in coins[:10]:  # Limita a 10 resultados
                    results.append({
                        'id': coin.get('id'),
                        'symbol': coin.get('symbol', '').upper(),
                        'name': coin.get('name'),
                        'market_cap_rank': coin.get('market_cap_rank')
                    })

                return results
            else:
                print(f"❌ Erro na busca: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Erro ao buscar criptomoeda: {e}")
            return []

    def get_crypto_info(self, crypto_id):
        """Obtém informações básicas de uma criptomoeda"""
        self._check_rate_limit()

        try:
            url = f"{COINGECKO_API_BASE}/coins/{crypto_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false'
            }

            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                data = response.json()

                info = {
                    'id': data.get('id'),
                    'symbol': data.get('symbol', '').upper(),
                    'name': data.get('name'),
                    'current_price': data.get('market_data', {}).get('current_price', {}).get('usd', 0),
                    'market_cap': data.get('market_data', {}).get('market_cap', {}).get('usd', 0),
                    'market_cap_rank': data.get('market_cap_rank'),
                    'total_volume': data.get('market_data', {}).get('total_volume', {}).get('usd', 0),
                    'price_change_24h': data.get('market_data', {}).get('price_change_percentage_24h', 0),
                    'description': data.get('description', {}).get('en', '')[:200] + '...'
                }

                return info
            else:
                print(f"❌ Erro ao obter informações: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Erro ao obter informações da criptomoeda: {e}")
            return None

    def get_historical_data_coingecko(self, crypto_id, days=365):
        """Coleta dados históricos via CoinGecko"""
        self._check_rate_limit()

        try:
            print(f"📊 Coletando dados históricos para {crypto_id} ({days} dias)...")

            url = f"{COINGECKO_API_BASE}/coins/{crypto_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily' if days > 90 else 'hourly'
            }

            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                data = response.json()

                # Processa dados
                prices = data.get('prices', [])
                volumes = data.get('total_volumes', [])
                market_caps = data.get('market_caps', [])

                if not prices:
                    print(f"❌ Nenhum dado de preço encontrado para {crypto_id}")
                    return None

                # Converte para DataFrame
                df_data = []
                for i, (timestamp, price) in enumerate(prices):
                    date = pd.to_datetime(timestamp, unit='ms')
                    volume = volumes[i][1] if i < len(volumes) else 0
                    market_cap = market_caps[i][1] if i < len(market_caps) else 0

                    df_data.append({
                        'date': date,
                        'price': price,
                        'volume': volume,
                        'market_cap': market_cap
                    })

                df = pd.DataFrame(df_data)
                df.set_index('date', inplace=True)
                df = df.sort_index()

                print(f"✅ Coletados {len(df)} registros para {crypto_id}")
                return df

            else:
                print(f"❌ Erro na API CoinGecko: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Erro ao coletar dados do CoinGecko: {e}")
            return None

    def get_historical_data_ccxt(self, symbol, exchange='binance', timeframe='1d', limit=365):
        """Coleta dados históricos via CCXT"""
        try:
            if exchange not in self.exchanges:
                print(f"❌ Exchange {exchange} não suportada")
                return None

            exchange_obj = self.exchanges[exchange]

            if not exchange_obj.has['fetchOHLCV']:
                print(f"❌ Exchange {exchange} não suporta OHLCV")
                return None

            print(f"📊 Coletando dados de {symbol} via {exchange}...")

            # Busca dados OHLCV
            ohlcv = exchange_obj.fetch_ohlcv(symbol, timeframe, limit=limit)

            if not ohlcv:
                print(f"❌ Nenhum dado encontrado para {symbol}")
                return None

            # Converte para DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('date', inplace=True)
            df.drop('timestamp', axis=1, inplace=True)

            # Renomeia colunas para padronizar
            df.rename(columns={'close': 'price'}, inplace=True)
            df['market_cap'] = 0  # CCXT não fornece market cap diretamente

            print(f"✅ Coletados {len(df)} registros para {symbol}")
            return df

        except Exception as e:
            print(f"❌ Erro ao coletar dados via CCXT: {e}")
            return None

    def get_historical_data_yfinance(self, symbol, period='1y'):
        """Coleta dados via yfinance (para cryptos listadas)"""
        try:
            print(f"📊 Tentando coletar {symbol} via yfinance...")

            # Adiciona sufixo USD se necessário
            if not symbol.endswith('-USD'):
                symbol = f"{symbol}-USD"

            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)

            if data.empty:
                print(f"❌ Nenhum dado encontrado para {symbol}")
                return None

            # Padroniza colunas
            df = pd.DataFrame()
            df['price'] = data['Close']
            df['volume'] = data['Volume']
            df['market_cap'] = 0  # yfinance não tem market cap direto

            print(f"✅ Coletados {len(df)} registros para {symbol}")
            return df

        except Exception as e:
            print(f"❌ Erro ao coletar dados via yfinance: {e}")
            return None

    def collect_crypto_data(self, crypto_id, days=365, methods=['coingecko', 'ccxt', 'yfinance']):
        """Coleta dados usando múltiplos métodos como fallback"""
        print(f"\n🎯 Iniciando coleta para {crypto_id}")

        # Tenta CoinGecko primeiro (mais confiável)
        if 'coingecko' in methods:
            data = self.get_historical_data_coingecko(crypto_id, days)
            if data is not None and not data.empty:
                return data

        # Fallback para CCXT
        if 'ccxt' in methods:
            # Tenta diferentes símbolos e exchanges
            crypto_info = POPULAR_CRYPTOS.get(crypto_id, {})
            symbol = crypto_info.get('symbol', crypto_id.upper())

            for exchange in ['binance', 'coinbase', 'kraken']:
                for symbol_format in [f"{symbol}/USDT", f"{symbol}/USD", f"{symbol}/BTC"]:
                    try:
                        data = self.get_historical_data_ccxt(symbol_format, exchange, limit=days)
                        if data is not None and not data.empty:
                            return data
                    except:
                        continue

        # Fallback para yfinance
        if 'yfinance' in methods:
            crypto_info = POPULAR_CRYPTOS.get(crypto_id, {})
            symbol = crypto_info.get('symbol', crypto_id.upper())

            data = self.get_historical_data_yfinance(symbol)
            if data is not None and not data.empty:
                return data

        print(f"❌ Não foi possível coletar dados para {crypto_id}")
        return None

    def save_data(self, data, filename):
        """Salva dados em CSV"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        filepath = os.path.join(DATA_DIR, filename)
        data.to_csv(filepath)
        print(f"💾 Dados salvos em: {filepath}")

    def load_data(self, filename):
        """Carrega dados de CSV"""
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            return pd.read_csv(filepath, index_col=0, parse_dates=True)
        return None

def main():
    """Função principal para teste"""
    collector = UniversalCryptoCollector()

    # Teste de busca
    print("🔍 Testando busca...")
    results = collector.search_crypto("bitcoin")
    for result in results[:3]:
        print(f"  • {result['name']} ({result['symbol']}) - ID: {result['id']}")

    # Teste de coleta
    print("\n📊 Testando coleta de dados...")
    data = collector.collect_crypto_data('bitcoin', days=30)
    if data is not None:
        print(f"✅ Dados coletados: {len(data)} registros")
        print(data.head())

if __name__ == "__main__":
    main()
