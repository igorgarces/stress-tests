import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

# Configuração de seletores para o fluxo completo
SELECTORS_CONFIG = {
    "login": {
        "username_field": "#root > div.login-container.fadeIn > div.form-container > div.bg-secondary.border-0.mb-0.card > div.px-lg-5.py-lg-5.card-body > form > div.mb-3.focused.form-group > div > input",
        "password_field": "#root > div.login-container.fadeIn > div.form-container > div.bg-secondary.border-0.mb-0.card > div.px-lg-5.py-lg-5.card-body > form > div:nth-child(2) > div > input", 
        "login_button": "#root > div.login-container.fadeIn > div.form-container > div.bg-secondary.border-0.mb-0.card > div.px-lg-5.py-lg-5.card-body > form > div.text-center > button"
    },
    "navigation": {
        "relatorios_menu": "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[6]/a",
        "callcenter_submenu": "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[6]/div/ul/li[1]/a",
        "pausas_option": "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[6]/div/ul/li[1]/div/ul/li[4]/a"
    },
    "reports": {
        "buscar_button": "//*[@id=\"root\"]/div[2]/div/div[1]/div[2]/div/div/div/div/div[2]/form/button",
        "baixar_relatorio": "//*[@id=\"root\"]/div[2]/div/div[1]/div[2]/div/div/div/div/div[2]/form/div[6]/div[2]/button[1]"
    }
}


