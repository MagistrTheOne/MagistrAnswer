# 🚀 Деплой Telegram-бота

## Вариант 1: Heroku (Рекомендуется)

### 1. Установка Heroku CLI
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# Или скачать с https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Подготовка проекта
```bash
# Инициализируем Git
git init
git add .
git commit -m "Initial commit"

# Создаем приложение на Heroku
heroku create your-bot-name-prometheus

# Устанавливаем переменные окружения
heroku config:set TELEGRAM_TOKEN=8284689308:AAFC2AyzhtrK3BkPMuWsDF6m2zhCGXvbkA4

# Деплоим
git push heroku main

# Запускаем worker процесс
heroku ps:scale worker=1
```

### 3. Проверка статуса
```bash
heroku logs --tail
heroku ps
```

## Вариант 2: Railway

### 1. Подготовка
- Зарегистрируйтесь на [railway.app](https://railway.app)
- Подключите GitHub репозиторий

### 2. Настройка
- Создайте новый проект
- Выберите "Deploy from GitHub repo"
- Укажите переменные окружения:
  - `TELEGRAM_TOKEN=8284689308:AAFC2AyzhtrK3BkPMuWsDF6m2zhCGXvbkA4`

### 3. Деплой
- Railway автоматически деплоит при push в main ветку
- Бот будет работать постоянно

## Вариант 3: Render

### 1. Подготовка
- Зарегистрируйтесь на [render.com](https://render.com)
- Подключите GitHub репозиторий

### 2. Создание Web Service
- New → Web Service
- Выберите репозиторий
- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py bot`

### 3. Переменные окружения
- Environment Variables:
  - `TELEGRAM_TOKEN=8284689308:AAFC2AyzhtrK3BkPMuWsDF6m2zhCGXvbkA4`

## Вариант 4: PythonAnywhere

### 1. Регистрация
- Зарегистрируйтесь на [pythonanywhere.com](https://pythonanywhere.com)
- Выберите бесплатный план

### 2. Загрузка кода
- Files → Upload a file (загрузите ZIP проекта)
- Или используйте Git:
```bash
git clone https://github.com/your-username/PrometheusAnswer.git
```

### 3. Установка зависимостей
```bash
cd PrometheusAnswer
pip3 install --user -r requirements.txt
```

### 4. Создание задачи
- Tasks → Add a new task
- Command: `cd ~/PrometheusAnswer && python main.py bot`
- Schedule: Daily (или другой интервал)

## 🔧 Настройка после деплоя

### 1. Проверка бота
- Найдите бота в Telegram по имени
- Отправьте `/start`
- Проверьте все функции

### 2. Мониторинг
- Проверяйте логи на платформе
- Настройте уведомления об ошибках

### 3. Обновления
- Push в main ветку = автоматический деплой
- Или обновляйте вручную через панель управления

## 🚨 Важные моменты

1. **Токен бота** должен быть в переменных окружения
2. **Worker процесс** должен быть запущен (не web)
3. **Логи** помогут отладить проблемы
4. **Перезапуск** может потребоваться при ошибках

## 📱 Тестирование бота

После деплоя:
1. Найдите бота в Telegram
2. Отправьте `/start`
3. Протестируйте все кнопки
4. Проверьте парсинг вопросов
5. Убедитесь, что анализ боли работает

---

**Выберите платформу по удобству. Heroku и Railway самые простые для начала!**
