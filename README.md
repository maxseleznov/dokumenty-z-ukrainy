# Документи з України — статичний сайт

Структура: `index.html` + сторінки послуг у підпапках (`/svidotstvo-pro-narodzhennya/` …), `assets/` (style.css, main.js, favicon.svg), `sitemap.xml`, `robots.txt`, `404.html`, `privacy.html`.

## Блог
Статті — у `blog_posts.py` (список `POSTS`). Додати статтю = додати словник і запустити `python3 build.py`.

## Як редагувати
Весь контент і шаблони — у `build.py` (словник `PAGES`, `SITE`, `INDEX_FAQ`). Після змін запустіть `python3 build.py` — усі HTML перегенеруються.
Дрібні правки можна робити прямо в HTML, але наступний запуск `build.py` їх перезапише.

## Перед публікацією
1. `build.py` → `SITE`: назва, ПІБ, номер свідоцтва, email, телефон, домен.
2. `assets/main.js` → `FORM_ENDPOINT` (Formspree/Basin/власний), `TELEGRAM_URL`, `WHATSAPP_URL`.
3. Замінити плейсхолдери `[N]`, `[РІК]` на головній.
4. GitHub Pages: завантажити вміст папки в репозиторій, додати файл `CNAME` з доменом, у налаштуваннях Pages увімкнути HTTPS.
5. Додати Google Analytics / Search Console (вставити тег у `head()` в `build.py`).
