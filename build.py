"""Собирает index.html (рус) и kk/index.html (каз) из src/page.html и словаря src/kk.json: добавляет <head> с SEO-мета, hreflang, Open Graph и JSON-LD.
Запуск: python3 build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
URL = "https://kaztelesystem.kz/"
TITLE = "Домашний интернет в Астане от 3 000 ₸ — безлимит | КазТелеСистем"
DESC = ("Безлимитный интернет в Астане от 3 000 ₸/мес, 100 Мбит/с за 4 999 ₸. "
        "Подключение бесплатно, цена не растёт после акции. Оператор связи с лицензией с 2006 года.")
TARIFFS = [(20, 3000), (30, 3500), (50, 4000), (100, 4999)]

SRC = (ROOT / "src" / "page.html").read_text(encoding="utf-8")
KK = json.loads((ROOT / "src" / "kk.json").read_text(encoding="utf-8"))


def translate_kk(html: str) -> str:
    """Переводит русские тексты страницы на казахский по словарю src/kk.json."""
    for ru, kk in KK["snippets"]:
        html = html.replace(ru, kk)
    for ru in sorted(KK["strings"], key=len, reverse=True):
        kk = KK["strings"][ru]
        esc = re.escape(ru)
        html = re.sub(r"(>\s*)" + esc + r"(\s*<)", lambda m: m.group(1) + kk + m.group(2), html)
        html = html.replace(f'"{ru}"', f'"{kk}"').replace(f"'{ru}'", f"'{kk}'")
    return html


def render(lang: str) -> str:
    page = SRC if lang == "ru" else translate_kk(SRC)
    page_url = URL if lang == "ru" else URL + "kk/"
    title = TITLE if lang == "ru" else KK["meta"]["title"]
    desc = DESC if lang == "ru" else KK["meta"]["description"]
    locale = "ru_KZ" if lang == "ru" else "kk_KZ"
    fonts = "\n".join(re.findall(r"<link[^>]+>", page))
    style = re.search(r"<style>.*?</style>", page, re.S).group(0)
    body = re.sub(r"<title>.*?</title>\s*", "", page)
    body = re.sub(r'<meta name="claude:[^>]*>\s*', "", body)
    body = re.sub(r"<link[^>]+>\s*", "", body)
    body = body.replace(style, "").strip()

    org = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Organization", "LocalBusiness"],
                "@id": URL + "#org",
                "name": "КазТелеСистем",
                "legalName": "ТОО «КазТелеСистем»",
                "alternateName": ["KazTeleSystem", "Казтелесистем"],
                "url": URL,
                "logo": URL + "favicon.svg",
                "image": URL + "og.png",
                "description": "Интернет-провайдер и оператор связи в Астане: безлимитный домашний интернет от 3 000 ₸, "
                               "городская телефония, строительство линий связи. Лицензия № 001181 от 01.03.2006.",
                "foundingDate": "2009",
                "telephone": "+7 7172 45 00 02",
                "email": "info@kaztelesystem.kz",
                "priceRange": "3000–4999 KZT",
                "address": [
                    {"@type": "PostalAddress", "streetAddress": "пр. Шәкәрім Құдайбердіұлы, 36/2, НП-5",
                     "addressLocality": "Астана", "postalCode": "010000", "addressCountry": "KZ"},
                    {"@type": "PostalAddress", "streetAddress": "пр. Кабанбай батыра, 40, ВП-43а",
                     "addressLocality": "Астана", "addressCountry": "KZ"},
                ],
                "areaServed": {"@type": "City", "name": "Астана"},
                "contactPoint": [
                    {"@type": "ContactPoint", "telephone": "+7 7172 45 00 02", "contactType": "customer service",
                     "availableLanguage": ["ru", "kk"]},
                    {"@type": "ContactPoint", "telephone": "+7 707 742 84 83", "contactType": "sales"},
                ],
                "paymentAccepted": "Kaspi, Kassa 24, StarBanking",
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": "Тарифы домашнего интернета",
                    "itemListElement": [
                        {"@type": "Offer", "name": f"Unlim {s}", "price": str(p), "priceCurrency": "KZT",
                         "description": f"Безлимитный интернет {s} Мбит/с, загрузка и отдача на одной скорости, цена в месяц с НДС",
                         "itemOffered": {"@type": "Service", "serviceType": "Домашний интернет", "name": f"Unlim {s}"}}
                        for s, p in TARIFFS
                    ],
                },
            },
            {"@type": "WebSite", "@id": URL + "#site", "url": URL, "name": "КазТелеСистем",
             "inLanguage": "ru-KZ" if lang == "ru" else "kk-KZ", "publisher": {"@id": URL + "#org"}},
        ],
    }
    faq = [(q, re.sub(r"<.*?>", "", a)) for q, a in re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body)]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

    head = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="ru-KZ" href="{URL}">
<link rel="alternate" hreflang="kk-KZ" href="{URL}kk/">
<link rel="alternate" hreflang="x-default" href="{URL}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="geo.region" content="KZ-AST">
<meta name="geo.placename" content="Астана">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:site_name" content="КазТелеСистем">
<meta property="og:url" content="{page_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{URL}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#04120B">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{fonts}
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
{style}
</head>
<body>
"""
    return head + body + "\n</body>\n</html>\n"

(ROOT / "index.html").write_text(render("ru"), encoding="utf-8")
(ROOT / "kk").mkdir(exist_ok=True)
(ROOT / "kk" / "index.html").write_text(render("kk"), encoding="utf-8")
print("Собраны index.html и kk/index.html")
