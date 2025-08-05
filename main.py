"""
Script principal para executar a análise completa QANX vs BTC
"""

import os
import sys
from datetime import datetime
import argparse

def main():
    parser = argparse.ArgumentParser(description='Análise QANX vs BTC')
    parser.add_argument('--collect', action='store_true', help='Coletar dados históricos')
    parser.add_argument('--analyze', action='store_true', help='Executar análise')
    parser.add_argument('--dashboard', action='store_true', help='Iniciar dashboard')
    parser.add_argument('--all', action='store_true', help='Executar tudo')
    
    args = parser.parse_args()
    
    if args.all:
        args.collect = True
        args.analyze = True
        args.dashboard = True
    
    if not any([args.collect, args.analyze, args.dashboard]):
        print("Uso: python main.py [--collect] [--analyze] [--dashboard] [--all]")
        return
    
    print("=== ANÁLISE QANX vs BTC ===")
    print(f"Iniciado em: {datetime.now()}")
    print()
    
    # 1. Coleta de dados
    if args.collect:
        print("1. Coletando dados históricos...")
        try:
            from data_collector import main as collect_data
            collect_data()
            print("✓ Dados coletados com sucesso!")
        except Exception as e:
            print(f"✗ Erro na coleta de dados: {e}")
            return
        print()
    
    # 2. Análise
    if args.analyze:
        print("2. Executando análise...")
        try:
            from analyzer import main as analyze_data
            analyzer = analyze_data()
            print("✓ Análise concluída com sucesso!")
        except Exception as e:
            print(f"✗ Erro na análise: {e}")
            return
        print()
    
    # 3. Dashboard
    if args.dashboard:
        print("3. Iniciando dashboard...")
        print("Dashboard será aberto em: http://127.0.0.1:8050")
        print("Pressione Ctrl+C para parar o servidor")
        try:
            from dashboard import app
            app.run_server(host='127.0.0.1', port=8050, debug=False)
        except KeyboardInterrupt:
            print("\n✓ Dashboard encerrado pelo usuário")
        except Exception as e:
            print(f"✗ Erro no dashboard: {e}")

if __name__ == "__main__":
    main()
