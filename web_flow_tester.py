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
        "telefonia_section": "//*[@id=\"root\"]/div[2]/div/div[1]/div/ul/li[2]/button"
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
    }
}


class WebFlowStressTester:
    """
    Teste de stress para fluxo web completo
    Versão otimizada para performance e confiabilidade
    """
    
    def __init__(self, headless=True):  # Padrão headless para stress test
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
        
        # Para modo com visualização, mantemos algumas otimizações mas não desabilitamos tudo
        if self.headless:
            chrome_options.add_argument("--disable-images")  # Desabilita imagens apenas em headless
            chrome_options.add_argument("--aggressive-cache-discard")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-renderer-backgrounding")
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)  # Aumentado para 15s para maior estabilidade
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
    
    def navigate_to_dashboards(self):
        """ETAPA 2: Navegação para Dashboards"""
        print("Navegando para Dashboards...")
        
        try:
            dashboard_tab = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS_CONFIG["navigation"]["dashboards_tab"]))
            )
            dashboard_tab.click()
            time.sleep(1)
            
            print("Navegacao para Dashboards concluida")
            return True
            
        except Exception as e:
            print(f"Erro ao navegar para Dashboards: {e}")
            raise
    
    def navigate_to_atendente(self):
        """ETAPA 3: Navegação para Atendente"""
        print("Navegando para Atendente...")
        
        try:
            atendente_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["atendente_tab"]))
            )
            atendente_tab.click()
            time.sleep(1)
            
            print("Navegacao para Atendente concluida")
            return True
            
        except Exception as e:
            print(f"Erro ao navegar para Atendente: {e}")
            raise
    
    def navigate_to_telefonia(self):
        """ETAPA 4: Navegação para Telefonia"""
        print("Navegando para Telefonia...")
        
        try:
            telefonia_section = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["telefonia_section"]))
            )
            telefonia_section.click()
            time.sleep(1)
            
            print("Navegacao para Telefonia concluida")
            return True
            
        except Exception as e:
            print(f"Erro ao navegar para Telefonia: {e}")
            raise
    
    def logar_filas_chat(self):
        """ETAPA 5: Clicar em 'Logar em filas do chat'"""
        print("Clicando em 'Logar em filas do chat'...")
        
        try:
            logar_filas_a = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["logar_filas_chat"]))
            )
            logar_filas_a.click()
            time.sleep(1)
            
            print("Clicado em 'Logar em filas do chat'")
            return True
            
        except Exception as e:
            print(f"Erro ao clicar em 'Logar em filas': {e}")
            raise
    
    def selecionar_filas(self):
        """ETAPA 6: Clicar em 'Selecione uma ou mais filas'"""
        print("Clicando em 'Selecione uma ou mais filas'...")
        
        try:
            selecionar_filas = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["selecionar_filas"]))
            )
            selecionar_filas.click()
            time.sleep(1)
            
            print("Clicado em 'Selecione uma ou mais filas'")
            return True
            
        except Exception as e:
            print(f"Erro ao selecionar filas: {e}")
            raise
    
    def digitar_qa1_e_clicar_elemento(self):
        """ETAPA 7: Digitar QA_1, pressionar ENTER e clicar no elemento específico"""
        print("Selecionando fila 'QA_1'...")
        
        try:
            # Clica no dropdown para abrir
            selecionar_filas = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["selecionar_filas"]))
            )
            selecionar_filas.click()
            time.sleep(0.5)
            
            # Digita "QA_1" no campo ativo
            active_element = self.driver.switch_to.active_element
            active_element.send_keys("QA_1")
            time.sleep(0.5)
            
            # Pressiona ENTER
            active_element.send_keys(Keys.ENTER)
            time.sleep(1)
            
            print("Digitado 'QA_1' e pressionado ENTER")
            
            # Clica no elemento específico
            elemento_especifico = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["elemento_especifico"]))
            )
            elemento_especifico.click()
            time.sleep(1)
            
            print("Clicado no elemento especifico")
            return True
            
        except Exception as e:
            print(f"Erro ao selecionar QA_1 e clicar no elemento: {e}")
            raise
    
    def iniciar_atendimento(self):
        """ETAPA 8: Clicar em 'Iniciar atendimento'"""
        print("Clicando em 'Iniciar atendimento'...")
        
        try:
            iniciar_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["iniciar_atendimento"]))
            )
            iniciar_btn.click()
            time.sleep(2)
            
            print("Atendimento iniciado com sucesso")
            return True
            
        except Exception as e:
            print(f"Erro ao iniciar atendimento: {e}")
            raise
    
    def ciclo_pausa(self, ciclo_num):
        """ETAPA 9: Executar ciclo de pausa/despausa"""
        print(f"Ciclo {ciclo_num}: Pausa/Despausa...")
        
        try:
            # PASSO 1: Selecionar pausa
            print("Selecionando pausa...")
            selecionar_pausa = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["selecionar_pausa"]))
            )
            selecionar_pausa.click()
            time.sleep(0.5)
            
            # PASSO 2: Digitar "banheiro" e pressionar ENTER
            print("Digitando 'banheiro'...")
            active_element = self.driver.switch_to.active_element
            active_element.send_keys("banheiro")
            time.sleep(0.5)
            active_element.send_keys(Keys.ENTER)
            time.sleep(1)
            
            # PASSO 3: Clicar em Pausar
            print("Clicando em Pausar...")
            botao_pausar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["botao_pausar"]))
            )
            botao_pausar.click()
            time.sleep(2)
            
            # PASSO 4: Aguardar em pausa
            tempo_pausa = random.uniform(2, 4)
            print(f"Aguardando {tempo_pausa:.1f} segundos em pausa...")
            time.sleep(tempo_pausa)
            
            # PASSO 5: Clicar em Despausar
            print("Clicando em Despausar...")
            botao_despausar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["botao_pausar"]))
            )
            botao_despausar.click()
            time.sleep(2)
            
            print(f"Ciclo {ciclo_num} concluido")
            return True
            
        except Exception as e:
            print(f"Erro no ciclo {ciclo_num}: {e}")
            return False

    def logout_fila(self):
        """ETAPA 10: Fazer logout da fila antes de reiniciar o ciclo"""
        print("Executando logout da fila...")
        
        try:
            # PASSO 1: Clicar em selecionar filas para logout
            print("Clicando em 'Selecione as filas' para logout...")
            logout_selecionar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["logout_fila_selecionar"]))
            )
            logout_selecionar.click()
            time.sleep(0.5)
            
            # PASSO 2: Digitar "QA_1" no campo ativo
            print("Digitando 'QA_1' para logout...")
            active_element = self.driver.switch_to.active_element
            active_element.send_keys("QA_1")
            time.sleep(0.5)
            
            # PASSO 3: Pressionar ENTER
            active_element.send_keys(Keys.ENTER)
            time.sleep(1)
            
            # PASSO 4: Clicar em "Fazer logout"
            print("Clicando em 'Fazer logout'...")
            logout_botao = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["logout_fila_botao"]))
            )
            logout_botao.click()
            time.sleep(2)
            
            print("Logout da fila realizado com sucesso")
            return True
            
        except Exception as e:
            print(f"Erro ao fazer logout da fila: {e}")
            return False
    
    def execute_complete_flow(self, url, username, password, num_ciclos=2):
        """
        Executa o fluxo completo do teste
        """
        print("INICIANDO FLUXO COMPLETO")
        print("=" * 50)
        
        if not self.setup_driver():
            return {"success": False, "error": "Falha ao configurar navegador"}
        
        flow_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_time": 0,
            "steps": {},
            "ciclos_pausa": [],
            "success": True
        }
        
        flow_start_time = time.time()
        
        try:
            # ETAPA 1: Login
            print("\nETAPA 1: LOGIN")
            step_start = time.time()
            self.login(url, username, password)
            flow_results["steps"]["login"] = time.time() - step_start
            
            # ETAPA 2: Dashboards
            print("\nETAPA 2: DASHBOARDS")
            step_start = time.time()
            self.navigate_to_dashboards()
            flow_results["steps"]["dashboards"] = time.time() - step_start
            
            # ETAPA 3: Atendente
            print("\nETAPA 3: ATENDENTE")
            step_start = time.time()
            self.navigate_to_atendente()
            flow_results["steps"]["atendente"] = time.time() - step_start
            
            # ETAPA 4: Telefonia
            print("\nETAPA 4: TELEFONIA")
            step_start = time.time()
            self.navigate_to_telefonia()
            flow_results["steps"]["telefonia"] = time.time() - step_start
            
            # ETAPA 5: Logar em filas do chat
            print("\nETAPA 5: LOGAR FILAS CHAT")
            step_start = time.time()
            self.logar_filas_chat()
            flow_results["steps"]["logar_filas"] = time.time() - step_start
            
            # ETAPA 6: Selecionar filas
            print("\nETAPA 6: SELECIONAR FILAS")
            step_start = time.time()
            self.selecionar_filas()
            flow_results["steps"]["selecionar_filas"] = time.time() - step_start
            
            # ETAPA 7: Digitar QA_1 e clicar no elemento específico
            print("\nETAPA 7: DIGITAR QA_1 E CLICAR ELEMENTO")
            step_start = time.time()
            self.digitar_qa1_e_clicar_elemento()
            flow_results["steps"]["digitar_qa1_elemento"] = time.time() - step_start
            
            # ETAPA 8: Iniciar atendimento
            print("\nETAPA 8: INICIAR ATENDIMENTO")
            step_start = time.time()
            self.iniciar_atendimento()
            flow_results["steps"]["iniciar_atendimento"] = time.time() - step_start
            
            # ETAPA 9: Ciclos de pausa/despausa
            print(f"\nETAPA 9: {num_ciclos} CICLOS PAUSA")
            step_start = time.time()
            
            ciclos_resultados = []
            for ciclo in range(num_ciclos):
                print(f"Ciclo {ciclo + 1}/{num_ciclos}")
                
                ciclo_inicio = time.time()
                sucesso = self.ciclo_pausa(ciclo + 1)
                ciclo_tempo = time.time() - ciclo_inicio
                
                ciclo_resultado = {
                    "ciclo": ciclo + 1,
                    "sucesso": sucesso,
                    "tempo": ciclo_tempo
                }
                ciclos_resultados.append(ciclo_resultado)
                
                # Se for o último ciclo, fazer logout antes de reiniciar
                if ciclo == num_ciclos - 1:
                    print("Ultimo ciclo concluido - executando logout da fila")
                    self.logout_fila()
                
                if ciclo < num_ciclos - 1:
                    espera = random.uniform(1, 2)
                    time.sleep(espera)
            
            flow_results["steps"]["ciclos_pausa"] = time.time() - step_start
            flow_results["ciclos_pausa"] = ciclos_resultados
            
            flow_results["total_time"] = time.time() - flow_start_time
            print(f"FLUXO CONCLUIDO EM {flow_results['total_time']:.2f}s")
            
        except Exception as e:
            print(f"Erro no fluxo: {e}")
            flow_results["success"] = False
            flow_results["error"] = str(e)
        
        finally:
            if self.driver:
                self.driver.quit()
        
        self.results.append(flow_results)
        return flow_results

    def pure_stress_test(self, url, username, password, num_execucoes=10, num_ciclos=5):
        """
        Teste de stress puro - executa múltiplas iterações completas
        incluindo login, configuração e ciclos de pausa/despausa com logout
        """
        print(f"TESTE DE STRESS PURO - {num_execucoes} EXECUCOES COMPLETAS")
        print("=" * 50)
        
        all_results = []
        start_time = time.time()
        
        for execucao in range(num_execucoes):
            print(f"\nExecucao {execucao + 1}/{num_execucoes}")
            print("-" * 30)
            
            # Executa fluxo completo com logout incluído
            result = self.execute_complete_flow(
                url=url,
                username=username,
                password=password,
                num_ciclos=num_ciclos
            )
            
            all_results.append(result)
            
            # Pausa entre execuções (mais curta para stress test)
            if execucao < num_execucoes - 1:
                pause_time = random.uniform(2, 3)  # Reduzido para stress test
                print(f"Aguardando {pause_time:.1f} segundos antes da proxima execucao...")
                time.sleep(pause_time)
        
        total_test_time = time.time() - start_time
        self._generate_pure_stress_report(all_results, total_test_time)
        return all_results

    def _generate_pure_stress_report(self, results, total_test_time):
        """Gera relatório detalhado do teste de stress puro"""
        print("\n" + "=" * 60)
        print("RELATORIO TESTE DE STRESS PURO")
        print("=" * 60)
        
        successful_flows = [r for r in results if r["success"]]
        failed_flows = [r for r in results if not r["success"]]
        
        print(f"Tempo total do teste: {total_test_time:.2f}s")
        print(f"Execucoes realizadas: {len(results)}")
        print(f"Fluxos bem-sucedidos: {len(successful_flows)}")
        print(f"Fluxos com falha: {len(failed_flows)}")
        print(f"Taxa de sucesso: {(len(successful_flows) / len(results)) * 100:.1f}%")
        
        if successful_flows:
            total_times = [flow["total_time"] for flow in successful_flows]
            avg_total_time = sum(total_times) / len(total_times)
            
            print(f"\nMETRICAS DE TEMPO:")
            print(f"Tempo medio por execucao: {avg_total_time:.2f}s")
            print(f"Tempo mais rapido: {min(total_times):.2f}s")
            print(f"Tempo mais lento: {max(total_times):.2f}s")
            
            # Análise detalhada dos passos
            if "steps" in successful_flows[0]:
                steps_analysis = {}
                for step_name in successful_flows[0]["steps"]:
                    step_times = [flow["steps"][step_name] for flow in successful_flows if step_name in flow["steps"]]
                    if step_times:
                        steps_analysis[step_name] = {
                            "avg": sum(step_times) / len(step_times),
                            "min": min(step_times),
                            "max": max(step_times)
                        }
                
                print(f"\nANALISE DETALHADA DOS PASSOS:")
                for step_name, metrics in steps_analysis.items():
                    print(f"  {step_name}: {metrics['avg']:.2f}s (min: {metrics['min']:.2f}s, max: {metrics['max']:.2f}s)")
            
            # Análise dos ciclos de pausa
            all_ciclos = []
            for flow in successful_flows:
                if "ciclos_pausa" in flow:
                    all_ciclos.extend(flow["ciclos_pausa"])
            
            successful_ciclos = [c for c in all_ciclos if c["sucesso"]]
            if successful_ciclos:
                ciclo_times = [c["tempo"] for c in successful_ciclos]
                print(f"\nCICLOS DE PAUSA:")
                print(f"  Total de ciclos: {len(all_ciclos)}")
                print(f"  Ciclos bem-sucedidos: {len(successful_ciclos)}")
                print(f"  Taxa de sucesso dos ciclos: {(len(successful_ciclos) / len(all_ciclos)) * 100:.1f}%")
                print(f"  Tempo medio por ciclo: {sum(ciclo_times) / len(ciclo_times):.2f}s")
        
        if failed_flows:
            print(f"\nFALHAS DETECTADAS:")
            for i, flow in enumerate(failed_flows):
                print(f"  Execucao {i+1}: {flow.get('error', 'Erro desconhecido')}")
        
        print("=" * 60)


