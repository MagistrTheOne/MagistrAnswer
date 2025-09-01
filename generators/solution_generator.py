import random
from typing import Dict, List

class SolutionGenerator:
    def __init__(self):
        # Шаблоны названий для разных типов боли
        self.name_templates = {
            'страх': ['FearBuster', 'CourageAI', 'BraveBot', 'AnxietySlayer'],
            'отчаяние': ['HopeHub', 'SolutionFinder', 'ProblemCrusher', 'MiracleMaker'],
            'одиночество': ['SocialBridge', 'ConnectionAI', 'CommunityHub', 'FriendFinder'],
            'неуверенность': ['ConfidenceBoost', 'DecisionHelper', 'ClarityAI', 'CertaintyBot'],
            'давление': ['StressReliever', 'PressureEase', 'CalmAI', 'ZenBot'],
            'сравнение': ['UniqueYou', 'IndividualAI', 'PersonalPath', 'SelfValue']
        }
        
        # Мемные элементы для рофл-контекста
        self.meme_elements = [
            "с API для холодильника",
            "интеграция с Tinder",
            "через блокчейн",
            "с машинным обучением",
            "через нейросеть",
            "с голосовым помощником",
            "через чат-бота",
            "с мобильным приложением",
            "через веб-интерфейс",
            "с push-уведомлениями"
        ]
        
        # Шаблоны решений
        self.solution_templates = [
            "AI-платформа, которая {action} и {benefit}",
            "Умный сервис, решающий {problem} через {method}",
            "Инновационное решение, которое {solves} и {improves}",
            "Платформа будущего, где {feature} помогает {outcome}"
        ]
    
    def generate_solution(self, pain_analysis: Dict[str, any]) -> Dict[str, str]:
        """Генерирует SaaS-решение на основе анализа боли"""
        main_pain = pain_analysis.get('main_pain', 'общая проблема')
        pain_categories = pain_analysis.get('pain_categories', [])
        
        # Генерируем название
        name = self._generate_name(pain_categories)
        
        # Генерируем описание решения
        description = self._generate_description(main_pain, pain_categories)
        
        # Генерируем мемный элемент
        meme_element = random.choice(self.meme_elements)
        
        # Формируем полное решение
        full_solution = self._format_solution(name, description, meme_element)
        
        return {
            'name': name,
            'description': description,
            'meme_element': meme_element,
            'full_solution': full_solution,
            'pain_addressed': main_pain
        }
    
    def _generate_name(self, pain_categories: List[str]) -> str:
        """Генерирует название решения"""
        if pain_categories:
            # Берем первую категорию боли для названия
            category = pain_categories[0]
            if category in self.name_templates:
                return random.choice(self.name_templates[category])
        
        # Если категория не найдена, используем общие названия
        general_names = ['ProblemSolver', 'PainKiller', 'SolutionAI', 'HelpBot']
        return random.choice(general_names)
    
    def _generate_description(self, main_pain: str, pain_categories: List[str]) -> str:
        """Генерирует описание решения"""
        template = random.choice(self.solution_templates)
        
        # Заполняем шаблон
        if "страх" in main_pain.lower():
            action = "анализирует страхи пользователя"
            benefit = "предоставляет персонализированные стратегии преодоления"
        elif "одиночество" in main_pain.lower():
            action = "создает социальные связи"
            benefit = "помогает найти единомышленников"
        elif "неуверенность" in main_pain.lower():
            action = "повышает уверенность в себе"
            benefit = "дает четкие рекомендации для действий"
        else:
            action = "анализирует проблему пользователя"
            benefit = "предлагает эффективные решения"
        
        return template.format(
            action=action,
            benefit=benefit,
            problem=main_pain,
            method="искусственный интеллект",
            solves=main_pain,
            improves="качество жизни",
            feature="умный анализ",
            outcome="решению проблем"
        )
    
    def _format_solution(self, name: str, description: str, meme_element: str) -> str:
        """Форматирует полное решение в мемном стиле"""
        return f"{name} — {description} {meme_element}. Через 3 месяца ты не узнаешь себя, потому что {name} изменит твою жизнь навсегда! 🚀"
    
    def generate_multiple_solutions(self, pain_analysis: Dict[str, any], count: int = 3) -> List[Dict[str, str]]:
        """Генерирует несколько вариантов решений"""
        solutions = []
        for _ in range(count):
            solution = self.generate_solution(pain_analysis)
            solutions.append(solution)
        return solutions
