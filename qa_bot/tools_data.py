"""
QA Bot — Tools Knowledge Base v3.0
Полные инструкции по установке, настройке и использованию инструментов тестировщика.
"""

TOOLS_CATEGORIES = {
    "bugtracking": {
        "name": "🐛 Баг-трекеры",
        "description": "Системы для управления дефектами и задачами",
        "tools": ["jira", "youtrack", "mantis"],
    },
    "api": {
        "name": "🔌 API тестирование",
        "description": "Инструменты для тестирования REST/GraphQL/gRPC API",
        "tools": ["postman", "insomnia", "httpie"],
    },
    "automation": {
        "name": "🤖 Автоматизация браузера",
        "description": "Фреймворки для автоматизации web UI тестирования",
        "tools": ["selenium", "playwright", "cypress"],
    },
    "performance": {
        "name": "⚡ Нагрузочное тестирование",
        "description": "Инструменты для проверки производительности",
        "tools": ["jmeter", "k6", "gatling"],
    },
    "mobile": {
        "name": "📱 Мобильное тестирование",
        "description": "Инструменты для тестирования iOS и Android приложений",
        "tools": ["appium", "charles"],
    },
    "traffic": {
        "name": "🔍 Перехват трафика",
        "description": "Инструменты для анализа HTTP/HTTPS запросов",
        "tools": ["fiddler", "mitmproxy", "wireshark"],
    },
    "database": {
        "name": "🗄️ Работа с БД",
        "description": "Инструменты для тестирования баз данных",
        "tools": ["dbeaver", "pgadmin"],
    },
    "ci_cd": {
        "name": "🔄 CI/CD",
        "description": "Инструменты непрерывной интеграции и доставки",
        "tools": ["jenkins", "gitlab_ci", "github_actions"],
    },
}

