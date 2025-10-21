#!/usr/bin/env python3
"""
Script principal para executar testes de stress
"""

import sys
import os
import time

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.basic_tester import BasicStressTester
    from configs.test_config import TARGET_CONFIG
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    sys.exit(1)

def main():
    print("🚀 INICIANDO TESTES DE STRESS")
    print("⚠️  Use apenas em ambiente de desenvolvimento!")
    
    confirm = input("❓ Continuar? (s/N): ")
    if confirm.lower() not in ['s', 'sim', 'y', 'yes']:
        print("❌ Testes cancelados")
        return
    
    tester = BasicStressTester()
    tester.test_all_endpoints()

if __name__ == "__main__":
    main()
