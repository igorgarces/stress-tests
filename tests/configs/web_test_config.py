"""
Configurações para testes web de fluxo de pausas
"""

# ⚠️ CONFIGURE COM SUAS INFORMAÇÕES
WEB_TEST_CONFIG = {
    "application_url": "https://sua-aplicacao.com/login",
    "credentials": {
        "username": "seu_usuario_teste",
        "password": "sua_senha_teste"
    },
    "selectors": {
        # ⚠️ AJUSTE ESTES SELECTORS para sua aplicação
        "login": {
            "username_field": "#username",  # ID do campo usuário
            "password_field": "#password",  # ID do campo senha
            "login_button": "#login-btn"    # ID do botão login
        },
        "navigation": {
            "dashboards_tab": "//span[contains(text(), 'Dashboards')]",
            "atendente_tab": "//a[contains(text(), 'Atendente')]",
            "telefonia_section": "//button[contains(text(), 'Telefonia')]"
        },
        "pauses": {
            "open_pause_button": "//button[contains(text(), 'Iniciar Pausa')]",
            "pause_type_dropdown": "#pause-type",
            "confirm_pause_button": "//button[contains(text(), 'Confirmar')]",
            "close_pause_button": "//button[contains(text(), 'Encerrar Pausa')]",
            "confirm_close_button": "//button[contains(text(), 'Sim')]"
        }
    },
    "test_parameters": {
        "headless": True,           # Executar sem interface gráfica
        "timeout": 15,              # Timeout para esperar elementos
        "num_users": 5,             # Usuários simultâneos para teste de stress
        "pause_cycles_per_user": 3, # Ciclos de pausa por usuário
        "min_wait_between_cycles": 3,
        "max_wait_between_cycles": 8
    }
}