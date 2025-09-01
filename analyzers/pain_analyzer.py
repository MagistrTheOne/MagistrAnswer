import re
from typing import Dict, List, Tuple

class PainAnalyzer:
    def __init__(self):
        # Ключевые слова для определения боли
        self.pain_keywords = {
            'страх': ['боюсь', 'страшно', 'пугает', 'волнуюсь', 'тревожно'],
            'отчаяние': ['не могу', 'не получается', 'застрял', 'безнадежно'],
            'одиночество': ['никто не понимает', 'один', 'некому помочь'],
            'неуверенность': ['сомневаюсь', 'не знаю', 'запутался', 'не уверен'],
            'давление': ['надо', 'должен', 'срочно', 'дедлайн', 'ожидания'],
            'сравнение': ['хуже других', 'отстаю', 'не успеваю', 'все лучше меня']
        }
        
        # Эмоциональные маркеры
        self.emotion_markers = {
            'гнев': ['злюсь', 'бесит', 'раздражает', 'ненавижу'],
            'грусть': ['грустно', 'тоскливо', 'печально', 'уныло'],
            'тревога': ['волнуюсь', 'беспокоюсь', 'тревожно', 'паника'],
            'раздражение': ['надоело', 'устал', 'достало', 'заело']
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
        
        # Формулируем основную боль
        main_pain = self._formulate_main_pain(pain_categories, emotions, urgency_level)
        
        return {
            'main_pain': main_pain,
            'pain_categories': pain_categories,
            'emotions': emotions,
            'urgency_level': urgency_level,
            'confidence_score': self._calculate_confidence(pain_categories, emotions)
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
        urgency_words = ['срочно', 'быстро', 'немедленно', 'сейчас', 'сегодня']
        
        if any(word in question for word in urgency_words):
            return 'высокий'
        elif 'вчера' in question or 'давно' in question:
            return 'низкий'
        else:
            return 'средний'
    
    def _formulate_main_pain(self, categories: List[str], emotions: List[str], urgency: str) -> str:
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
        
        return ". ".join(pain_description)
    
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
