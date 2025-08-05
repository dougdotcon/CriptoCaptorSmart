# 🔥 CriptoCaptorSmart CYBERPUNK TERMINAL 🔥

## 🎯 Visão Geral

Sistema universal de análise de criptomoedas com interface terminal cyberpunk. Analise qualquer criptomoeda com indicadores técnicos avançados, correlações e insights em tempo real.

## ✨ Características Cyberpunk

### 🎨 Interface Terminal Futurística
- **Banner ASCII animado** com arte cyberpunk
- **Cores neon** (ciano, verde, amarelo, magenta, vermelho)
- **Animações de carregamento** com caracteres especiais
- **Menus estilizados** com bordas ASCII
- **Feedback visual** para todas as operações

### 🚀 Funcionalidades Universais
- **Busca de qualquer criptomoeda** via múltiplas APIs
- **Análise técnica completa** (RSI, MACD, Bollinger Bands, etc.)
- **Análise de correlação** entre duas criptomoedas
- **Identificação de ciclos** de mercado (bull/bear)
- **Criptomoedas populares** pré-configuradas
- **Dashboard cyberpunk** (em desenvolvimento)

## 🛠️ Instalação

### 1. Método Automático (Recomendado)
```bash
python start_crypto_cyberpunk.py
```
O script irá verificar e instalar automaticamente todas as dependências necessárias.

### 2. Método Manual
```bash
pip install -r requirements.txt
python cyberpunk_crypto_terminal.py
```

### 3. Windows (Batch)
```cmd
start_crypto_cyberpunk.bat
```

## 🎮 Como Usar

### 1. Inicialização
Execute o launcher:
```bash
python start_crypto_cyberpunk.py
```

