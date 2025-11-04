#!/usr/bin/env python3
"""
Debug simplificado para isolar o problema
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

def test_simple():
    print("🧪 TESTE SIMPLIFICADO")
    print("=" * 40)
    
    # Configuração básica do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    try:
        print("1. 🛠️ Instanciando driver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("   ✅ Driver criado")
        
        print("2. 🌐 Navegando para a URL...")
        driver.get("https://testesqa.g4flex.com.br:9090/")
        print("   ✅ Página carregada")
        
        print("3. ⏳ Aguardando 5 segundos...")
        time.sleep(5)
        
        print("4. 📸 Tentando screenshot...")
        driver.save_screenshot("debug_simple.png")
        print("   ✅ Screenshot salvo")
        
        print("5. 🚪 Fechando driver...")
        driver.quit()
        print("   ✅ Driver fechado")
        
        print("🎉 TESTE SIMPLIFICADO CONCLUÍDO!")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        print(f"❌ Tipo do erro: {type(e)}")

if __name__ == "__main__":
    test_simple()
