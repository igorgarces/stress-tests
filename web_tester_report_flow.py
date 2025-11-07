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
        "dashboards_tab": "#root > nav > div > div.navbar-inner > div > ul > li:nth-child(1)",
        "atendente_tab": "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[1]/div/ul/li[5]/a",
        "telefonia_section": "//*[@id=\"root\"]/div[2]/div/div[1]/div/ul/li[2]/button",
        "relatorios_menu": "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[6]/a",
        "callcenter_submenu": "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[6]/div/ul/li[1]/a",
        "autenticacao_option": "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[6]/div/ul/li[1]/div/ul/li[1]/a"
    },
    "attendance": {
        "logar_filas_chat": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/a",
        "selecionar_filas": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div/form/div/div/div[1]",
        "elemento_especifico": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div/span",
        "iniciar_atendimento": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div/form/button",
        "selecionar_pausa": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div[2]/form/div/div/div/div",
        "botao_pausar": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div[2]/form/div/button",
        "logout_fila_selecionar": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div[3]/form/div/div/div/div[1]/div[1]",
        "logout_fila_botao": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div[3]/form/div/button"
    },
    "reports": {
        "baixar_relatorio": "//*[@id=\"button_csv\"]",
        "filter_button": "//button[contains(text(), 'Filtrar') or contains(@class, 'filter')]",
        "refresh_button": "//button[contains(text(), 'Atualizar') or contains(@class, 'refresh')]"
    }
}