TOOLS_DATA = {
    # ─── БАГ-ТРЕКЕРЫ ───────────────────────────────────────────────────────────

    "jira": {
        "name": "Jira",
        "emoji": "📋",
        "category": "bugtracking",
        "tagline": "Самый популярный в мире баг-трекер и менеджер задач",
        "description": (
            "<b>Jira</b> — платформа Atlassian для управления проектами и дефектами. "
            "Используется в 65%+ IT-компаний. Поддерживает Scrum, Kanban, Waterfall. "
            "На каждом собеседовании QA спросят: 'Работал с Jira?'"
        ),
        "install": (
            "<b>Установка / Начало работы:</b>\n"
            "1️⃣ <b>Cloud (рекомендуется):</b>\n"
            "   • Открой <a href='https://www.atlassian.com/software/jira'>atlassian.com/jira</a>\n"
            "   • Нажми <i>Get it free</i> → зарегистрируйся\n"
            "   • Бесплатно до 10 пользователей\n\n"
            "2️⃣ <b>Data Center (локально):</b>\n"
            "   • Требует Java 11+, PostgreSQL/MySQL\n"
            "   • Скачай с <a href='https://www.atlassian.com/software/jira/download'>сайта</a>\n"
            "   • <code>java -jar atlassian-jira-*.jar</code>"
        ),
        "features": (
            "<b>Ключевые функции:</b>\n"
            "• <b>Issue tracking</b> — создание задач/багов с полями: Summary, Description, Priority, "
            "Severity, Steps to Reproduce, Expected/Actual Result, Attachments\n"
            "• <b>Workflow</b> — настраиваемые статусы: Open → In Progress → In Review → Done\n"
            "• <b>Boards</b> — Scrum (спринты) и Kanban (поток задач)\n"
            "• <b>Filters + JQL</b> — мощный язык запросов для поиска:\n"
            "  <code>project = QA AND issuetype = Bug AND priority = High</code>\n"
            "• <b>Dashboards</b> — метрики: burn-down chart, velocity, bug rate\n"
            "• <b>Интеграции</b> — GitLab, GitHub, Confluence, Slack, TestRail"
        ),
        "usage_example": (
            "<b>Пример: как правильно создать баг в Jira</b>\n\n"
            "<b>Summary:</b> <code>[Login] Пользователь не может войти с валидным паролем</code>\n"
            "<b>Type:</b> Bug | <b>Priority:</b> High | <b>Severity:</b> Critical\n"
            "<b>Environment:</b> Chrome 120, Windows 11, Staging\n\n"
            "<b>Steps to Reproduce:</b>\n"
            "1. Открыть example.com/login\n"
            "2. Ввести: user@test.com / Test1234!\n"
            "3. Нажать «Войти»\n\n"
            "<b>Expected:</b> Успешный вход в личный кабинет\n"
            "<b>Actual:</b> Ошибка 401 «Invalid credentials»\n"
            "<b>Attachments:</b> screenshot.png, network-log.har"
        ),
        "tips": [
            "💡 Изучи JQL — это как SQL для Jira. Незаменимо для фильтрации",
            "💡 Используй «Link issue» для связи бага с задачей, которая его вызвала",
            "💡 Шаблоны (Issue Templates) экономят время при повторяющихся багах",
        ],
        "docs_url": "https://support.atlassian.com/jira-software-cloud/",
    },

    "youtrack": {
        "name": "YouTrack",
        "emoji": "🔶",
        "category": "bugtracking",
        "tagline": "Умный баг-трекер от JetBrains с мощным поиском",
        "description": (
            "<b>YouTrack</b> от JetBrains — альтернатива Jira. "
            "Умный поиск, горячие клавиши, интеграция с IDE. "
            "Бесплатно до 10 пользователей в Cloud."
        ),
        "install": (
            "<b>Начало работы:</b>\n"
            "🌐 <b>Cloud:</b> <a href='https://www.jetbrains.com/youtrack/'>jetbrains.com/youtrack</a> → Get started free\n\n"
            "💻 <b>Локально (Docker):</b>\n"
            "<pre>docker run -it --name youtrack \\\n"
            "  -v ~/youtrack/data:/opt/youtrack/data \\\n"
            "  -p 8080:8080 \\\n"
            "  jetbrains/youtrack:latest</pre>"
        ),
        "features": (
            "<b>Ключевые функции:</b>\n"
            "• <b>Естественный поиск</b> — <code>for: me #Unresolved priority: High</code>\n"
            "• <b>Agile boards</b> — Scrum + Kanban из коробки\n"
            "• <b>Time tracking</b> — учёт времени прямо в задаче\n"
            "• <b>Workflows (Kotlin)</b> — автоматизация без плагинов\n"
            "• <b>VCS интеграция</b> — GitHub, GitLab, Bitbucket"
        ),
        "usage_example": (
            "<b>Пример запросов:</b>\n"
            "<code>#Unresolved for: me</code> — мои открытые задачи\n"
            "<code>project: QA type: Bug sort by: priority</code> — все баги\n"
            "<code>created: today assignee: {QA Team}</code> — сегодняшние задачи команды"
        ),
        "tips": [
            "💡 Горячие клавиши: 'c' — создать задачу, '/' — поиск",
            "💡 Интеграция с IntelliJ IDEA: баги прямо в IDE",
        ],
        "docs_url": "https://www.jetbrains.com/help/youtrack/standalone/",
    },

    "mantis": {
        "name": "MantisBT",
        "emoji": "🦗",
        "category": "bugtracking",
        "tagline": "Простой open-source баг-трекер",
        "description": (
            "<b>MantisBT</b> — бесплатный open-source баг-трекер. "
            "Прост в установке, хорошо подходит для небольших команд."
        ),
        "install": (
            "<b>Установка (Docker):</b>\n"
            "<pre>docker run -d -p 80:80 \\\n"
            "  -e MANTIS_DB_HOST=db \\\n"
            "  vimagick/mantisbt</pre>\n\n"
            "Или скачай с <a href='https://www.mantisbt.org/download.php'>mantisbt.org</a>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Базовый workflow: New → Assigned → Resolved → Closed\n"
            "• Email уведомления\n"
            "• REST API\n"
            "• Плагины для расширения"
        ),
        "usage_example": (
            "<b>Когда выбирать MantisBT:</b>\n"
            "✅ Небольшая команда (до 10 чел)\n"
            "✅ Нет бюджета на Jira\n"
            "✅ Нужно simple & fast\n"
            "❌ Крупные enterprise-проекты — лучше Jira"
        ),
        "tips": [
            "💡 MantisBT проще Jira, но функций меньше",
            "💡 Хорошо интегрируется с Git через плагин Source Control",
        ],
        "docs_url": "https://docs.mantisbt.org/",
    },

    # ─── API ТЕСТИРОВАНИЕ ──────────────────────────────────────────────────────

    "postman": {
        "name": "Postman",
        "emoji": "📮",
        "category": "api",
        "tagline": "Стандарт индустрии для тестирования API",
        "description": (
            "<b>Postman</b> — главный инструмент QA для API тестирования. "
            "Используется повсеместно. Обязателен для резюме Junior QA. "
            "GUI-интерфейс, коллекции, автотесты на JavaScript."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "🌐 Скачай с <a href='https://www.postman.com/downloads/'>postman.com/downloads</a>\n"
            "• Windows: .exe установщик\n"
            "• Mac: .dmg или <code>brew install --cask postman</code>\n"
            "• Linux: snap install postman / .tar.gz\n\n"
            "<b>Или используй Web:</b> <a href='https://web.postman.co'>web.postman.co</a> (бесплатно)"
        ),
        "features": (
            "<b>Ключевые функции:</b>\n"
            "• <b>HTTP запросы</b> — GET, POST, PUT, DELETE, PATCH, HEAD\n"
            "• <b>Коллекции</b> — организация запросов по папкам\n"
            "• <b>Environments</b> — переменные для dev/staging/prod\n"
            "• <b>Tests (JS)</b> — автоматическая проверка ответов:\n"
            "  <pre>pm.test('Status 200', () => {\n  pm.response.to.have.status(200);\n});\npm.test('Body has id', () => {\n  pm.expect(pm.response.json().id).to.exist;\n});</pre>\n"
            "• <b>Pre-request Scripts</b> — подготовка данных перед запросом\n"
            "• <b>Collection Runner</b> — запуск всей коллекции\n"
            "• <b>Mock Server</b> — эмуляция API\n"
            "• <b>Newman</b> — запуск коллекций из CLI в CI/CD"
        ),
        "usage_example": (
            "<b>Пример теста авторизации:</b>\n\n"
            "1. <b>POST /api/auth/login</b>\n"
            "Body (JSON):\n"
            "<pre>{\"email\": \"test@test.com\", \"password\": \"Test1234!\"}</pre>\n\n"
            "2. <b>Tests (вкладка):</b>\n"
            "<pre>pm.test(\"Status 200\", () => {\n  pm.response.to.have.status(200);\n});\nconst json = pm.response.json();\npm.test(\"Token exists\", () => {\n  pm.expect(json.token).to.be.a('string');\n});\npm.environment.set(\"auth_token\", json.token);</pre>\n\n"
            "3. Далее в запросах используешь: <code>{{auth_token}}</code>"
        ),
        "tips": [
            "💡 Используй Environment Variables: {{base_url}}, {{token}} — не хардкодь URL",
            "💡 Pre-request Script может генерировать тестовые данные: <code>pm.variables.set('email', 'test'+Date.now()+'@test.com')</code>",
            "💡 Newman позволяет запускать коллекции в CI: <code>newman run collection.json -e env.json</code>",
            "💡 Экспортируй коллекцию в репозиторий — это и есть автотесты",
        ],
        "docs_url": "https://learning.postman.com/docs/",
    },

    "insomnia": {
        "name": "Insomnia",
        "emoji": "😴",
        "category": "api",
        "tagline": "Лёгкая альтернатива Postman с поддержкой GraphQL",
        "description": (
            "<b>Insomnia</b> — быстрый API-клиент с отличной поддержкой GraphQL. "
            "Open-source, меньше bloatware чем Postman."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "🌐 <a href='https://insomnia.rest/download'>insomnia.rest/download</a>\n"
            "• Windows/Mac/Linux: скачай и установи\n"
            "• Mac: <code>brew install --cask insomnia</code>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• REST, GraphQL, gRPC, WebSocket поддержка\n"
            "• Нативный GraphQL editor с автодополнением\n"
            "• Environment Variables\n"
            "• Шаблонные теги: <code>{% faker 'email' %}</code>\n"
            "• Git sync (встроенный)"
        ),
        "usage_example": (
            "<b>GraphQL запрос:</b>\n"
            "<pre>query GetUser($id: ID!) {\n  user(id: $id) {\n    id\n    name\n    email\n  }\n}</pre>"
        ),
        "tips": [
            "💡 Идеален для GraphQL API — лучше чем Postman",
            "💡 Inso CLI — аналог Newman для Insomnia",
        ],
        "docs_url": "https://docs.insomnia.rest/",
    },

    "httpie": {
        "name": "HTTPie",
        "emoji": "🖥️",
        "category": "api",
        "tagline": "Удобный HTTP-клиент для терминала",
        "description": (
            "<b>HTTPie</b> — командная строка для HTTP запросов. "
            "Гораздо удобнее curl для тестирования API вручную."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "• Windows: <code>winget install HTTPie.HTTPie</code> или скачай GUI\n"
            "• Mac: <code>brew install httpie</code>\n"
            "• Linux: <code>pip install httpie</code> или <code>apt install httpie</code>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Читаемый синтаксис вместо curl\n"
            "• JSON по умолчанию\n"
            "• Цветной вывод\n"
            "• Сессии"
        ),
        "usage_example": (
            "<b>Примеры команд:</b>\n"
            "<pre>http GET api.example.com/users</pre>\n"
            "<pre>http POST api.example.com/login email=test@test.com password=123</pre>\n"
            "<pre>http PUT api.example.com/users/1 Authorization:'Bearer TOKEN' name='John'</pre>"
        ),
        "tips": [
            "💡 Намного читаемее curl, освой для быстрой отладки API",
            "💡 --download флаг — скачать файл по API",
        ],
        "docs_url": "https://httpie.io/docs",
    },

    # ─── АВТОМАТИЗАЦИЯ БРАУЗЕРА ────────────────────────────────────────────────

    "selenium": {
        "name": "Selenium",
        "emoji": "🤖",
        "category": "automation",
        "tagline": "Стандарт автоматизации браузера уже 15+ лет",
        "description": (
            "<b>Selenium WebDriver</b> — самый популярный инструмент автоматизации браузера. "
            "Поддерживает Python, Java, C#, JS. Работает в Chrome, Firefox, Safari, Edge."
        ),
        "install": (
            "<b>Установка (Python):</b>\n"
            "<pre>pip install selenium</pre>\n\n"
            "<b>WebDriver Manager (авто-загрузка драйверов):</b>\n"
            "<pre>pip install webdriver-manager</pre>\n\n"
            "<b>Минимальный тест:</b>\n"
            "<pre>from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom webdriver_manager.chrome import ChromeDriverManager\n\ndriver = webdriver.Chrome(ChromeDriverManager().install())\ndriver.get('https://google.com')\nprint(driver.title)\ndriver.quit()</pre>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Поддержка всех браузеров\n"
            "• Многоязычный (Python, Java, JS, C#, Ruby)\n"
            "• Selenium Grid — параллельный запуск\n"
            "• Page Object Model (POM) — архитектурный паттерн\n"
            "• Headless mode: <code>options.add_argument('--headless')</code>"
        ),
        "usage_example": (
            "<b>Пример: тест авторизации с POM</b>\n"
            "<pre>class LoginPage:\n  def __init__(self, driver):\n    self.driver = driver\n  \n  def login(self, email, password):\n    self.driver.find_element(By.ID, 'email').send_keys(email)\n    self.driver.find_element(By.ID, 'password').send_keys(password)\n    self.driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()\n  \n  def get_error(self):\n    return self.driver.find_element(By.CLASS_NAME, 'error').text\n\n# Тест\npage = LoginPage(driver)\npage.login('bad@test.com', 'wrong')\nassert page.get_error() == 'Invalid credentials'</pre>"
        ),
        "tips": [
            "💡 Используй явные ожидания WebDriverWait, не time.sleep()",
            "💡 Page Object Model — обязательный паттерн для поддерживаемых тестов",
            "💡 Selenium IDE (расширение Chrome) — запись сценариев без кода",
            "💡 Selenium Grid — запуск тестов в параллели на разных браузерах",
        ],
        "docs_url": "https://www.selenium.dev/documentation/",
    },

    "playwright": {
        "name": "Playwright",
        "emoji": "🎭",
        "category": "automation",
        "tagline": "Современный фреймворк от Microsoft. Быстрее Selenium",
        "description": (
            "<b>Playwright</b> от Microsoft — современная альтернатива Selenium. "
            "Быстрее, стабильнее, умеет перехватывать сеть и работать с несколькими вкладками. "
            "Поддерживает Python, JS/TS, Java, C#."
        ),
        "install": (
            "<b>Установка (Python):</b>\n"
            "<pre>pip install playwright\nplaywright install</pre>\n\n"
            "<b>Или через Node.js:</b>\n"
            "<pre>npm init playwright@latest</pre>"
        ),
        "features": (
            "<b>Ключевые преимущества над Selenium:</b>\n"
            "• <b>Auto-wait</b> — сам ждёт элементы, нет явных ожиданий\n"
            "• <b>Network intercept</b> — мокаем API в тестах\n"
            "• <b>Multi-tab</b> — работа с несколькими вкладками\n"
            "• <b>Screenshot/Video</b> — при падении теста сразу скриншот\n"
            "• <b>Codegen</b> — запись тестов через GUI: <code>playwright codegen example.com</code>\n"
            "• <b>Trace Viewer</b> — пошаговый просмотр упавшего теста"
        ),
        "usage_example": (
            "<b>Пример теста (Python):</b>\n"
            "<pre>from playwright.sync_api import sync_playwright\n\nwith sync_playwright() as p:\n  browser = p.chromium.launch()\n  page = browser.new_page()\n  \n  # Перехват API — мокаем ответ\n  page.route('**/api/user', lambda r: r.fulfill(\n    json={'name': 'Test User'}\n  ))\n  \n  page.goto('https://example.com')\n  page.fill('#email', 'test@test.com')\n  page.click('button[type=submit]')\n  \n  # Автоматически ждёт элемент\n  page.wait_for_selector('.dashboard')\n  assert 'Dashboard' in page.title()\n  browser.close()</pre>"
        ),
        "tips": [
            "💡 <code>playwright codegen URL</code> — записывает тест в браузере",
            "💡 <code>--ui</code> флаг — визуальный запуск тестов с Trace Viewer",
            "💡 Playwright быстрее Selenium в 2-5 раз на сложных сценариях",
            "💡 Network mocking — незаменимо для тестирования без реального backend",
        ],
        "docs_url": "https://playwright.dev/python/docs/intro",
    },

    "cypress": {
        "name": "Cypress",
        "emoji": "🌲",
        "category": "automation",
        "tagline": "E2E тестирование прямо в браузере",
        "description": (
            "<b>Cypress</b> — JavaScript E2E фреймворк. "
            "Работает непосредственно в браузере, видит всё что происходит. "
            "Популярен в frontend-командах."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "<pre>npm install cypress --save-dev\nnpx cypress open</pre>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Визуальный Test Runner — видишь тест в браузере\n"
            "• Time Travel — снимок состояния на каждом шаге\n"
            "• Auto-retry — сам повторяет при нестабильных элементах\n"
            "• Network stubbing\n"
            "• Component testing (Vue, React)"
        ),
        "usage_example": (
            "<b>Пример теста:</b>\n"
            "<pre>describe('Login', () => {\n  it('успешный вход', () => {\n    cy.visit('/login')\n    cy.get('#email').type('test@test.com')\n    cy.get('#password').type('Test1234!')\n    cy.get('[type=submit]').click()\n    cy.url().should('include', '/dashboard')\n    cy.contains('Welcome').should('be.visible')\n  })\n})</pre>"
        ),
        "tips": [
            "💡 Cypress работает только в браузере и только на JS/TS",
            "💡 Лучший выбор если у вас JS-стек и frontend-команда",
            "💡 Selenium/Playwright — если нужна кроссбраузерность или Python",
        ],
        "docs_url": "https://docs.cypress.io/",
    },

    # ─── НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ ──────────────────────────────────────────────

    "jmeter": {
        "name": "Apache JMeter",
        "emoji": "⚡",
        "category": "performance",
        "tagline": "Стандарт нагрузочного тестирования",
        "description": (
            "<b>JMeter</b> — самый популярный инструмент нагрузочного тестирования. "
            "Бесплатный, open-source. Тестирует HTTP, JDBC, FTP, WebSocket."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "1. Установи Java 8+ (<a href='https://www.java.com'>java.com</a>)\n"
            "2. Скачай JMeter: <a href='https://jmeter.apache.org/download_jmeter.cgi'>jmeter.apache.org</a>\n"
            "3. Распакуй → <code>bin/jmeter.bat</code> (Windows) / <code>bin/jmeter.sh</code> (Mac/Linux)"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• GUI и CLI режим\n"
            "• Thread Groups — симуляция пользователей\n"
            "• Ramp-up period — постепенное увеличение нагрузки\n"
            "• Assertions — проверка ответов\n"
            "• Listeners — графики и отчёты (Response Time, TPS)\n"
            "• Плагины: jpgc для расширенных метрик\n"
            "• Интеграция с CI через CLI: <code>jmeter -n -t test.jmx -l result.jtl</code>"
        ),
        "usage_example": (
            "<b>Базовый тест нагрузки:</b>\n"
            "1. Thread Group: 100 пользователей, ramp-up 60 сек\n"
            "2. HTTP Request: GET /api/products\n"
            "3. Assertion: Response Code = 200\n"
            "4. Listener: View Results Tree + Summary Report\n\n"
            "<b>Что смотреть в результатах:</b>\n"
            "• Average Response Time < 500ms — норма\n"
            "• Error Rate < 1% — допустимо\n"
            "• Throughput (TPS) — транзакций в секунду"
        ),
        "tips": [
            "💡 В GUI только разрабатывай тесты, запускай в CLI — GUI жрёт много RAM",
            "💡 Плагин BlazeMeter Recorder — записывает сценарий как действие в браузере",
            "💡 Используй CSV Data Set — параметризация с разными пользователями",
        ],
        "docs_url": "https://jmeter.apache.org/usermanual/index.html",
    },

    "k6": {
        "name": "k6",
        "emoji": "🚀",
        "category": "performance",
        "tagline": "Современное нагрузочное тестирование на JavaScript",
        "description": (
            "<b>k6</b> от Grafana Labs — современный инструмент нагрузки. "
            "Скрипты на JS, CLI, отличная интеграция с CI/CD."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "• Windows: <code>winget install k6</code>\n"
            "• Mac: <code>brew install k6</code>\n"
            "• Linux: <a href='https://k6.io/docs/getting-started/installation/'>инструкция</a>\n"
            "• Docker: <code>docker run --rm grafana/k6 run script.js</code>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Скрипты на JavaScript/TypeScript\n"
            "• Сценарии нагрузки: constant VUs, ramp-up, stress\n"
            "• Threshold-проверки в скрипте\n"
            "• Интеграция с Grafana для дашбордов\n"
            "• k6 Cloud — облачный запуск из многих регионов"
        ),
        "usage_example": (
            "<b>Пример скрипта k6:</b>\n"
            "<pre>import http from 'k6/http';\nimport { check, sleep } from 'k6';\n\nexport const options = {\n  vus: 50,          // 50 виртуальных пользователей\n  duration: '30s',  // 30 секунд\n  thresholds: {\n    http_req_duration: ['p(95)<500'], // 95% запросов < 500ms\n    http_req_failed: ['rate<0.01'],   // ошибки < 1%\n  },\n};\n\nexport default function () {\n  const res = http.get('https://api.example.com/products');\n  check(res, { 'status 200': (r) => r.status === 200 });\n  sleep(1);\n}</pre>\n\n"
            "<code>k6 run script.js</code>"
        ),
        "tips": [
            "💡 k6 намного быстрее JMeter на одной машине",
            "💡 Используй k6 Cloud для запуска из 20+ регионов мира",
            "💡 Grafana + InfluxDB + k6 = идеальный стек мониторинга нагрузки",
        ],
        "docs_url": "https://k6.io/docs/",
    },

    "gatling": {
        "name": "Gatling",
        "emoji": "🔫",
        "category": "performance",
        "tagline": "Нагрузочное тестирование на Scala/Java",
        "description": (
            "<b>Gatling</b> — мощный инструмент нагрузки с красивыми HTML отчётами. "
            "Популярен в Java/Scala командах."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "1. Установи Java 11+\n"
            "2. Скачай с <a href='https://gatling.io/open-source/'>gatling.io</a>\n"
            "3. <code>bin/gatling.sh</code> (Mac/Linux) / <code>bin/gatling.bat</code> (Windows)"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• DSL на Scala — читаемые сценарии\n"
            "• HTML отчёты с перцентилями\n"
            "• Recorder (GUI) — запись сценариев\n"
            "• Maven/Gradle плагины\n"
            "• Gatling Enterprise — облачный запуск"
        ),
        "usage_example": (
            "<b>Пример сценария (Scala):</b>\n"
            "<pre>val scn = scenario(\"Browse Products\")\n  .exec(http(\"Get Products\")\n    .get(\"/api/products\")\n    .check(status.is(200))\n  )\n\nsetUp(\n  scn.inject(\n    rampUsers(100).during(60.seconds)\n  )\n).protocols(httpProtocol)</pre>"
        ),
        "tips": [
            "💡 Лучшие HTML отчёты из всех инструментов нагрузки",
            "💡 Выбирай Gatling если команда пишет на Java/Scala",
        ],
        "docs_url": "https://docs.gatling.io/",
    },

    # ─── МОБИЛЬНОЕ ТЕСТИРОВАНИЕ ────────────────────────────────────────────────

    "appium": {
        "name": "Appium",
        "emoji": "📱",
        "category": "mobile",
        "tagline": "Selenium для мобильных приложений",
        "description": (
            "<b>Appium</b> — стандарт автоматизации мобильного тестирования. "
            "Работает с нативными, гибридными и web-приложениями. iOS и Android."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "1. <code>npm install -g appium</code>\n"
            "2. <code>appium driver install uiautomator2</code> (Android)\n"
            "3. <code>appium driver install xcuitest</code> (iOS)\n"
            "4. <code>pip install Appium-Python-Client</code>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• iOS и Android с одним кодом\n"
            "• Поддержка реальных устройств и эмуляторов\n"
            "• Appium Inspector — GUI для поиска элементов\n"
            "• Совместим с Selenium WebDriver протоколом"
        ),
        "usage_example": (
            "<b>Пример теста (Python):</b>\n"
            "<pre>from appium import webdriver\n\ncaps = {\n  'platformName': 'Android',\n  'deviceName': 'emulator-5554',\n  'app': '/path/app.apk',\n  'automationName': 'UiAutomator2'\n}\n\ndriver = webdriver.Remote('http://localhost:4723/wd/hub', caps)\nelement = driver.find_element('id', 'com.app:id/login_btn')\nelement.click()\ndriver.quit()</pre>"
        ),
        "tips": [
            "💡 Appium Inspector — незаменим для поиска UI элементов",
            "💡 Реальные устройства для финального тестирования, эмуляторы для разработки автотестов",
            "💡 BrowserStack / Sauce Labs — облачные фермы устройств",
        ],
        "docs_url": "https://appium.io/docs/en/latest/",
    },

    "charles": {
        "name": "Charles Proxy",
        "emoji": "🔭",
        "category": "mobile",
        "tagline": "Перехват HTTPS трафика мобильных приложений",
        "description": (
            "<b>Charles Proxy</b> — прокси для перехвата HTTP/HTTPS трафика. "
            "Незаменим для мобильного тестирования: видишь все запросы приложения."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "1. Скачай с <a href='https://www.charlesproxy.com/download/'>charlesproxy.com</a>\n"
            "2. Установи SSL сертификат Charles на телефон\n"
            "3. Настрой прокси на телефоне: IP компьютера, порт 8888"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Просмотр всех HTTP/HTTPS запросов\n"
            "• Breakpoints — редактирование запросов на лету\n"
            "• Map Remote — подмена URL (prod → staging)\n"
            "• Map Local — возврат локального файла вместо API\n"
            "• Throttling — эмуляция медленного интернета (3G, Edge)"
        ),
        "usage_example": (
            "<b>Типичные сценарии:</b>\n"
            "📌 <b>Map Local</b> — возвращаем ошибку 500 чтобы проверить обработку:\n"
            "Proxy → Map Local → Map From: api/products → Map To: error500.json\n\n"
            "📌 <b>Throttling</b> — проверяем поведение на 3G:\n"
            "Proxy → Throttle Settings → Preset: 3G"
        ),
        "tips": [
            "💡 Мастхэв для мобильного QA — без него вслепую",
            "💡 Breakpoints позволяет тестировать edge cases без изменения кода",
            "💡 Платный ($50), но есть 30-дневный триал",
        ],
        "docs_url": "https://www.charlesproxy.com/documentation/",
    },

    # ─── ПЕРЕХВАТ ТРАФИКА ──────────────────────────────────────────────────────

    "fiddler": {
        "name": "Fiddler",
        "emoji": "🎻",
        "category": "traffic",
        "tagline": "Бесплатный перехватчик HTTP трафика для Windows",
        "description": (
            "<b>Fiddler Classic</b> — бесплатный HTTP дебаггер для Windows. "
            "Перехватывает весь трафик браузера и приложений."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "• Fiddler Classic (бесплатно): <a href='https://www.telerik.com/fiddler/fiddler-classic'>telerik.com/fiddler</a>\n"
            "• Fiddler Everywhere (платный, кроссплатформенный): <a href='https://www.telerik.com/fiddler'>telerik.com/fiddler/fiddler-everywhere</a>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Перехват HTTP/HTTPS запросов\n"
            "• AutoResponder — подмена ответов\n"
            "• Breakpoints\n"
            "• FiddlerScript — автоматизация через JS\n"
            "• Composer — создание кастомных запросов"
        ),
        "usage_example": (
            "<b>AutoResponder пример:</b>\n"
            "1. Tools → AutoResponder\n"
            "2. Add Rule: If URL contains /api/login → Return 403.json\n"
            "3. Проверяем обработку 403 в приложении"
        ),
        "tips": [
            "💡 Для Windows — Fiddler, для Mac/Linux — Charles или mitmproxy",
            "💡 Для установки HTTPS сертификата: Tools → Options → HTTPS → Trust Certificate",
        ],
        "docs_url": "https://docs.telerik.com/fiddler/",
    },

    "mitmproxy": {
        "name": "mitmproxy",
        "emoji": "🕵️",
        "category": "traffic",
        "tagline": "Open-source прокси для продвинутых пользователей",
        "description": (
            "<b>mitmproxy</b> — бесплатный open-source прокси. "
            "Python API для скриптования перехватов. "
            "Кроссплатформенный: Windows/Mac/Linux."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "<pre>pip install mitmproxy</pre>\n\n"
            "Или скачай с <a href='https://mitmproxy.org/'>mitmproxy.org</a>"
        ),
        "features": (
            "<b>Три инструмента в одном:</b>\n"
            "• <code>mitmproxy</code> — интерактивный TUI\n"
            "• <code>mitmdump</code> — CLI для скриптов\n"
            "• <code>mitmweb</code> — web-интерфейс\n\n"
            "<b>Python API для автоматизации:</b>\n"
            "<pre>def request(flow):\n  if '/api/login' in flow.request.url:\n    flow.response = http.Response.make(\n      403, b'Forbidden'\n    )</pre>"
        ),
        "usage_example": (
            "<b>Запуск web UI:</b>\n"
            "<code>mitmweb --listen-port 8080</code>\n\n"
            "<b>Записать все запросы в файл:</b>\n"
            "<code>mitmdump -w traffic.log</code>"
        ),
        "tips": [
            "💡 mitmproxy бесплатен и мощнее Fiddler для автоматизации",
            "💡 Используй для API fuzzing и security testing",
        ],
        "docs_url": "https://docs.mitmproxy.org/",
    },

    "wireshark": {
        "name": "Wireshark",
        "emoji": "🦈",
        "category": "traffic",
        "tagline": "Анализатор сетевых пакетов",
        "description": (
            "<b>Wireshark</b> — стандарт анализа сетевого трафика. "
            "Работает на уровне TCP/IP пакетов. Мощнее чем HTTP-прокси."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "• Скачай с <a href='https://www.wireshark.org/download.html'>wireshark.org</a>\n"
            "• Mac: <code>brew install wireshark</code>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Перехват пакетов на уровне сети\n"
            "• Мощные фильтры: <code>http.request.method == 'POST'</code>\n"
            "• Анализ протоколов: HTTP, DNS, TCP, UDP, TLS\n"
            "• Follow TCP Stream — восстановление HTTP сессии"
        ),
        "usage_example": (
            "<b>Полезные фильтры:</b>\n"
            "<code>http</code> — только HTTP\n"
            "<code>http.response.code == 500</code> — все 500 ошибки\n"
            "<code>ip.addr == 192.168.1.1</code> — трафик конкретного IP\n"
            "<code>dns</code> — DNS запросы"
        ),
        "tips": [
            "💡 Wireshark для network-level анализа, Fiddler/Charles для HTTP",
            "💡 Wireshark не видит HTTPS содержимое без приватного ключа",
        ],
        "docs_url": "https://www.wireshark.org/docs/",
    },

    # ─── РАБОТА С БД ──────────────────────────────────────────────────────────

    "dbeaver": {
        "name": "DBeaver",
        "emoji": "🗄️",
        "category": "database",
        "tagline": "Универсальный клиент для любых баз данных",
        "description": (
            "<b>DBeaver Community</b> — бесплатный универсальный DB клиент. "
            "Поддерживает PostgreSQL, MySQL, Oracle, SQLite, MongoDB, Redis и 80+ других. "
            "Обязателен для QA инженера."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "🌐 <a href='https://dbeaver.io/download/'>dbeaver.io/download</a>\n"
            "• Windows: .exe установщик\n"
            "• Mac: .dmg или <code>brew install --cask dbeaver-community</code>\n"
            "• Linux: .deb, .rpm, snap"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Подключение к 80+ СУБД\n"
            "• SQL редактор с автодополнением\n"
            "• Визуальный редактор данных (без SQL)\n"
            "• ER Diagram — автогенерация схемы БД\n"
            "• Экспорт: CSV, Excel, JSON, SQL\n"
            "• SSH туннель для подключения к боевой БД"
        ),
        "usage_example": (
            "<b>Типичные задачи QA:</b>\n"
            "1. Проверить что данные сохранились после теста:\n"
            "<code>SELECT * FROM users WHERE email = 'test@test.com';</code>\n\n"
            "2. Очистить тестовые данные:\n"
            "<code>DELETE FROM orders WHERE created_at > '2024-01-01' AND user_id = 999;</code>\n\n"
            "3. Проверить foreign key:\n"
            "<code>SELECT o.*, u.email FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = 123;</code>"
        ),
        "tips": [
            "💡 Горячая клавиша Ctrl+Enter — выполнить запрос",
            "💡 F3 — форматирование SQL запроса",
            "💡 SSH туннель: Connection Settings → SSH → Use SSH Tunnel",
            "💡 Mock Data генератор — создаёт тестовые данные",
        ],
        "docs_url": "https://dbeaver.com/docs/dbeaver/",
    },

    "pgadmin": {
        "name": "pgAdmin",
        "emoji": "🐘",
        "category": "database",
        "tagline": "Официальный клиент для PostgreSQL",
        "description": (
            "<b>pgAdmin 4</b> — официальный инструмент для PostgreSQL. "
            "Веб-интерфейс, мониторинг, управление пользователями."
        ),
        "install": (
            "<b>Установка:</b>\n"
            "🌐 <a href='https://www.pgadmin.org/download/'>pgadmin.org/download</a>\n"
            "Или через Docker:\n"
            "<pre>docker run -p 5050:80 \\\n  -e PGADMIN_EMAIL=admin@admin.com \\\n  -e PGADMIN_PASSWORD=admin \\\n  dpage/pgadmin4</pre>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Query Tool — полноценный SQL редактор\n"
            "• EXPLAIN — план выполнения запроса\n"
            "• pgAgent — планировщик задач\n"
            "• Backup/Restore\n"
            "• Dashboard — мониторинг сервера"
        ),
        "usage_example": (
            "<b>EXPLAIN ANALYZE (оптимизация):</b>\n"
            "<pre>EXPLAIN ANALYZE\nSELECT * FROM orders\nWHERE user_id = 123\nAND status = 'pending';</pre>\n\n"
            "Показывает: Seq Scan vs Index Scan, время выполнения, стоимость"
        ),
        "tips": [
            "💡 Используй pgAdmin для PostgreSQL, DBeaver для нескольких СУБД",
            "💡 EXPLAIN ANALYZE помогает найти медленные запросы",
        ],
        "docs_url": "https://www.pgadmin.org/docs/",
    },

    # ─── CI/CD ─────────────────────────────────────────────────────────────────

    "jenkins": {
        "name": "Jenkins",
        "emoji": "🏗️",
        "category": "ci_cd",
        "tagline": "Классика CI/CD — настраиваемый до бесконечности",
        "description": (
            "<b>Jenkins</b> — самый популярный CI/CD сервер. "
            "Open-source, 1800+ плагинов. "
            "Настраивается для любого workflow."
        ),
        "install": (
            "<b>Установка (Docker — проще всего):</b>\n"
            "<pre>docker run -d -p 8080:8080 \\\n  -v jenkins_home:/var/jenkins_home \\\n  jenkins/jenkins:lts</pre>\n\n"
            "Открой <code>http://localhost:8080</code>, введи initial admin password."
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Pipeline as Code (Jenkinsfile)\n"
            "• 1800+ плагинов: Git, Docker, Slack, JUnit...\n"
            "• Distributed builds — агенты на разных серверах\n"
            "• Blue Ocean UI — красивый интерфейс пайплайнов\n"
            "• Параметризованные билды"
        ),
        "usage_example": (
            "<b>Jenkinsfile — запуск тестов:</b>\n"
            "<pre>pipeline {\n  agent any\n  stages {\n    stage('Test') {\n      steps {\n        sh 'pip install -r requirements.txt'\n        sh 'pytest tests/ --junitxml=results.xml'\n      }\n      post {\n        always {\n          junit 'results.xml'\n        }\n      }\n    }\n  }\n}</pre>"
        ),
        "tips": [
            "💡 Jenkins мощный, но требует администрирования. GitLab CI проще",
            "💡 Blue Ocean плагин — красивый UI для пайплайнов",
        ],
        "docs_url": "https://www.jenkins.io/doc/",
    },

    "github_actions": {
        "name": "GitHub Actions",
        "emoji": "⚙️",
        "category": "ci_cd",
        "tagline": "CI/CD прямо в GitHub — бесплатно для open-source",
        "description": (
            "<b>GitHub Actions</b> — встроенный CI/CD в GitHub. "
            "Бесплатно для публичных репозиториев. "
            "Yaml-конфиги, тысячи готовых action из маркетплейса."
        ),
        "install": (
            "<b>Начало работы:</b>\n"
            "1. Создай файл в репозитории: <code>.github/workflows/test.yml</code>\n"
            "2. GitHub автоматически запустит его по событиям (push, PR)"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Триггеры: push, pull_request, schedule, manual\n"
            "• Matrix builds — тест на Python 3.9/3.10/3.11\n"
            "• 15000+ готовых Actions в маркетплейсе\n"
            "• Secrets для хранения ключей\n"
            "• Artifacts — сохранение результатов тестов"
        ),
        "usage_example": (
            "<b>Пример workflow для тестов:</b>\n"
            "<pre>name: Tests\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-python@v4\n        with:\n          python-version: '3.11'\n      - run: pip install -r requirements.txt\n      - run: pytest tests/ -v --tb=short\n      - uses: actions/upload-artifact@v3\n        if: failure()\n        with:\n          name: test-results\n          path: reports/</pre>"
        ),
        "tips": [
            "💡 Идеален если уже используешь GitHub",
            "💡 act — запуск GitHub Actions локально: <code>act push</code>",
            "💡 secrets.GITHUB_TOKEN — автоматически доступен без настройки",
        ],
        "docs_url": "https://docs.github.com/en/actions",
    },

    "gitlab_ci": {
        "name": "GitLab CI/CD",
        "emoji": "🦊",
        "category": "ci_cd",
        "tagline": "Полноценный DevOps в одном инструменте",
        "description": (
            "<b>GitLab CI/CD</b> — встроенный CI/CD в GitLab. "
            "Часто используется в корпоративных проектах. "
            "`.gitlab-ci.yml` в корне репозитория."
        ),
        "install": (
            "<b>Начало работы:</b>\n"
            "1. Создай <code>.gitlab-ci.yml</code> в репозитории\n"
            "2. GitLab автоматически запускает пайплайн\n\n"
            "<b>Или самохостинг:</b>\n"
            "<a href='https://docs.gitlab.com/ee/install/docker.html'>GitLab Docker install</a>"
        ),
        "features": (
            "<b>Функции:</b>\n"
            "• Pipeline: stages → jobs → scripts\n"
            "• Merge Request pipelines\n"
            "• Environments — deploy на dev/staging/prod\n"
            "• Registry: Docker, NPM, Python (PyPI)\n"
            "• Security scanning: SAST, DAST, dependency check"
        ),
        "usage_example": (
            "<b>Пример .gitlab-ci.yml:</b>\n"
            "<pre>stages:\n  - test\n  - deploy\n\ntest:\n  stage: test\n  image: python:3.11\n  script:\n    - pip install -r requirements.txt\n    - pytest tests/ -v\n  artifacts:\n    reports:\n      junit: report.xml\n\ndeploy:\n  stage: deploy\n  script:\n    - echo 'Deploying...'\n  only:\n    - main</pre>"
        ),
        "tips": [
            "💡 GitLab CI проще Jenkins, встроен в платформу",
            "💡 Используй cache: для ускорения pip install",
        ],
        "docs_url": "https://docs.gitlab.com/ee/ci/",
    },
}