def get_user_preferences():
    """
    Obtém as preferências do usuário de forma interativa
    """
    print("CONFIGURAÇÃO DO TESTE DE STRESS")
    print("=" * 40)
    
    # Escolha de visualização do navegador
    print("\nVISUALIZAÇÃO DO NAVEGADOR:")
    print("1. Modo Headless (recomendado para performance) - Navegador invisível")
    print("2. Modo com Visualização - Navegador visível")
    
    while True:
        try:
            escolha_visualizacao = input("\nEscolha o modo (1 ou 2): ").strip()
            if escolha_visualizacao == "1":
                headless = True
                print("✓ Modo Headless selecionado")
                break
            elif escolha_visualizacao == "2":
                headless = False
                print("✓ Modo com Visualização selecionado")
                break
            else:
                print(" Opção inválida. Digite 1 ou 2.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            exit()
        except Exception as e:
            print(f"Erro: {e}")
    
    # Configurações do teste
    print("\nCONFIGURAÇÕES DO TESTE:")
    
    while True:
        try:
            num_execucoes = input("Número de execuções (padrão: 10): ").strip()
            if num_execucoes == "":
                num_execucoes = 10
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
            num_ciclos = input("Ciclos por execução (padrão: 5): ").strip()
            if num_ciclos == "":
                num_ciclos = 5
                break
            else:
                num_ciclos = int(num_ciclos)
                if num_ciclos > 0:
                    break
                else:
                    print(" O número deve ser maior que 0.")
        except ValueError:
            print(" Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            exit()
    
    return headless, num_execucoes, num_ciclos


def main():
    """Execução principal do teste de stress"""
    print("TESTE DE STRESS PURO - SISTEMA DE ATENDIMENTO")
    print("=" * 50)
    
    # Obtém preferências do usuário
    headless, num_execucoes, num_ciclos = get_user_preferences()
    
    # Cria o tester com as configurações escolhidas
    tester = WebFlowStressTester(headless=headless)
    
    # Configurações do sistema
    URL = "https://testesqa.g4flex.com.br:9090/"
    USERNAME = "claudio.igor"
    PASSWORD = "cldgor123"
    
    print(f"\nRESUMO DA CONFIGURAÇÃO:")
    print(f"  URL: {URL}")
    print(f"  Usuario: {USERNAME}")
    print(f"  Modo: {'Headless (invisível)' if headless else 'Com Visualização (visível)'}")
    print(f"  Execuções: {num_execucoes}")
    print(f"  Ciclos por execução: {num_ciclos}")
    
    # Aviso sobre performance
    if not headless:
        print(f"\n  AVISO: Modo com visualização ativado.")
        print(f"   O teste pode ser mais lento devido à renderização gráfica.")
        print(f"   Para melhor performance, recomenda-se usar o modo Headless.")
    
    confirm = input("\nDeseja iniciar o teste de stress? (s/N): ").strip().lower()
    
    if confirm in ['s', 'sim', 'y', 'yes']:
        print("\n" + " INICIANDO TESTE DE STRESS PURO...")
        print("=" * 50)
        
        try:
            stress_results = tester.pure_stress_test(
                URL, 
                USERNAME, 
                PASSWORD, 
                num_execucoes, 
                num_ciclos
            )
            
            print("\n Teste de stress concluído com sucesso!")
            
        except KeyboardInterrupt:
            print("\n\n Teste interrompido pelo usuário.")
        except Exception as e:
            print(f"\n\n Erro durante o teste: {e}")
            
    else:
        print(" Teste cancelado pelo usuário.")


if __name__ == "__main__":
    main()