class WebFlowStressTester:
    """
    Teste de stress para fluxo web completo
    Versão otimizada para performance e confiabilidade
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
        """ETAPA 1: Processo de login"""
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

    def navigate_to_reports_flow(self):
        """Navega para o fluxo de relatórios: Relatórios -> CallCenter -> Autenticação"""
        print("Navegando para fluxo de relatórios...")
        
        try:
            # ETAPA 1: Clicar em "Relatórios" (menu já está aberto automaticamente)
            print("Clicando em 'Relatórios'...")
            relatorios_menu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["relatorios_menu"]))
            )
            relatorios_menu.click()
            time.sleep(1)
            
            # ETAPA 2: Clicar em "CallCenter"
            print("Clicando em 'CallCenter'...")
            callcenter_submenu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["callcenter_submenu"]))
            )
            callcenter_submenu.click()
            time.sleep(1)
            
            # ETAPA 3: Clicar em "Autenticação"
            print("Clicando em 'Autenticação'...")
            autenticacao_option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["autenticacao_option"]))
            )
            autenticacao_option.click()
            time.sleep(2)
            
            print("Navegação para relatórios de autenticação concluída")
            return True
            
        except Exception as e:
            print(f"Erro ao navegar para relatórios: {e}")
            raise

    def stress_download_reports(self, num_downloads=20, delay_between_clicks=0.1):
        """
        Realiza múltiplos downloads de relatórios em sequência rápida
        para estressar o servidor
        """
        print(f"Iniciando stress de downloads: {num_downloads} cliques rápidos")
        print(f"Delay entre cliques: {delay_between_clicks}s")
        
        download_results = {
            "total_downloads": num_downloads,
            "successful_downloads": 0,
            "failed_downloads": 0,
            "start_time": time.time(),
            "individual_times": []
        }
        
        try:
            for i in range(num_downloads):
                print(f"Download {i+1}/{num_downloads}...")
                
                try:
                    download_start = time.time()
                    
                    # Localizar e clicar no botão de download
                    baixar_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["reports"]["baixar_relatorio"]))
                    )
                    
                    # Scroll para o elemento para garantir visibilidade
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", baixar_btn)
                    time.sleep(0.1)
                    
                    # Clicar no botão
                    baixar_btn.click()
                    
                    download_time = time.time() - download_start
                    download_results["individual_times"].append(download_time)
                    download_results["successful_downloads"] += 1
                    
                    print(f"  ✓ Clique {i+1} realizado em {download_time:.2f}s")
                    
                    # Delay mínimo entre cliques (muito curto para stress)
                    if i < num_downloads - 1:
                        time.sleep(delay_between_clicks)
                        
                except Exception as e:
                    print(f"  ✗ Erro no download {i+1}: {e}")
                    download_results["failed_downloads"] += 1
                    download_results["individual_times"].append(0)
                    
                    # Tentar continuar mesmo com erro
                    time.sleep(0.5)
                    continue
            
            download_results["total_time"] = time.time() - download_results["start_time"]
            download_results["avg_time_per_download"] = (
                sum(download_results["individual_times"]) / len(download_results["individual_times"])
                if download_results["individual_times"] else 0
            )
            
            print(f"\nResumo dos downloads:")
            print(f"  Total de tentativas: {download_results['total_downloads']}")
            print(f"  Downloads bem-sucedidos: {download_results['successful_downloads']}")
            print(f"  Downloads com falha: {download_results['failed_downloads']}")
            print(f"  Tempo total: {download_results['total_time']:.2f}s")
            print(f"  Tempo médio por download: {download_results['avg_time_per_download']:.2f}s")
            
            return download_results
            
        except Exception as e:
            print(f"Erro crítico durante stress de downloads: {e}")
            download_results["error"] = str(e)
            return download_results

    def execute_report_stress_test(self, url, username, password, num_downloads=20, delay_between_clicks=0.1):
        """
        Executa teste de stress focado em downloads de relatórios
        """
        print("INICIANDO TESTE DE STRESS - FLUXO DE RELATÓRIOS")
        print("=" * 50)
        
        if not self.setup_driver():
            return {"success": False, "error": "Falha ao configurar navegador"}
        
        test_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_type": "report_stress_test",
            "total_time": 0,
            "steps": {},
            "download_results": {},
            "success": True
        }
        
        test_start_time = time.time()
        
        try:
            # ETAPA 1: Login
            print("\nETAPA 1: LOGIN")
            step_start = time.time()
            self.login(url, username, password)
            test_results["steps"]["login"] = time.time() - step_start
            
            # ETAPA 2: Navegação para relatórios
            print("\nETAPA 2: NAVEGAÇÃO PARA RELATÓRIOS")
            step_start = time.time()
            self.navigate_to_reports_flow()
            test_results["steps"]["navigation"] = time.time() - step_start
            
            # ETAPA 3: Aguardar carregamento da página de relatórios
            print("\nETAPA 3: AGUARDANDO CARREGAMENTO")
            time.sleep(3)
            
            # ETAPA 4: Stress de downloads
            print("\nETAPA 4: STRESS DE DOWNLOADS")
            step_start = time.time()
            download_results = self.stress_download_reports(num_downloads, delay_between_clicks)
            test_results["steps"]["download_stress"] = time.time() - step_start
            test_results["download_results"] = download_results
            
            test_results["total_time"] = time.time() - test_start_time
            print(f"\nTESTE DE STRESS CONCLUÍDO EM {test_results['total_time']:.2f}s")
            
        except Exception as e:
            print(f"Erro no teste de stress: {e}")
            test_results["success"] = False
            test_results["error"] = str(e)
        
        finally:
            if self.driver:
                self.driver.quit()
        
        self.results.append(test_results)
        return test_results

    def advanced_report_stress_test(self, url, username, password, num_execucoes=5, num_downloads=20, delay_between_clicks=0.1):
        """
        Teste de stress avançado com múltiplas execuções do fluxo de relatórios
        """
        print(f"TESTE DE STRESS AVANÇADO - {num_execucoes} EXECUÇÕES")
        print("=" * 50)
        
        all_results = []
        start_time = time.time()
        
        for execucao in range(num_execucoes):
            print(f"\nExecução {execucao + 1}/{num_execucoes}")
            print("-" * 30)
            
            result = self.execute_report_stress_test(
                url=url,
                username=username,
                password=password,
                num_downloads=num_downloads,
                delay_between_clicks=delay_between_clicks
            )
            
            all_results.append(result)
            
            # Pausa entre execuções
            if execucao < num_execucoes - 1:
                pause_time = random.uniform(2, 4)
                print(f"Aguardando {pause_time:.1f} segundos antes da próxima execução...")
                time.sleep(pause_time)
        
        total_test_time = time.time() - start_time
        self._generate_report_stress_summary(all_results, total_test_time)
        return all_results

    def _generate_report_stress_summary(self, results, total_test_time):
        """Gera relatório detalhado do teste de stress de relatórios"""
        print("\n" + "=" * 70)
        print("RELATÓRIO DETALHADO - TESTE DE STRESS DE RELATÓRIOS")
        print("=" * 70)
        
        successful_tests = [r for r in results if r["success"]]
        failed_tests = [r for r in results if not r["success"]]
        
        print(f"Tempo total do teste: {total_test_time:.2f}s")
        print(f"Execuções realizadas: {len(results)}")
        print(f"Testes bem-sucedidos: {len(successful_tests)}")
        print(f"Testes com falha: {len(failed_tests)}")
        print(f"Taxa de sucesso: {(len(successful_tests) / len(results)) * 100:.1f}%")
        
        if successful_tests:
            # Estatísticas de downloads
            total_download_attempts = 0
            total_successful_downloads = 0
            total_failed_downloads = 0
            all_download_times = []
            
            for test in successful_tests:
                if "download_results" in test:
                    dr = test["download_results"]
                    total_download_attempts += dr["total_downloads"]
                    total_successful_downloads += dr["successful_downloads"]
                    total_failed_downloads += dr["failed_downloads"]
                    all_download_times.extend(dr["individual_times"])
            
            print(f"\nESTATÍSTICAS DE DOWNLOAD:")
            print(f"  Total de cliques no botão: {total_download_attempts}")
            print(f"  Cliques bem-sucedidos: {total_successful_downloads}")
            print(f"  Cliques com falha: {total_failed_downloads}")
            print(f"  Taxa de sucesso: {(total_successful_downloads / total_download_attempts) * 100:.1f}%")
            
            if all_download_times:
                avg_download_time = sum(all_download_times) / len(all_download_times)
                max_download_time = max(all_download_times)
                min_download_time = min(all_download_times)
                
                print(f"  Tempo médio por clique: {avg_download_time:.3f}s")
                print(f"  Tempo mais rápido: {min_download_time:.3f}s")
                print(f"  Tempo mais lento: {max_download_time:.3f}s")
            
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
                
                print(f"\nANÁLISE DE PERFORMANCE POR ETAPA:")
                for step_name, metrics in steps_analysis.items():
                    print(f"  {step_name}: {metrics['avg']:.2f}s (min: {metrics['min']:.2f}s, max: {metrics['max']:.2f}s)")
        
        if failed_tests:
            print(f"\nFALHAS DETECTADAS:")
            for i, test in enumerate(failed_tests):
                print(f"  Execução {i+1}: {test.get('error', 'Erro desconhecido')}")
        
        print("=" * 70)


def get_report_stress_preferences():
    """
    Obtém as preferências do usuário para o teste de stress de relatórios
    """
    print("CONFIGURAÇÃO DO TESTE DE STRESS - RELATÓRIOS")
    print("=" * 50)
    
    # Escolha de visualização do navegador
    print("\nVISUALIZAÇÃO DO NAVEGADOR:")
    print("1. Modo Headless (recomendado para performance máxima)")
    print("2. Modo com Visualização (para monitoramento)")
    
    while True:
        try:
            escolha_visualizacao = input("\nEscolha o modo (1 ou 2): ").strip()
            if escolha_visualizacao == "1":
                headless = True
                print(" Modo Headless selecionado")
                break
            elif escolha_visualizacao == "2":
                headless = False
                print(" Modo com Visualização selecionado")
                break
            else:
                print(" Opção inválida. Digite 1 ou 2.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            exit()
        except Exception as e:
            print(f"Erro: {e}")
    
    # Configurações do teste de stress
    print("\nCONFIGURAÇÕES DO TESTE DE STRESS:")
    
    while True:
        try:
            num_execucoes = input("Número de execuções completas (padrão: 3): ").strip()
            if num_execucoes == "":
                num_execucoes = 3
                break
            else:
                num_execucoes = int(num_execucoes)
                if num_execucoes > 0:
                    break
                else:
                    print(" O número deve ser maior que 0.")
        except ValueError:
            print(" Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            exit()
    
    while True:
        try:
            num_downloads = input("Número de downloads por execução (padrão: 20): ").strip()
            if num_downloads == "":
                num_downloads = 20
                break
            else:
                num_downloads = int(num_downloads)
                if num_downloads > 0:
                    break
                else:
                    print(" O número deve ser maior que 0.")
        except ValueError:
            print(" Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            exit()
    
    while True:
        try:
            delay_input = input("Delay entre cliques em segundos (padrão: 0.1): ").strip()
            if delay_input == "":
                delay_between_clicks = 0.1
                break
            else:
                delay_between_clicks = float(delay_input)
                if delay_between_clicks >= 0:
                    break
                else:
                    print(" O delay não pode ser negativo.")
        except ValueError:
            print(" Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            exit()
    
    return headless, num_execucoes, num_downloads, delay_between_clicks


def main():
    """Execução principal do teste de stress de relatórios"""
    print(" TESTE DE STRESS AVANÇADO - FLUXO DE RELATÓRIOS")
    print("=" * 60)
    print("Este teste irá executar múltiplos downloads rápidos para")
    print("estressar o servidor e verificar a performance sob carga.")
    print("=" * 60)
    
    # Obtém preferências do usuário
    headless, num_execucoes, num_downloads, delay_between_clicks = get_report_stress_preferences()
    
    # Cria o tester com as configurações escolhidas
    tester = WebFlowStressTester(headless=headless)
    
    # Configurações do sistema
    URL = "https://testesqa.g4flex.com.br:9090/"
    USERNAME = "claudio.igor"
    PASSWORD = "cldgor123"
    
    print(f"\n RESUMO DA CONFIGURAÇÃO:")
    print(f"  URL: {URL}")
    print(f"  Usuário: {USERNAME}")
    print(f"  Modo: {'Headless' if headless else 'Com Visualização'}")
    print(f"  Execuções completas: {num_execucoes}")
    print(f"  Downloads por execução: {num_downloads}")
    print(f"  Delay entre cliques: {delay_between_clicks}s")
    print(f"  Total de cliques estimados: {num_execucoes * num_downloads}")
    
    # Aviso sobre o teste agressivo
    if delay_between_clicks < 0.5:
        print(f"\n  AVISO: Teste agressivo configurado!")
        print(f"   Delay muito curto ({delay_between_clicks}s) pode sobrecarregar o servidor.")
        print(f"   Certifique-se de que este é o comportamento desejado.")
    
    if not headless:
        print(f"\n  INFO: Modo com visualização ativado.")
        print(f"   Você verá o navegador executando os downloads em tempo real.")
    
    confirm = input("\n Deseja iniciar o teste de stress? (s/N): ").strip().lower()
    
    if confirm in ['s', 'sim', 'y', 'yes']:
        print("\n" + " INICIANDO TESTE DE STRESS AGressIVO...")
        print("=" * 60)
        
        try:
            stress_results = tester.advanced_report_stress_test(
                URL, 
                USERNAME, 
                PASSWORD, 
                num_execucoes, 
                num_downloads, 
                delay_between_clicks
            )
            
            print("\n Teste de stress de relatórios concluído com sucesso!")
            
        except KeyboardInterrupt:
            print("\n\n Teste interrompido pelo usuário.")
        except Exception as e:
            print(f"\n\n Erro durante o teste: {e}")
            
    else:
        print(" Teste cancelado pelo usuário.")


if __name__ == "__main__":
    main()