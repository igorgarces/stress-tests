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

# ⚡ SELECTORS CORRIGIDOS PARA O FLUXO COMPLETO
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
        # ETAPA: Logar em filas do chat (ícone SVG)
        "logar_filas_chat": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/a/svg/path",
        
        # ETAPA: Selecionar uma ou mais filas
        "selecionar_filas": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div/form/div/div/div[1]",
        
        # ETAPA: Selecionar fila QA_1
        "fila_qa1": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div/form/div/div/div[1]",
        
        # ETAPA: Iniciar atendimento
        "iniciar_atendimento": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div/form/button",
        
        # ETAPA: Selecionar uma pausa
        "selecionar_pausa": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div[2]/form/div/div/div/div",
        
        # ETAPA: Selecionar banheiro
        "pausa_banheiro": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div[2]/form/div/div/div/div/div[1]",
        
        # ETAPA: Botão pausar/despausar (mesmo botão)
        "botao_pausar": "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/div/div[2]/form/div/button"
    }
}

class WebFlowStressTester:
    """
    Versão ULTRA OTIMIZADA com fluxo completo - MÁXIMA VELOCIDADE
    """
    
    def __init__(self, headless=True):  # Headless por padrão para performance
        self.headless = headless
        self.driver = None
        self.wait = None
        self.results = []
        
    def setup_driver(self):
        """Configura o driver do Chrome ultra otimizado"""
        print("🛠️ Configurando navegador...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)  # Timeout reduzido
            print("✅ Navegador configurado com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def login(self, url, username, password):
        """ETAPA 1: Login RÁPIDO"""
        print(f"🔐 Fazendo login...")
        
        try:
            self.driver.get(url)
            time.sleep(2)  # Reduzido de 5s
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS_CONFIG["login"]["username_field"]))
            )
            
            password_field = self.driver.find_element(By.CSS_SELECTOR, SELECTORS_CONFIG["login"]["password_field"])
            login_button = self.driver.find_element(By.CSS_SELECTOR, SELECTORS_CONFIG["login"]["login_button"])
            
            # Preenchimento rápido
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()
            
            time.sleep(3)  # Reduzido de 6s
            
            print("✅ Login realizado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            raise
    
    def navigate_to_dashboards(self):
        """ETAPA 2: Navega para Dashboards RÁPIDO"""
        print("📊 Navegando para Dashboards...")
        
        try:
            dashboard_tab = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS_CONFIG["navigation"]["dashboards_tab"]))
            )
            dashboard_tab.click()
            time.sleep(1)  # Reduzido de 4s
            
            print("✅ Navegação para Dashboards concluída")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Dashboards: {e}")
            raise
    
    def navigate_to_atendente(self):
        """ETAPA 3: Navega para Atendente RÁPIDO"""
        print("👤 Navegando para Atendente...")
        
        try:
            atendente_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["atendente_tab"]))
            )
            atendente_tab.click()
            time.sleep(1)  # Reduzido de 4s
            
            print("✅ Navegação para Atendente concluída")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Atendente: {e}")
            raise
    
    def navigate_to_telefonia(self):
        """ETAPA 4: Navega para Telefonia RÁPIDO"""
        print("📞 Navegando para Telefonia...")
        
        try:
            telefonia_section = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["navigation"]["telefonia_section"]))
            )
            telefonia_section.click()
            time.sleep(1)  # Reduzido de 4s
            
            print("✅ Navegação para Telefonia concluída")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Telefonia: {e}")
            raise
    
    def logar_filas_chat(self):
        """ETAPA 5: Clicar em 'Logar em filas do chat' RÁPIDO"""
        print("💬 Clicando em 'Logar em filas do chat'...")
        
        try:
            # Estratégia direta - tenta o elemento A primeiro
            try:
                logar_filas_a = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/a"))
                )
                logar_filas_a.click()
                time.sleep(1)  # Reduzido de 3s
                
            except:
                # Fallback via JavaScript
                logar_filas_a = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[7]/a"))
                )
                self.driver.execute_script("arguments[0].click();", logar_filas_a)
                time.sleep(1)
            
            print("✅ Clicado em 'Logar em filas do chat'")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao clicar em 'Logar em filas': {e}")
            raise
    
    def selecionar_filas(self):
        """ETAPA 6: Clicar em 'Selecione uma ou mais filas' RÁPIDO"""
        print("📋 Clicando em 'Selecione uma ou mais filas'...")
        
        try:
            selecionar_filas = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["selecionar_filas"]))
            )
            selecionar_filas.click()
            time.sleep(1)  # Reduzido de 3s
            
            print("✅ Clicado em 'Selecione uma ou mais filas'")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao selecionar filas: {e}")
            raise
    
    def selecionar_qa1(self):
        """ETAPA 7: Selecionar fila QA_1 RÁPIDO"""
        print("🔘 Selecionando fila 'QA_1'...")
        
        try:
            # Método direto - clica no dropdown e digita
            selecionar_filas = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["selecionar_filas"]))
            )
            selecionar_filas.click()
            time.sleep(0.5)
            
            # Procura campo de input rapidamente
            input_field = None
            input_selectors = [
                "//input[@type='text']",
                "//input[@type='search']",
                "//input[contains(@class, 'search')]"
            ]
            
            for selector in input_selectors:
                try:
                    input_field = self.driver.find_element(By.XPATH, selector)
                    if input_field.is_displayed():
                        break
                except:
                    continue
            
            if input_field:
                # Digitação rápida
                input_field.clear()
                input_field.send_keys("QA_1")
                time.sleep(0.5)
                input_field.send_keys(Keys.ENTER)
                time.sleep(0.5)
            else:
                # Fallback - clica diretamente
                fila_qa1 = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["fila_qa1"]))
                )
                fila_qa1.click()
                time.sleep(0.5)
            
            print("✅ Fila 'QA_1' selecionada")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao selecionar QA_1: {e}")
            raise
    
    def iniciar_atendimento(self):
        """ETAPA 8: Clicar em 'Iniciar atendimento' RÁPIDO"""
        print("🚀 Clicando em 'Iniciar atendimento'...")
        
        try:
            iniciar_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["iniciar_atendimento"]))
            )
            iniciar_btn.click()
            time.sleep(2)  # Reduzido de 5s
            
            print("✅ Atendimento iniciado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar atendimento: {e}")
            raise
    
    def ciclo_pausa(self, ciclo_num):
        """ETAPA 9: Executar ciclo de pausa/despausa RÁPIDO"""
        print(f"⏸️  Ciclo {ciclo_num}: Pausa/Despausa...")
        
        try:
            # PASSO 1: Selecionar pausa
            selecionar_pausa = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["selecionar_pausa"]))
            )
            selecionar_pausa.click()
            time.sleep(0.5)
            
            # PASSO 2: Selecionar banheiro
            pausa_banheiro = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["pausa_banheiro"]))
            )
            pausa_banheiro.click()
            time.sleep(0.5)
            
            # PASSO 3: Clicar em Pausar
            botao_pausar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["botao_pausar"]))
            )
            botao_pausar.click()
            time.sleep(2)  # Reduzido de 4s
            
            # PASSO 4: Aguardar em pausa (tempo reduzido)
            tempo_pausa = random.uniform(2, 4)  # Reduzido de 8-12s
            time.sleep(tempo_pausa)
            
            # PASSO 5: Clicar em Despausar
            botao_despausar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS_CONFIG["attendance"]["botao_pausar"]))
            )
            botao_despausar.click()
            time.sleep(2)  # Reduzido de 4s
            
            print(f"   ✅ Ciclo {ciclo_num} concluído")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro no ciclo {ciclo_num}: {e}")
            return False
    
    def execute_complete_flow(self, url, username, password, num_ciclos=2):
        """
        FLUXO COMPLETO ULTRA RÁPIDO
        """
        print("🚀 INICIANDO FLUXO COMPLETO - MODO RÁPIDO")
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
            print("\n1️⃣  LOGIN")
            step_start = time.time()
            self.login(url, username, password)
            flow_results["steps"]["login"] = time.time() - step_start
            
            # ETAPA 2: Dashboards
            print("\n2️⃣  DASHBOARDS")
            step_start = time.time()
            self.navigate_to_dashboards()
            flow_results["steps"]["dashboards"] = time.time() - step_start
            
            # ETAPA 3: Atendente
            print("\n3️⃣  ATENDENTE")
            step_start = time.time()
            self.navigate_to_atendente()
            flow_results["steps"]["atendente"] = time.time() - step_start
            
            # ETAPA 4: Telefonia
            print("\n4️⃣  TELEFONIA")
            step_start = time.time()
            self.navigate_to_telefonia()
            flow_results["steps"]["telefonia"] = time.time() - step_start
            
            # ETAPA 5: Logar em filas do chat
            print("\n5️⃣  LOGAR FILAS CHAT")
            step_start = time.time()
            self.logar_filas_chat()
            flow_results["steps"]["logar_filas"] = time.time() - step_start
            
            # ETAPA 6: Selecionar filas
            print("\n6️⃣  SELECIONAR FILAS")
            step_start = time.time()
            self.selecionar_filas()
            flow_results["steps"]["selecionar_filas"] = time.time() - step_start
            
            # ETAPA 7: Selecionar QA_1
            print("\n7️⃣  SELECIONAR QA_1")
            step_start = time.time()
            self.selecionar_qa1()
            flow_results["steps"]["selecionar_qa1"] = time.time() - step_start
            
            # ETAPA 8: Iniciar atendimento
            print("\n8️⃣  INICIAR ATENDIMENTO")
            step_start = time.time()
            self.iniciar_atendimento()
            flow_results["steps"]["iniciar_atendimento"] = time.time() - step_start
            
            # ETAPA 9: Ciclos de pausa/despausa
            print(f"\n9️⃣  {num_ciclos} CICLOS PAUSA")
            step_start = time.time()
            
            ciclos_resultados = []
            for ciclo in range(num_ciclos):
                print(f"   🔄 Ciclo {ciclo + 1}/{num_ciclos}")
                
                ciclo_inicio = time.time()
                sucesso = self.ciclo_pausa(ciclo + 1)
                ciclo_tempo = time.time() - ciclo_inicio
                
                ciclo_resultado = {
                    "ciclo": ciclo + 1,
                    "sucesso": sucesso,
                    "tempo": ciclo_tempo
                }
                ciclos_resultados.append(ciclo_resultado)
                
                # Pausa mínima entre ciclos
                if ciclo < num_ciclos - 1:
                    espera = random.uniform(1, 2)  # Reduzido de 5-8s
                    time.sleep(espera)
            
            flow_results["steps"]["ciclos_pausa"] = time.time() - step_start
            flow_results["ciclos_pausa"] = ciclos_resultados
            
            flow_results["total_time"] = time.time() - flow_start_time
            print(f"\n🎉 FLUXO CONCLUÍDO EM {flow_results['total_time']:.2f}s")
            
        except Exception as e:
            print(f"❌ Erro no fluxo: {e}")
            flow_results["success"] = False
            flow_results["error"] = str(e)
        
        finally:
            if self.driver:
                self.driver.quit()
        
        self.results.append(flow_results)
        return flow_results

    def stress_test_flow(self, url, username, password, num_users=5, num_ciclos=3):
        """
        TESTE DE STRESS ULTRA RÁPIDO
        """
        print(f"💥 STRESS TEST - {num_users} USUÁRIOS")
        print("=" * 40)
        
        all_results = []
        
        for user in range(num_users):
            print(f"\n🎭 USUÁRIO {user + 1}/{num_users}")
            
            result = self.execute_complete_flow(
                url=url,
                username=f"{username}{user+1}",  # Usuários sequenciais
                password=password,
                num_ciclos=num_ciclos
            )
            
            all_results.append(result)
            
            # Pausa mínima entre usuários
            if user < num_users - 1:
                pause_time = random.uniform(3, 5)  # Reduzido de 15-25s
                time.sleep(pause_time)
        
        self._generate_stress_report(all_results)
        return all_results

    def _generate_stress_report(self, results):
        """Gera relatório rápido"""
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO STRESS TEST")
        print("=" * 50)
        
        successful_flows = [r for r in results if r["success"]]
        failed_flows = [r for r in results if not r["success"]]
        
        print(f"👥 Usuários testados: {len(results)}")
        print(f"✅ Fluxos bem-sucedidos: {len(successful_flows)}")
        print(f"❌ Fluxos com falha: {len(failed_flows)}")
        print(f"📈 Taxa de sucesso: {(len(successful_flows) / len(results)) * 100:.1f}%")
        
        if successful_flows:
            total_times = [flow["total_time"] for flow in successful_flows]
            avg_total_time = sum(total_times) / len(total_times)
            
            print(f"\n⏱️  TEMPO MÉDIO: {avg_total_time:.2f}s")
            print(f"⚡ Mais rápido: {min(total_times):.2f}s")
            print(f"🐌 Mais lento: {max(total_times):.2f}s")
            
            # Ciclos bem-sucedidos
            all_ciclos = []
            for flow in successful_flows:
                all_ciclos.extend(flow["ciclos_pausa"])
            
            successful_ciclos = [c for c in all_ciclos if c["sucesso"]]
            if successful_ciclos:
                print(f"🔄 Ciclos pausa: {len(successful_ciclos)}/{len(all_ciclos)} bem-sucedidos")
        
        print("=" * 50)

