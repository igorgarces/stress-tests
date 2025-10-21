import pytest
import sys
import os

# Adiciona o src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from basic_tester import BasicStressTester

class TestBasicTester:
    """Testes para o BasicStressTester"""

    def test_init(self):
        """Testa inicialização do testador"""
        tester = BasicStressTester()
        assert tester.base_url.startswith('http')
        assert tester.timeout == 10
        assert isinstance(tester.results, list)

    def test_single_endpoint_success(self):
        """Testa requisição única bem-sucedida"""
        tester = BasicStressTester()
        # Este teste pode ser adaptado para mockar requests
        assert tester is not None

    def test_generate_report_empty(self):
        """Testa geração de relatório com dados vazios"""
        tester = BasicStressTester()
        # Simula resultados vazios
        report = tester.generate_report()
        assert report is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])