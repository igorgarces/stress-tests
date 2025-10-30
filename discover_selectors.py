#!/usr/bin/env python3
"""
Ferramenta para descobrir seletores da sua aplicação
"""

def print_selector_guide():
    print("🎯 GUIA PARA DESCOBRIR SELECTORS")
    print("=" * 50)
    
    print("\n🔍 Como encontrar seletores:")
    print("1. Abra sua aplicação no Chrome")
    print("2. Pressione F12 para abrir DevTools")
    print("3. Clique no ícone de inspeção (🔍)")
    print("4. Clique no elemento que quer testar")
    print("5. No DevTools, procure por:")
    print("   - id: #meu-id")
    print("   - class: .minha-classe") 
    print("   - name: input[name='username']")
    print("   - text: //button[contains(text(), 'Login')]")
    
    print("\n📝 Exemplos de seletores comuns:")
    print("• Campo usuário: #username, input[name='user']")
    print("• Campo senha: #password, input[type='password']")
    print("• Botão login: button[type='submit'], #login-btn")
    print("• Aba Dashboards: //span[contains(text(), 'Dashboards')]")
    print("• Botão Selecionar Filas: //button[contains(text(), 'Selecionar Filas')]")
    
    print("\n💡 Dica: Comece testando com modo headless=False para ver o que acontece!")

if __name__ == "__main__":
    print_selector_guide()
