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

class TelefoniaStressTester:
    """
    Teste de stress otimizado para telefonia - CORREÇÃO CALCULO TEMPO
    """
    
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.results = []
        
    def setup_driver(self):
        """Configura o driver do Chrome otimizado"""
        print("🛠️ Configurando navegador...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ Navegador configurado com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            return False
    
    def login(self, url, username, password):
        """ETAPA 1: Login rápido"""
        print(f"🔐 Fazendo login...")
        
        try:
            self.driver.get(url)
            time.sleep(2)
            
            # Login rápido
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
            
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()
            time.sleep(3)
            
            print("✅ Login realizado")
            return True
            
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False

    def navigate_to_dashboards(self):
        """ETAPA 2: Navega para Dashboards"""
        print("📊 Navegando para Dashboards...")
        
        try:
            dashboard_tab = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                    "#root > nav > div > div.navbar-inner > div > ul > li:nth-child(1)"
                ))
            )
            dashboard_tab.click()
            time.sleep(1)
            
            print("✅ Navegação para Dashboards concluída")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Dashboards: {e}")
            return False

    def navigate_to_atendente(self):
        """ETAPA 3: Navega para Atendente"""
        print("👤 Navegando para Atendente...")
        
        try:
            atendente_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/nav/div/div[2]/div/ul/li[1]/div/ul/li[5]/a"
                ))
            )
            atendente_tab.click()
            time.sleep(1)
            
            print("✅ Navegação para Atendente concluída")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Atendente: {e}")
            return False

    def navigate_to_telefonia(self):
        """ETAPA 4: Navega para Telefonia"""
        print("📞 Navegando para Telefonia...")
        
        try:
            telefonia_section = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/div/ul/li[2]/button"
                ))
            )
            telefonia_section.click()
            time.sleep(1)
            
            print("✅ Navegação para Telefonia concluída")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Telefonia: {e}")
            return False
    
    def logar_telefonia(self):
        """ETAPA 5: Clicar em Logar Telefonia"""
        print("📱 Clicando em 'Logar Telefonia'...")
        
        try:
            logar_telefonia_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/a"
                ))
            )
            logar_telefonia_btn.click()
            time.sleep(1)
            
            print("✅ Clicado em 'Logar Telefonia'")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao clicar em 'Logar Telefonia': {e}")
            return False
    
    def selecionar_suporte_com_enter(self):
        """ETAPA 6: Selecionar Suporte usando ENTER - CORRIGIDO"""
        print("🔄 Selecionando Suporte com ENTER...")
        
        try:
            # Primeiro, vamos focar no elemento body para garantir que podemos enviar keys
            body = self.driver.find_element(By.TAG_NAME, "body")
            
            # Clica em "Selecione" para abrir o dropdown
            selecione_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div/div[2]/form/div[1]/div/div[1]/div[2]/div"
                ))
            )
            selecione_btn.click()
            time.sleep(1)
            
            # Aguarda o dropdown abrir
            time.sleep(1)
            
            # Pressiona ENTER no body para selecionar a opção padrão
            print("   ⌨️ Pressionando ENTER para Suporte...")
            body.send_keys(Keys.ENTER)
            time.sleep(0.5)
            
            print("✅ Suporte selecionado com ENTER")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao selecionar Suporte: {e}")
            # Tenta método alternativo
            return self.selecionar_suporte_alternativo()
    
    def selecionar_suporte_alternativo(self):
        """Método alternativo para selecionar Suporte"""
        print("   🔄 Tentando método alternativo para Suporte...")
        
        try:
            # Tenta encontrar e clicar diretamente na opção Suporte
            suporte_opcao = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//div[contains(text(), 'Suporte') or contains(@class, 'suporte')]"
                ))
            )
            suporte_opcao.click()
            time.sleep(0.5)
            print("   ✅ Suporte selecionado (método alternativo)")
            return True
            
        except Exception as e:
            print(f"   ❌ Método alternativo também falhou: {e}")
            return False
    
    def selecionar_ramal_1010_com_enter(self):
        """ETAPA 7: Selecionar Ramal 1010 usando ENTER - CORRIGIDO"""
        print("🔢 Selecionando Ramal 1010 com ENTER...")
        
        try:
            # Primeiro, vamos focar no elemento body
            body = self.driver.find_element(By.TAG_NAME, "body")
            
            # Clica em "Selecione o ramal" para abrir o dropdown
            selecione_ramal = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div/div[2]/form/div[2]/div/div"
                ))
            )
            selecione_ramal.click()
            time.sleep(1)
            
            # Aguarda o dropdown abrir
            time.sleep(1)
            
            # Pressiona ENTER no body para selecionar a opção padrão
            print("   ⌨️ Pressionando ENTER para Ramal 1010...")
            body.send_keys(Keys.ENTER)
            time.sleep(0.5)
            
            print("✅ Ramal 1010 selecionado com ENTER")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao selecionar Ramal 1010: {e}")
            # Tenta método alternativo
            return self.selecionar_ramal_1010_alternativo()
    
    def selecionar_ramal_1010_alternativo(self):
        """Método alternativo para selecionar Ramal 1010"""
        print("   🔄 Tentando método alternativo para Ramal 1010...")
        
        try:
            # Tenta encontrar e clicar diretamente na opção 1010
            ramal_1010_opcao = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//div[contains(text(), '1010') or contains(@class, '1010')]"
                ))
            )
            ramal_1010_opcao.click()
            time.sleep(0.5)
            print("   ✅ Ramal 1010 selecionado (método alternativo)")
            return True
            
        except Exception as e:
            print(f"   ❌ Método alternativo também falhou: {e}")
            return False
    
    def iniciar_atendimento_telefonia(self):
        """ETAPA 8: Iniciar Atendimento Telefonia"""
        print("🚀 Iniciando atendimento telefonia...")
        
        try:
            iniciar_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div/div[2]/form/div[3]/button"
                ))
            )
            iniciar_btn.click()
            time.sleep(2)
            
            print("✅ Atendimento telefonia iniciado")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar atendimento telefonia: {e}")
            return False
    
    def ciclo_pausa_telefonia(self, ciclo_num):
        """ETAPA 9: Ciclo de Pausa/Despausa"""
        print(f"⏸️  Ciclo {ciclo_num}: Pausa/Despausa...")
        
        try:
            # Clica novamente em "Logar Telefonia" para abrir menu de pausa
            self.logar_telefonia()
            time.sleep(0.5)
            
            # PASSO 1: Selecionar pausa
            print("   📝 Selecionando pausa...")
            escolher_pausa = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div[2]/form/div/div/div/div/div[2]/div"
                ))
            )
            escolher_pausa.click()
            time.sleep(0.5)
            
            # PASSO 2: Selecionar "Bacula"
            print("   🕐 Selecionando 'Bacula'...")
            bacula_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div[2]/form/div/div/div/div/div[1]/div[1]"
                ))
            )
            bacula_btn.click()
            time.sleep(0.5)
            
            # PASSO 3: Clicar em "Pausar"
            print("   ⏸️  Clicando em 'Pausar'...")
            pausar_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div[2]/form/div/button"
                ))
            )
            pausar_btn.click()
            time.sleep(2)
            
            # PASSO 4: Aguardar em pausa (tempo reduzido)
            tempo_pausa = random.uniform(3, 5)
            print(f"   ⏰ Em pausa por {tempo_pausa:.1f}s...")
            time.sleep(tempo_pausa)
            
            # PASSO 5: Clicar em "Despausar"
            print("   ▶️  Clicando em 'Despausar'...")
            despausar_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div[2]/form/div/button"
                ))
            )
            despausar_btn.click()
            time.sleep(2)
            
            print(f"   ✅ Ciclo {ciclo_num} concluído")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro no ciclo {ciclo_num}: {e}")
            return False
    
    def execute_complete_flow(self, url, username, password, num_ciclos=3):
        """
        FLUXO COMPLETO - COM CORREÇÃO DO CÁLCULO DE TEMPO
        """
        print("🚀 INICIANDO FLUXO COMPLETO - TELEFONIA CORRIGIDO")
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
            # ETAPA 1: Login - CORREÇÃO DO CÁLCULO DE TEMPO
            print("\n1️⃣  LOGIN")
            step_start = time.time()  # CORREÇÃO AQUI
            if not self.login(url, username, password):
                raise Exception("Falha no login")
            flow_results["steps"]["login"] = time.time() - step_start
            
            # ETAPA 2: Dashboards
            print("\n2️⃣  DASHBOARDS")
            step_start = time.time()
            if not self.navigate_to_dashboards():
                raise Exception("Falha na navegação para Dashboards")
            flow_results["steps"]["dashboards"] = time.time() - step_start
            
            # ETAPA 3: Atendente
            print("\n3️⃣  ATENDENTE")
            step_start = time.time()
            if not self.navigate_to_atendente():
                raise Exception("Falha na navegação para Atendente")
            flow_results["steps"]["atendente"] = time.time() - step_start
            
            # ETAPA 4: Telefonia
            print("\n4️⃣  TELEFONIA")
            step_start = time.time()
            if not self.navigate_to_telefonia():
                raise Exception("Falha na navegação para Telefonia")
            flow_results["steps"]["telefonia"] = time.time() - step_start
            
            # ETAPA 5: Logar Telefonia
            print("\n5️⃣  LOGAR TELEFONIA")
            step_start = time.time()
            if not self.logar_telefonia():
                raise Exception("Falha ao logar telefonia")
            flow_results["steps"]["logar_telefonia"] = time.time() - step_start
            
            # ETAPA 6: Selecionar Suporte COM ENTER CORRIGIDO
            print("\n6️⃣  SELECIONAR SUPORTE (ENTER CORRIGIDO)")
            step_start = time.time()
            if not self.selecionar_suporte_com_enter():
                raise Exception("Falha ao selecionar suporte")
            flow_results["steps"]["selecionar_suporte"] = time.time() - step_start
            
            # ETAPA 7: Selecionar Ramal 1010 COM ENTER CORRIGIDO
            print("\n7️⃣  SELECIONAR RAMAL 1010 (ENTER CORRIGIDO)")
            step_start = time.time()
            if not self.selecionar_ramal_1010_com_enter():
                raise Exception("Falha ao selecionar ramal")
            flow_results["steps"]["selecionar_ramal"] = time.time() - step_start
            
            # ETAPA 8: Iniciar Atendimento
            print("\n8️⃣  INICIAR ATENDIMENTO")
            step_start = time.time()
            if not self.iniciar_atendimento_telefonia():
                raise Exception("Falha ao iniciar atendimento")
            flow_results["steps"]["iniciar_atendimento"] = time.time() - step_start
            
            # ETAPA 9: Ciclos de Pausa/Despausa
            print(f"\n9️⃣  {num_ciclos} CICLOS PAUSA/DESPAUSA")
            step_start = time.time()
            
            ciclos_resultados = []
            for ciclo in range(num_ciclos):
                print(f"   🔄 Ciclo {ciclo + 1}/{num_ciclos}")
                
                ciclo_inicio = time.time()
                sucesso = self.ciclo_pausa_telefonia(ciclo + 1)
                ciclo_tempo = time.time() - ciclo_inicio
                
                ciclo_resultado = {
                    "ciclo": ciclo + 1,
                    "sucesso": sucesso,
                    "tempo": ciclo_tempo
                }
                ciclos_resultados.append(ciclo_resultado)
                
                # Pausa mínima entre ciclos
                if ciclo < num_ciclos - 1:
                    espera = random.uniform(1, 2)
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

def main():
    """Execução principal"""
    print("🎯 TESTE TELEFONIA - CORREÇÃO CÁLCULO TEMPO")
    print("=" * 50)
    
    tester = TelefoniaStressTester(headless=False)
    
    # ⚠️ CONFIGURAÇÃO
    URL = "https://testesqa.g4flex.com.br:9090/"
    USERNAME = "claudio.igor"
    PASSWORD = "cldgor123"
    
    print("Executando fluxo completo telefonia corrigido...")
    
    result = tester.execute_complete_flow(
        url=URL,
        username=USERNAME,
        password=PASSWORD,
        num_ciclos=3
    )
    
    if result["success"]:
        print("\n🎉 SUCESSO! Fluxo telefonia executado.")
        print(f"📊 Tempo total: {result['total_time']:.2f}s")
        print(f"🔄 Ciclos executados: {len(result['ciclos_pausa'])}")
    else:
        print(f"\n❌ FALHA: {result.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    main()