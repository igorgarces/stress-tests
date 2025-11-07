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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AtendimentoStressTester:
    """
    Teste de STRESS - Com múltiplas estratégias para elementos dinâmicos
    """
    
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.results = []
        
    def setup_driver(self):
        """Configura o driver do Chrome"""
        print("Configurando navegador...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            print("   Modo: INVISIVEL")
        else:
            print("   Modo: VISIVEL")
            
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
            print("Navegador configurado com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao configurar navegador: {e}")
            return False
    
    def fechar_notificacoes(self):
        """Fecha notificações/toasts que podem estar cobrindo elementos"""
        try:
            print("   Verificando notificacoes...")
            toast_selectors = [
                "//div[contains(@class, 'Toastify__toast')]",
                "//div[contains(@class, 'notification')]",
                "//div[contains(@class, 'alert')]",
                "//div[contains(@class, 'toast')]",
                "//*[contains(text(), 'Fechar')]",
                "//button[contains(@class, 'close')]"
            ]
            
            for selector in toast_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            print("   Fechando notificacao...")
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(0.5)
                            return True
                except:
                    continue
            return False
        except Exception as e:
            print(f"   Erro ao verificar notificacoes: {e}")
            return False
    
    def esperar_carregamento(self, tempo=2):
        """Aguarda carregamento da página"""
        print(f"   Aguardando carregamento ({tempo}s)...")
        time.sleep(tempo)
    
    def tentar_clique_multiplas_estrategias(self, seletor, tipo='xpath', descricao=""):
        """Tenta clicar em elemento usando múltiplas estratégias"""
        print(f"   Tentando clicar em: {descricao}")
        
        estrategias = [
            self._clicar_direto,
            self._clicar_javascript,
            self._clicar_actions,
            self._clicar_coordenadas
        ]
        
        for i, estrategia in enumerate(estrategias, 1):
            print(f"   Tentativa {i}/4: {estrategia.__name__}")
            try:
                if estrategia(seletor, tipo):
                    print(f"   Sucesso com {estrategia.__name__}")
                    return True
            except Exception as e:
                print(f"   Falha: {e}")
                continue
        
        print(f"   Todas as estrategias falharam para: {descricao}")
        return False
    
    def _clicar_direto(self, seletor, tipo='xpath'):
        """Tenta clique direto"""
        if tipo == 'xpath':
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, seletor)))
        else:
            elemento = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
        elemento.click()
        return True
    
    def _clicar_javascript(self, seletor, tipo='xpath'):
        """Tenta clique via JavaScript"""
        if tipo == 'xpath':
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, seletor)))
        else:
            elemento = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
        self.driver.execute_script("arguments[0].click();", elemento)
        return True
    
    def _clicar_actions(self, seletor, tipo='xpath'):
        """Tenta clique via Actions"""
        from selenium.webdriver.common.action_chains import ActionChains
        if tipo == 'xpath':
            elemento = self.wait.until(EC.element_to_be_clickable((By.XPATH, seletor)))
        else:
            elemento = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
        actions = ActionChains(self.driver)
        actions.move_to_element(elemento).click().perform()
        return True
    
    def _clicar_coordenadas(self, seletor, tipo='xpath'):
        """Tenta clique via coordenadas"""
        if tipo == 'xpath':
            elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, seletor)))
        else:
            elemento = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
        
        # Obtém coordenadas e clica via JavaScript
        x = elemento.location['x'] + elemento.size['width'] // 2
        y = elemento.location['y'] + elemento.size['height'] // 2
        
        script = f"""
        var element = document.elementFromPoint({x}, {y});
        if (element) {{
            element.click();
            return true;
        }}
        return false;
        """
        result = self.driver.execute_script(script)
        return bool(result)
    
    def selecionar_ramal_avancado(self):
        """ETAPA 3: Seleção avançada de ramal - VERSÃO CORRIGIDA"""
        print("   Iniciando selecao avancada de ramal...")
        
        # Seletor do dropdown de ramal (para abrir a lista)
        seletor_dropdown = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[10]/div/div/form/div/div/div/div[1]"
        
        # 1. Primeiro, clicar para abrir o dropdown
        print("   Clicando para abrir dropdown de ramais...")
        if not self.tentar_clique_multiplas_estrategias(seletor_dropdown, 'xpath', "Abrir dropdown ramais"):
            print("   Nao foi possivel abrir o dropdown")
            return False
        
        # Aguarda a lista carregar
        self.esperar_carregamento(2)
        
        # 2. Estratégias específicas para selecionar um ramal
        print("   Procurando opcoes de ramal...")
        
        # ESTRATÉGIA 1: Buscar por elementos de lista específicos
        opcoes_ramal_selectors = [
            "//div[contains(@class, 'dropdown-menu')]//div[contains(@class, 'dropdown-item')]",
            "//div[contains(@class, 'menu')]//div[contains(@class, 'item')]",
            "//div[contains(@class, 'select__menu')]//div[contains(@class, 'option')]",
            "//div[contains(@class, 'ramal')]",
            "//div[contains(text(), '17')]",  # Busca por números que começam com 17
            "//*[contains(text(), '1787')]",  # Busca específica pelo ramal
            "//div[@role='option']",
            "//div[@role='listbox']//div",
        ]
        
        for selector in opcoes_ramal_selectors:
            try:
                opcoes = self.driver.find_elements(By.XPATH, selector)
                print(f"   Encontrados {len(opcoes)} elementos com selector: {selector}")
                
                for i, opcao in enumerate(opcoes):
                    if opcao.is_displayed() and opcao.is_enabled():
                        texto = opcao.text
                        print(f"   Opcao {i+1}: '{texto}'")
                        
                        # Tenta clicar se contém número de ramal
                        if any(char.isdigit() for char in texto):
                            print(f"   Tentando selecionar ramal: {texto}")
                            try:
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", opcao)
                                time.sleep(0.5)
                                self.driver.execute_script("arguments[0].click();", opcao)
                                print(f"   Ramal selecionado: {texto}")
                                self.esperar_carregamento(2)
                                return True
                            except Exception as e:
                                print(f"   Erro ao clicar: {e}")
                                continue
            except Exception as e:
                print(f"   Erro com selector {selector}: {e}")
                continue
        
        # ESTRATÉGIA 2: Usar teclado para navegar
        print("   Tentando navegacao por teclado...")
        try:
            body = self.driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            body.send_keys(Keys.ENTER)
            time.sleep(1)
            
            # Verifica se alguma opção foi selecionada
            dropdown_atual = self.driver.find_element(By.XPATH, seletor_dropdown)
            if dropdown_atual.text.strip() and dropdown_atual.text != "":
                print(f"   Ramal selecionado via teclado: {dropdown_atual.text}")
                return True
        except Exception as e:
            print(f"   Navegacao por teclado falhou: {e}")
        
        # ESTRATÉGIA 3: Tentar clicar em qualquer opção visível
        print("   Tentando clicar em qualquer opcao disponivel...")
        try:
            # Busca todos os elementos clicáveis no dropdown
            opcoes = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'dropdown-menu')]//*")
            for opcao in opcoes:
                if opcao.is_displayed() and opcao.is_enabled():
                    try:
                        texto = opcao.text
                        if texto.strip():
                            print(f"   Clicando em: '{texto}'")
                            self.driver.execute_script("arguments[0].click();", opcao)
                            self.esperar_carregamento(2)
                            print("   Opcao selecionada")
                            return True
                    except:
                        continue
        except Exception as e:
            print(f"   Estrategia 3 falhou: {e}")
        
        print("   Todas as estrategias falharam na selecao do ramal")
        return False

    def login_rapido(self, url, username, password):
        """ETAPA 1: Login rápido"""
        try:
            print(f"   Acessando: {url}")
            self.driver.get(url)
            self.esperar_carregamento(2)
            
            self.fechar_notificacoes()
            
            # Preenche login
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
            
            print(f"   Preenchendo usuario: {username}")
            username_field.clear()
            username_field.send_keys(username)
            
            print("   Preenchendo senha: ***")
            password_field.clear()
            password_field.send_keys(password)
            
            print("   Clicando em Login...")
            login_button.click()
            self.esperar_carregamento(3)
            
            self.fechar_notificacoes()
            
            # Verificação de sucesso
            if "login" not in self.driver.current_url.lower():
                print("   Login bem-sucedido!")
                return True
            else:
                print("   Login falhou")
                return False
            
        except Exception as e:
            print(f"   Erro no login: {e}")
            return False

    def clicar_iniciar_atendimento(self):
        """ETAPA 2: Clicar em 'Iniciar Atendimento'"""
        seletor = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[10]/a"
        return self.tentar_clique_multiplas_estrategias(seletor, 'xpath', "Iniciar Atendimento")

    def clicar_conectar(self):
        """ETAPA 4: Clicar em 'Conectar'"""
        seletor = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[10]/div/div/form/button"
        sucesso = self.tentar_clique_multiplas_estrategias(seletor, 'xpath', "Conectar")
        if sucesso:
            self.esperar_carregamento(4)  # Tempo maior para conectar
        return sucesso

    def clicar_desconectar(self):
        """ETAPA 5: Clicar em 'Desconectar'"""
        seletor = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[1]/li[10]/div/div/div[2]"
        sucesso = self.tentar_clique_multiplas_estrategias(seletor, 'xpath', "Desconectar")
        if sucesso:
            self.esperar_carregamento(3)  # Tempo para desconectar
        return sucesso

    def fazer_logout(self):
        """ETAPA FINAL: Fazer logout"""
        try:
            print("   Fazendo logout...")
            self.fechar_notificacoes()
            
            # Clica no perfil
            perfil_seletor = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[2]/li/a"
            if self.tentar_clique_multiplas_estrategias(perfil_seletor, 'xpath', "Perfil"):
                self.esperar_carregamento(1)
                
                # Clica em Sair
                sair_seletor = "//*[@id=\"root\"]/div[2]/div/div[1]/nav/div/div/ul[2]/li/div/button[4]"
                if self.tentar_clique_multiplas_estrategias(sair_seletor, 'xpath', "Sair"):
                    self.esperar_carregamento(2)
                    print("   Logout realizado")
                    return True
            
            print("   Logout parcialmente bem-sucedido")
            return False
            
        except Exception as e:
            print(f"   Erro no logout: {e}")
            return False

    def execute_complete_cycle(self, url, username, password, cycle_number):
        """Executa UM ciclo completo com estratégias avançadas"""
        print(f"\nCICLO {cycle_number}")
        print("=" * 40)
        print("   Usando estrategias avancadas...")
        
        cycle_start = time.time()
        
        # ETAPA 1: Login
        login_success = self.login_rapido(url, username, password)
        
        if login_success:
            self.esperar_carregamento(2)
            
            # ETAPA 2: Iniciar Atendimento
            iniciar_success = self.clicar_iniciar_atendimento()
            
            if iniciar_success:
                # ETAPA 3: Seleção Avançada de Ramal
                ramal_success = self.selecionar_ramal_avancado()
                
                if ramal_success:
                    # ETAPA 4: Conectar
                    conectar_success = self.clicar_conectar()
                    
                    if conectar_success:
                        # Aguarda tempo conectado
                        tempo_conectado = random.uniform(5, 10)
                        print(f"   Aguardando {tempo_conectado:.1f}s conectado...")
                        time.sleep(tempo_conectado)
                        
                        # ETAPA 5: Desconectar
                        desconectar_success = self.clicar_desconectar()
                        
                        if desconectar_success:
                            print("   Ciclo completo bem-sucedido!")
                        else:
                            print("   Falha ao desconectar")
                    else:
                        print("   Falha ao conectar")
                else:
                    print("   Falha na selecao do ramal")
            else:
                print("   Falha ao iniciar atendimento")
            
            # Logout independente do resultado
            self.fazer_logout()
        else:
            print("   Login falhou")
            self.driver.get(url)
            self.esperar_carregamento(2)
        
        cycle_time = time.time() - cycle_start
        
        result = {
            "cycle": cycle_number,
            "login_success": login_success,
            "iniciar_success": iniciar_success if login_success else False,
            "ramal_success": ramal_success if iniciar_success else False,
            "conectar_success": conectar_success if ramal_success else False,
            "desconectar_success": desconectar_success if conectar_success else False,
            "time": cycle_time
        }
        
        print(f"   Ciclo concluido em {cycle_time:.2f}s")
        return result
    
    def stress_test_atendimento(self, url, username, password, num_cycles=6):
        """
        TESTE DE STRESS - Com estratégias avançadas
        """
        print("STRESS TEST AVANCADO")
        print(f"Usuario: {username}")
        print(f"Ciclos: {num_cycles}")
        print(f"Multiplas estrategias para elementos dinamicos")
        print(f"4 metodos de clique + 3 estrategias dropdown")
        if not self.headless:
            print("MODO VISUALIZACAO ATIVADO")
        print("=" * 60)
        
        if not self.setup_driver():
            return {"success": False, "error": "Falha ao configurar navegador"}
        
        all_results = []
        total_start_time = time.time()
        
        try:
            for cycle in range(num_cycles):
                print(f"\nPROGRESSO: Ciclo {cycle + 1}/{num_cycles}")
                
                result = self.execute_complete_cycle(url, username, password, cycle + 1)
                all_results.append(result)
                
                # Pausa entre ciclos
                if cycle < num_cycles - 1:
                    pause_time = random.uniform(3, 6)
                    print(f"Aguardando {pause_time:.1f}s antes do proximo ciclo...")
                    time.sleep(pause_time)
            
            total_time = time.time() - total_start_time
            
            # Relatório detalhado
            successful_logins = sum(1 for r in all_results if r["login_success"])
            successful_iniciar = sum(1 for r in all_results if r["iniciar_success"])
            successful_ramal = sum(1 for r in all_results if r["ramal_success"])
            successful_conectar = sum(1 for r in all_results if r["conectar_success"])
            successful_desconectar = sum(1 for r in all_results if r["desconectar_success"])
            
            print(f"\nRELATORIO FINAL")
            print("=" * 50)
            print(f"TOTAL DE CICLOS: {len(all_results)}")
            print(f"LOGINS: {successful_logins}/{len(all_results)}")
            print(f"INICIAR ATENDIMENTO: {successful_iniciar}/{successful_logins}")
            print(f"SELECIONAR RAMAL: {successful_ramal}/{successful_iniciar}")
            print(f"CONECTAR: {successful_conectar}/{successful_ramal}")
            print(f"DESCONECTAR: {successful_desconectar}/{successful_conectar}")
            print(f"TEMPO TOTAL: {total_time:.2f}s")
            print(f"VELOCIDADE: {len(all_results)/total_time:.2f} ciclos/segundo")
            
            return {
                "success": True,
                "total_cycles": len(all_results),
                "successful_logins": successful_logins,
                "successful_iniciar": successful_iniciar,
                "successful_ramal": successful_ramal,
                "successful_conectar": successful_conectar,
                "successful_desconectar": successful_desconectar,
                "total_time": total_time,
                "speed": len(all_results)/total_time,
                "results": all_results
            }
            
        except Exception as e:
            print(f"Erro durante stress test: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            if self.driver:
                print("Fechando navegador...")
                self.driver.quit()

def main():
    """Execução principal - Versão Avançada"""
    print("STRESS TEST - ESTRATEGIAS AVANCADAS")
    print("Multiplos metodos para contornar elementos dinamicos")
    print("=" * 50)
    
    visualizar = input("Deseja ver o navegador durante o teste? (s/N): ").strip().lower()
    headless = visualizar not in ['s', 'sim', 'y', 'yes']
    
    tester = AtendimentoStressTester(headless=headless)
    
    URL = "https://testesqa.g4flex.com.br:9090/"
    USERNAME = "claudio.igor"
    PASSWORD = "cldgor123"
    NUM_CICLOS = 5
    
    print(f"\nConfiguracao Avancada:")
    print(f"   URL: {URL}")
    print(f"   Usuario: {USERNAME}")
    print(f"   Ciclos: {NUM_CICLOS}")
    print(f"   Estrategias: 4 metodos clique + 3 dropdown")
    print(f"   Timeout: 15 segundos")
    print(f"   Visualizacao: {'DESATIVADA' if headless else 'ATIVADA'}")
    
    results = tester.stress_test_atendimento(
        url=URL,
        username=USERNAME,
        password=PASSWORD,
        num_cycles=NUM_CICLOS
    )
    
    if results["success"]:
        print(f"\nTESTE CONCLUIDO COM ESTRATEGIAS AVANCADAS!")
        taxa_sucesso = (results['successful_desconectar'] / results['total_cycles']) * 100
        print(f"Taxa de sucesso geral: {taxa_sucesso:.1f}%")
    else:
        print(f"\nTESTE FALHOU: {results.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    main()