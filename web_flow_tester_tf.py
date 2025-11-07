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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TelefoniaStressTester:
    """
    Teste de STRESS para Telefonia - Com múltiplas estratégias para elementos dinâmicos
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

    def digitar_texto_avancado(self, texto, descricao=""):
        """Digita texto no elemento ativo com múltiplas estratégias"""
        print(f"   Digitando '{texto}' em {descricao}...")
        
        estrategias = [
            self._digitar_direto,
            self._digitar_javascript,
            self._digitar_actions
        ]
        
        for i, estrategia in enumerate(estrategias, 1):
            print(f"   Tentativa {i}/3: {estrategia.__name__}")
            try:
                if estrategia(texto):
                    print(f"   Sucesso ao digitar com {estrategia.__name__}")
                    return True
            except Exception as e:
                print(f"   Falha: {e}")
                continue
        
        print(f"   Todas as estrategias falharam para digitar: {texto}")
        return False
    
    def _digitar_direto(self, texto):
        """Digita texto diretamente no elemento ativo"""
        active_element = self.driver.switch_to.active_element
        
        # Verifica se é um campo de input
        tag_name = active_element.tag_name.lower()
        if tag_name not in ['input', 'textarea']:
            return False
        
        # Limpa o campo
        active_element.send_keys(Keys.CONTROL + "a")
        active_element.send_keys(Keys.DELETE)
        time.sleep(0.5)
        
        # Digita caractere por caractere
        for char in texto:
            active_element.send_keys(char)
            time.sleep(0.1)
        
        time.sleep(1)
        return True
    
    def _digitar_javascript(self, texto):
        """Digita texto via JavaScript"""
        active_element = self.driver.switch_to.active_element
        
        # Limpa via JavaScript
        self.driver.execute_script("arguments[0].value = '';", active_element)
        time.sleep(0.5)
        
        # Digita via JavaScript
        self.driver.execute_script(f"arguments[0].value = '{texto}';", active_element)
        
        # Dispara evento de input
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", active_element)
        time.sleep(1)
        return True
    
    def _digitar_actions(self, texto):
        """Digita texto via Actions"""
        active_element = self.driver.switch_to.active_element
        actions = ActionChains(self.driver)
        
        # Limpa o campo
        actions.click(active_element).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        time.sleep(0.5)
        
        # Digita o texto
        actions.send_keys(texto).perform()
        time.sleep(1)
        return True

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

    def navegar_para_dashboards(self):
        """ETAPA 2: Navegar para Dashboards"""
        return self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/nav/div/div[2]/div/ul/li[1]/a",
            'xpath', 
            "Menu Dashboards"
        )

    def navegar_para_atendente(self):
        """ETAPA 3: Navegar para Atendente"""
        return self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/nav/div/div[2]/div/ul/li[1]/div/ul/li[5]/a",
            'xpath', 
            "Opção Atendente"
        )

    def navegar_para_telefonia(self):
        """ETAPA 4: Navegar para Telefonia"""
        return self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/div[2]/div/div[1]/div/ul/li[2]/button",
            'xpath', 
            "Seção Telefonia"
        )

    def configurar_atendimento_telefonia(self):
        """ETAPA 5: Configurar Atendimento Telefonia - COM ESTRATÉGIAS AVANÇADAS"""
        print("\n" + "="*50)
        print("ETAPA 5: CONFIGURAR ATENDIMENTO TELEFONIA")
        print("="*50)
        
        # 1. Abrir Logar Filas
        print("   1. Abrindo Logar Filas...")
        if not self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/a",
            'xpath',
            "Abrir Logar Filas"
        ):
            return False
        
        time.sleep(3)
        
        # 2. Clicar em Selecionar (Suporte)
        print("   2. Clicando em Selecionar Suporte...")
        if not self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div/div[2]/form/div[1]/div/div[1]/div[1]",
            'xpath',
            "Dropdown Suporte"
        ):
            return False
        
        time.sleep(2)
        
        # 3. Digitar "suporte" com estratégias avançadas
        print("   3. Digitando 'suporte'...")
        if not self.digitar_texto_avancado("suporte", "campo Suporte"):
            return False
        
        # 4. Pressionar ENTER
        print("   4. Pressionando ENTER...")
        try:
            active_element = self.driver.switch_to.active_element
            active_element.send_keys(Keys.ENTER)
            print("   ✓ ENTER pressionado para suporte")
            time.sleep(2)
        except Exception as e:
            print(f"   ✗ Erro ao pressionar ENTER: {e}")
            return False
        
        # 5. Clicar no elemento específico
        print("   5. Clicando no elemento específico...")
        if not self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div/div[1]",
            'xpath',
            "Elemento específico pós-suporte"
        ):
            return False
        
        time.sleep(2)
        
        # 6. Clicar em Selecionar Ramal
        print("   6. Clicando em Selecionar Ramal...")
        if not self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div/div[2]/form/div[2]/div/div/div[1]",
            'xpath',
            "Dropdown Ramal"
        ):
            return False
        
        time.sleep(2)
        
        # 7. Digitar "1718" com estratégias avançadas
        print("   7. Digitando '1718'...")
        if not self.digitar_texto_avancado("1718", "campo Ramal"):
            return False
        
        # 8. Pressionar ENTER
        print("   8. Pressionando ENTER...")
        try:
            active_element = self.driver.switch_to.active_element
            active_element.send_keys(Keys.ENTER)
            print("   ✓ ENTER pressionado para ramal")
            time.sleep(2)
        except Exception as e:
            print(f"   ✗ Erro ao pressionar ENTER: {e}")
            return False
        
        # 9. Clicar em Iniciar Atendimento
        print("   9. Clicando em Iniciar Atendimento...")
        if not self.tentar_clique_multiplas_estrategias(
            "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div/div[2]/form/div[3]/button",
            'xpath',
            "Botão Iniciar Atendimento"
        ):
            return False
        
        time.sleep(3)
        
        print("   ✓ Atendimento telefonia configurado e iniciado com sucesso")
        return True

    def ciclo_pausa_despausa(self, numero_ciclo):
        """ETAPA 6: Ciclo de Pausa/Despausa - COM ESTRATÉGIAS AVANÇADAS"""
        print(f"\n" + "="*50)
        print(f"ETAPA 6: CICLO PAUSA/DESPAUSA #{numero_ciclo}")
        print("="*50)
        
        try:
            # 1. Selecionar pausa
            print("   1. Selecionando pausa...")
            if not self.tentar_clique_multiplas_estrategias(
                "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div[2]/form/div/div/div/div/div[1]",
                'xpath',
                "Dropdown Pausa"
            ):
                return False
            
            time.sleep(2)
            
            # 2. Digitar "bacula" com estratégias avançadas
            print("   2. Digitando 'bacula'...")
            if not self.digitar_texto_avancado("bacula", "campo Pausa"):
                return False
            
            # 3. Pressionar ENTER
            print("   3. Pressionando ENTER...")
            try:
                active_element = self.driver.switch_to.active_element
                active_element.send_keys(Keys.ENTER)
                print("   ✓ ENTER pressionado para pausa")
                time.sleep(2)
            except Exception as e:
                print(f"   ✗ Erro ao pressionar ENTER: {e}")
                return False
            
            # 4. Clicar em Pausar
            print("   4. Clicando em Pausar...")
            if not self.tentar_clique_multiplas_estrategias(
                "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div[2]/form/div/button",
                'xpath',
                "Botão Pausar"
            ):
                return False
            
            time.sleep(3)
            
            # 5. Clicar em Despausar
            print("   5. Clicando em Despausar...")
            if not self.tentar_clique_multiplas_estrategias(
                "//*[@id='root']/div[2]/div/div[1]/nav/div/div/ul[1]/li[9]/div/div[2]/form/div/button",
                'xpath',
                "Botão Despausar"
            ):
                return False
            
            time.sleep(2)
            
            print(f"   ✓ Ciclo {numero_ciclo} concluído com sucesso")
            return True
            
        except Exception as e:
            print(f"   ✗ Erro no ciclo {numero_ciclo}: {e}")
            return False

    def executar_fluxo_completo(self, num_ciclos_pausa=2):
        """Executa o fluxo completo do teste com estratégias avançadas"""
        print("INICIANDO TESTE DE TELEFONIA - ESTRATÉGIAS AVANÇADAS")
        print("="*60)
        
        if not self.setup_driver():
            return {"sucesso": False, "erro": "Falha ao configurar navegador"}
        
        resultados = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tempo_total": 0,
            "etapas": {},
            "ciclos_pausa": [],
            "sucesso": True
        }
        
        inicio_tempo = time.time()
        
        try:
            # ETAPA 1: Login
            inicio_etapa = time.time()
            if not self.login_rapido("https://testesqa.g4flex.com.br:9090/", "claudio.igor", "cldgor123"):
                raise Exception("Falha no login")
            resultados["etapas"]["login"] = time.time() - inicio_etapa
            
            # ETAPA 2: Dashboards
            inicio_etapa = time.time()
            if not self.navegar_para_dashboards():
                raise Exception("Falha ao navegar para Dashboards")
            resultados["etapas"]["dashboards"] = time.time() - inicio_etapa
            
            # ETAPA 3: Atendente
            inicio_etapa = time.time()
            if not self.navegar_para_atendente():
                raise Exception("Falha ao navegar para Atendente")
            resultados["etapas"]["atendente"] = time.time() - inicio_etapa
            
            # ETAPA 4: Telefonia
            inicio_etapa = time.time()
            if not self.navegar_para_telefonia():
                raise Exception("Falha ao navegar para Telefonia")
            resultados["etapas"]["telefonia"] = time.time() - inicio_etapa
            
            # ETAPA 5: Configurar Atendimento Telefonia
            inicio_etapa = time.time()
            if not self.configurar_atendimento_telefonia():
                raise Exception("Falha ao configurar atendimento telefonia")
            resultados["etapas"]["configurar_atendimento"] = time.time() - inicio_etapa
            
            # ETAPA 6: Ciclos de Pausa/Despausa
            print(f"\nINICIANDO {num_ciclos_pausa} CICLOS DE PAUSA/DESPAUSA")
            inicio_etapa = time.time()
            
            ciclos_resultados = []
            for i in range(num_ciclos_pausa):
                ciclo_inicio = time.time()
                sucesso = self.ciclo_pausa_despausa(i + 1)
                ciclo_tempo = time.time() - ciclo_inicio
                
                ciclos_resultados.append({
                    "ciclo": i + 1,
                    "sucesso": sucesso,
                    "tempo": ciclo_tempo
                })
                
                if i < num_ciclos_pausa - 1:
                    espera = random.uniform(2, 3)
                    print(f"   Aguardando {espera:.1f}s antes do próximo ciclo...")
                    time.sleep(espera)
            
            resultados["etapas"]["ciclos_pausa"] = time.time() - inicio_etapa
            resultados["ciclos_pausa"] = ciclos_resultados
            
            resultados["tempo_total"] = time.time() - inicio_tempo
            print(f"\n FLUXO CONCLUÍDO EM {resultados['tempo_total']:.2f}s")
            
        except Exception as e:
            print(f"\n ERRO NO FLUXO: {e}")
            resultados["sucesso"] = False
            resultados["erro"] = str(e)
        
        finally:
            if self.driver:
                print("\nFechando navegador...")
                self.driver.quit()
        
        self.results.append(resultados)
        return resultados

def main():
    """Execução principal - Versão Avançada"""
    print("TESTE DE TELEFONIA - ESTRATÉGIAS AVANÇADAS")
    print("Multiplos metodos para contornar elementos dinamicos")
    print("=" * 50)
    
    visualizar = input("Deseja ver o navegador durante o teste? (s/N): ").strip().lower()
    headless = visualizar not in ['s', 'sim', 'y', 'yes']
    
    tester = TelefoniaStressTester(headless=headless)
    
    print(f"\nConfiguracao Avancada:")
    print(f"   Estrategias: 4 metodos clique + 3 metodos digitacao")
    print(f"   Timeout: 15 segundos")
    print(f"   Visualizacao: {'DESATIVADA' if headless else 'ATIVADA'}")
    
    resultado = tester.executar_fluxo_completo(num_ciclos_pausa=2)
    
    if resultado["sucesso"]:
        print("\n TESTE CONCLUÍDO COM SUCESSO!")
        print(f"  Tempo total: {resultado['tempo_total']:.2f}s")
        print(f" Ciclos executados: {len(resultado['ciclos_pausa'])}")
        
        print("\n ESTATÍSTICAS DETALHADAS:")
        for etapa, tempo in resultado["etapas"].items():
            print(f"   {etapa}: {tempo:.2f}s")
        
        ciclos_sucesso = sum(1 for ciclo in resultado["ciclos_pausa"] if ciclo["sucesso"])
        print(f"\n Ciclos bem-sucedidos: {ciclos_sucesso}/{len(resultado['ciclos_pausa'])}")
        
    else:
        print(f"\n FALHA NO TESTE: {resultado.get('erro', 'Erro desconhecido')}")

if __name__ == "__main__":
    main()