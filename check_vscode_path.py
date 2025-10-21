#!/usr/bin/env python3
"""
Verifica se o VS Code está na pasta correta
"""

import os

def main():
    current_dir = os.getcwd()
    expected_dir = "/home/suporte/stress-tests"
    
    print(f"📁 Diretório atual: {current_dir}")
    print(f"📁 Diretório esperado: {expected_dir}")
    
    if current_dir == expected_dir:
        print("✅ VS Code está na pasta CORRETA!")
        
        # Verifica arquivos
        files = ["run_tests.py", "src/basic_tester.py", "configs/test_config.py"]
        for file in files:
            if os.path.exists(file):
                print(f"✅ {file} existe")
            else:
                print(f"❌ {file} não existe")
                
    else:
        print("❌ VS Code está na pasta ERRADA!")
        print("💡 Solução: File → Open Folder → /home/suporte/stress-tests")

if __name__ == "__main__":
    main()
