import requests
import random
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import config

class QuestionParser:
    def __init__(self):
        """Инициализация парсера"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Альтернативные URL для парсинга
        self.urls = [
            "https://otvet.mail.ru",
            "https://otvet.mail.ru/popular",
            "https://otvet.mail.ru/question",
            "https://otvet.mail.ru/answer"
        ]
        
        # Игровые категории вопросов
        self.game_categories = {
            'любовь': ['отношения', 'любовь', 'брак', 'семья', 'свидание', 'развод', 'измена', 'ревность'],
            'работа': ['карьера', 'работа', 'бизнес', 'деньги', 'зарплата', 'начальник', 'коллеги', 'увольнение'],
            'здоровье': ['здоровье', 'болезнь', 'врач', 'лечение', 'диета', 'спорт', 'похудение', 'курение'],
            'образование': ['учеба', 'экзамен', 'школа', 'университет', 'знания', 'домашка', 'учитель', 'оценки'],
            'технологии': ['компьютер', 'интернет', 'смартфон', 'программа', 'гаджет', 'соцсети', 'игры', 'вирусы'],
            'путешествия': ['путешествие', 'отпуск', 'поездка', 'страна', 'город', 'билеты', 'отель', 'чемодан']
        }
        
        # Рофло-вопросы для разнообразия
        self.roflo_questions = [
            "Почему мой холодильник не понимает мои эмоции?",
            "Как заставить тостер делать тосты с настроением?",
            "Почему интернет не работает, когда я хочу посмотреть мемы?",
            "Как объяснить коту, что он не может быть программистом?",
            "Почему мой телефон злится, когда я его роняю?",
            "Как заставить стиральную машину стирать мои проблемы?",
            "Почему микроволновка не может готовить счастье?",
            "Как научить телевизор показывать только хорошие новости?",
            "Почему мой ноутбук грустит по вечерам?",
            "Как заставить принтер печатать деньги?",
            "Почему мой смартфон завидует айфону?",
            "Как объяснить навигатору, что я хочу заблудиться?",
            "Почему мой планшет не может заменить психолога?",
            "Как заставить кофемашину варить кофе счастья?",
            "Почему мой компьютер не понимает сарказм?",
            "Как научить робота-пылесоса убирать мои мысли?",
            "Почему мой смарт-часы не могут остановить время?",
            "Как заставить умный дом понимать мои эмоции?",
            "Почему мой ноутбук не может генерировать мемы?",
            "Как объяснить ассистенту, что я хочу быть ленивым?",
            "Почему мой телефон не может предсказывать будущее?",
            "Как заставить умную колонку петь мои любимые песни?",
            "Почему мой планшет не может читать мысли?",
            "Как научить смарт-часы понимать мои мечты?",
            "Почему мой компьютер не может создать идеальный мем?",
            "Как заставить умный холодильник готовить счастье?",
            "Почему мой смартфон не может лечить депрессию?",
            "Как объяснить роботу, что я хочу быть человеком?",
            "Почему мой ноутбук не может генерировать идеи?",
            "Как заставить умную лампу светить радостью?",
            "Почему мой планшет не может предсказывать погоду?",
            "Как научить смарт-часы понимать мои чувства?",
            "Почему мой компьютер не может создать шедевр?",
            "Как заставить умную кофемашину варить вдохновение?",
            "Почему мой телефон не может читать эмоции?",
            "Как объяснить ассистенту, что я хочу быть гением?",
            "Почему мой ноутбук не может генерировать счастье?",
            "Как заставить умный дом понимать мои желания?",
            "Почему мой планшет не может создавать искусство?",
            "Как научить смарт-часы понимать мои цели?",
            "Почему мой компьютер не может предсказывать успех?",
            "Как заставить умную колонку петь мои мечты?",
            "Почему мой смартфон не может генерировать идеи?",
            "Как объяснить роботу, что я хочу быть творцом?",
            "Почему мой ноутбук не может создавать будущее?",
            "Как заставить умный холодильник готовить мечты?",
            "Почему мой планшет не может читать судьбу?",
            "Как научить смарт-часы понимать мои амбиции?",
            "Почему мой компьютер не может генерировать гениальность?",
            "Как заставить умную лампу светить вдохновением?",
            "Почему мой телефон не может предсказывать счастье?",
            "Как объяснить ассистенту, что я хочу быть пророком?"
        ]
    
    def get_random_question(self) -> Optional[Dict[str, str]]:
        """Получает случайный вопрос с Answer Mail.ru"""
        # Сначала пробуем получить реальный вопрос
        for url in self.urls:
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                questions = self._extract_questions(soup)
                
                if questions:
                    question = random.choice(questions)
                    return {
                        'text': question['text'],
                        'source': 'Answer Mail.ru',
                        'type': 'real'
                    }
                    
            except Exception as e:
                continue
        
        # Если не удалось получить реальный вопрос, возвращаем рофло-вопрос
        return self.get_roflo_question()
    
    def get_roflo_question(self) -> Dict[str, str]:
        """Получает случайный рофло-вопрос"""
        question = random.choice(self.roflo_questions)
        return {
            'text': question,
            'source': 'Рофло-генератор',
            'type': 'roflo'
        }
    
    def get_multiple_questions(self, count: int = 10) -> List[Dict[str, str]]:
        """Получает несколько вопросов для демонстрации"""
        questions = []
        
        # Добавляем рофло-вопросы
        roflo_count = min(count // 2, len(self.roflo_questions))
        roflo_selection = random.sample(self.roflo_questions, roflo_count)
        
        for question in roflo_selection:
            questions.append({
                'text': question,
                'source': 'Рофло-генератор',
                'type': 'roflo'
            })
        
        # Пытаемся добавить реальные вопросы
        try:
            for url in self.urls[:2]:  # Берем только первые 2 URL
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    real_questions = self._extract_questions(soup)
                    
                    if real_questions:
                        # Берем случайные реальные вопросы
                        real_count = min(count - len(questions), len(real_questions))
                        real_selection = random.sample(real_questions, real_count)
                        
                        for question in real_selection:
                            questions.append({
                                'text': question['text'],
                                'source': 'Answer Mail.ru',
                                'type': 'real'
                            })
                        
                        break
                        
                except Exception:
                    continue
                    
        except Exception:
            pass
        
        # Если вопросов все еще мало, добавляем еще рофло
        while len(questions) < count:
            roflo_question = random.choice(self.roflo_questions)
            if not any(q['text'] == roflo_question for q in questions):
                questions.append({
                    'text': roflo_question,
                    'source': 'Рофло-генератор',
                    'type': 'roflo'
                })
        
        return questions[:count]
    
    def process_user_question(self, user_question: str) -> Dict[str, str]:
        """Обрабатывает вопрос от пользователя"""
        return {
            'text': user_question,
            'source': 'Пользователь',
            'type': 'custom'
        }
    
    def get_question_by_category(self, category: str) -> Optional[Dict[str, str]]:
        """Получает вопрос по игровой категории"""
        if category.lower() in self.game_categories:
            # Ищем вопросы с ключевыми словами категории
            for url in self.urls:
                try:
                    response = self.session.get(url, timeout=15)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    questions = self._extract_questions_by_category(soup, category)
                    
                    if questions:
                        question = random.choice(questions)
                        return {
                            'text': question['text'],
                            'source': 'Answer Mail.ru',
                            'type': 'category',
                            'category': category
                        }
                        
                except Exception as e:
                    continue
        
        return None
    
    def get_random_question_by_category(self, category: str = None) -> Optional[Dict[str, str]]:
        """Получает случайный вопрос по категории или общий"""
        if category and category.lower() in self.game_categories:
            return self.get_question_by_category(category)
        else:
            return self.get_random_question()
    
    def _extract_questions(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлекает вопросы из HTML с расширенными селекторами"""
        questions = []
        
        # Расширенный список селекторов для поиска вопросов
        selectors = [
            '.question__text',
            '.question-title',
            '.question',
            'h2 a',
            '.qa-item__title',
            '.question-item__title',
            '.question-item__text',
            '.qa-question__title',
            '.qa-question__text',
            'h3 a',
            'h4 a',
            '.title a',
            '.text a',
            'a[href*="question"]',
            'a[href*="answer"]'
        ]
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    print(f"🔍 Найден селектор: {selector} ({len(elements)} элементов)")
                    for element in elements[:15]:  # Берем больше элементов
                        text = element.get_text(strip=True)
                        if text and len(text) > 15 and len(text) < 200:  # Фильтруем по длине
                            # Проверяем, что это похоже на вопрос
                            if any(word in text.lower() for word in ['как', 'что', 'где', 'когда', 'почему', 'зачем', 'можно ли', 'стоит ли']):
                                questions.append({
                                    'text': text,
                                    'source': 'Answer Mail.ru'
                                })
                    if questions:
                        break
            except Exception as e:
                print(f"⚠️ Ошибка при обработке селектора {selector}: {e}")
                continue
        
        # Если не нашли по селекторам, ищем по тексту
        if not questions:
            questions = self._extract_questions_by_text(soup)
        
        return questions
    
    def _extract_questions_by_category(self, soup: BeautifulSoup, category: str) -> List[Dict[str, str]]:
        """Извлекает вопросы по конкретной категории"""
        questions = []
        keywords = self.game_categories.get(category.lower(), [])
        
        # Ищем все ссылки с текстом
        links = soup.find_all('a', href=True)
        
        for link in links:
            text = link.get_text(strip=True)
            if text and len(text) > 20 and len(text) < 150:
                # Проверяем, что текст содержит ключевые слова категории
                if any(keyword in text.lower() for keyword in keywords):
                    questions.append({
                        'text': text,
                        'source': 'Answer Mail.ru'
                    })
                    if len(questions) >= 10:
                        break
        
        return questions
    
    def _extract_questions_by_text(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлекает вопросы по тексту, если селекторы не сработали"""
        questions = []
        
        # Ищем все ссылки с текстом
        links = soup.find_all('a', href=True)
        
        for link in links:
            text = link.get_text(strip=True)
            if text and len(text) > 20 and len(text) < 150:
                # Проверяем, что это похоже на вопрос
                if any(word in text.lower() for word in ['как', 'что', 'где', 'когда', 'почему', 'зачем', 'можно ли', 'стоит ли', 'помогите', 'подскажите']):
                    questions.append({
                        'text': text,
                        'source': 'Answer Mail.ru'
                    })
                    if len(questions) >= 10:
                        break
        
        return questions
    
    def get_questions_by_category(self, category: str = "popular") -> List[Dict[str, str]]:
        """Получает вопросы по категории"""
        try:
            url = f"{config.ANSWER_MAIL_RU_URL}/{category}"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return self._extract_questions(soup)
            
        except Exception as e:
            print(f"❌ Ошибка при получении вопросов по категории: {e}")
            return []
    
    def close(self):
        """Закрывает сессию"""
        self.session.close()
