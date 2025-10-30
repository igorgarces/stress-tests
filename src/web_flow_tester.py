import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

class WebFlowStressTester:
    """
    Testador de stress para fluxo completo de atendimento
    Fluxo: Login → Dashboards → Atendente → Telefonia → Selecionar Filas → Iniciar/Pausar Atendimento
    """
    
    def __init__(self, headless=True):
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
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--user-agent=Stress-Tester-Bot")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)  # Aumentei timeout para 20s
            self.actions = ActionChains(self.driver)
            print("✅ Navegador configurado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao configurar navegador: {e}")
            raise
    
    def login(self, url, username, password):
        """Faz login na aplicação"""
        print(f"🔐 Fazendo login em {url}")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # Aguarda página carregar
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # ⚠️ AJUSTE ESTES SELECTORS para seu sistema de login
            # Tenta encontrar campos de login por diferentes seletores
            selectors_to_try = [
                ("username", [
                    "input[name='username']", "input[name='user']", "input[type='text']",
                    "#username", "#user", "#email", "input#username", "input#user"
                ]),
                ("password", [
                    "input[name='password']", "input[type='password']", 
                    "#password", "input#password"
                ]),
                ("login_button", [
                    "button[type='submit']", "input[type='submit']", "button.login",
                    "#login-btn", ".login-button", "button:contains('Login')"
                ])
            ]
            
            username_field = None
            password_field = None
            login_button = None
            
            # Tenta encontrar os campos
            for field_name, selectors in selectors_to_try:
                for selector in selectors:
                    try:
                        if field_name == "username":
                            username_field = self.wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            break
                        elif field_name == "password":
                            password_field = self.wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            break
                        elif field_name == "login_button":
                            login_button = self.wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            break
                    except:
                        continue
            
            if not username_field or not password_field or not login_button:
                print("❌ Não foi possível encontrar os campos de login")
                print("💡 Tente ajustar os seletores no código")
                raise Exception("Campos de login não encontrados")
            
            # Preenche credenciais
            username_field.clear()
            username_field.send_keys(username)
            
            password_field.clear()
            password_field.send_keys(password)
            
            # Clica no botão de login
            login_button.click()
            
            # Aguarda login completar (redirecionamento ou mudança na página)
            time.sleep(5)
            print("✅ Login realizado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            # Tira screenshot para debug
            try:
                self.driver.save_screenshot("login_error.png")
                print("📸 Screenshot salva como 'login_error.png'")
            except:
                pass
            raise
    
    def navigate_to_dashboards(self):
        """Navega para a aba Dashboards"""
        print("📊 Navegando para Dashboards...")
        
        try:
            # ⚠️ AJUSTE ESTE SELECTOR para sua aplicação
            dashboard_selectors = [
                "//span[contains(text(), 'Dashboards')]",
                "//a[contains(text(), 'Dashboards')]",
                "//li[contains(text(), 'Dashboards')]",
                "//button[contains(text(), 'Dashboards')]",
                "#dashboard-tab",
                ".dashboard-tab"
            ]
            
            dashboard_tab = None
            for selector in dashboard_selectors:
                try:
                    if selector.startswith("//"):
                        dashboard_tab = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        dashboard_tab = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except:
                    continue
            
            if not dashboard_tab:
                raise Exception("Aba Dashboards não encontrada")
            
            dashboard_tab.click()
            time.sleep(3)
            print("✅ Navegação para Dashboards concluída")
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Dashboards: {e}")
            raise
    
    def navigate_to_atendente(self):
        """Navega para a seção Atendente dentro de Dashboards"""
        print("👤 Navegando para Atendente...")
        
        try:
            # ⚠️ AJUSTE ESTE SELECTOR para sua aplicação
            atendente_selectors = [
                "//span[contains(text(), 'Atendente')]",
                "//a[contains(text(), 'Atendente')]",
                "//button[contains(text(), 'Atendente')]",
                "//div[contains(text(), 'Atendente')]",
                "#atendente-tab",
                ".atendente-tab"
            ]
            
            atendente_tab = None
            for selector in atendente_selectors:
                try:
                    if selector.startswith("//"):
                        atendente_tab = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        atendente_tab = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except:
                    continue
            
            if not atendente_tab:
                raise Exception("Seção Atendente não encontrada")
            
            atendente_tab.click()
            time.sleep(3)
            print("✅ Navegação para Atendente concluída")
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Atendente: {e}")
            raise
    
    def navigate_to_telefonia(self):
        """Navega para a seção Telefonia dentro de Atendente"""
        print("📞 Navegando para Telefonia...")
        
        try:
            # ⚠️ AJUSTE ESTE SELECTOR para sua aplicação
            telefonia_selectors = [
                "//span[contains(text(), 'Telefonia')]",
                "//button[contains(text(), 'Telefonia')]",
                "//a[contains(text(), 'Telefonia')]",
                "//div[contains(text(), 'Telefonia')]",
                "#telefonia-tab",
                ".telefonia-tab"
            ]
            
            telefonia_section = None
            for selector in telefonia_selectors:
                try:
                    if selector.startswith("//"):
                        telefonia_section = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        telefonia_section = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except:
                    continue
            
            if not telefonia_section:
                raise Exception("Seção Telefonia não encontrada")
            
            telefonia_section.click()
            time.sleep(3)
            print("✅ Navegação para Telefonia concluída")
            
        except Exception as e:
            print(f"❌ Erro ao navegar para Telefonia: {e}")
            raise
    
    def select_fila_and_start_attendance(self):
        """
        Seleciona fila teste e inicia atendimento
        """
        print("🎯 Selecionando fila e iniciando atendimento...")
        
        try:
            # PASSO 1: Clicar em "Selecionar Filas" na AppBar
            print("   📋 Clicando em 'Selecionar Filas'...")
            
            fila_selectors = [
                "//button[contains(text(), 'Selecionar Filas')]",
                "//span[contains(text(), 'Selecionar Filas')]",
                "//a[contains(text(), 'Selecionar Filas')]",
                "#select-queues",
                ".select-queues-btn",
                "button[aria-label*='filas']",
                "button[title*='filas']"
            ]
            
            select_fila_btn = None
            for selector in fila_selectors:
                try:
                    if selector.startswith("//"):
                        select_fila_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        select_fila_btn = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except:
                    continue
            
            if not select_fila_btn:
                raise Exception("Botão 'Selecionar Filas' não encontrado")
            
            select_fila_btn.click()
            time.sleep(2)
            
            # PASSO 2: Selecionar "Fila Teste"
            print("   🔘 Selecionando 'Fila Teste'...")
            
            fila_test_selectors = [
                "//span[contains(text(), 'Fila Teste')]",
                "//div[contains(text(), 'Fila Teste')]",
                "//label[contains(text(), 'Fila Teste')]",
                "//option[contains(text(), 'Fila Teste')]",
                "#queue-test",
                ".queue-test-item",
                "input[value*='test']"
            ]
            
            fila_test_option = None
            for selector in fila_test_selectors:
                try:
                    if selector.startswith("//"):
                        fila_test_option = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        fila_test_option = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except:
                    continue
            
            if not fila_test_option:
                raise Exception("Opção 'Fila Teste' não encontrada")
            
            fila_test_option.click()
            time.sleep(2)
            
            # PASSO 3: Confirmar seleção (se houver botão de confirmar)
            confirm_selectors = [
                "//button[contains(text(), 'Confirmar')]",
                "//button[contains(text(), 'Aplicar')]",
                "//button[contains(text(), 'Salvar')]",
                "//button[contains(text(), 'OK')]",
                "#confirm-selection",
                ".confirm-btn"
            ]
            
            for selector in confirm_selectors:
                try:
                    if selector.startswith("//"):
                        confirm_btn = self.driver.find_element(By.XPATH, selector)
                    else:
                        confirm_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if confirm_btn.is_displayed():
                        confirm_btn.click()
                        time.sleep(2)
                    break
                except:
                    continue
            
            # PASSO 4: Clicar para "Iniciar Atendimento" no mesmo lugar
            print("   🚀 Clicando para 'Iniciar Atendimento'...")
            
            start_attendance_selectors = [
                "//button[contains(text(), 'Iniciar Atendimento')]",
                "//span[contains(text(), 'Iniciar Atendimento')]",
                "//button[contains(text(), 'Start')]",
                "#start-attendance",
                ".start-attendance-btn",
                "button[aria-label*='iniciar']",
                "button[title*='iniciar']"
            ]
            
            # Tenta clicar no mesmo botão de "Selecionar Filas" novamente
            start_attendance_btn = select_fila_btn  # Pode ser o mesmo botão
            
            # Se não for o mesmo, procura botão específico
            if not start_attendance_btn.get_attribute("innerHTML").lower().count("iniciar"):
                for selector in start_attendance_selectors:
                    try:
                        if selector.startswith("//"):
                            start_attendance_btn = self.wait.until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                        else:
                            start_attendance_btn = self.wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                        break
                    except:
                        continue
            
            if not start_attendance_btn:
                raise Exception("Botão 'Iniciar Atendimento' não encontrado")
            
            start_attendance_btn.click()
            time.sleep(3)
            
            print("✅ Atendimento iniciado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao selecionar fila e iniciar atendimento: {e}")
            raise
    
    def toggle_attendance_pause(self, action="pausar"):
        """
        Clica no mesmo botão para pausar/retomar atendimento
        action: "pausar" ou "retomar"
        """
        print(f"⏸️  Clicando para {action} atendimento...")
        
        try:
            # Procura o mesmo botão usado para iniciar atendimento
            toggle_selectors = [
                "//button[contains(text(), 'Selecionar Filas')]",
                "//button[contains(text(), 'Iniciar Atendimento')]",
                "//button[contains(text(), 'Pausar')]",
                "//button[contains(text(), 'Retomar')]",
                "//span[contains(text(), 'Pausar')]",
                "//span[contains(text(), 'Retomar')]",
                "#attendance-toggle",
                ".attendance-toggle-btn"
            ]
            
            toggle_btn = None
            for selector in toggle_selectors:
                try:
                    if selector.startswith("//"):
                        toggle_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        toggle_btn = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    # Verifica se o botão está visível e clicável
                    if toggle_btn.is_displayed() and toggle_btn.is_enabled():
                        break
                except:
                    continue
            
            if not toggle_btn:
                raise Exception(f"Botão para {action} não encontrado")
            
            # Clica no botão
            toggle_btn.click()
            time.sleep(3)
            
            print(f"✅ Ação '{action}' executada com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao {action} atendimento: {e}")
            raise
    
    def manage_attendance_cycle(self, num_cycles=3):
        """
        Gerencia ciclos de pausa/retomada do atendimento
        """
        print(f"🔄 Gerenciando {num_cycles} ciclos de atendimento...")
        
        cycle_results = []
        
        for cycle in range(num_cycles):
            print(f"   🔄 Ciclo {cycle + 1}/{num_cycles}")
            
            try:
                # FASE 1: Pausar atendimento
                pause_start = time.time()
                self.toggle_attendance_pause("pausar")
                pause_time = time.time() - pause_start
                
                # Aguarda um tempo em pausa
                pause_duration = random.uniform(5, 10)
                print(f"      ⏸️  Em pausa por {pause_duration:.1f}s...")
                time.sleep(pause_duration)
                
                # FASE 2: Retomar atendimento
                resume_start = time.time()
                self.toggle_attendance_pause("retomar")
                resume_time = time.time() - resume_start
                
                # Resultado do ciclo
                cycle_result = {
                    "cycle": cycle + 1,
                    "pause_time": pause_time,
                    "resume_time": resume_time,
                    "pause_duration": pause_duration,
                    "total_time": pause_time + resume_time,
                    "success": True
                }
                
                cycle_results.append(cycle_result)
                print(f"      ✅ Ciclo {cycle + 1}: Pausar={pause_time:.2f}s, Retomar={resume_time:.2f}s")
                
                # Pausa entre ciclos (se não for o último)
                if cycle < num_cycles - 1:
                    wait_time = random.uniform(3, 7)
                    print(f"      ⏰ Aguardando {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"      ❌ Erro no ciclo {cycle + 1}: {e}")
                cycle_results.append({
                    "cycle": cycle + 1,
                    "error": str(e),
                    "success": False
                })
                continue
        
        return cycle_results
    
    def execute_complete_flow(self, url, username, password, num_cycles=3):
        """
        Executa o fluxo completo uma vez
        """
        print("🚀 INICIANDO FLUXO COMPLETO DE ATENDIMENTO")
        print("=" * 60)
        
        flow_start_time = time.time()
        flow_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_time": 0,
            "steps": {},
            "attendance_cycles": [],
            "success": True
        }
        
        try:
            # Setup do navegador
            self.setup_driver()
            
            # PASSO 1: Login
            step_start = time.time()
            self.login(url, username, password)
            flow_results["steps"]["login"] = time.time() - step_start
            
            # PASSO 2: Navegação para Dashboards
            step_start = time.time()
            self.navigate_to_dashboards()
            flow_results["steps"]["dashboards"] = time.time() - step_start
            
            # PASSO 3: Navegação para Atendente
            step_start = time.time()
            self.navigate_to_atendente()
            flow_results["steps"]["atendente"] = time.time() - step_start
            
            # PASSO 4: Navegação para Telefonia
            step_start = time.time()
            self.navigate_to_telefonia()
            flow_results["steps"]["telefonia"] = time.time() - step_start
            
            # PASSO 5: Selecionar fila e iniciar atendimento
            step_start = time.time()
            self.select_fila_and_start_attendance()
            flow_results["steps"]["iniciar_atendimento"] = time.time() - step_start
            
            # PASSO 6: Ciclos de pausa/retomada
            step_start = time.time()
            attendance_cycles = self.manage_attendance_cycle(num_cycles)
            flow_results["steps"]["ciclos_atendimento"] = time.time() - step_start
            flow_results["attendance_cycles"] = attendance_cycles
            
            # Tempo total
            flow_results["total_time"] = time.time() - flow_start_time
            
            print(f"✅ Fluxo completo executado em {flow_results['total_time']:.2f}s")
            
        except Exception as e:
            print(f"❌ Erro no fluxo completo: {e}")
            flow_results["success"] = False
            flow_results["error"] = str(e)
            
        finally:
            # Fecha o navegador
            if self.driver:
                self.driver.quit()
        
        self.results.append(flow_results)
        return flow_results
    
    def stress_test_flow(self, url, username, password, num_users=3, num_cycles=2):
        """
        Teste de stress com múltiplos usuários simulados
        """
        print(f"👥 TESTE DE STRESS COM {num_users} USUÁRIOS SIMULADOS")
        print("=" * 60)
        
        all_results = []
        
        for user in range(num_users):
            print(f"\n🎭 Usuário {user + 1}/{num_users}")
            
            result = self.execute_complete_flow(
                url=url,
                username=username,
                password=password,
                num_cycles=num_cycles
            )
            
            all_results.append(result)
            
            # Pausa entre usuários (exceto o último)
            if user < num_users - 1:
                pause_time = random.uniform(10, 20)
                print(f"⏰ Aguardando {pause_time:.1f}s antes do próximo usuário...")
                time.sleep(pause_time)
        
        self._generate_attendance_report(all_results)
        return all_results
    
    def _generate_attendance_report(self, results):
        """
        Gera relatório detalhado do teste de atendimento
        """
        print("\n" + "=" * 70)
        print("📊 RELATÓRIO DO TESTE DE ATENDIMENTO")
        print("=" * 70)
        
        successful_flows = [r for r in results if r["success"]]
        failed_flows = [r for r in results if not r["success"]]
        
        print(f"👥 Total de usuários simulados: {len(results)}")
        print(f"✅ Fluxos bem-sucedidos: {len(successful_flows)}")
        print(f"❌ Fluxos com falha: {len(failed_flows)}")
        print(f"📈 Taxa de sucesso: {(len(successful_flows) / len(results)) * 100:.1f}%")
        
        if successful_flows:
            # Estatísticas de tempo
            total_times = [flow["total_time"] for flow in successful_flows]
            avg_total_time = sum(total_times) / len(total_times)
            
            print(f"\n⏱️  TEMPO MÉDIO POR FLUXO: {avg_total_time:.2f}s")
            print(f"   ⚡ Mais rápido: {min(total_times):.2f}s")
            print(f"   🐌 Mais lento: {max(total_times):.2f}s")
            
            # Estatísticas por etapa
            steps = ["login", "dashboards", "atendente", "telefonia", "iniciar_atendimento", "ciclos_atendimento"]
            print(f"\n📋 TEMPO MÉDIO POR ETAPA:")
            for step in steps:
                step_times = [flow["steps"][step] for flow in successful_flows if step in flow["steps"]]
                if step_times:
                    avg_step_time = sum(step_times) / len(step_times)
                    print(f"   • {step.replace('_', ' ').title()}: {avg_step_time:.2f}s")
            
            # Estatísticas dos ciclos de atendimento
            all_attendance_cycles = []
            for flow in successful_flows:
                all_attendance_cycles.extend(flow["attendance_cycles"])
            
            successful_cycles = [c for c in all_attendance_cycles if c["success"]]
            if successful_cycles:
                pause_times = [c["pause_time"] for c in successful_cycles]
                resume_times = [c["resume_time"] for c in successful_cycles]
                
                print(f"\n⏸️  ESTATÍSTICAS DOS CICLOS:")
                print(f"   • Total de ciclos: {len(all_attendance_cycles)}")
                print(f"   • Ciclos bem-sucedidos: {len(successful_cycles)}")
                print(f"   • Tempo médio para pausar: {sum(pause_times) / len(pause_times):.2f}s")
                print(f"   • Tempo médio para retomar: {sum(resume_times) / len(resume_times):.2f}s")
        
        print("=" * 70)
