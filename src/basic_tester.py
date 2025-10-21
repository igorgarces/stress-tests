import requests
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
        
        print("\n" + "=" * 60)
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