class PausasReportStressTester:
    """
    Teste de stress para relatórios de pausas
    Versão profissional com métricas detalhadas
    """
    
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.results = []
        
    def setup_driver(self):
        """Configura o driver do Chrome com otimizações para performance"""
        print("Configurando navegador...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            print("Modo headless ativado")
        else:
            print("Modo com visualizacao ativado - navegador visivel")
            
        # Otimizações para performance
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        
        # Configurações de download para evitar diálogos
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "/tmp/downloads",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            print("Navegador configurado com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao configurar navegador: {e}")
            return False
    
    def login(self, url, username, password):
        """Processo de login"""
        print("Executando login...")
        
        try:
            self.driver.get(url)
            time.sleep(2)
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS_CONFIG["login"]["username_field"]))
            )
            
            password_field = self.driver.find_element(By.CSS_SELECTOR, SELECTORS_CONFIG["login"]["password_field"])
            login_button = self.driver.find_element(By.CSS_SELECTOR, SELECTORS_CONFIG["login"]["login_button"])
            
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()
            
            time.sleep(3)
            
            print("Login realizado com sucesso")
            return True
            
        except Exception as e:
            print(f"Erro no login: {e}")
            raise

    def navigate_to_pausas_reports(self):
        """Navega para o fluxo de relatórios de pausas"""
        print("Navegando para relatorios de pausas...")
        
        try:
            # Clicar em "Relatorios"
            print("Clicando em 'Relatorios'...")
            relatorios_menu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["relatorios_menu"]))
            )
            relatorios_menu.click()
            time.sleep(1)
            
            # Clicar em "CallCenter"
            print("Clicando em 'CallCenter'...")
            callcenter_submenu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["callcenter_submenu"]))
            )
            callcenter_submenu.click()
            time.sleep(1)
            
            # Clicar em "Pausas"
            print("Clicando em 'Pausas'...")
            pausas_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["pausas_option"]))
            )
            pausas_option.click()
            time.sleep(3)
            
            print("Navegacao para relatorios de pausas concluida")
            return True
            
        except Exception as e:
            print(f"Erro ao navegar para relatorios de pausas: {e}")
            raise

    def execute_search_cycle(self, cycle_number):
        """
        Executa um ciclo completo: Buscar -> Baixar Relatorio
        """
        print(f"Ciclo {cycle_number}: Executando busca e download...")
        
        cycle_results = {
            "cycle": cycle_number,
            "search_success": False,
            "download_success": False,
            "search_time": 0,
            "download_time": 0,
            "total_time": 0
        }
        
        cycle_start = time.time()
        
        try:
            # Passo 1: Clicar em Buscar
            print("  Clicando em 'Buscar'...")
            search_start = time.time()
            
            buscar_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["reports"]["buscar_button"]))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", buscar_btn)
            buscar_btn.click()
            
            # Aguardar resultados da busca
            time.sleep(2)
            
            cycle_results["search_time"] = time.time() - search_start
            cycle_results["search_success"] = True
            print("  Busca concluida com sucesso")
            
            # Passo 2: Clicar em Baixar Relatorio
            print("  Clicando em 'Baixar Relatorio'...")
            download_start = time.time()
            
            baixar_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["reports"]["baixar_relatorio"]))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", baixar_btn)
            baixar_btn.click()
            
            # Aguardar processamento do download
            time.sleep(1)
            
            cycle_results["download_time"] = time.time() - download_start
            cycle_results["download_success"] = True
            print("  Download concluido com sucesso")
            
        except Exception as e:
            print(f"  Erro no ciclo {cycle_number}: {e}")
            cycle_results["error"] = str(e)
        
        cycle_results["total_time"] = time.time() - cycle_start
        return cycle_results

    def stress_pausas_reports(self, num_cycles=20, delay_between_cycles=0.5):
        """
        Realiza múltiplos ciclos de busca e download de relatórios de pausas
        """
        print(f"Iniciando stress de relatorios de pausas: {num_cycles} ciclos")
        print(f"Delay entre ciclos: {delay_between_cycles}s")
        
        stress_results = {
            "total_cycles": num_cycles,
            "successful_cycles": 0,
            "failed_cycles": 0,
            "start_time": time.time(),
            "cycles": []
        }
        
        try:
            for cycle in range(num_cycles):
                print(f"Ciclo {cycle + 1}/{num_cycles}")
                
                cycle_result = self.execute_search_cycle(cycle + 1)
                stress_results["cycles"].append(cycle_result)
                
                if cycle_result["search_success"] and cycle_result["download_success"]:
                    stress_results["successful_cycles"] += 1
                    print(f"  Ciclo {cycle + 1} concluido em {cycle_result['total_time']:.2f}s")
                else:
                    stress_results["failed_cycles"] += 1
                    print(f"  Ciclo {cycle + 1} falhou")
                
                # Delay entre ciclos
                if cycle < num_cycles - 1:
                    time.sleep(delay_between_cycles)
            
            stress_results["total_time"] = time.time() - stress_results["start_time"]
            
            # Calcular métricas
            successful_times = [c["total_time"] for c in stress_results["cycles"] 
                              if c["search_success"] and c["download_success"]]
            
            if successful_times:
                stress_results["avg_cycle_time"] = sum(successful_times) / len(successful_times)
                stress_results["min_cycle_time"] = min(successful_times)
                stress_results["max_cycle_time"] = max(successful_times)
            else:
                stress_results["avg_cycle_time"] = 0
                stress_results["min_cycle_time"] = 0
                stress_results["max_cycle_time"] = 0
            
            print(f"\nResumo dos ciclos:")
            print(f"  Total de ciclos: {stress_results['total_cycles']}")
            print(f"  Ciclos bem-sucedidos: {stress_results['successful_cycles']}")
            print(f"  Ciclos com falha: {stress_results['failed_cycles']}")
            print(f"  Tempo total: {stress_results['total_time']:.2f}s")
            print(f"  Tempo medio por ciclo: {stress_results['avg_cycle_time']:.2f}s")
            
            return stress_results
            
        except Exception as e:
            print(f"Erro critico durante stress de relatorios: {e}")
            stress_results["error"] = str(e)
            return stress_results

    def execute_pausas_stress_test(self, url, username, password, num_cycles=20, delay_between_cycles=0.5):
        """
        Executa teste de stress completo para relatórios de pausas
        """
        print("INICIANDO TESTE DE STRESS - RELATORIOS DE PAUSAS")
        print("=" * 50)
        
        if not self.setup_driver():
            return {"success": False, "error": "Falha ao configurar navegador"}
        
        test_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_type": "pausas_report_stress_test",
            "total_time": 0,
            "steps": {},
            "stress_results": {},
            "success": True
        }
        
        test_start_time = time.time()
        
        try:
            # ETAPA 1: Login
            print("\nETAPA 1: LOGIN")
            step_start = time.time()
            self.login(url, username, password)
            test_results["steps"]["login"] = time.time() - step_start
            
            # ETAPA 2: Navegação para relatórios de pausas
            print("\nETAPA 2: NAVEGACAO PARA RELATORIOS DE PAUSAS")
            step_start = time.time()
            self.navigate_to_pausas_reports()
            test_results["steps"]["navigation"] = time.time() - step_start
            
            # ETAPA 3: Aguardar carregamento da página
            print("\nETAPA 3: AGUARDANDO CARREGAMENTO")
            time.sleep(3)
            
            # ETAPA 4: Stress de ciclos de busca e download
            print("\nETAPA 4: STRESS DE CICLOS")
            step_start = time.time()
            stress_results = self.stress_pausas_reports(num_cycles, delay_between_cycles)
            test_results["steps"]["stress_cycles"] = time.time() - step_start
            test_results["stress_results"] = stress_results
            
            test_results["total_time"] = time.time() - test_start_time
            print(f"\nTESTE DE STRESS CONCLUIDO EM {test_results['total_time']:.2f}s")
            
        except Exception as e:
            print(f"Erro no teste de stress: {e}")
            test_results["success"] = False
            test_results["error"] = str(e)
        
        finally:
            if self.driver:
                self.driver.quit()
        
        self.results.append(test_results)
        return test_results

    def advanced_pausas_stress_test(self, url, username, password, num_executions=5, num_cycles=20, delay_between_cycles=0.5):
        """
        Teste de stress avançado com múltiplas execuções
        """
        print(f"TESTE DE STRESS AVANCADO - {num_executions} EXECUCOES")
        print("=" * 50)
        
        all_results = []
        start_time = time.time()
        
        for execution in range(num_executions):
            print(f"\nExecucao {execution + 1}/{num_executions}")
            print("-" * 30)
            
            result = self.execute_pausas_stress_test(
                url=url,
                username=username,
                password=password,
                num_cycles=num_cycles,
                delay_between_cycles=delay_between_cycles
            )
            
            all_results.append(result)
            
            # Pausa entre execuções
            if execution < num_executions - 1:
                pause_time = random.uniform(3, 5)
                print(f"Aguardando {pause_time:.1f} segundos antes da proxima execucao...")
                time.sleep(pause_time)
        
        total_test_time = time.time() - start_time
        self._generate_pausas_stress_summary(all_results, total_test_time)
        return all_results

    def _generate_pausas_stress_summary(self, results, total_test_time):
        """Gera relatório detalhado do teste de stress"""
        print("\n" + "=" * 70)
        print("RELATORIO DETALHADO - TESTE DE STRESS DE RELATORIOS DE PAUSAS")
        print("=" * 70)
        
        successful_tests = [r for r in results if r["success"]]
        failed_tests = [r for r in results if not r["success"]]
        
        print(f"Tempo total do teste: {total_test_time:.2f}s")
        print(f"Execucoes realizadas: {len(results)}")
        print(f"Testes bem-sucedidos: {len(successful_tests)}")
        print(f"Testes com falha: {len(failed_tests)}")
        print(f"Taxa de sucesso: {(len(successful_tests) / len(results)) * 100:.1f}%")
        
        if successful_tests:
            # Estatísticas dos ciclos
            total_cycles_attempted = 0
            total_successful_cycles = 0
            total_failed_cycles = 0
            all_cycle_times = []
            
            for test in successful_tests:
                if "stress_results" in test:
                    sr = test["stress_results"]
                    total_cycles_attempted += sr["total_cycles"]
                    total_successful_cycles += sr["successful_cycles"]
                    total_failed_cycles += sr["failed_cycles"]
                    
                    # Coletar tempos dos ciclos bem-sucedidos
                    for cycle in sr["cycles"]:
                        if cycle["search_success"] and cycle["download_success"]:
                            all_cycle_times.append(cycle["total_time"])
            
            print(f"\nESTATISTICAS DOS CICLOS:")
            print(f"  Total de ciclos executados: {total_cycles_attempted}")
            print(f"  Ciclos bem-sucedidos: {total_successful_cycles}")
            print(f"  Ciclos com falha: {total_failed_cycles}")
            print(f"  Taxa de sucesso: {(total_successful_cycles / total_cycles_attempted) * 100:.1f}%")
            
            if all_cycle_times:
                avg_cycle_time = sum(all_cycle_times) / len(all_cycle_times)
                max_cycle_time = max(all_cycle_times)
                min_cycle_time = min(all_cycle_times)
                
                print(f"  Tempo medio por ciclo: {avg_cycle_time:.2f}s")
                print(f"  Tempo mais rapido: {min_cycle_time:.2f}s")
                print(f"  Tempo mais lento: {max_cycle_time:.2f}s")
            
            # Análise de performance por etapa
            if "steps" in successful_tests[0]:
                steps_analysis = {}
                for step_name in successful_tests[0]["steps"]:
                    step_times = [test["steps"][step_name] for test in successful_tests if step_name in test["steps"]]
                    if step_times:
                        steps_analysis[step_name] = {
                            "avg": sum(step_times) / len(step_times),
                            "min": min(step_times),
                            "max": max(step_times)
                        }
                
                print(f"\nANALISE DE PERFORMANCE POR ETAPA:")
                for step_name, metrics in steps_analysis.items():
                    print(f"  {step_name}: {metrics['avg']:.2f}s (min: {metrics['min']:.2f}s, max: {metrics['max']:.2f}s)")
        
        if failed_tests:
            print(f"\nFALHAS DETECTADAS:")
            for i, test in enumerate(failed_tests):
                print(f"  Execucao {i+1}: {test.get('error', 'Erro desconhecido')}")
        
        print("=" * 70)


