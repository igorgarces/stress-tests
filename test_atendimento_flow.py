#!/usr/bin/env python3
"""
Teste específico para fluxo completo de atendimento
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.web_flow_tester import WebFlowStressTester

def main():
    print("🎯 TESTE COMPLETO: FLUXO DE ATENDIMENTO")
    print("=" * 60)
    print("📋 Fluxo a ser testado:")
    print("   1. 🔐 Login")
    print("   2. 📊 Dashboards → Atendente → Telefonia") 
    print("   3. 🎯 Selecionar Filas → Fila Teste")
    print("   4. 🚀 Iniciar Atendimento")
    print("   5. ⏸️  Ciclos de Pausar/Retomar")
    print("=" * 60)
    
    # Configuração interativa
    print("📝 Configure sua aplicação:")
    url = input("🌐 URL da aplicação (ex: http://localhost:3000): ").strip()
    username = input("👤 Usuário: ").strip()
    password = input("🔒 Senha: ").strip()
    
    if not url or not username or not password:
        print("❌ Todas as informações são obrigatórias!")
        return
    
    print(f"\n⚙️  Configuração:")
    print(f"   URL: {url}")
    print(f"   Usuário: {username}")
    print(f"   Senha: {'*' * len(password)}")
    
    # Parâmetros do teste
    num_users = input("\n👥 Número de usuários simulados [3]: ").strip()
    num_users = int(num_users) if num_users else 3
    
    num_cycles = input("🔄 Ciclos de pausa por usuário [2]: ").strip()
    num_cycles = int(num_cycles) if num_cycles else 2
    
    headless = input("🖥️  Executar em modo headless (sem interface) [s/N]: ").strip()
    headless = headless.lower() in ['s', 'sim', 'y', 'yes']
    
    print(f"\n🎯 Parâmetros do teste:")
    print(f"   • Usuários: {num_users}")
    print(f"   • Ciclos por usuário: {num_cycles}") 
    print(f"   • Modo headless: {'Sim' if headless else 'Não'}")
    
    confirm = input("\n❓ Confirmar e executar teste? (s/N): ")
    if confirm.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Teste cancelado")
        return
    
    tester = WebFlowStressTester(headless=headless)
    
    try:
        print("🚀 Iniciando teste completo...")
        results = tester.stress_test_flow(
            url=url,
            username=username,
            password=password,
            num_users=num_users,
            num_cycles=num_cycles
        )
        
        print("\n🎉 Teste concluído!")
        print("💡 Verifique o relatório acima para análise de performance")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("\n🔧 Para configurar corretamente:")
        print("   1. Teste manualmente o fluxo no navegador")
        print("   2. Use F12 para inspecionar elementos e descobrir os seletores corretos")
        print("   3. Ajuste os seletores no arquivo web_flow_tester.py")
        print("   4. Execute novamente")

if __name__ == "__main__":
    main()
