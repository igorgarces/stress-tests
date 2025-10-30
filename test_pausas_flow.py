#!/usr/bin/env python3
"""
Script simplificado para testar fluxo de pausas
"""

import sys
import os

# Adiciona o diretório atual ao path para importar src
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.web_flow_tester import WebFlowStressTester
    print("✅ Módulos importados com sucesso")
except ImportError as e:
    print(f"❌ Erro na importação: {e}")
    print("📁 Verificando estrutura...")
    
    # Lista arquivos para debug
    print("Arquivos em src/:")
    if os.path.exists("src"):
        for file in os.listdir("src"):
            if file.endswith(".py"):
                print(f"  - {file}")
    else:
        print("  ❌ Pasta src/ não existe")
    
    sys.exit(1)

def main():
    print("🎯 TESTE ESPECÍFICO: FLUXO DE PAUSAS")
    print("=====================================")
    
    # Configuração básica - AJUSTE ESTES VALORES!
    TEST_CONFIG = {
        "url": "https://sua-aplicacao.com/login",  # ⚠️ MUDE AQUI
        "username": "seu_usuario",                 # ⚠️ MUDE AQUI  
        "password": "sua_senha",                   # ⚠️ MUDE AQUI
        "num_users": 2,                            # Comece com 2 usuários
        "pause_cycles": 2                          # 2 ciclos de pausa por usuário
    }
    
    print(f"🌐 Aplicação: {TEST_CONFIG['url']}")
    print(f"👤 Usuário: {TEST_CONFIG['username']}")
    print(f"👥 Usuários simulados: {TEST_CONFIG['num_users']}")
    print(f"⏸️  Ciclos de pausa por usuário: {TEST_CONFIG['pause_cycles']}")
    print("")
    print("⚠️  IMPORTANTE: Você precisa ajustar:")
    print("   1. URL da aplicação")
    print("   2. Credenciais de login") 
    print("   3. Selectors no arquivo web_flow_tester.py")
    print("")
    
    confirm = input("❓ Continuar com teste DEMO? (s/N): ")
    if confirm.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Teste cancelado")
        return
    
    tester = WebFlowStressTester(headless=True)
    
    try:
        print("🚀 Iniciando teste...")
        results = tester.stress_test_flow(
            url=TEST_CONFIG["url"],
            username=TEST_CONFIG["username"],
            password=TEST_CONFIG["password"],
            num_users=TEST_CONFIG["num_users"],
            num_pause_cycles=TEST_CONFIG["pause_cycles"]
        )
        
        print("\n🎉 Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("\n🔧 Para resolver:")
        print("   1. Instale dependências: pip install selenium webdriver-manager")
        print("   2. Configure URL e credenciais neste script")
        print("   3. Ajuste os selectors no web_flow_tester.py")

if __name__ == "__main__":
    main()
