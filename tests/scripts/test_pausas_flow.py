#!/usr/bin/env python3
"""
Script simplificado para testar fluxo de pausas
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.web_flow_tester import WebFlowStressTester
from configs.web_test_config import WEB_TEST_CONFIG

def main():
    print("🎯 TESTE ESPECÍFICO: FLUXO DE PAUSAS")
    print("=====================================")
    
    config = WEB_TEST_CONFIG
    
    print(f"🌐 Aplicação: {config['application_url']}")
    print(f"👤 Usuário: {config['credentials']['username']}")
    print(f"👥 Usuários simulados: {config['test_parameters']['num_users']}")
    print(f"⏸️  Ciclos de pausa por usuário: {config['test_parameters']['pause_cycles_per_user']}")
    print("")
    
    confirm = input("❓ Executar teste? (s/N): ")
    if confirm.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Teste cancelado")
        return
    
    tester = WebFlowStressTester(
        headless=config['test_parameters']['headless']
    )
    
    try:
        results = tester.stress_test_flow(
            url=config['application_url'],
            username=config['credentials']['username'],
            password=config['credentials']['password'],
            num_users=config['test_parameters']['num_users'],
            num_pause_cycles=config['test_parameters']['pause_cycles_per_user']
        )
        
        print("\n🎉 Teste concluído!")
        print("💡 Verifique o relatório acima para análise de performance")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("\n🔧 Solução de problemas:")
        print("   1. Verifique se o Chrome está instalado")
        print("   2. Confirme as credenciais em configs/web_test_config.py")
        print("   3. Ajuste os selectors para sua aplicação")
        print("   4. Teste manualmente o fluxo primeiro")

if __name__ == "__main__":
    main()