import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class LoginLogoutStressTester:
    """
    Teste de STRESS de login/logout - USUÁRIO ÚNICO
    Fluxo: Login → Navegação → Perfil → Sair
    """
    
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.results = []
        
    def setup_driver(self):
        """Configura o driver do Chrome"""
        print("🛠️ Configurando navegador...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            print("   👻 Modo: INVISÍVEL")
        else:
            print("   👀 Modo: VISÍVEL")
            
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 8)
            print("✅ Navegador configurado com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def login_rapido(self, url, username, password):
        """ETAPA 1: Login rápido"""
        try:
            print(f"   🌐 Acessando: {url}")
            self.driver.get(url)
            time.sleep(1.5)
            
            # Login direto
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 
                    "#root > div.login-container.fadeIn > div.form-container > div.bg-secondary.border-0.mb-0.card > div.px-lg-5.py-lg-5.card-body > form > div.mb-3.focused.form-group > div > input"
                ))
            )
            password_field = self.driver.find_element(By.CSS_SELECTOR, 
                "#root > div.login-container.fadeIn > div.form-container > div.bg-secondary.border-0.mb-0.card > div.px-lg-5.py-lg-5.card-body > form > div:nth-child(2) > div > input"
            )
            login_button = self.driver.find_element(By.CSS_SELECTOR, 
                "#root > div.login-container.fadeIn > div.form-container > div.bg-secondary.border-0.mb-0.card > div.px-lg-5.py-lg-5.card-body > form > div.text-center > button"
            )
            
            print(f"   👤 Preenchendo usuário: {username}")
            username_field.clear()
            username_field.send_keys(username)
            
            print("   🔒 Preenchendo senha: ***")
            password_field.clear()
            password_field.send_keys(password)
            
            print("   🖱️ Clicando em Login...")
            login_button.click()
            time.sleep(2.5)
            
            # Verificação de sucesso
            if "login" not in self.driver.current_url.lower():
                print("   ✅ Login bem-sucedido!")
                return True
            else:
                print("   ❌ Login falhou")
                return False
            
        except Exception as e:
            print(f"   ❌ Erro no login: {e}")
            return False

    def navegar_para_dashboards(self):
        """ETAPA 2: Navega para Dashboards"""
        try:
            print("   📊 Navegando para Dashboards...")
            dashboard_tab = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "#root > nav > div > div.navbar-inner > div > ul > li:nth-child(1)"
                ))
            )
            dashboard_tab.click()
            time.sleep(1)
            print("   ✅ Dashboards acessado")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao navegar para Dashboards: {e}")
            return False

    def navegar_para_atendente(self):
        """ETAPA 3: Navega para Atendente"""
        try:
            print("   👤 Navegando para Atendente...")
            atendente_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[1]/div/ul/li[5]/a"
                ))
            )
            atendente_tab.click()
            time.sleep(1)
            print("   ✅ Atendente acessado")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao navegar para Atendente: {e}")
            return False

    def clicar_no_perfil(self):
        """ETAPA 4: Clica no perfil do usuário"""
        try:
            print("   👤 Clicando no perfil...")
            perfil_seletor = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[2]/li/a"
            
            perfil_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, perfil_seletor))
            )
            perfil_element.click()
            time.sleep(1)
            print("   ✅ Perfil clicado")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao clicar no perfil: {e}")
            return False

    def clicar_em_sair(self):
        """ETAPA 5: Clica em 'Sair'"""
        try:
            print("   🚪 Clicando em 'Sair'...")
            sair_seletor = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[2]/li/div/button[4]"
            
            sair_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, sair_seletor))
            )
            sair_element.click()
            time.sleep(2)
            print("   ✅ Sair clicado")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao clicar em Sair: {e}")
            return False

    def verificar_logout_sucesso(self):
        """Verifica se o logout foi bem-sucedido"""
        try:
            # Verifica se voltou para a página de login
            if "login" in self.driver.current_url.lower():
                return True
            
            # Verifica se os campos de login estão presentes
            login_fields = self.driver.find_elements(By.CSS_SELECTOR, 
                "#root > div.login-container.fadeIn > div.form-container > div.bg-secondary.border-0.mb-0.card > div.px-lg-5.py-lg-5.card-body > form"
            )
            
            if login_fields:
                return True
                
            return False
            
        except Exception as e:
            print(f"   ⚠️ Erro na verificação de logout: {e}")
            return False

    def execute_complete_cycle(self, url, username, password, cycle_number):
        """Executa UM ciclo completo: Login → Navegação → Perfil → Sair"""
        print(f"\n🔄 CICLO {cycle_number}")
        print("=" * 30)
        
        cycle_start = time.time()
        
        # ETAPA 1: Login
        login_success = self.login_rapido(url, username, password)
        
        if login_success:
            # ETAPA 2: Navegação rápida pelo sistema
            print("   🧭 Navegando pelo sistema...")
            
            self.navegar_para_dashboards()
            self.navegar_para_atendente()
            
            # Tempo aleatório navegando
            navegacao_time = random.uniform(1, 2)
            print(f"   ⏰ Navegando por {navegacao_time:.1f}s...")
            time.sleep(navegacao_time)
            
            # ETAPA 3: Logout completo
            print("   🚪 Iniciando logout...")
            perfil_success = self.clicar_no_perfil()
            
            if perfil_success:
                sair_success = self.clicar_em_sair()
                
                if sair_success:
                    logout_verified = self.verificar_logout_sucesso()
                    if logout_verified:
                        print("   ✅ Logout bem-sucedido!")
                    else:
                        print("   ⚠️ Logout realizado mas verificação falhou")
                else:
                    print("   ❌ Falha ao clicar em Sair")
            else:
                print("   ❌ Falha ao clicar no Perfil")
                
        else:
            print("   ❌ Login falhou - recarregando página...")
            self.driver.get(url)
            time.sleep(1)
        
        cycle_time = time.time() - cycle_start
        
        result = {
            "cycle": cycle_number,
            "login_success": login_success,
            "logout_success": sair_success if login_success else False,
            "time": cycle_time
        }
        
        print(f"   ⏱️  Ciclo concluído em {cycle_time:.2f}s")
        return result
    
    def stress_test_single_user(self, url, username, password, num_cycles=20):
        """
        TESTE DE STRESS - USUÁRIO ÚNICO
        Fluxo completo: Login → Navegação → Perfil → Sair
        """
        print(f"💥 STRESS TEST - USUÁRIO ÚNICO")
        print(f"👤 Usuário: {username}")
        print(f"🔄 Ciclos: {num_cycles}")
        print(f"🎯 Fluxo: Login → Dashboards → Atendente → Perfil → Sair")
        if not self.headless:
            print("👀 MODO VISUALIZAÇÃO ATIVADO")
        print("=" * 50)
        
        if not self.setup_driver():
            return {"success": False, "error": "Falha ao configurar navegador"}
        
        all_results = []
        total_start_time = time.time()
        
        try:
            for cycle in range(num_cycles):
                if cycle % 5 == 0:  # Log a cada 5 ciclos
                    print(f"\n📊 Progresso: Ciclo {cycle + 1}/{num_cycles}")
                
                # Executa ciclo completo
                result = self.execute_complete_cycle(url, username, password, cycle + 1)
                all_results.append(result)
                
                # Pausa mínima entre ciclos
                if cycle < num_cycles - 1:
                    pause_time = random.uniform(0.5, 1.5)
                    time.sleep(pause_time)
            
            total_time = time.time() - total_start_time
            
            # Relatório final
            successful_logins = sum(1 for r in all_results if r["login_success"])
            successful_logouts = sum(1 for r in all_results if r["logout_success"])
            
            print(f"\n🎯 TESTE CONCLUÍDO")
            print("=" * 40)
            print(f"📊 TOTAL DE CICLOS: {len(all_results)}")
            print(f"✅ LOGINS BEM-SUCEDIDOS: {successful_logins}")
            print(f"🚪 LOGOUTS BEM-SUCEDIDOS: {successful_logouts}")
            print(f"📈 TAXA DE SUCESSO LOGIN: {(successful_logins/len(all_results))*100:.1f}%")
            print(f"📈 TAXA DE SUCESSO LOGOUT: {(successful_logouts/len(all_results))*100:.1f}%")
            print(f"⏱️  TEMPO TOTAL: {total_time:.2f}s")
            print(f"⚡ VELOCIDADE: {len(all_results)/total_time:.2f} ciclos/segundo")
            
            if successful_logins > 0:
                login_times = [r["time"] for r in all_results if r["login_success"]]
                avg_time = sum(login_times) / len(login_times)
                print(f"🏎️  TEMPO MÉDIO POR CICLO: {avg_time:.2f}s")
            
            return {
                "success": True,
                "total_cycles": len(all_results),
                "successful_logins": successful_logins,
                "successful_logouts": successful_logouts,
                "total_time": total_time,
                "speed": len(all_results)/total_time,
                "results": all_results
            }
            
        except Exception as e:
            print(f"❌ Erro durante stress test: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            if self.driver:
                print("🔄 Fechando navegador...")
                self.driver.quit()

def main():
    """Execução principal - USUÁRIO ÚNICO"""
    print("💥 STRESS TEST - LOGIN/LOGOUT COMPLETO")
    print("👤 USUÁRIO ÚNICO - FLUXO COMPLETO")
    print("=" * 50)
    
    # Opção de visualização
    visualizar = input("👀 Deseja ver o navegador durante o teste? (s/N): ").strip().lower()
    headless = visualizar not in ['s', 'sim', 'y', 'yes']
    
    tester = LoginLogoutStressTester(headless=headless)
    
    # CONFIGURAÇÃO
    URL = "https://testesqa.g4flex.com.br:9090/"
    USERNAME = "claudio.igor"
    PASSWORD = "cldgor123"
    NUM_CICLOS = 15
    
    print(f"\n⚙️  Configuração:")
    print(f"   URL: {URL}")
    print(f"   Usuário: {USERNAME}")
    print(f"   Ciclos: {NUM_CICLOS}")
    print(f"   Fluxo: Login → Dashboards → Atendente → Perfil → Sair")
    print(f"   Visualização: {'DESATIVADA' if headless else 'ATIVADA'}")
    
    # Executa teste
    results = tester.stress_test_single_user(
        url=URL,
        username=USERNAME,
        password=PASSWORD,
        num_cycles=NUM_CICLOS
    )
    
    if results["success"]:
        print(f"\n🎉 STRESS TEST CONCLUÍDO!")
        print(f"📈 Performance: {results['speed']:.2f} ciclos/segundo")
        print(f"✅ {results['successful_logins']}/{results['total_cycles']} logins bem-sucedidos")
        print(f"🚪 {results['successful_logouts']}/{results['total_cycles']} logouts bem-sucedidos")
    else:
        print(f"\n💥 STRESS TEST FALHOU: {results.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    main()