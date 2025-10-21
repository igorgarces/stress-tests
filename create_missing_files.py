#!/usr/bin/env python3
"""
Cria todos os arquivos faltantes do projeto
"""

import os

def create_file(filepath, content):
    """Cria um arquivo com conteúdo"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✅ Criado: {filepath}")

def main():
    base_dir = os.path.expanduser("~/stress-tests")
    
    # Arquivo run_tests.py
    run_tests_content = '''#!/usr/bin/env python3
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
'''
    
    # Arquivo configs/test_config.py
    test_config_content = '''"""
Configurações dos testes de stress
"""

TARGET_CONFIG = {
    "base_url": "https://jsonplaceholder.typicode.com",
    "timeout": 10,
    "headers": {
        "User-Agent": "Stress-Tester/1.0",
        "Content-Type": "application/json"
    }
}

ENDPOINTS = [
    "/posts/1",
    "/users/1", 
    "/comments/1",
    "/posts"
]

TEST_CONFIG = {
    "basic": {
        "requests_per_endpoint": 5,
        "delay_between_requests": 0.5
    }
}
'''
    
    # Arquivo src/basic_tester.py
    basic_tester_content = '''import requests
import time
import statistics
from configs.test_config import TARGET_CONFIG, ENDPOINTS, TEST_CONFIG

class BasicStressTester:
    def __init__(self):
        self.base_url = TARGET_CONFIG["base_url"]
        self.timeout = TARGET_CONFIG["timeout"]
        self.headers = TARGET_CONFIG["headers"]
        self.results = []
        
    def test_single_endpoint(self, endpoint, method="GET"):
        print(f"🔍 Testando {method} {endpoint}")
        
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response_time = time.time() - start_time
            
            result = {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code == 200,
            }
            
            self.results.append(result)
            status_icon = "✅" if result["success"] else "❌"
            print(f"   {status_icon} Status: {result['status_code']} | Tempo: {result['response_time']:.3f}s")
            return result
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def test_all_endpoints(self):
        print("🚀 INICIANDO TESTES SEQUENCIAIS")
        print("=" * 50)
        
        for endpoint in ENDPOINTS:
            self.test_single_endpoint(endpoint)
            time.sleep(0.5)
        
        self.generate_report()
    
    def generate_report(self):
        if not self.results:
            print("📝 Nenhum resultado")
            return
        
        successful = [r for r in self.results if r["success"]]
        total = len(self.results)
        success_rate = (len(successful) / total) * 100 if total > 0 else 0
        
        if successful:
            response_times = [r["response_time"] for r in successful]
            avg_time = statistics.mean(response_times)
        else:
            avg_time = 0
        
        print("\\n" + "=" * 60)
        print("📊 RELATÓRIO DOS TESTES")
        print("=" * 60)
        print(f"📈 Total de requisições: {total}")
        print(f"✅ Bem-sucedidas: {len(successful)}")
        print(f"❌ Com erro: {total - len(successful)}")
        print(f"📊 Taxa de sucesso: {success_rate:.1f}%")
        print(f"⏱️  Tempo médio: {avg_time:.3f}s")
        print("=" * 60)

if __name__ == "__main__":
    tester = BasicStressTester()
    tester.test_all_endpoints()
'''
    
    # Criar todos os arquivos
    files_to_create = [
        ("run_tests.py", run_tests_content),
        ("configs/test_config.py", test_config_content),
        ("src/basic_tester.py", basic_tester_content),
        ("src/__init__.py", ""),
        ("configs/__init__.py", ""),
        ("requirements.txt", "requests==2.31.0\npytest==7.4.0\npsutil==5.9.5"),
    ]
    
    for filepath, content in files_to_create:
        full_path = os.path.join(base_dir, filepath)
        create_file(full_path, content)
    
    print("\\n🎉 TODOS OS ARQUIVOS FORAM CRIADOS!")
    print("👉 Agora execute: python run_tests.py")

if __name__ == "__main__":
    main()

