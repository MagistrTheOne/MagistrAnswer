#!/usr/bin/env python3
"""
Вопрос Магистру — автоматическая фабрика боли и решений
Главный оркестратор системы
"""

import asyncio
import sys
import os
from typing import Dict, Optional

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parsers.question_parser import QuestionParser
from analyzers.pain_analyzer import PainAnalyzer
from generators.solution_generator import SolutionGenerator
from telegram_bot.bot import PrometheusBot
from telegram_bot.game_bot import GamePrometheusBot
import config

class PrometheusOrchestrator:
    """Главный оркестратор системы 'Вопрос Магистру'"""
    
    def __init__(self):
        self.question_parser = QuestionParser()
        self.pain_analyzer = PainAnalyzer()
        self.solution_generator = SolutionGenerator()
        self.stats = {
            'questions_processed': 0,
            'solutions_generated': 0,
            'pain_analyses': 0
        }
    
    def run_cli_demo(self):
        """Запускает демо-версию в консоли"""
        print("🗿 Вопрос Магистру — автоматическая фабрика боли и решений!")
        print("=" * 60)
        
        try:
            # Получаем случайный вопрос
            print("🔍 Ищу случайный вопрос...")
            question_data = self.question_parser.get_random_question()
            
            if not question_data:
                print("❌ Не удалось получить вопрос. Возможно, проблемы с парсингом.")
                return
            
            print(f"\n❓ **Вопрос:** {question_data['text']}")
            print(f"📍 **Источник:** {question_data['source']}")
            print("-" * 60)
            
            # Анализируем боль
            print("🧠 Анализирую скрытую боль...")
            pain_analysis = self.pain_analyzer.analyze_pain(question_data['text'])
            
            print(f"💔 **Основная боль:** {pain_analysis['main_pain']}")
            print(f"📊 **Уверенность:** {pain_analysis['confidence_score']:.0%}")
            print(f"🎭 **Эмоции:** {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}")
            print(f"⚡ **Срочность:** {pain_analysis['urgency_level']}")
            print(f"🚨 **Серьезность:** {pain_analysis['severity_level']}")
            print(f"🎯 **Тип вопроса:** {pain_analysis['question_type']}")
            print("-" * 60)
            
            # Генерируем решение
            print("💡 Генерирую SaaS-решение...")
            solution = self.solution_generator.generate_solution(pain_analysis)
            
            print(f"🚀 **{solution['name']}**")
            print(f"💡 **Решение:** {solution['full_solution']}")
            print(f"🎯 **Решает боль:** {solution['pain_addressed']}")
            print("-" * 60)
            
            # Показываем рекомендации
            if pain_analysis.get('recommendations'):
                print("💡 **Рекомендации:**")
                for i, rec in enumerate(pain_analysis['recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
                print("-" * 60)
            
            # Обновляем статистику
            self.stats['questions_processed'] += 1
            self.stats['pain_analyses'] += 1
            self.stats['solutions_generated'] += 1
            
            # Показываем итоговый результат
            print("\n🎯 **ИТОГОВЫЙ АНАЛИЗ МАГИСТРА:**")
            print("=" * 60)
            print(f"❓ **Вопрос:** {question_data['text']}")
            print(f"💔 **Боль:** {pain_analysis['main_pain']}")
            print(f"💡 **SaaS-решение:** {solution['full_solution']}")
            print("=" * 60)
            print(f"🎭 **Уровень рофла:** 10/10")
            print(f"🚀 **Готовность к инвестициям:** 100%")
            print(f"📊 **Обработано вопросов:** {self.stats['questions_processed']}")
            
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.question_parser.close()
    
    def run_telegram_bot(self):
        """Запускает обычного Telegram-бота"""
        print("🤖 Запускаю обычного Telegram-бота...")
        bot = PrometheusBot()
        bot.run()
    
    def run_game_bot(self):
        """Запускает игрового Telegram-бота"""
        print("🎮 Запускаю игрового Telegram-бота...")
        bot = GamePrometheusBot()
        bot.run()
    
    def run_interactive_mode(self):
        """Запускает интерактивный режим"""
        print("🗿 Вопрос Магистру — интерактивный режим")
        print("=" * 60)
        
        while True:
            print("\nВыберите действие:")
            print("1. 🗿 Новый вопрос Магистру")
            print("2. 🔥 Анализ боли")
            print("3. 💡 SaaS-решение")
            print("4. 🎯 Полный анализ")
            print("5. 📊 Статистика")
            print("6. 🤖 Запустить обычного Telegram-бота")
            print("7. 🎮 Запустить игрового Telegram-бота")
            print("0. Выход")
            
            choice = input("\nВаш выбор: ").strip()
            
            if choice == "1":
                self._handle_new_question_interactive()
            elif choice == "2":
                self._handle_pain_analysis_interactive()
            elif choice == "3":
                self._handle_solution_generation_interactive()
            elif choice == "4":
                self._handle_full_analysis_interactive()
            elif choice == "5":
                self._show_statistics()
            elif choice == "6":
                print("🤖 Переключаюсь на обычного Telegram-бота...")
                self.run_telegram_bot()
                break
            elif choice == "7":
                print("🎮 Переключаюсь на игрового Telegram-бота...")
                self.run_game_bot()
                break
            elif choice == "0":
                print("👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Попробуйте еще раз.")
    
    def _handle_new_question_interactive(self):
        """Обрабатывает новый вопрос в интерактивном режиме"""
        if not hasattr(self, '_current_question'):
            print("🔍 Ищу случайный вопрос...")
            question_data = self.question_parser.get_random_question()
            
            if question_data:
                self._current_question = question_data
                self._current_pain_analysis = None
                self._current_solution = None
                
                print(f"\n❓ **Вопрос:** {question_data['text']}")
                print(f"📍 **Источник:** {question_data['source']}")
                self.stats['questions_processed'] += 1
            else:
                print("❌ Не удалось получить вопрос.")
        else:
            print("❓ У вас уже есть вопрос. Сначала проанализируйте его.")
    
    def _handle_pain_analysis_interactive(self):
        """Обрабатывает анализ боли в интерактивном режиме"""
        if not hasattr(self, '_current_question'):
            print("❌ Сначала получите вопрос!")
            return
        
        if not self._current_pain_analysis:
            print("🧠 Анализирую скрытую боль...")
            pain_analysis = self.pain_analyzer.analyze_pain(self._current_question['text'])
            self._current_pain_analysis = pain_analysis
            
            print(f"💔 **Основная боль:** {pain_analysis['main_pain']}")
            print(f"📊 **Уверенность:** {pain_analysis['confidence_score']:.0%}")
            print(f"🎭 **Эмоции:** {', '.join(pain_analysis['emotions']) if pain_analysis['emotions'] else 'не определены'}")
            print(f"⚡ **Срочность:** {pain_analysis['urgency_level']}")
            print(f"🚨 **Серьезность:** {pain_analysis['severity_level']}")
            print(f"🎯 **Тип вопроса:** {pain_analysis['question_type']}")
            
            if pain_analysis.get('recommendations'):
                print("💡 **Рекомендации:**")
                for i, rec in enumerate(pain_analysis['recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
            
            self.stats['pain_analyses'] += 1
        else:
            print("🧠 Анализ боли уже выполнен.")
    
    def _handle_solution_generation_interactive(self):
        """Обрабатывает генерацию решения в интерактивном режиме"""
        if not hasattr(self, '_current_question'):
            print("❌ Сначала получите вопрос!")
            return
        
        if not self._current_pain_analysis:
            print("❌ Сначала проанализируйте боль!")
            return
        
        if not self._current_solution:
            print("💡 Генерирую SaaS-решение...")
            solution = self.solution_generator.generate_solution(self._current_pain_analysis)
            self._current_solution = solution
            
            print(f"🚀 **{solution['name']}**")
            print(f"💡 **Решение:** {solution['full_solution']}")
            print(f"🎯 **Решает боль:** {solution['pain_addressed']}")
            self.stats['solutions_generated'] += 1
        else:
            print("💡 Решение уже сгенерировано.")
    
    def _handle_full_analysis_interactive(self):
        """Обрабатывает полный анализ в интерактивном режиме"""
        if not hasattr(self, '_current_question'):
            print("❌ Сначала получите вопрос!")
            return
        
        if not self._current_pain_analysis or not self._current_solution:
            print("❌ Сначала выполните полный анализ!")
            return
        
        print("\n🎯 **ПОЛНЫЙ АНАЛИЗ МАГИСТРА:**")
        print("=" * 60)
        print(f"❓ **Вопрос:** {self._current_question['text']}")
        print(f"💔 **Боль:** {self._current_pain_analysis['main_pain']}")
        print(f"💡 **SaaS-решение:** {self._current_solution['full_solution']}")
        print("=" * 60)
        print(f"🎭 **Уровень рофла:** 10/10")
        print(f"🚀 **Готовность к инвестициям:** 100%")
    
    def _show_statistics(self):
        """Показывает статистику"""
        print("\n📊 **СТАТИСТИКА ВОПРОСОВ МАГИСТРА:**")
        print("=" * 40)
        print(f"🗿 **Обработано вопросов:** {self.stats['questions_processed']}")
        print(f"🔥 **Анализов боли:** {self.stats['pain_analyses']}")
        print(f"💡 **Сгенерировано решений:** {self.stats['solutions_generated']}")
        print(f"🎭 **Уровень смеха в чате:** 9/10")
        print(f"📱 **Мемов в Telegram:** ∞")
        print(f"💰 **Инвесторов, спросивших 'а можно реально?':** 0 (пока)")
        print(f"🚀 **Готовность к IPO:** 99.9%")

def main():
    """Главная функция"""
    print("🚀 Запуск системы 'Вопрос Магистру'...")
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "cli":
            orchestrator = PrometheusOrchestrator()
            orchestrator.run_cli_demo()
        elif mode == "bot":
            orchestrator = PrometheusOrchestrator()
            orchestrator.run_telegram_bot()
        elif mode == "game":
            orchestrator = PrometheusOrchestrator()
            orchestrator.run_game_bot()
        elif mode == "interactive":
            orchestrator = PrometheusOrchestrator()
            orchestrator.run_interactive_mode()
        else:
            print("❌ Неверный режим. Используйте: cli, bot, game, или interactive")
    else:
        # По умолчанию запускаем интерактивный режим
        orchestrator = PrometheusOrchestrator()
        orchestrator.run_interactive_mode()

if __name__ == "__main__":
    main()