def main():
    """Execução principal"""
    print("🎯 FLUXO COMPLETO - MODO RÁPIDO")
    print("❌ SEM SCREENSHOTS - 🏎️  MÁXIMA VELOCIDADE")
    print("=" * 50)
    
    tester = WebFlowStressTester(headless=True)
    
    # ⚠️ CONFIGURAÇÃO
    URL = "https://testesqa.g4flex.com.br:9090/"
    USERNAME = "claudio.igor"
    PASSWORD = "cldgor123"
    
    print("Executando fluxo completo rápido...")
    
    result = tester.execute_complete_flow(
        url=URL,
        username=USERNAME,
        password=PASSWORD,
        num_ciclos=2
    )
    
    if result["success"]:
        print("\n🎉 SUCESSO! Fluxo executado.")
        print(f"📊 Tempo total: {result['total_time']:.2f}s")
        print(f"🔄 Ciclos executados: {len(result['ciclos_pausa'])}")
        
        # Teste de stress automático
        stress = input("\n🧪 Executar stress test? (s/N): ").strip().lower()
        if stress in ['s', 'sim', 'y', 'yes']:
            num_users = 5
            num_ciclos = 3
            
            print(f"\n💥 INICIANDO STRESS TEST: {num_users} usuários")
            stress_results = tester.stress_test_flow(URL, USERNAME, PASSWORD, num_users, num_ciclos)
            
    else:
        print(f"\n❌ FALHA: {result.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    main()