# ⚡ QUICK START (3 Minutes)

**Самая простая инструкция для тех кто не шарит в коде.**

---

## 🎯 Что нужно сделать (всего 3 шага!)

### ШАГ 1: Получить API ключ OpenAI

1. Иди сюда: https://platform.openai.com/signup
2. Зарегистрируйся (или войди)
3. Добавь карту: Billing → Payment methods
4. Создай ключ: API keys → Create new secret key
5. **СКОПИРУЙ КЛЮЧ** - он выглядит так: `sk-proj-abc123...`

**💰 Стоимость:** ~$1-2 в день тестирования

---

### ШАГ 2: Добавить ключ в проект

#### Вариант А: В Терминале (рекомендую)
```bash
# 1. Открой терминал в папке проекта
cd Skyro_case

# 2. Скопируй пример файла
cp .env.example .env

# 3. Открой файл
nano .env
# (или: code .env если у тебя VSCode)

# 4. Найди строку:
OPENAI_API_KEY=sk-your-openai-api-key-here

# 5. Замени на ТВОЙ ключ:
OPENAI_API_KEY=sk-proj-твой_настоящий_ключ_сюда

# 6. Сохрани:
# В nano: Ctrl+X, потом Y, потом Enter
```

#### Вариант Б: Через Проводник (проще для новичков)

**Windows:**
1. Открой папку `Skyro_case` в Проводнике
2. Найди файл `.env.example`
3. Правый клик → Копировать
4. Правый клик в пустом месте → Вставить
5. Переименуй копию в `.env` (убери `.example`)
6. Открой `.env` в Блокноте
7. Найди: `OPENAI_API_KEY=sk-your-openai-api-key-here`
8. Замени на: `OPENAI_API_KEY=sk-proj-твой_ключ`
9. Сохрани (Ctrl+S)

**Mac:**
1. Открой папку `Skyro_case` в Finder
2. Найди файл `.env.example`
3. Cmd+D (дублировать)
4. Переименуй в `.env`
5. Открой в TextEdit
6. Замени ключ
7. Сохрани (Cmd+S)

**⚠️ ВАЖНО:** Файл должен называться ТОЧНО `.env` (с точкой, без расширения)

---

### ШАГ 3: Запустить

```bash
# Убедись что ты в папке проекта
cd Skyro_case

# Одна команда запускает всё:
docker-compose up -d
```

**Подожди 2-3 минуты** пока всё загрузится.

Потом открой в браузере: **http://localhost:8501**

---

## ✅ Проверка что всё работает

1. Открой http://localhost:8501
2. Должен быть чат с заголовком "🧠 Skyro Knowledge Assistant"
3. Спроси что-нибудь: "What are our Q1 2024 OKRs?"
4. Получишь ответ с источниками документов

**Если видишь ответ - ГОТОВО! 🎉**

---

## 🔥 Частые косяки

### "Cannot connect to Docker daemon"
**Решение:** Запусти Docker Desktop (должна быть иконка кита)

### "Port already in use"
**Решение:**
```bash
docker-compose down
docker-compose up -d
```

### "Invalid API key"
**Решение:** Проверь файл `.env`:
- Ключ начинается с `sk-proj-` или `sk-`?
- Нет лишних пробелов?
- Файл точно называется `.env`?

### Backend всё время перезапускается
**Решение:**
```bash
# Посмотри логи что не так:
docker-compose logs backend

# Обычно проблема в неправильном API ключе
```

### UI показывает "System Offline"
**Решение:**
```bash
# Перезапусти backend:
docker-compose restart backend

# Подожди минуту, обнови страницу в браузере
```

---

## 🛑 Остановить всё

```bash
docker-compose down
```

---

## 📚 Подробные гайды

Если что-то непонятно, читай:
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - полная инструкция для новичков
- [README.md](README.md) - техническая документация
- [HOW_TO_ADD_PDF_WORD.md](HOW_TO_ADD_PDF_WORD.md) - как добавить свои файлы

---

## 🎓 Что дальше?

1. Попробуй задать разные вопросы
2. Добавь свои документы (в `data/documents/`)
3. Посмотри API документацию: http://localhost:8000/docs

---

**Всё ещё не работает?**
1. Прочитай логи: `docker-compose logs backend`
2. Погугли ошибку
3. Создай issue: https://github.com/kaiyrbek777/Skyro_case/issues

**Удачи! 🚀**
