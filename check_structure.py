#!/usr/bin/env python3
"""
Verifica se a estrutura do projeto está correta
"""

import os
import sys

def check_project_structure():
    print("🔍 VERIFICANDO ESTRUTURA DO PROJETO")
    print("=" * 50)
    
    required_files = [
        "src/__init__.py",
        "src/web_flow_tester.py", 
        "test_pausas_flow.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    # Verifica se pode importar
    print("\n🔧 Testando importações...")
    try:
        sys.path.insert(0, os.getcwd())
        from src.web_flow_tester import WebFlowStressTester
        print("✅ Importação de WebFlowStressTester: OK")
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
    
    print("\n" + "=" * 50)
    
    if missing_files:
        print(f"🚨 Faltam {len(missing_files)} arquivos:")
        for missing in missing_files:
            print(f"   - {missing}")
    else:
        print("🎉 Estrutura OK! Execute: python test_pausas_flow.py")

if __name__ == "__main__":
    check_project_structure()