def get_pausas_stress_preferences():
    """
    Obtém as preferências do usuário para o teste de stress
    """
    print("CONFIGURACAO DO TESTE DE STRESS - RELATORIOS DE PAUSAS")
    print("=" * 50)
    
    # Escolha de visualização do navegador
    print("\nVISUALIZACAO DO NAVEGADOR:")
    print("1. Modo Headless (recomendado para performance maxima)")
    print("2. Modo com Visualizacao (para monitoramento)")
    
    while True:
        try:
            escolha_visualizacao = input("\nEscolha o modo (1 ou 2): ").strip()
            if escolha_visualizacao == "1":
                headless = True
                print("Modo Headless selecionado")
                break
            elif escolha_visualizacao == "2":
                headless = False
                print("Modo com Visualizacao selecionado")
                break
            else:
                print("Opcao invalida. Digite 1 ou 2.")
        except KeyboardInterrupt:
            print("\nOperacao cancelada pelo usuario.")
            exit()
        except Exception as e:
            print(f"Erro: {e}")
    
    # Configurações do teste de stress
    print("\nCONFIGURACOES DO TESTE DE STRESS:")
    
    while True:
        try:
            num_executions = input("Numero de execucoes completas (padrao: 3): ").strip()
            if num_executions == "":
                num_executions = 3
                break
            else:
                num_executions = int(num_executions)
                if num_executions > 0:
                    break
                else:
                    print("O numero deve ser maior que 0.")
        except ValueError:
            print("Por favor, digite um numero valido.")
        except KeyboardInterrupt:
            print("\nOperacao cancelada pelo usuario.")
            exit()
    
    while True:
        try:
            num_cycles = input("Numero de ciclos por execucao (padrao: 20): ").strip()
            if num_cycles == "":
                num_cycles = 20
                break
            else:
                num_cycles = int(num_cycles)
                if num_cycles > 0:
                    break
                else:
                    print("O numero deve ser maior que 0.")
        except ValueError:
            print("Por favor, digite um numero valido.")
        except KeyboardInterrupt:
            print("\nOperacao cancelada pelo usuario.")
            exit()
    
    while True:
        try:
            delay_input = input("Delay entre ciclos em segundos (padrao: 0.5): ").strip()
            if delay_input == "":
                delay_between_cycles = 0.5
                break
            else:
                delay_between_cycles = float(delay_input)
                if delay_between_cycles >= 0:
                    break
                else:
                    print("O delay nao pode ser negativo.")
        except ValueError:
            print("Por favor, digite um numero valido.")
        except KeyboardInterrupt:
            print("\nOperacao cancelada pelo usuario.")
            exit()
    
    return headless, num_executions, num_cycles, delay_between_cycles


