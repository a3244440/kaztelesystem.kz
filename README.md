# kaztelesystem.kz

Сайт интернет-провайдера ТОО «КазТелеСистем» (Астана). Статический одностраничник без фреймворков.

## Структура

| Файл | Что это |
|---|---|
| `src/page.html` | Исходник страницы: разметка, стили, скрипт |
| `build.py` | Собирает `index.html`: добавляет `<head>` с SEO-мета, hreflang, Open Graph и JSON-LD (Organization, LocalBusiness, тарифы, FAQPage) |
| `index.html` | Готовая страница для хостинга (генерируется, руками не править) |
| `robots.txt` | Открыт для поисковиков и ИИ-ботов (GPTBot, PerplexityBot, ClaudeBot, Google-Extended) |
| `sitemap.xml` | Карта сайта с hreflang ru/kk |
| `llms.txt` | Краткая справка о компании для ИИ-поисковиков (GEO) |
| `favicon.svg` | Иконка сайта |

## Как обновить

1. Правьте `src/page.html` (тарифы, тексты, FAQ).
2. Запустите `python3 build.py` — FAQ-разметка и тарифы в JSON-LD обновятся автоматически (тарифы — в списке `TARIFFS` в `build.py`).
3. Загрузите `index.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, `favicon.svg` в корень сайта.

## До запуска

- Подтвердить актуальность тарифов (на старом сайте — «с 1 января 2019 года»).
- Добавить `og.png` (1200×630) для превью в мессенджерах.
- Сделать казахскую версию `/kk/` (ссылки и hreflang уже стоят).
- Проверить, что `wp-content/themes/Kaztelesistem/img/1.pdf` (публичный договор) остаётся доступен после переноса.
- Зарегистрировать сайт в Google Search Console и Яндекс Вебмастере, отправить sitemap; обновить карточку в 2ГИС и Google Maps.
