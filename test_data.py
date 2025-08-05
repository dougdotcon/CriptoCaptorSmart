"""
Script para testar se os dados estão sendo carregados corretamente
"""

from analyzer import QANXBTCAnalyzer
import pandas as pd

def test_data():
    print("=== TESTE DE DADOS ===")
    
    # Carrega dados
    analyzer = QANXBTCAnalyzer()
    analyzer.load_data()
    
    print(f"Dados carregados: {len(analyzer.merged_data)} registros")
    print(f"Período: {analyzer.merged_data.index.min()} a {analyzer.merged_data.index.max()}")
    print(f"Colunas: {list(analyzer.merged_data.columns)}")
    
    # Mostra primeiros registros
    print("\n=== PRIMEIROS 5 REGISTROS ===")
    print(analyzer.merged_data.head())
    
    # Mostra últimos registros
    print("\n=== ÚLTIMOS 5 REGISTROS ===")
    print(analyzer.merged_data.tail())
    
    # Estatísticas básicas
    print("\n=== ESTATÍSTICAS BÁSICAS ===")
    print(analyzer.merged_data.describe())
    
    # Verifica se há dados nulos
    print("\n=== DADOS NULOS ===")
    print(analyzer.merged_data.isnull().sum())
    
    return analyzer.merged_data

if __name__ == "__main__":
    data = test_data()