### 2. Menu Principal
```
╔═══════════════════════════════════════════════════════════════════════════╗
║                           MENU PRINCIPAL                                 ║
╠═══════════════════════════════════════════════════════════════════════════╣
║ [1] ► BUSCAR CRIPTOMOEDAS                                                ║
║ [2] ► ANÁLISE INDIVIDUAL                                                 ║
║ [3] ► ANÁLISE COMPARATIVA                                                ║
║ [4] ► DASHBOARD CYBERPUNK                                                ║
║ [5] ► CRYPTOS POPULARES                                                  ║
║ [6] ► CONFIGURAÇÕES                                                      ║
║ [0] ► DESCONECTAR DO SISTEMA                                             ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 3. Fluxo de Análise
1. **Busque uma criptomoeda** (opção 1) ou **selecione uma popular** (opção 5)
2. **Execute análise individual** (opção 2) para indicadores técnicos
3. **Compare duas cryptos** (opção 3) para análise de correlação
4. **Visualize no dashboard** (opção 4) para gráficos interativos

## 📊 Análises Disponíveis

### 🔍 Análise Individual
- **Performance**: Retorno total, anualizado, volatilidade, Sharpe ratio
- **Indicadores Técnicos**: RSI, MACD, Bollinger Bands, médias móveis
- **Suporte/Resistência**: Níveis técnicos importantes
- **Ciclos de Mercado**: Identificação de bull/bear markets

### 🔗 Análise Comparativa
- **Correlação de Preços**: Correlação entre duas criptomoedas
- **Correlação de Retornos**: Análise de movimentos sincronizados
- **Análise de Lag**: Identificação de atrasos entre movimentos
- **Correlação Móvel**: Evolução da correlação ao longo do tempo

## 🌐 APIs Suportadas

### 📡 Fontes de Dados
- **CoinGecko API**: Dados históricos completos e informações de mercado
- **CCXT**: Dados de exchanges em tempo real (Binance, Coinbase, Kraken)
- **yfinance**: Dados de criptomoedas listadas em bolsas tradicionais

### 🔄 Sistema de Fallback
O sistema tenta múltiplas fontes automaticamente:
1. **CoinGecko** (principal) - Dados históricos confiáveis
2. **CCXT** (fallback) - Dados de exchanges
3. **yfinance** (fallback) - Para cryptos listadas

## 💎 Criptomoedas Pré-Configuradas

- **Bitcoin (BTC)** - A criptomoeda original
- **Ethereum (ETH)** - Plataforma de contratos inteligentes
- **QAN Platform (QANX)** - Blockchain quantum-resistente
- **Cardano (ADA)** - Blockchain de terceira geração
- **Solana (SOL)** - Blockchain de alta performance
- **Polkadot (DOT)** - Interoperabilidade entre blockchains
- **Chainlink (LINK)** - Oráculos descentralizados
- **Polygon (MATIC)** - Solução de escalabilidade Ethereum

## 🎨 Visual Cyberpunk

### 🌈 Esquema de Cores
- **Verde Matrix** (#00FF41) - Sucesso e dados positivos
- **Rosa Neon** (#FF0080) - Alertas e destaques
- **Ciano** (#00D4FF) - Informações e navegação
- **Dourado** (#FFD700) - Avisos importantes
- **Vermelho** (#FF4444) - Erros e dados negativos

### 🎭 Elementos Visuais
- **Bordas ASCII** estilizadas
- **Animações de loading** com caracteres especiais
- **Símbolos cyberpunk** (▓▒░, ►, ✓, ✗, ⚠, ℹ)
- **Banner ASCII** personalizado

## 🔧 Arquitetura do Sistema

### 📁 Estrutura de Arquivos
```
CriptoCaptorSmart/
├── start_crypto_cyberpunk.py      # 🚀 Launcher principal
├── start_crypto_cyberpunk.bat     # 🪟 Launcher Windows
├── cyberpunk_crypto_terminal.py   # 🎮 Interface cyberpunk
├── crypto_config.py               # ⚙️ Configurações centralizadas
├── crypto_data_collector.py       # 📊 Coletor universal de dados
├── crypto_analyzer_universal.py   # 🔍 Analisador universal
├── requirements.txt               # 📦 Dependências
├── data/                          # 💾 Dados coletados
├── charts/                        # 📈 Gráficos gerados
├── logs/                          # 📝 Logs do sistema
└── cache/                         # 🗄️ Cache temporário
```

### 🧩 Módulos Principais
- **Terminal Interface**: Interface cyberpunk com menus ASCII
- **Data Collector**: Coleta dados de múltiplas APIs
- **Universal Analyzer**: Análise técnica e correlações
- **Config Manager**: Configurações centralizadas
- **Cache System**: Sistema de cache para performance

## ⚡ Performance e Otimizações

### 🚀 Características de Performance
- **Cache inteligente** - Evita requests desnecessários
- **Rate limiting** - Respeita limites das APIs
- **Fallback automático** - Múltiplas fontes de dados
- **Processamento assíncrono** - Para operações longas
- **Memória otimizada** - Interface terminal leve

### 📊 Capacidades
- **Análise de até 2000 dias** de dados históricos
- **Múltiplas criptomoedas** simultaneamente
- **Indicadores técnicos** em tempo real
- **Correlações complexas** com análise de lag

## 🔐 Configurações Avançadas

### 🎛️ Parâmetros Configuráveis
- **Janelas de análise**: Correlação, volatilidade, tendências
- **Thresholds**: Bull/bear market, correlações altas/baixas
- **Timeouts**: Requests, conexões, cache
- **Rate limits**: Controle de chamadas às APIs

### 🌍 Variáveis de Ambiente
```bash
COINGECKO_API_KEY=sua_chave_aqui
COINMARKETCAP_API_KEY=sua_chave_aqui
```

## 🚀 Próximas Funcionalidades

- [ ] **Dashboard Web Cyberpunk** - Interface web com visual futurístico
- [ ] **Análise de Portfolio** - Gestão de carteira de criptomoedas
- [ ] **Alertas em Tempo Real** - Notificações de preços e indicadores
- [ ] **Backtesting** - Teste de estratégias históricas
- [ ] **Machine Learning** - Predições baseadas em IA
- [ ] **API REST** - Integração com outros sistemas
- [ ] **Mobile App** - Aplicativo móvel cyberpunk

## 🎯 Casos de Uso

### 📈 Para Traders
- Análise técnica completa de qualquer criptomoeda
- Identificação de correlações entre ativos
- Sinais de entrada/saída baseados em indicadores

### 🔬 Para Pesquisadores
- Análise de correlações entre criptomoedas
- Identificação de padrões de mercado
- Dados históricos para estudos acadêmicos

### 💼 Para Investidores
- Análise de performance de longo prazo
- Identificação de ciclos de mercado
- Diversificação baseada em correlações

## 🔥 Comandos Rápidos

### Iniciar Sistema
```bash
python start_crypto_cyberpunk.py
```

### Análise Rápida (exemplo)
1. Execute o sistema
2. Digite `5` (Cryptos Populares)
3. Selecione Bitcoin (`1`)
4. Digite `2` (Análise Individual)
5. Selecione Bitcoin (`1`)
6. Digite `365` (dias de histórico)

### Comparação Rápida (exemplo)
1. Selecione Bitcoin e Ethereum
2. Digite `3` (Análise Comparativa)
3. Veja correlações e padrões

## 🎨 Personalização

A interface pode ser facilmente personalizada modificando:
- **Cores** no arquivo `crypto_config.py`
- **Arte ASCII** nos banners
- **Animações** de carregamento
- **Símbolos** cyberpunk
- **Thresholds** de análise

## 🆘 Solução de Problemas

### ❌ Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 🌐 Erro de Conexão
- Verifique sua conexão com a internet
- Algumas APIs podem ter rate limits
- Tente novamente após alguns minutos

### 📊 Dados Não Encontrados
- Verifique se o nome/símbolo da criptomoeda está correto
- Algumas cryptos podem não ter dados históricos suficientes
- Tente uma criptomoeda mais popular

## 🎯 Conclusão

O **CriptoCaptorSmart Cyberpunk Terminal** oferece uma experiência única e moderna para análise de criptomoedas, combinando funcionalidade avançada com um visual futurístico impressionante.

**Bem-vindo ao futuro da análise de criptomoedas! 🔥**

---

*Desenvolvido com 💚 para a comunidade crypto*

### 2. Ciclos do Bitcoin
- Identificação de bull/bear markets
- Performance do QANX em diferentes ciclos
- Análise de timing entre movimentos

### 3. Teste da Teoria de Manipulação
- Comportamento do QANX após grandes movimentos do BTC
- Análise estatística de significância
- Padrões de volume durante movimentos

### 4. Métricas de Performance
- Retorno total e anualizado
- Volatilidade
- Sharpe ratio
- Maximum drawdown
- Win rate

## Dashboard

O dashboard web inclui:

- **Cards de Métricas**: Correlação atual, preços, período de análise
- **Gráfico de Preços**: Evolução temporal normalizada e absoluta
- **Correlação Móvel**: Evolução da correlação ao longo do tempo
- **Retornos Diários**: Comparação de volatilidade
- **Análise de Volume**: Padrões de negociação
- **Scatter Plot**: Correlação visual de retornos
- **Insights Automáticos**: Conclusões baseadas na análise

### Controles Interativos
- Seletor de período de análise
- Ajuste da janela de correlação móvel
- Filtros por data

## Acesso ao Dashboard

Após iniciar o dashboard, acesse:
```
http://127.0.0.1:8050
```

## APIs Utilizadas

- **CoinGecko API**: Dados históricos gratuitos
- Limite de rate: ~50 requests/minuto
- Dados disponíveis: preço, volume, market cap

## Dependências Principais

- `pandas`: Manipulação de dados
- `numpy`: Cálculos numéricos
- `plotly`: Gráficos interativos
- `dash`: Framework web
- `scipy`: Análise estatística
- `requests`: Requisições HTTP

## Resultados Esperados

A análise fornecerá:

1. **Correlação Quantificada**: Grau de correlação entre QANX e BTC
2. **Evidência da Teoria**: Testes estatísticos da hipótese de manipulação
3. **Padrões Temporais**: Identificação de lags e ciclos
4. **Insights Acionáveis**: Conclusões para estratégias de trading

## Limitações

- Dados limitados pela disponibilidade da API
- Correlação não implica causalidade
- Mercado de criptomoedas é altamente volátil
- Análise baseada apenas em dados de preço/volume

## Próximos Passos

- Integração com mais exchanges
- Análise de dados on-chain
- Machine learning para predição
- Alertas automáticos de correlação

## Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme conexão com internet para APIs
3. Verifique logs de erro no terminal
