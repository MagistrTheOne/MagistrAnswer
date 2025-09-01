import asyncio
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import sys
import os

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.question_parser import QuestionParser
from analyzers.pain_analyzer import PainAnalyzer
from generators.solution_generator import SolutionGenerator
import config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GamePrometheusBot:
    def __init__(self):
        self.question_parser = QuestionParser()
        self.pain_analyzer = PainAnalyzer()
        self.solution_generator = SolutionGenerator()
        self.user_sessions = {}  # Храним сессии пользователей
        self.game_stats = {}      # Статистика игр
        
        # Игровые категории
        self.game_categories = [
            'любовь', 'работа', 'здоровье', 'образование', 
            'технологии', 'путешествия', 'случайно'
        ]
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        username = update.effective_user.first_name or "Игрок"
        
        # Инициализируем сессию пользователя
        self.user_sessions[user_id] = {
            'username': username,
            'score': 0,
            'questions_asked': 0,
            'current_question': None,
            'current_analysis': None,
            'current_solution': None,
            'game_mode': 'menu'
        }
        
        # Инициализируем статистику
        if user_id not in self.game_stats:
            self.game_stats[user_id] = {
                'total_score': 0,
                'games_played': 0,
                'best_score': 0
            }
        
        welcome_text = f"""
🎮 **Добро пожаловать в игру "Вопрос Магистру"!**

Привет, {username}! 👋

🎯 **Цель игры:** Задавай вопросы, получай анализ боли и SaaS-решения!

📊 **Твой счет:** {self.user_sessions[user_id]['score']} очков
🏆 **Лучший результат:** {self.game_stats[user_id]['best_score']} очков

**Доступные команды:**
/play - 🎮 Начать игру
/ask - ❓ Задать свой вопрос
/category - 🎯 Вопрос по категории
/stats - 📊 Статистика
/help - ❓ Помощь
        """
        
        keyboard = [
            [InlineKeyboardButton("🎮 Начать игру", callback_data="start_game")],
            [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")],
            [InlineKeyboardButton("🎯 По категории", callback_data="by_category")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")],
            [InlineKeyboardButton("🏆 Лидеры", callback_data="leaderboard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def play_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /play - начало игры"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        # Сбрасываем счет для новой игры
        self.user_sessions[user_id]['score'] = 0
        self.user_sessions[user_id]['game_mode'] = 'playing'
        
        await self.start_game_round(update, user_id)
    
    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /ask - задать свой вопрос"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        self.user_sessions[user_id]['game_mode'] = 'waiting_question'
        
        await update.message.reply_text(
            "❓ **Задай свой вопрос:**\n\n"
            "Просто напиши любой вопрос, и я проанализирую скрытую боль!",
            parse_mode='Markdown'
        )
    
    async def category_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /category - вопрос по категории"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        keyboard = []
        for i in range(0, len(self.game_categories), 2):
            row = []
            row.append(InlineKeyboardButton(
                self.game_categories[i].title(), 
                callback_data=f"cat_{self.game_categories[i]}"
            ))
            if i + 1 < len(self.game_categories):
                row.append(InlineKeyboardButton(
                    self.game_categories[i + 1].title(), 
                    callback_data=f"cat_{self.game_categories[i + 1]}"
                ))
            keyboard.append(row)
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎯 **Выбери категорию вопроса:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /stats - показать статистику"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        session = self.user_sessions[user_id]
        stats = self.game_stats[user_id]
        
        stats_text = f"""
📊 **Статистика игрока {session['username']}**

🎮 **Текущая игра:**
   Счет: {session['score']} очков
   Вопросов задано: {session['questions_asked']}

🏆 **Общая статистика:**
   Игр сыграно: {stats['games_played']}
   Общий счет: {stats['total_score']} очков
   Лучший результат: {stats['best_score']} очков

🎯 **Достижения:**
   {'🥇 Мастер боли' if stats['best_score'] >= 100 else '🥈 Знаток' if stats['best_score'] >= 50 else '🥉 Новичок'}
        """
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help - показать помощь"""
        help_text = """
❓ **Помощь по игре "Вопрос Магистру"**

🎮 **Как играть:**
1. Используй /play для начала игры
2. Отвечай на вопросы и получай очки
3. Задавай свои вопросы командой /ask
4. Выбирай категории командой /category

🎯 **Система очков:**
   • Правильный анализ боли: +10 очков
   • Креативное решение: +5 очков
   • Быстрый ответ: +3 очка

🏆 **Достижения:**
   • Новичок: 0-49 очков
   • Знаток: 50-99 очков
   • Мастер боли: 100+ очков

📱 **Основные команды:**
   /start - Главное меню
   /play - Начать игру
   /ask - Задать вопрос
   /category - По категории
   /stats - Статистика
   /help - Эта помощь

🎭 **РОФЛО-команды:**
   /rofl - 🎭 Рофло вопрос
   /bazar - 🗣️ Иу это базаришь да?
   /shiza - 🧘 Креативное шиза
   /vazshe - 🤔 Полный рофло-анализ
   /demo50 - 🚀 Демо 50 рофло-вопросов

🎭 **Цель:** Стань лучшим аналитиком боли и генератором SaaS-решений!
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def rofl_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /rofl - рофло вопрос"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        # Получаем случайный рофло-вопрос
        question_data = self.question_parser.get_random_question()
        
        if not question_data:
            await update.message.reply_text("❌ Не удалось получить рофло-вопрос. Попробуйте позже.")
            return
        
        # Анализируем боль с рофло-стилем
        pain_analysis = self.pain_analyzer.analyze_pain(question_data['text'])
        
        # Генерируем максимально рофло-решение
        solution = self.solution_generator.generate_solution(pain_analysis)
        
        # Рофло-рейтинг
        rofl_level = self._calculate_rofl_level(pain_analysis, solution)
        
        rofl_text = f"""
🎭 **РОФЛО-ВОПРОС МАГИСТРА:**

❓ **Вопрос:** {question_data['text']}
📍 **Источник:** {question_data['source']}

💔 **Анализ боли (рофло-стиль):**
   🚨 Основная боль: {pain_analysis['main_pain']}
   🎭 Эмоции: {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}
   ⚡ Срочность: {pain_analysis['urgency_level']}
   🚨 Серьезность: {pain_analysis['severity_level']}

💡 **РОФЛО-SaaS-решение:**
   🚀 **{solution['name']}**
   {solution['full_solution']}

🎯 **РОФЛО-рейтинг:**
   {rofl_level['stars']} **Уровень рофла:** {rofl_level['description']}
   💰 **Оценка стартапа:** {rofl_level['startup_value']}
   🚀 **Готовность к IPO:** {rofl_level['ipo_readiness']}
   ⏰ **Время до выхода:** {rofl_level['exit_time']}

🎭 **Магистр сказал:** {rofl_level['magistr_quote']}
        """
        
        keyboard = [
            [InlineKeyboardButton("🎭 Еще рофло", callback_data="more_rofl")],
            [InlineKeyboardButton("🎮 Играть", callback_data="start_game")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(rofl_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def bazar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /bazar - агрессивный анализ"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        # Получаем случайный вопрос
        question_data = self.question_parser.get_random_question()
        
        if not question_data:
            await update.message.reply_text("❌ Не удалось получить вопрос для базара.")
            return
        
        # Агрессивный анализ
        pain_analysis = self.pain_analyzer.analyze_pain(question_data['text'])
        
        bazar_text = f"""
🗣️ **ИУ ЭТО БАЗАРИШЬ ДА?**

❓ **Вопрос:** {question_data['text']}

💥 **АГРЕССИВНЫЙ АНАЛИЗ:**
   🚨 **БОЛЬ:** {pain_analysis['main_pain'].upper()}
   😤 **ЭМОЦИИ:** {', '.join(pain_analysis['emotions']).upper() if pain_analysis['emotions'] else 'НЕ ОПРЕДЕЛЕНЫ'}
   ⚡ **СРОЧНОСТЬ:** {pain_analysis['urgency_level'].upper()}
   🚨 **СЕРЬЕЗНОСТЬ:** {pain_analysis['severity_level'].upper()}

💡 **БАЗАР-РЕШЕНИЕ:**
   🚀 **{self._generate_bazar_solution_name(pain_analysis)}**
   {self._generate_bazar_solution(pain_analysis)}

🎯 **БАЗАР-СТАТИСТИКА:**
   💪 **Уровень базара:** {self._calculate_bazar_level(pain_analysis)}
   🗣️ **Готовность к базару:** 100%
   🚀 **IPO через:** {random.choice(['завтра', 'через неделю', 'уже вчера'])}
        """
        
        keyboard = [
            [InlineKeyboardButton("🗣️ Еще базар", callback_data="more_bazar")],
            [InlineKeyboardButton("🎮 Играть", callback_data="start_game")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(bazar_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def shiza_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /shiza - креативное шиза"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        # Получаем случайный вопрос
        question_data = self.question_parser.get_random_question()
        
        if not question_data:
            await update.message.reply_text("❌ Не удалось получить вопрос для шизы.")
            return
        
        # Креативный анализ
        pain_analysis = self.pain_analyzer.analyze_pain(question_data['text'])
        
        # Генерируем максимально креативное решение
        solution = self.solution_generator.generate_solution(pain_analysis)
        
        shiza_text = f"""
🧘 **КРЕАТИВНОЕ ШИЗА:**

❓ **Вопрос:** {question_data['text']}

🧠 **КРЕАТИВНЫЙ АНАЛИЗ:**
   💫 **БОЛЬ:** {pain_analysis['main_pain']}
   🌈 **ЭМОЦИИ:** {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}
   ✨ **СРОЧНОСТЬ:** {pain_analysis['urgency_level']}
   🌟 **СЕРЬЕЗНОСТЬ:** {pain_analysis['severity_level']}

💡 **КРЕАТИВНОЕ ШИЗА-РЕШЕНИЕ:**
   🚀 **{solution['name']}**
   {solution['full_solution']}

🎨 **КРЕАТИВНОСТЬ:**
   🌈 **Уровень креатива:** {self._calculate_creativity_level(pain_analysis)}
   🧘 **Шиза-коэффициент:** {random.randint(80, 120)}%
   💫 **Готовность к креативу:** Бесконечность%
   🚀 **IPO через:** {random.choice(['когда-нибудь', 'в параллельной вселенной', 'уже произошло'])}
        """
        
        keyboard = [
            [InlineKeyboardButton("🧘 Еще шиза", callback_data="more_shiza")],
            [InlineKeyboardButton("🎮 Играть", callback_data="start_game")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(shiza_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def vazshe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /vazshe - полный рофло-анализ"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        # Получаем случайный вопрос
        question_data = self.question_parser.get_random_question()
        
        if not question_data:
            await update.message.reply_text("❌ Не удалось получить вопрос для ваще.")
            return
        
        # Полный анализ
        pain_analysis = self.pain_analyzer.analyze_pain(question_data['text'])
        solution = self.solution_generator.generate_solution(pain_analysis)
        
        # Рофло-рейтинг
        rofl_level = self._calculate_rofl_level(pain_analysis, solution)
        
        vazshe_text = f"""
🤔 **ВАЩЕ ПОЛНЫЙ РОФЛО-АНАЛИЗ:**

❓ **Вопрос:** {question_data['text']}
📍 **Источник:** {question_data['source']}

🧠 **АНАЛИЗ БОЛИ:**
   💔 Основная боль: {pain_analysis['main_pain']}
   📊 Уверенность: {pain_analysis['confidence_score']:.0%}
   🎭 Эмоции: {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}
   ⚡ Срочность: {pain_analysis['urgency_level']}
   🚨 Серьезность: {pain_analysis['severity_level']}
   🎯 Тип вопроса: {pain_analysis['question_type']}

💡 **SaaS-РЕШЕНИЕ:**
   🚀 **{solution['name']}**
   {solution['full_solution']}
   🎯 Решает боль: {solution['pain_addressed']}

🎭 **РОФЛО-СТАТИСТИКА:**
   {rofl_level['stars']} **Уровень рофла:** {rofl_level['description']}
   💰 **Оценка стартапа:** {rofl_level['startup_value']}
   🚀 **Готовность к IPO:** {rofl_level['ipo_readiness']}
   ⏰ **Время до выхода:** {rofl_level['exit_time']}
   🎯 **Коэффициент рофла:** {random.randint(50, 200)}%

💡 **Рекомендации:**
{chr(10).join([f"   • {rec}" for rec in pain_analysis['recommendations'][:3]])}

🎭 **Магистр сказал:** {rofl_level['magistr_quote']}
        """
        
        keyboard = [
            [InlineKeyboardButton("🤔 Еще ваще", callback_data="more_vazshe")],
            [InlineKeyboardButton("🎮 Играть", callback_data="start_game")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(vazshe_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if query.data == "start_game":
            await self.start_game_round(query, user_id)
        elif query.data == "ask_question":
            await self.handle_ask_question(query, user_id)
        elif query.data == "by_category":
            await self.show_categories(query, user_id)
        elif query.data == "show_stats":
            await self.show_user_stats(query, user_id)
        elif query.data == "leaderboard":
            await self.show_leaderboard(query, user_id)
        elif query.data.startswith("cat_"):
            category = query.data[4:]
            await self.get_question_by_category(query, user_id, category)
        elif query.data == "analyze_pain":
            await self.analyze_pain_game(query, user_id)
        elif query.data == "generate_solution":
            await self.generate_solution_game(query, user_id)
        elif query.data == "next_question":
            await self.start_game_round(query, user_id)
        elif query.data == "end_game":
            await self.end_game(query, user_id)
        elif query.data == "more_rofl":
            await self.rofl_command(query, context)
        elif query.data == "more_bazar":
            await self.bazar_command(query, context)
        elif query.data == "more_shiza":
            await self.shiza_command(query, context)
        elif query.data == "more_vazshe":
            await self.vazshe_command(query, context)
        elif query.data == "main_menu":
            await self.start(query, context)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        if user_id not in self.user_sessions:
            return
        
        session = self.user_sessions[user_id]
        
        if session['game_mode'] == 'waiting_question':
            await self.process_user_question(update, user_id, message_text)
        elif session['game_mode'] == 'playing':
            # В игровом режиме можно отвечать на вопросы
            await self.handle_game_answer(update, user_id, message_text)
    
    async def start_game_round(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начинает новый раунд игры"""
        user_id = update.effective_user.id
        
        # Получаем случайный вопрос
        question_data = self.question_parser.get_random_question()
        
        if not question_data:
            await self.send_message(update, "❌ Не удалось получить вопрос. Попробуйте позже.")
            return
        
        # Сохраняем вопрос в сессии
        self.user_sessions[user_id]['current_question'] = question_data
        
        # Показываем вопрос
        keyboard = [
            [InlineKeyboardButton("🧠 Анализировать боль", callback_data="analyze_pain")],
            [InlineKeyboardButton("🎯 Пропустить вопрос", callback_data="next_question")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = f"""
🎮 **Раунд {self.user_sessions[user_id]['questions_asked'] + 1}**

❓ **Вопрос:** {question_data['text']}
📍 **Источник:** {question_data['source']}

**Что делаем дальше?**
        """
        
        await self.send_message(update, text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def process_user_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, question_text: str):
        """Обрабатывает вопрос от пользователя"""
        user_id = update.effective_user.id
        
        # Создаем объект вопроса
        question_data = self.question_parser.process_user_question(question_text)
        self.user_sessions[user_id]['current_question'] = question_data
        
        # Анализируем боль
        pain_analysis = self.pain_analyzer.analyze_pain(question_text)
        self.user_sessions[user_id]['current_analysis'] = pain_analysis
        
        # Генерируем решение
        solution = self.solution_generator.generate_solution(pain_analysis)
        self.user_sessions[user_id]['current_solution'] = solution
        
        # Начисляем очки
        points = self._calculate_points(pain_analysis, solution)
        self.user_sessions[user_id]['score'] += points
        self.user_sessions[user_id]['questions_asked'] += 1
        
        # Показываем результат
        result_text = f"""
❓ **Твой вопрос:** {question_text}

🧠 **Анализ боли:**
   💔 Основная боль: {pain_analysis['main_pain']}
   📊 Уверенность: {pain_analysis['confidence_score']:.0%}
   🎭 Эмоции: {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}
   ⚡ Срочность: {pain_analysis['urgency_level']}
   🚨 Серьезность: {pain_analysis['severity_level']}

💡 **SaaS-решение:**
   🚀 {solution['name']}
   {solution['full_solution']}

💡 **Рекомендации:**
{chr(10).join([f"   • {rec}" for rec in pain_analysis['recommendations'][:3]])}

🎯 **Получено очков:** +{points}
🏆 **Общий счет:** {self.user_sessions[user_id]['score']}
        """
        
        keyboard = [
            [InlineKeyboardButton("🎮 Следующий вопрос", callback_data="next_question")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        # Сбрасываем режим
        self.user_sessions[user_id]['game_mode'] = 'menu'
    
    async def analyze_pain_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Анализирует боль в игровом режиме"""
        user_id = update.effective_user.id
        session = self.user_sessions[user_id]
        
        if not session['current_question']:
            await self.send_message(update, "❌ Нет активного вопроса")
            return
        
        question = session['current_question']
        pain_analysis = self.pain_analyzer.analyze_pain(question['text'])
        session['current_analysis'] = pain_analysis
        
        # Начисляем очки за анализ
        analysis_points = 10
        session['score'] += analysis_points
        
        text = f"""
🧠 **Анализ боли:**

❓ **Вопрос:** {question['text']}

💔 **Основная боль:** {pain_analysis['main_pain']}
📊 **Уверенность:** {pain_analysis['confidence_score']:.0%}
🎭 **Эмоции:** {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}
⚡ **Срочность:** {pain_analysis['urgency_level']}
🚨 **Серьезность:** {pain_analysis['severity_level']}
🎯 **Тип вопроса:** {pain_analysis['question_type']}

💡 **Рекомендации:**
{chr(10).join([f"   • {rec}" for rec in pain_analysis['recommendations'][:2]])}

🎯 **Получено очков:** +{analysis_points}
🏆 **Общий счет:** {session['score']}

**Теперь генерируем SaaS-решение!**
        """
        
        keyboard = [
            [InlineKeyboardButton("💡 SaaS-решение", callback_data="generate_solution")],
            [InlineKeyboardButton("🎯 Следующий вопрос", callback_data="next_question")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_message(update, text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def generate_solution_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Генерирует решение в игровом режиме"""
        user_id = update.effective_user.id
        session = self.user_sessions[user_id]
        
        if not session['current_analysis']:
            await self.send_message(update, "❌ Сначала проанализируйте боль")
            return
        
        solution = self.solution_generator.generate_solution(session['current_analysis'])
        session['current_solution'] = solution
        
        # Начисляем очки за решение
        solution_points = 5
        session['score'] += solution_points
        session['questions_asked'] += 1
        
        text = f"""
💡 **SaaS-решение:**

🚀 **{solution['name']}**

{solution['full_solution']}

🎯 **Решает боль:** {solution['pain_addressed']}

🎯 **Получено очков:** +{solution_points}
🏆 **Общий счет:** {session['score']}
📊 **Вопросов в игре:** {session['questions_asked']}

**Отличная работа! Продолжаем игру?**
        """
        
        keyboard = [
            [InlineKeyboardButton("🎮 Следующий вопрос", callback_data="next_question")],
            [InlineKeyboardButton("🏁 Завершить игру", callback_data="end_game")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_message(update, text, reply_markup=reply_markup, parse_mode='Markdown')
    
    def _calculate_points(self, pain_analysis: dict, solution: dict) -> int:
        """Рассчитывает очки за ответ"""
        points = 0
        
        # Базовые очки за анализ
        points += 10
        
        # Бонус за точность анализа
        if pain_analysis['confidence_score'] > 0.8:
            points += 5
        
        # Бонус за креативность решения
        if 'мемный' in solution.get('meme_element', '').lower():
            points += 3
        
        return points
    
    async def send_message(self, update: Update, text: str, reply_markup=None, parse_mode=None):
        """Отправляет сообщение в зависимости от типа обновления"""
        if hasattr(update, 'edit_message_text'):
            await update.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        else:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    
    def run(self):
        """Запускает бота"""
        if not config.TELEGRAM_TOKEN:
            logger.error("TELEGRAM_TOKEN не установлен!")
            return
        
        application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("play", self.play_command))
        application.add_handler(CommandHandler("ask", self.ask_command))
        application.add_handler(CommandHandler("category", self.category_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("rofl", self.rofl_command))
        application.add_handler(CommandHandler("bazar", self.bazar_command))
        application.add_handler(CommandHandler("shiza", self.shiza_command))
        application.add_handler(CommandHandler("vazshe", self.vazshe_command))
        application.add_handler(CommandHandler("demo50", self.demo50_command))
        
        application.add_handler(CallbackQueryHandler(self.button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
        
        # Запускаем бота
        logger.info("Игровой бот запущен!")
        application.run_polling()
    
    async def demo50_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /demo50 - демонстрация 50 рофло-вопросов"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text("❌ Сначала используйте /start")
            return
        
        await update.message.reply_text("🎭 **Запускаю демонстрацию 50 рофло-вопросов...**\n\nЭто займет несколько секунд! ⏳", parse_mode='Markdown')
        
        # Получаем 50 вопросов
        questions = self.question_parser.get_multiple_questions(50)
        
        # Генерируем решения для каждого вопроса
        demo_results = []
        for i, question in enumerate(questions[:50], 1):
            try:
                # Анализируем боль
                pain_analysis = self.pain_analyzer.analyze_pain(question['text'])
                
                # Генерируем решение
                solution = self.solution_generator.generate_solution(pain_analysis)
                
                # Рофло-рейтинг
                rofl_level = self._calculate_rofl_level(pain_analysis, solution)
                
                demo_results.append({
                    'number': i,
                    'question': question,
                    'pain_analysis': pain_analysis,
                    'solution': solution,
                    'rofl_level': rofl_level
                })
                
                # Показываем прогресс каждые 10 вопросов
                if i % 10 == 0:
                    progress_text = f"🎯 **Обработано вопросов:** {i}/50\n🚀 **Продолжаем анализ...**"
                    await update.message.reply_text(progress_text, parse_mode='Markdown')
                    
            except Exception as e:
                # Если что-то пошло не так, добавляем простой результат
                demo_results.append({
                    'number': i,
                    'question': question,
                    'pain_analysis': {'main_pain': 'техническая ошибка', 'confidence_score': 0.1},
                    'solution': {'name': 'ErrorBot', 'full_solution': 'Исправляет ошибки в рофло-анализе'},
                    'rofl_level': {'stars': '🌟', 'description': 'Ошибка рофла'}
                })
        
        # Показываем итоговую статистику
        await self._show_demo50_summary(update, demo_results)
    
    async def _show_demo50_summary(self, update: Update, demo_results: list):
        """Показывает итоговую статистику демонстрации"""
        # Подсчитываем статистику
        total_questions = len(demo_results)
        roflo_questions = sum(1 for r in demo_results if r['question']['type'] == 'roflo')
        real_questions = total_questions - roflo_questions
        
        # Средние показатели
        avg_confidence = sum(r['pain_analysis']['confidence_score'] for r in demo_results) / total_questions
        avg_rofl_level = sum(len(r['rofl_level']['stars']) for r in demo_results) / total_questions
        
        # Топ-5 самых рофло-решений
        top_solutions = sorted(demo_results, key=lambda x: x['solution'].get('rofl_level', 0), reverse=True)[:5]
        
        summary_text = f"""
🎭 **ДЕМОНСТРАЦИЯ 50 РОФЛО-ВОПРОСОВ ЗАВЕРШЕНА!**

📊 **Общая статистика:**
   • Всего вопросов: {total_questions}
   • Рофло-вопросы: {roflo_questions}
   • Реальные вопросы: {real_questions}
   • Средняя уверенность: {avg_confidence:.1%}
   • Средний рофло-уровень: {avg_rofl_level:.1f} звезд

🏆 **ТОП-5 самых рофло-решений:**

"""
        
        for i, result in enumerate(top_solutions, 1):
            summary_text += f"""
{i}. **{result['solution']['name']}**
   ❓ Вопрос: {result['question']['text'][:50]}...
   💔 Боль: {result['pain_analysis']['main_pain']}
   {result['rofl_level']['stars']} Уровень рофла: {result['rofl_level']['description']}
   💰 Оценка: {result['rofl_level']['startup_value']}
"""
        
        summary_text += f"""

🎯 **Рекомендации:**
   • Используй /rofl для случайных рофло-вопросов
   • Команда /bazar для агрессивного анализа
   • /shiza для креативного шиза
   • /vazshe для полного рофло-анализа

🚀 **Готов к IPO:** {len([r for r in demo_results if 'IPO' in str(r['rofl_level'])])} решений!
        """
        
        # Создаем кнопки для навигации
        keyboard = [
            [InlineKeyboardButton("🎭 Еще рофло", callback_data="more_rofl")],
            [InlineKeyboardButton("🗣️ Базар", callback_data="more_bazar")],
            [InlineKeyboardButton("🧘 Шиза", callback_data="more_shiza")],
            [InlineKeyboardButton("🤔 Ваще", callback_data="more_vazshe")],
            [InlineKeyboardButton("🎮 Играть", callback_data="start_game")],
            [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(summary_text, reply_markup=reply_markup, parse_mode='Markdown')
