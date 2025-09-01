import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot конфигурация
TELEGRAM_TOKEN = "8284689308:AAFC2AyzhtrK3BkPMuWsDF6m2zhCGXvbkA4"  # Временное решение
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Парсер конфигурация
ANSWER_MAIL_RU_URL = "https://otvet.mail.ru"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Настройки запросов
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 1.0

# Промпты для анализа
PAIN_ANALYSIS_PROMPT = """
Проанализируй скрытую боль в вопросе: "{question}"
Определи:
1. Основную проблему
2. Эмоциональное состояние автора
3. Скрытые страхи или ограничения
"""

SOLUTION_GENERATION_PROMPT = """
На основе боли: "{pain}"
Создай SaaS-решение в формате:
- Название (креативное)
- Описание проблемы
- Как решает боль
- Мемный элемент
"""
