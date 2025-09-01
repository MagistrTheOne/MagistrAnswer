import requests
import random
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import config

class QuestionParser:
    def __init__(self):
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
    
    def get_random_question(self) -> Optional[Dict[str, str]]:
        """Получает случайный вопрос с Answer Mail.ru"""
        for url in self.urls:
            try:
                print(f"🔍 Пробую URL: {url}")
                response = self.session.get(
                    url,
                    timeout=15,  # Увеличиваем таймаут
                    allow_redirects=True
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                questions = self._extract_questions(soup)
                
                if questions:
                    question = random.choice(questions)
                    print(f"✅ Найдено вопросов: {len(questions)}")
                    time.sleep(config.DELAY_BETWEEN_REQUESTS)
                    return question
                
            except requests.exceptions.Timeout:
                print(f"⏰ Таймаут для {url}")
                continue
            except requests.exceptions.RequestException as e:
                print(f"❌ Ошибка запроса для {url}: {e}")
                continue
            except Exception as e:
                print(f"❌ Общая ошибка для {url}: {e}")
                continue
        
        print("❌ Не удалось получить вопросы ни с одного URL")
        return None
    
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
