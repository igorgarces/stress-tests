"""
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
