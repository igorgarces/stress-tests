#!/bin/bash

echo "🔧 CORRIGINDO DEPENDÊNCIAS DO PYTHON 3.12"
echo "=========================================="

# Instala pacotes do sistema necessários
echo "📦 Instalando pacotes do sistema..."
sudo apt update
sudo apt install -y python3-distutils python3-venv python3-pip

# Remove venv corrompido
echo "🗑️  Removendo ambiente virtual problemático..."
cd ~/stress-tests
rm -rf venv

# Cria novo venv
echo "🐍 Criando novo ambiente virtual..."
python3 -m venv venv

# Ativa venv
echo "🚀 Ativando ambiente virtual..."
source venv/bin/activate

# Atualiza pip
echo "🔄 Atualizando pip..."
pip install --upgrade pip

# Instala dependências básicas
echo "📚 Instalando dependências básicas..."
pip install requests==2.31.0
pip install locust==2.15.1
pip install pytest==7.4.0
pip install psutil==5.9.5

# Verifica instalações
echo "🔍 Verificando instalações..."
python -c "import requests; print('✅ requests instalado')"
python -c "import locust; print('✅ locust instalado')"
python -c "import pytest; print('✅ pytest instalado')"
python -c "import psutil; print('✅ psutil instalado')"

echo ""
echo "🎉 DEPENDÊNCIAS INSTALADAS COM SUCESSO!"
echo "👉 Execute: python run_tests.py"
