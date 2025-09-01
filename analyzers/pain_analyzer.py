import re
from typing import Dict, List, Tuple

class PainAnalyzer:
    def __init__(self):
        # Ключевые слова для определения боли
        self.pain_keywords = {
            'страх': ['боюсь', 'страшно', 'пугает', 'волнуюсь', 'тревожно', 'паника', 'ужас', 'кошмар'],
            'отчаяние': ['не могу', 'не получается', 'застрял', 'безнадежно', 'отчаялся', 'сдался', 'бессилен'],
            'одиночество': ['никто не понимает', 'один', 'некому помочь', 'одиноко', 'покинутый', 'заброшенный'],
            'неуверенность': ['сомневаюсь', 'не знаю', 'запутался', 'не уверен', 'колеблюсь', 'не определился'],
            'давление': ['надо', 'должен', 'срочно', 'дедлайн', 'ожидания', 'обязан', 'вынужден'],
            'сравнение': ['хуже других', 'отстаю', 'не успеваю', 'все лучше меня', 'проигрываю', 'не дотягиваю'],
            'вина': ['виноват', 'накосячил', 'наделал дел', 'провалил', 'подвел', 'ошибся'],
            'стыд': ['стыдно', 'неловко', 'неудобно', 'смущаюсь', 'краснею', 'скромничаю'],
            'гнев': ['злюсь', 'бесит', 'раздражает', 'ненавижу', 'в ярости', 'в бешенстве'],
            'зависть': ['завидую', 'хочу как у других', 'несправедливо', 'почему у них есть', 'не хватает']
        }
        
        # Эмоциональные маркеры
        self.emotion_markers = {
            'гнев': ['злюсь', 'бесит', 'раздражает', 'ненавижу', 'в ярости', 'в бешенстве', 'достало'],
            'грусть': ['грустно', 'тоскливо', 'печально', 'уныло', 'меланхолия', 'депрессия'],
            'тревога': ['волнуюсь', 'беспокоюсь', 'тревожно', 'паника', 'стресс', 'напряжение'],
            'раздражение': ['надоело', 'устал', 'достало', 'заело', 'вымотался', 'измотался'],
            'восторг': ['восторг', 'восторженно', 'восхищение', 'восхищен', 'в восторге'],
            'надежда': ['надеюсь', 'верю', 'уверен', 'оптимизм', 'светлое будущее'],
            'любовь': ['люблю', 'любовь', 'влюблен', 'симпатия', 'привязанность'],
            'благодарность': ['спасибо', 'благодарен', 'ценю', 'признателен', 'обязан']
        }
        
        # Контекстные маркеры для определения серьезности
        self.context_markers = {
            'срочность': ['срочно', 'быстро', 'немедленно', 'сейчас', 'сегодня', 'завтра', 'вчера'],
            'важность': ['важно', 'критично', 'жизненно', 'смертельно', 'необходимо'],
            'частота': ['постоянно', 'всегда', 'никогда', 'часто', 'редко', 'иногда'],
            'влияние': ['влияет', 'мешает', 'мешает жить', 'портит', 'разрушает']
        }
    
    def analyze_pain(self, question: str) -> Dict[str, any]:
        """Анализирует скрытую боль в вопросе"""
        question_lower = question.lower()
        
        # Определяем основные категории боли
        pain_categories = self._identify_pain_categories(question_lower)
        
        # Анализируем эмоциональное состояние
        emotions = self._analyze_emotions(question_lower)
        
        # Определяем уровень срочности
        urgency_level = self._analyze_urgency(question_lower)
        
        # Определяем серьезность проблемы
        severity_level = self._analyze_severity(question_lower)
        
        # Определяем тип вопроса
        question_type = self._analyze_question_type(question_lower)
        
        # Формулируем основную боль
        main_pain = self._formulate_main_pain(pain_categories, emotions, urgency_level, severity_level)
        
        # Генерируем рекомендации
        recommendations = self._generate_recommendations(pain_categories, emotions, question_type)
        
        return {
            'main_pain': main_pain,
            'pain_categories': pain_categories,
            'emotions': emotions,
            'urgency_level': urgency_level,
            'severity_level': severity_level,
            'question_type': question_type,
            'confidence_score': self._calculate_confidence(pain_categories, emotions),
            'recommendations': recommendations
        }
    
    def _identify_pain_categories(self, question: str) -> List[str]:
        """Определяет категории боли"""
        found_categories = []
        
        for category, keywords in self.pain_keywords.items():
            if any(keyword in question for keyword in keywords):
                found_categories.append(category)
        
        return found_categories
    
    def _analyze_emotions(self, question: str) -> List[str]:
        """Анализирует эмоциональное состояние"""
        found_emotions = []
        
        for emotion, markers in self.emotion_markers.items():
            if any(marker in question for marker in markers):
                found_emotions.append(emotion)
        
        return found_emotions
    
    def _analyze_urgency(self, question: str) -> str:
        """Определяет уровень срочности"""
        urgency_words = self.context_markers['срочность']
        
        if any(word in question for word in urgency_words):
            return 'высокий'
        elif 'вчера' in question or 'давно' in question:
            return 'низкий'
        else:
            return 'средний'
    
    def _analyze_severity(self, question: str) -> str:
        """Определяет серьезность проблемы"""
        severity_words = self.context_markers['важность'] + self.context_markers['влияние']
        
        if any(word in question for word in severity_words):
            return 'высокая'
        elif 'может быть' in question or 'возможно' in question:
            return 'низкая'
        else:
            return 'средняя'
    
    def _analyze_question_type(self, question: str) -> str:
        """Определяет тип вопроса"""
        if any(word in question for word in ['как', 'что делать', 'помогите', 'подскажите']):
            return 'просьба о помощи'
        elif any(word in question for word in ['почему', 'зачем', 'откуда', 'когда']):
            return 'поиск причины'
        elif any(word in question for word in ['можно ли', 'стоит ли', 'правильно ли']):
            return 'поиск подтверждения'
        elif any(word in question for word in ['что думаете', 'ваше мнение', 'как считаете']):
            return 'поиск мнения'
        else:
            return 'общий вопрос'
    
    def _formulate_main_pain(self, categories: List[str], emotions: List[str], urgency: str, severity: str) -> str:
        """Формулирует основную боль на основе анализа"""
        if not categories and not emotions:
            return "неопределенная потребность в помощи"
        
        pain_description = []
        
        if categories:
            pain_description.append(f"проблема с {', '.join(categories)}")
        
        if emotions:
            pain_description.append(f"эмоциональное состояние: {', '.join(emotions)}")
        
        if urgency == 'высокий':
            pain_description.append("высокая срочность решения")
        
        if severity == 'высокая':
            pain_description.append("критическая важность")
        
        return ". ".join(pain_description)
    
    def _generate_recommendations(self, categories: List[str], emotions: List[str], question_type: str) -> List[str]:
        """Генерирует рекомендации на основе анализа"""
        recommendations = []
        
        if 'страх' in categories:
            recommendations.append("Попробуйте техники дыхания и медитации")
            recommendations.append("Обратитесь к специалисту по тревожности")
        
        if 'одиночество' in categories:
            recommendations.append("Присоединитесь к сообществам по интересам")
            recommendations.append("Попробуйте новые хобби для знакомств")
        
        if 'неуверенность' in categories:
            recommendations.append("Составьте план действий с конкретными шагами")
            recommendations.append("Начните с малых достижений")
        
        if 'работа' in categories:
            recommendations.append("Проанализируйте свои сильные стороны")
            recommendations.append("Рассмотрите возможности развития")
        
        if question_type == 'просьба о помощи':
            recommendations.append("Не бойтесь просить о помощи у близких")
            recommendations.append("Обратитесь к профессионалам в данной области")
        
        if not recommendations:
            recommendations.append("Попробуйте разбить проблему на части")
            recommendations.append("Ищите поддержку в сообществах")
        
        return recommendations
    
    def _calculate_confidence(self, categories: List[str], emotions: List[str]) -> float:
        """Рассчитывает уверенность в анализе"""
        total_indicators = len(categories) + len(emotions)
        
        if total_indicators == 0:
            return 0.3
        elif total_indicators <= 2:
            return 0.6
        elif total_indicators <= 4:
            return 0.8
        else:
            return 0.95
