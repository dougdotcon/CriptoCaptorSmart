#!/usr/bin/env python3
"""
🔥 CriptoCaptorSmart CYBERPUNK TERMINAL 🔥
Interface Terminal Cyberpunk ASCII para Análise Universal de Criptomoedas
"""

import os
import sys
import time
import threading
from datetime import datetime
import colorama
from colorama import Fore, Back, Style
import pyfiglet
from tqdm import tqdm

from crypto_config import (
    CYBERPUNK_COLORS, CYBERPUNK_SYMBOLS, POPULAR_CRYPTOS,
    ANIMATION_SPEED, LOADING_FRAMES, ensure_directories
)
from crypto_data_collector import UniversalCryptoCollector
from crypto_analyzer_universal import UniversalCryptoAnalyzer

# Inicializar colorama para Windows
colorama.init()

class CryptoCaptorTerminal:
    def __init__(self):
        self.running = True
        self.current_operation = None
        self.collector = UniversalCryptoCollector()
        self.analyzer = UniversalCryptoAnalyzer()
        self.selected_cryptos = []
        self.analysis_data = {}

        # Garante que diretórios existem
        ensure_directories()

    def clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        """Exibe o banner cyberpunk ASCII"""
        self.clear_screen()

        # Banner principal
        banner = pyfiglet.figlet_format("CRYPTO", font="slant")
        print(f"{Fore.CYAN}{Style.BRIGHT}{banner}{Style.RESET_ALL}")

        # Subtítulo cyberpunk
        print(f"{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    ▓▓▓ CriptoCaptorSmart CYBERPUNK TERMINAL v2.0 ▓▓▓{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}")

        # Arte ASCII cyberpunk
        ascii_art = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║   ██████╗██████╗ ██╗██████╗ ████████╗ ██████╗                            ║
    ║  ██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██╔═══██╗                           ║
    ║  ██║     ██████╔╝██║██████╔╝   ██║   ██║   ██║                           ║
    ║  ██║     ██╔══██╗██║██╔═══╝    ██║   ██║   ██║                           ║
    ║  ╚██████╗██║  ██║██║██║        ██║   ╚██████╔╝                           ║
    ║   ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝    ╚═════╝                            ║
    ║                    Universal Crypto Analysis System                      ║
    ╚══════════════════════════════════════════════════════════════════════════╝
        """
        print(f"{Fore.MAGENTA}{ascii_art}{Style.RESET_ALL}")

        # Status do sistema
        print(f"{Fore.GREEN}[SISTEMA ONLINE]{Style.RESET_ALL} {Fore.CYAN}Neural Network Activated{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[CONEXÃO]{Style.RESET_ALL} {Fore.CYAN}Crypto Matrix Interface Ready{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[TIMESTAMP]{Style.RESET_ALL} {Fore.YELLOW}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'═' * 80}{Style.RESET_ALL}")

    def print_menu(self):
        """Exibe o menu principal cyberpunk"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                           MENU PRINCIPAL                                 ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[1]{Style.RESET_ALL} {Fore.YELLOW}► BUSCAR CRIPTOMOEDAS{Style.RESET_ALL}                                      {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[2]{Style.RESET_ALL} {Fore.YELLOW}► ANÁLISE INDIVIDUAL{Style.RESET_ALL}                                       {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[3]{Style.RESET_ALL} {Fore.YELLOW}► ANÁLISE COMPARATIVA{Style.RESET_ALL}                                     {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[4]{Style.RESET_ALL} {Fore.YELLOW}► DASHBOARD CYBERPUNK{Style.RESET_ALL}                                     {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[5]{Style.RESET_ALL} {Fore.YELLOW}► CRYPTOS POPULARES{Style.RESET_ALL}                                       {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}[6]{Style.RESET_ALL} {Fore.YELLOW}► CONFIGURAÇÕES{Style.RESET_ALL}                                           {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.RED}[0]{Style.RESET_ALL} {Fore.RED}► DESCONECTAR DO SISTEMA{Style.RESET_ALL}                                   {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

    def get_user_input(self, prompt, input_type="string"):
        """Obtém entrada do usuário com estilo cyberpunk"""
        while True:
            try:
                print(f"\n{Fore.GREEN}┌─[{Fore.CYAN}CRYPTO{Fore.GREEN}]─[{Fore.YELLOW}INPUT{Fore.GREEN}]{Style.RESET_ALL}")
                user_input = input(f"{Fore.GREEN}└──╼ {Fore.CYAN}{prompt}{Style.RESET_ALL} {Fore.GREEN}►{Style.RESET_ALL} ")

                if input_type == "int":
                    return int(user_input)
                elif input_type == "choice":
                    if user_input in ['0', '1', '2', '3', '4', '5', '6']:
                        return user_input
                    else:
                        self.print_error("Opção inválida! Digite 0, 1, 2, 3, 4, 5 ou 6.")
                        continue
                else:
                    return user_input.strip()
            except ValueError:
                self.print_error(f"Entrada inválida! Digite um {input_type} válido.")
            except KeyboardInterrupt:
                self.print_warning("\nOperação cancelada pelo usuário.")
                return None

    def print_success(self, message):
        """Exibe mensagem de sucesso"""
        print(f"\n{Fore.GREEN}[{CYBERPUNK_SYMBOLS['success']} SUCESSO]{Style.RESET_ALL} {Fore.WHITE}{message}{Style.RESET_ALL}")

    def print_error(self, message):
        """Exibe mensagem de erro"""
        print(f"\n{Fore.RED}[{CYBERPUNK_SYMBOLS['error']} ERRO]{Style.RESET_ALL} {Fore.WHITE}{message}{Style.RESET_ALL}")

    def print_warning(self, message):
        """Exibe mensagem de aviso"""
        print(f"\n{Fore.YELLOW}[{CYBERPUNK_SYMBOLS['warning']} AVISO]{Style.RESET_ALL} {Fore.WHITE}{message}{Style.RESET_ALL}")

    def print_info(self, message):
        """Exibe mensagem informativa"""
        print(f"\n{Fore.CYAN}[{CYBERPUNK_SYMBOLS['info']} INFO]{Style.RESET_ALL} {Fore.WHITE}{message}{Style.RESET_ALL}")

    def loading_animation(self, message, duration=2):
        """Animação de carregamento cyberpunk"""
        frames = ['▓', '▒', '░', '▒']

        for i in range(int(duration / ANIMATION_SPEED)):
            frame = frames[i % len(frames)]
            print(f"\r{Fore.CYAN}[{frame * 3}]{Style.RESET_ALL} {Fore.YELLOW}{message}{Style.RESET_ALL} {Fore.CYAN}[{frame * 3}]{Style.RESET_ALL}", end='', flush=True)
            time.sleep(ANIMATION_SPEED)

        print(f"\r{Fore.GREEN}[{CYBERPUNK_SYMBOLS['success']}]{Style.RESET_ALL} {Fore.WHITE}{message} - Concluído!{Style.RESET_ALL}")

    def search_cryptos(self):
        """Busca criptomoedas"""
        self.print_banner()
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                         BUSCAR CRIPTOMOEDAS                               ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        query = self.get_user_input("Digite o nome ou símbolo da criptomoeda")
        if not query:
            return

        self.loading_animation("Buscando criptomoedas", 2)

        results = self.collector.search_crypto(query)

        if not results:
            self.print_error("Nenhuma criptomoeda encontrada!")
            input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            return

        print(f"\n{Fore.GREEN}Resultados encontrados:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")

        for i, crypto in enumerate(results, 1):
            rank = f"#{crypto['market_cap_rank']}" if crypto['market_cap_rank'] else "N/A"
            print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {Fore.YELLOW}{crypto['name']}{Style.RESET_ALL} ({Fore.CYAN}{crypto['symbol']}{Style.RESET_ALL}) - Rank: {rank}")
            print(f"    ID: {crypto['id']}")

        print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")

        choice = self.get_user_input("Selecione uma opção (número) ou ENTER para voltar")
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                selected = results[idx]
                self.print_success(f"Selecionado: {selected['name']} ({selected['symbol']})")
                self.selected_cryptos.append(selected)

        input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")

    def show_popular_cryptos(self):
        """Mostra criptomoedas populares"""
        self.print_banner()
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        CRIPTOMOEDAS POPULARES                             ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}Criptomoedas pré-configuradas:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")

        for i, (crypto_id, info) in enumerate(POPULAR_CRYPTOS.items(), 1):
            print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {Fore.YELLOW}{info['name']}{Style.RESET_ALL} ({Fore.CYAN}{info['symbol']}{Style.RESET_ALL})")
            print(f"    ID: {crypto_id}")

        print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")

        choice = self.get_user_input("Selecione uma opção (número) ou ENTER para voltar")
        if choice and choice.isdigit():
            idx = int(choice) - 1
            crypto_list = list(POPULAR_CRYPTOS.items())
            if 0 <= idx < len(crypto_list):
                crypto_id, info = crypto_list[idx]
                selected = {
                    'id': crypto_id,
                    'name': info['name'],
                    'symbol': info['symbol'],
                    'market_cap_rank': None
                }
                self.print_success(f"Selecionado: {info['name']} ({info['symbol']})")
                self.selected_cryptos.append(selected)

        input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")

    def individual_analysis(self):
        """Análise individual de criptomoeda"""
        if not self.selected_cryptos:
            self.print_warning("Nenhuma criptomoeda selecionada! Use a opção 1 ou 5 primeiro.")
            input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            return

        self.print_banner()
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                         ANÁLISE INDIVIDUAL                               ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        # Lista cryptos selecionadas
        print(f"\n{Fore.GREEN}Criptomoedas selecionadas:{Style.RESET_ALL}")
        for i, crypto in enumerate(self.selected_cryptos, 1):
            print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {crypto['name']} ({crypto['symbol']})")

        choice = self.get_user_input("Selecione qual analisar (número)")
        if not choice or not choice.isdigit():
            return

        idx = int(choice) - 1
        if not (0 <= idx < len(self.selected_cryptos)):
            self.print_error("Opção inválida!")
            return

        crypto = self.selected_cryptos[idx]

        # Coleta dados
        self.loading_animation(f"Coletando dados de {crypto['name']}", 3)

        days = self.get_user_input("Quantos dias de histórico? (padrão: 365)", "string")
        days = int(days) if days.isdigit() else 365

        data = self.collector.collect_crypto_data(crypto['id'], days)

        if data is None or data.empty:
            self.print_error("Não foi possível coletar dados!")
            input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            return

        # Análise
        self.loading_animation("Executando análise", 2)

        self.analyzer.load_data(data, crypto1_name=crypto['name'])
        results = self.analyzer.analyze_single_crypto()

        # Exibe resultados
        self.show_analysis_results(crypto['name'], results)

    def show_analysis_results(self, crypto_name, results):
        """Exibe resultados da análise"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                    RESULTADOS DA ANÁLISE - {crypto_name:<20}           ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        perf = results['performance']
        tech = results['technical']

        print(f"\n{Fore.YELLOW}📊 PERFORMANCE:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Preço Atual: ${perf['current_price']:.4f}")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Retorno Total: {perf['total_return']:.2f}%")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Retorno Anualizado: {perf['annualized_return']:.2f}%")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Volatilidade: {perf['volatility']:.2f}%")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Max Drawdown: {perf['max_drawdown']:.2f}%")

        print(f"\n{Fore.YELLOW}🔧 ANÁLISE TÉCNICA:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} RSI: {tech['rsi']:.1f} ({tech['rsi_signal']})")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} MACD: {tech['macd_signal']}")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Bollinger Bands: {tech['bb_position']}")
        print(f"  {Fore.GREEN}►{Style.RESET_ALL} Tendência: {tech['trend']}")

        input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")

    def run(self):
        """Loop principal da interface"""
        while self.running:
            self.print_banner()
            self.print_menu()

            choice = self.get_user_input("Selecione uma opção", "choice")

            if choice == "1":
                self.search_cryptos()
            elif choice == "2":
                self.individual_analysis()
            elif choice == "3":
                self.print_info("Análise comparativa em desenvolvimento...")
                input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            elif choice == "4":
                self.print_info("Dashboard cyberpunk em desenvolvimento...")
                input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            elif choice == "5":
                self.show_popular_cryptos()
            elif choice == "6":
                self.print_info("Configurações em desenvolvimento...")
                input(f"\n{Fore.YELLOW}Pressione ENTER para continuar...{Style.RESET_ALL}")
            elif choice == "0":
                self.print_success("Desconectando do sistema...")
                self.loading_animation("Finalizando conexões", 2)
                self.running = False
            elif choice is None:
                continue

def main():
    """Função principal"""
    try:
        terminal = CryptoCaptorTerminal()
        terminal.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Sistema interrompido pelo usuário.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n\n{Fore.RED}Erro inesperado: {e}{Style.RESET_ALL}")
    finally:
        print(f"\n{Fore.CYAN}Obrigado por usar o CriptoCaptorSmart! 🔥{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