def main():
    """Execução principal do teste de stress de relatórios de pausas"""
    print("TESTE DE STRESS AVANCADO - RELATORIOS DE PAUSAS")
    print("=" * 60)
    print("Este teste executara multiplos ciclos de busca e download")
    print("de relatorios de pausas para verificar a performance do sistema.")
    print("=" * 60)
    
    # Obtém preferências do usuário
    headless, num_executions, num_cycles, delay_between_cycles = get_pausas_stress_preferences()
    
    # Cria o tester com as configurações escolhidas
    tester = PausasReportStressTester(headless=headless)
    
    # Configurações do sistema
    URL = "https://testesqa.g4flex.com.br:9090/"
    USERNAME = "claudio.igor"
    PASSWORD = "cldgor123"
    
    print(f"\nRESUMO DA CONFIGURACAO:")
    print(f"  URL: {URL}")
    print(f"  Usuario: {USERNAME}")
    print(f"  Modo: {'Headless' if headless else 'Com Visualizacao'}")
    print(f"  Execucoes completas: {num_executions}")
    print(f"  Ciclos por execucao: {num_cycles}")
    print(f"  Delay entre ciclos: {delay_between_cycles}s")
    print(f"  Total de ciclos estimados: {num_executions * num_cycles}")
    
    # Aviso sobre o teste agressivo
    if delay_between_cycles < 0.5:
        print(f"\nAVISO: Teste agressivo configurado!")
        print(f"  Delay muito curto ({delay_between_cycles}s) pode sobrecarregar o servidor.")
    
    if not headless:
        print(f"\nINFORMACAO: Modo com visualizacao ativado.")
        print(f"  Voce vera o navegador executando os ciclos em tempo real.")
    
    confirm = input("\nDeseja iniciar o teste de stress? (s/N): ").strip().lower()
    
    if confirm in ['s', 'sim', 'y', 'yes']:
        print("\nINICIANDO TESTE DE STRESS...")
        print("=" * 60)
        
        try:
            stress_results = tester.advanced_pausas_stress_test(
                URL, 
                USERNAME, 
                PASSWORD, 
                num_executions, 
                num_cycles, 
                delay_between_cycles
            )
            
            print("\nTeste de stress de relatorios de pausas concluido com sucesso!")
            
        except KeyboardInterrupt:
            print("\nTeste interrompido pelo usuario.")
        except Exception as e:
            print(f"\nErro durante o teste: {e}")
            
    else:
        print("Teste cancelado pelo usuario.")


if __name__ == "__main__":
    main()
