import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
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

class PrometheusBot:
    def __init__(self):
        self.question_parser = QuestionParser()
        self.pain_analyzer = PainAnalyzer()
        self.solution_generator = SolutionGenerator()
        self.current_data = {}  # Храним текущие данные для пользователя
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        keyboard = [
            [InlineKeyboardButton("🗿 Новый вопрос Магистру", callback_data="new_question")],
            [InlineKeyboardButton("🔥 Анализ боли", callback_data="analyze_pain")],
            [InlineKeyboardButton("💡 SaaS-решение", callback_data="generate_solution")],
            [InlineKeyboardButton("🎯 Полный анализ", callback_data="full_analysis")],
            [InlineKeyboardButton("📊 Статистика", callback_data="statistics")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = """
🤖 **Вопрос Магистру** — автоматическая фабрика боли и решений!

Система анализирует случайные вопросы и генерирует SaaS-решения в мемном стиле.

Выберите действие:
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if query.data == "new_question":
            await self.handle_new_question(query, user_id)
        elif query.data == "analyze_pain":
            await self.handle_pain_analysis(query, user_id)
        elif query.data == "generate_solution":
            await self.handle_solution_generation(query, user_id)
        elif query.data == "full_analysis":
            await self.handle_full_analysis(query, user_id)
        elif query.data == "statistics":
            await self.handle_statistics(query, user_id)
    
    async def handle_new_question(self, query, user_id):
        """Обрабатывает запрос нового вопроса"""
        await query.edit_message_text("🔍 Ищу случайный вопрос...")
        
        try:
            question_data = self.question_parser.get_random_question()
            
            if question_data:
                self.current_data[user_id] = {
                    'question': question_data['text'],
                    'source': question_data['source']
                }
                
                keyboard = [
                    [InlineKeyboardButton("🔥 Анализ боли", callback_data="analyze_pain")],
                    [InlineKeyboardButton("💡 SaaS-решение", callback_data="generate_solution")],
                    [InlineKeyboardButton("🎯 Полный анализ", callback_data="full_analysis")],
                    [InlineKeyboardButton("🗿 Новый вопрос", callback_data="new_question")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                text = f"""
🗿 **Вопрос Магистру:**

❓ **Вопрос:** "{question_data['text']}"
📍 **Источник:** {question_data['source']}

Теперь выберите, что делать с этим вопросом:
                """
                
                await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                await query.edit_message_text("❌ Не удалось найти вопрос. Попробуйте еще раз.")
                
        except Exception as e:
            logger.error(f"Ошибка при получении вопроса: {e}")
            await query.edit_message_text("❌ Произошла ошибка. Попробуйте позже.")
    
    async def handle_pain_analysis(self, query, user_id):
        """Обрабатывает анализ боли"""
        if user_id not in self.current_data:
            await query.edit_message_text("❌ Сначала получите вопрос!")
            return
        
        question = self.current_data[user_id]['question']
        await query.edit_message_text("🧠 Анализирую скрытую боль...")
        
        try:
            pain_analysis = self.pain_analyzer.analyze_pain(question)
            self.current_data[user_id]['pain_analysis'] = pain_analysis
            
            keyboard = [
                [InlineKeyboardButton("💡 SaaS-решение", callback_data="generate_solution")],
                [InlineKeyboardButton("🎯 Полный анализ", callback_data="full_analysis")],
                [InlineKeyboardButton("🗿 Новый вопрос", callback_data="new_question")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = f"""
🔥 **Анализ боли:**

❓ **Вопрос:** "{question}"

💔 **Основная боль:** {pain_analysis['main_pain']}
📊 **Уверенность:** {pain_analysis['confidence_score']:.0%}
🎭 **Эмоции:** {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}
⚡ **Срочность:** {pain_analysis['urgency_level']}

Теперь можно генерировать решение!
            """
            
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Ошибка при анализе боли: {e}")
            await query.edit_message_text("❌ Ошибка анализа. Попробуйте еще раз.")
    
    async def handle_solution_generation(self, query, user_id):
        """Обрабатывает генерацию решения"""
        if user_id not in self.current_data:
            await query.edit_message_text("❌ Сначала получите вопрос!")
            return
        
        if 'pain_analysis' not in self.current_data[user_id]:
            await query.edit_message_text("❌ Сначала проанализируйте боль!")
            return
        
        await query.edit_message_text("💡 Генерирую SaaS-решение...")
        
        try:
            pain_analysis = self.current_data[user_id]['pain_analysis']
            solution = self.solution_generator.generate_solution(pain_analysis)
            
            self.current_data[user_id]['solution'] = solution
            
            keyboard = [
                [InlineKeyboardButton("🎯 Полный анализ", callback_data="full_analysis")],
                [InlineKeyboardButton("🗿 Новый вопрос", callback_data="new_question")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = f"""
💡 **SaaS-решение:**

🚀 **{solution['name']}**

{solution['full_solution']}

🎯 **Решает боль:** {solution['pain_addressed']}
            """
            
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Ошибка при генерации решения: {e}")
            await query.edit_message_text("❌ Ошибка генерации. Попробуйте еще раз.")
    
    async def handle_full_analysis(self, query, user_id):
        """Обрабатывает полный анализ"""
        if user_id not in self.current_data:
            await query.edit_message_text("❌ Сначала получите вопрос!")
            return
        
        user_data = self.current_data[user_id]
        
        if 'pain_analysis' not in user_data or 'solution' not in user_data:
            await query.edit_message_text("❌ Сначала выполните полный анализ!")
            return
        
        keyboard = [
            [InlineKeyboardButton("🗿 Новый вопрос", callback_data="new_question")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = f"""
🎯 **Полный анализ Магистра:**

❓ **Вопрос:** "{user_data['question']}"

💔 **Боль:** {user_data['pain_analysis']['main_pain']}

💡 **SaaS-решение:** {user_data['solution']['full_solution']}

🎭 **Уровень рофла:** 10/10
🚀 **Готовность к инвестициям:** 100%
        """
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_statistics(self, query, user_id):
        """Обрабатывает статистику"""
        keyboard = [
            [InlineKeyboardButton("🗿 Новый вопрос", callback_data="new_question")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = """
📊 **Статистика Вопросов Магистра:**

🎭 **Уровень смеха в чате:** 9/10
📱 **Мемов в Telegram:** ∞
💰 **Инвесторов, спросивших 'а можно реально?':** 0 (пока)
🚀 **Готовность к IPO:** 99.9%

*Данные обновляются в реальном времени*
        """
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    def run(self):
        """Запускает бота"""
        if not config.TELEGRAM_TOKEN:
            logger.error("TELEGRAM_TOKEN не установлен!")
            return
        
        application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Запускаем бота
        logger.info("Бот запущен!")
        application.run_polling()
