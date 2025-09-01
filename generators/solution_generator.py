import random
from typing import Dict, List

class SolutionGenerator:
    def __init__(self):
        # Префиксы для названий решений
        self.name_prefixes = [
            "AI", "Smart", "Cloud", "Digital", "Future", "Next", "Pro", "Ultra", "Max", "Elite",
            "Rofl", "Meme", "Pain", "Solution", "Helper", "Fixer", "Resolver", "Analyzer", "Generator"
        ]
        
        # Суффиксы для названий решений
        self.name_suffixes = [
            "AI", "Pro", "Plus", "Max", "Ultra", "Elite", "Premium", "Enterprise", "Cloud", "Hub",
            "Bot", "App", "Tool", "Platform", "System", "Service", "API", "SDK", "Framework"
        ]
        
        # Мемные элементы для решений
        self.meme_elements = [
            "с котиками и единорогами", "с блокчейном и ИИ", "для холодильника с эмоциями",
            "с API для тостера", "для анализа боли через мемы", "с рофло-рейтингом",
            "для генерации SaaS из ничего", "с предсказанием IPO", "для лечения депрессии мемами",
            "с анализом конспирологии", "для создания невозможных API", "с мемной медитацией"
        ]
        
        # Рофло-фразы для решений
        self.roflo_phrases = [
            "Через 3 месяца ты не узнаешь себя!",
            "Это изменит твою жизнь навсегда!",
            "Готов к IPO уже завтра!",
            "Никто не устоит перед этим!",
            "Абсолютное оружие против проблем!",
            "Мощнейшее решение в истории!",
            "Уничтожает боль навсегда!",
            "Решает все проблемы одним махом!",
            "Это боль уровня 'нужен API для всего'!",
            "Серьезная боль, но можно сделать SaaS!",
            "Есть потенциал для стартапа!",
            "Может быть, стоит подумать еще...",
            "Готовность к IPO: 99.9%!",
            "Время до выхода: 3 месяца!",
            "Оценка стартапа: $100M+!",
            "Коэффициент рофла: 200%!",
            "Уровень креатива: БЕЗУМНО КРЕАТИВНЫЙ!",
            "Шиза-коэффициент: 120%!",
            "Готовность к креативу: Бесконечность%!",
            "IPO через: когда-нибудь в параллельной вселенной!"
        ]
        
        # Категории боли для более точных решений
        self.pain_categories = {
            'страх': ['AI-терапевт страха', 'Страх-анализатор Pro', 'Безопасность-максимум'],
            'одиночество': ['Социальный хаб', 'Друзья-генератор', 'Одиночество-убийца'],
            'неуверенность': ['Уверенность-бустер', 'Самооценка-максимайзер', 'Смелость-инжектор'],
            'работа': ['Карьера-ракета', 'Зарплата-увеличитель', 'Босс-укротитель'],
            'здоровье': ['Здоровье-оптимизатор', 'Энергия-генератор', 'Сон-мастер'],
            'образование': ['Знания-загрузчик', 'Ум-ускоритель', 'Гений-активатор'],
            'технологии': ['Гаджет-синхронизатор', 'Интернет-улучшитель', 'Технология-мастер'],
            'путешествия': ['Путешествие-планировщик', 'Приключение-генератор', 'Мир-открыватель']
        }
    
    def generate_solution(self, pain_analysis: dict) -> dict:
        """Генерирует SaaS-решение на основе анализа боли"""
        # Определяем основную категорию боли
        main_pain_category = self._get_main_pain_category(pain_analysis)
        
        # Генерируем название
        name = self._generate_name(main_pain_category)
        
        # Генерируем описание
        description = self._generate_description(pain_analysis, name)
        
        # Генерируем мемный элемент
        meme_element = random.choice(self.meme_elements)
        
        # Генерируем рофло-фразу
        roflo_phrase = random.choice(self.roflo_phrases)
        
        # Формируем полное решение
        full_solution = f"{description} {meme_element}. {roflo_phrase} 🚀"
        
        return {
            'name': name,
            'description': description,
            'full_solution': full_solution,
            'meme_element': meme_element,
            'roflo_phrase': roflo_phrase,
            'pain_addressed': pain_analysis['main_pain'],
            'category': main_pain_category,
            'roflo_level': self._calculate_roflo_level(pain_analysis),
            'startup_potential': self._calculate_startup_potential(pain_analysis),
            'meme_score': self._calculate_meme_score(pain_analysis)
        }
    
    def _get_main_pain_category(self, pain_analysis: dict) -> str:
        """Определяет основную категорию боли"""
        pain_categories = pain_analysis.get('pain_categories', [])
        
        if not pain_categories:
            return 'общие'
        
        # Ищем наиболее подходящую категорию
        for category in pain_categories:
            if category in self.pain_categories:
                return category
        
        return 'общие'
    
    def _generate_name(self, pain_category: str) -> str:
        """Генерирует название решения"""
        if pain_category in self.pain_categories:
            return random.choice(self.pain_categories[pain_category])
        
        prefix = random.choice(self.name_prefixes)
        suffix = random.choice(self.name_suffixes)
        
        return f"{prefix}{suffix}"
    
    def _generate_description(self, pain_analysis: dict, name: str) -> str:
        """Генерирует описание решения"""
        descriptions = [
            f"{name} — революционная платформа, которая использует передовые технологии ИИ для решения проблем",
            f"{name} — инновационное решение, объединяющее блокчейн, машинное обучение и облачные вычисления",
            f"{name} — прорывная система, которая анализирует боль и генерирует персонализированные решения",
            f"{name} — умная платформа будущего, где технологии встречаются с человеческими потребностями",
            f"{name} — креативное решение, которое превращает проблемы в возможности для роста",
            f"{name} — мощный инструмент, использующий big data для анализа и решения сложных задач",
            f"{name} — интуитивная система, которая понимает твои потребности лучше, чем ты сам",
            f"{name} — революционный подход к решению повседневных проблем через инновации",
            f"{name} — умная экосистема, которая адаптируется к твоему образу жизни",
            f"{name} — прорывная технология, которая делает невозможное возможным"
        ]
        
        return random.choice(descriptions)
    
    def _calculate_roflo_level(self, pain_analysis: dict) -> int:
        """Рассчитывает уровень рофла (1-10)"""
        confidence = pain_analysis.get('confidence_score', 0.5)
        urgency = pain_analysis.get('urgency_level', 'средний')
        severity = pain_analysis.get('severity_level', 'средняя')
        
        # Базовый уровень
        level = 5
        
        # Бонусы за уверенность
        if confidence > 0.8:
            level += 3
        elif confidence > 0.6:
            level += 2
        elif confidence > 0.4:
            level += 1
        
        # Бонусы за срочность
        if urgency == 'высокий':
            level += 2
        elif urgency == 'средний':
            level += 1
        
        # Бонусы за серьезность
        if severity == 'высокая':
            level += 2
        elif severity == 'средняя':
            level += 1
        
        return min(level, 10)
    
    def _calculate_startup_potential(self, pain_analysis: dict) -> str:
        """Рассчитывает потенциал стартапа"""
        roflo_level = self._calculate_roflo_level(pain_analysis)
        
        if roflo_level >= 9:
            return "🚀 Готов к IPO завтра!"
        elif roflo_level >= 7:
            return "💪 Серийный стартап!"
        elif roflo_level >= 5:
            return "🎯 Есть потенциал!"
        else:
            return "🤔 Может быть..."
    
    def _calculate_meme_score(self, pain_analysis: dict) -> int:
        """Рассчитывает мемный скор (1-100)"""
        emotions = pain_analysis.get('emotions', [])
        question_type = pain_analysis.get('question_type', '')
        
        score = 50  # Базовый скор
        
        # Бонусы за эмоции
        if 'гнев' in emotions:
            score += 20
        if 'страх' in emotions:
            score += 15
        if 'отчаяние' in emotions:
            score += 25
        
        # Бонусы за тип вопроса
        if 'просьба о помощи' in question_type:
            score += 10
        if 'поиск причины' in question_type:
            score += 5
        
        return min(score, 100)
