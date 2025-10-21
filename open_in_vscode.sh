#!/bin/bash

# 🚀 Script para abrir o projeto no VS Code
# 📍 Localização: ~/stress-tests/open_in_vscode.sh

echo "=========================================="
echo "🚀 ABRINDO PROJETO NO VS CODE"
echo "=========================================="

# Verifica o diretório atual
CURRENT_DIR=$(pwd)
echo "📁 Diretório atual: $CURRENT_DIR"

# Verifica se estamos no diretório correto
EXPECTED_DIR="stress-tests"
if [[ "$CURRENT_DIR" != *"$EXPECTED_DIR" ]]; then
    echo "❌ ERRO: Execute este script de DENTRO da pasta stress-tests"
    echo "💡 Solução: cd ~/stress-tests"
    exit 1
fi

echo "✅ Diretório correto detectado"

# Verifica se o VS Code está instalado
if ! command -v code &> /dev/null; then
    echo "❌ VS Code não encontrado no sistema"
    echo "📦 Tentando instalar VS Code..."
    
    # Detecta o gerenciador de pacotes
    if command -v snap &> /dev/null; then
        echo "🔧 Instalando via Snap..."
        sudo snap install --classic code
    elif command -v apt &> /dev/null; then
        echo "🔧 Instalando via APT..."
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
        sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
        sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
        sudo apt update
        sudo apt install code
    else
        echo "❌ Não foi possível determinar o gerenciador de pacotes"
        echo "🌐 Baixe manualmente de: https://code.visualstudio.com/download"
        exit 1
    fi
fi

echo "✅ VS Code está instalado"

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual 'venv' não encontrado"
    echo "🔧 Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "✅ Ambiente virtual verificado"

# Ativa o ambiente virtual temporariamente para instalar dependências
echo "📦 Verificando dependências Python..."
source venv/bin/activate

# Verifica se as dependências estão instaladas
if ! python -c "import requests" &> /dev/null; then
    echo "🔧 Instalando dependências do requirements.txt..."
    pip install -r requirements.txt
fi

echo "✅ Dependências verificadas"

# Abre o VS Code no diretório atual
echo "🔄 Abrindo VS Code..."
echo "💡 Dica: Use F5 para executar os testes com debug!"
echo "💡 Dica: Use Ctrl+Shift+P → 'Python: Select Interpreter' para escolher o venv"
echo ""

code .

echo "=========================================="
echo "🎉 VS CODE ABERTO COM SUCESSO!"
echo "=========================================="
echo ""
echo "📋 PRÓXIMOS PASSOS NO VS CODE:"
echo "1. Aguarde o VS Code abrir"
echo "2. Vá em Terminal → New Terminal (ou Ctrl+Shift+`)"
echo "3. No terminal do VS Code, verifique se aparece (venv)"
echo "4. Execute: python run_tests.py"
echo "5. Ou pressione F5 para debug"
echo ""
echo "⚠️  LEMBRETE: Use ambiente de DESENVOLVIMENTO, nunca produção!"
