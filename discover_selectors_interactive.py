#!/usr/bin/env python3
"""
Ferramenta interativa para descobrir seletores
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class SelectorDiscoverer:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def setup_driver(self, headless=False):
        """Configura o navegador"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver
    
    def discover_element(self, url, description):
        """
        Ajuda a descobrir seletores para um elemento específico
        """
        print(f"\n🎯 Procurando: {description}")
        print("=" * 50)
        
        self.driver.get(url)
        time.sleep(3)
        
        print("🔍 Inspecione o elemento no navegador e digite:")
        print("1. Seletor CSS (ex: #username, .login-btn)")
        print("2. XPath (ex: //button[contains(text(), 'Login')])")
        print("3. 'sair' para terminar")
        
        while True:
            selector_type = input("\n📝 Tipo de seletor [css/xpath]: ").strip().lower()
            
            if selector_type == 'sair':
                break
                
            selector = input("🔧 Digite o seletor: ").strip()
            
            if selector == 'sair':
                break
            
            try:
                if selector_type == 'css' or not selector.startswith('//'):
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                else:
                    element = self.driver.find_element(By.XPATH, selector)
                
                print(f"✅ Elemento encontrado!")
                print(f"📋 Tag: {element.tag_name}")
                print(f"🔖 Texto: {element.text}")
                print(f"🎯 Seletor: {selector}")
                
                # Destaca o elemento
                self.driver.execute_script("arguments[0].style.border='3px solid red'", element)
                time.sleep(2)
                
                save = input("💾 Salvar este seletor? (s/N): ").strip().lower()
                if save in ['s', 'sim', 'y', 'yes']:
                    return selector
                    
            except Exception as e:
                print(f"❌ Elemento não encontrado: {e}")
                print("💡 Tente outro seletor")
        
        return None
    
    def close(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()

def main():
    print("🎯 DESCOBRIDOR DE SELECTORS")
    print("=" * 50)
    
    url = input("🌐 URL da aplicação: ").strip()
    if not url:
        print("❌ URL é obrigatória!")
        return
    
    discoverer = SelectorDiscoverer()
    
    try:
        discoverer.setup_driver(headless=False)
        
        selectors = {}
        elements_to_find = [
            "Campo de usuário",
            "Campo de senha", 
            "Botão de login",
            "Aba Dashboards",
            "Seção Atendente",
            "Seção Telefonia",
            "Botão 'Selecionar Filas'",
            "Opção 'Fila Teste'",
            "Botão 'Iniciar Atendimento'",
            "Botão 'Pausar/Retomar'"
        ]
        
        for element_desc in elements_to_find:
            selector = discoverer.discover_element(url, element_desc)
            if selector:
                selectors[element_desc] = selector
                print(f"✅ {element_desc}: {selector}")
            else:
                print(f"⏭️  Pulando {element_desc}")
            
            cont = input("\n▶️  Continuar para próximo elemento? (s/N): ").strip().lower()
            if cont not in ['s', 'sim', 'y', 'yes']:
                break
        
        # Mostra resumo
        print("\n📋 SELECTORS ENCONTRADOS:")
        print("=" * 50)
        for desc, selector in selectors.items():
            print(f"• {desc}: {selector}")
            
        # Gera código Python
        print("\n🐍 CÓDIGO PARA web_flow_tester.py:")
        print("=" * 50)
        for desc, selector in selectors.items():
            var_name = desc.lower().replace(' ', '_').replace("'", "")
            print(f"# {desc}")
            print(f"{var_name}_selector = \"{selector}\"")
        
    finally:
        discoverer.close()

if __name__ == "__main__":
    main()
