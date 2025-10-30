#!/usr/bin/env python3
"""
Teste interativo - pede informações durante a execução
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.web_flow_tester import WebFlowStressTester

def main():
    print("🎯 TESTE INTERATIVO - FLUXO DE PAUSAS")
    print("=" * 50)
    
    # Coleta informações do usuário
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
    
    confirm = input("\n❓ Confirmar e executar teste? (s/N): ")
    if confirm.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Teste cancelado")
        return
    
    tester = WebFlowStressTester(headless=True)
    
    try:
        print("🚀 Iniciando teste...")
        results = tester.stress_test_flow(
            url=url,
            username=username,
            password=password,
            num_users=2,          # Comece com 2 usuários
            num_pause_cycles=2     # Comece com 2 ciclos
        )
        
        print("\n🎉 Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("\n🔧 Possíveis soluções:")
        print("   1. Verifique se a URL está correta")
        print("   2. Confirme se a aplicação está rodando")
        print("   3. Teste manualmente no navegador primeiro")
        print("   4. Verifique credenciais")

if __name__ == "__main__":
    main()
