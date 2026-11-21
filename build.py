#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор статичного сайту «Документи з України». Запуск: python3 build.py"""
import os, html, json, datetime, hashlib
from pages_data import PAGES as SERVICE_PAGES
from countries import COUNTRY_PAGES
from blog_posts import POSTS

SITE = {
    "name": "Документи з України",
    "domain": "https://dokumenty-z-ukrainy.com.ua",
    "lawyer": "Адвокатське бюро «Селезньов і партнери»",
    "lawyer_short": "АБ «Селезньов і партнери»",
    "person": "Максим Селезньов",
    "cert": "000208",
    "city": "м. Вінниця, вул. А. Артинова, 46, офіс 110",
    "offices": "Вінниця · Київ · Харків",
    "email": os.environ.get("SITE_EMAIL", "rozirvannya@gmail.com"),  # публічна адреса бюро; можна перевизначити змінною середовища
    "phone": "+380 93 768 84 16",
    "phone_raw": "+380937688416",
    "telegram": "https://t.me/Online_Advokat_UA",
    "whatsapp": "https://wa.me/380937688416",
    "viber": "viber://chat?number=%2B380937688416",
    "unba": "https://erau.unba.org.ua/profile/58196",
    "instagram": "https://www.instagram.com/rozlucheni/",
    "facebook": "https://www.facebook.com/RozirvannyaShlubuOnline",
    "youtube": "https://www.youtube.com/@rozlucheni",
    "reviews": "https://razvod-online.com.ua/feedback",
    "cases": "2 000+",
}
OUT = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
PAGES = SERVICE_PAGES + COUNTRY_PAGES

def _v(rel):
    try: return hashlib.md5(open(os.path.join(OUT, rel), "rb").read()).hexdigest()[:8]
    except FileNotFoundError: return "0"
ASSET_V = {"css": _v("assets/style.css"), "js": _v("assets/main.js"), "fonts": _v("assets/fonts.css")}

# ---------------------------------------------------------------- ціни та строки (єдине джерело)
# value, назва в селекті, група для конфігуратора
DOC_OPTIONS = [
    ("narodzhennya", "Свідоцтво про народження", "svid"),
    ("shlyub", "Свідоцтво про шлюб", "svid"),
    ("rozirvannya", "Свідоцтво про розірвання шлюбу", "svid"),
    ("smert", "Свідоцтво про смерть", "svid"),
    ("vytyag", "Витяг з ДРАЦС", "vyt"),
    ("nesudymist", "Витяг про несудимість", "nes"),
    ("rnokpp", "РНОКПП (ідентифікаційний код)", "rnokpp"),
    ("apostyl", "Апостиль на мій документ", "apostyl"),
    ("kilka", "Кілька документів / не знаю", "svid"),
]
COUNTRIES = ["Польща", "Німеччина", "Чехія", "Італія", "Іспанія", "Канада", "США", "Велика Британія", "Інша країна"]
PRICE = {"svid": 80, "vyt": 80, "nes": 100, "rnokpp": 50, "apostyl": 50, "delivery": 60}
PACK = {"p1": PRICE["svid"], "p2": PRICE["svid"] + PRICE["apostyl"], "p3": PRICE["svid"] + PRICE["apostyl"] + PRICE["delivery"]}

MARK_PATHS = '<path class="ln" d="M58 30L34.29 42.77Q32 44 29.71 42.77L6 30L6.00 52.00Q6 56 10.00 56.00L54.00 56.00Q58 56 58.00 52.00L58 30L48.00 30.00Q45 30 45.00 27.00L45.00 9.20Q45 6 41.80 6.00L22.20 6.00Q19 6 19.00 9.20L19.00 27.00Q19 30 16.00 30.00L6 30"/><path class="uap" fill-rule="evenodd" transform="translate(32 19) scale(1.06) translate(-32 -19)" d="M29.070 14.0H31.021V20.276Q31.021 21.372 30.554 22.123Q30.088 22.873 29.269 23.252Q28.450 23.630 27.387 23.630Q26.323 23.630 25.498 23.252Q24.672 22.873 24.206 22.123Q23.739 21.372 23.739 20.276V14.0H25.697V20.276Q25.697 20.916 25.899 21.320Q26.101 21.725 26.483 21.914Q26.865 22.103 27.387 22.103Q27.922 22.103 28.297 21.914Q28.672 21.725 28.871 21.320Q29.070 20.916 29.070 20.276Z M38.903 23.5 38.244 21.496H34.831L34.172 23.5H32.091L35.621 14.0H37.441L40.991 23.5ZM37.741 19.963 36.534 16.303 35.334 19.963Z"/>'
MARK = '<svg aria-hidden="true" viewBox="0 0 64 64"><use href="#mark"/></svg>'
ICO_TG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="#1d93d2" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm4.6 6.8-1.6 7.6c-.1.5-.4.7-.9.4l-2.4-1.8-1.2 1.1c-.1.1-.2.2-.5.2l.2-2.5 4.5-4.1c.2-.2 0-.3-.3-.1l-5.6 3.5-2.4-.8c-.5-.2-.5-.5.1-.8l9.4-3.6c.4-.2.8.1.7.9z"/></svg>'
ICO_WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="#1fa855" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8c.1.2 1.9 2.9 4.6 4 1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>'
ICO_VB = '<svg width="18" height="18" viewBox="0 0 24 24" fill="#6a56e0" aria-hidden="true"><path d="M12 1.5C6.3 1.5 2.6 4.7 2.6 10.2v3.4c0 3.4 1.6 5.8 4.2 7v2.6c0 .5.5.7.9.4l2.7-2.5h1.6c5.7 0 9.4-3.2 9.4-8.7v-2.2c0-5.5-3.7-8.7-9.4-8.7zm4.3 12.6c-.3.6-1.4 1.2-2 1.2-.6.1-1.1 0-3.4-1-2.7-1.2-4.4-4-4.5-4.2-.2-.2-1.1-1.5-1.1-2.8s.7-2 .9-2.3c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.6.8c-.1.1-.2.3-.1.5.4.8 1.1 1.7 1.9 2.3.3.2.5.3.7.4.2.1.4.1.6-.1l.8-1c.2-.2.4-.2.6-.1l2 1c.3.1.5.2.5.4 0 .1 0 .7-.2 1z"/></svg>'

NAV = [("/#docs", "Документи"), ("/#diia", "Коли не Дія"), ("/#countries", "Країни"), ("/#price", "Вартість"), ("/blog/", "Блог")]


# ---------------------------------------------------------------- SEO-заголовки (<title>), до 60 символів, без повтору бренду
SEO_TITLES = {
    "/": "Документи з України за кордон — без поїздки і довіреності",
    "/svidotstvo-pro-narodzhennya/": "Дублікат свідоцтва про народження з України за кордон",
    "/svidotstvo-pro-shlyub/": "Дублікат свідоцтва про шлюб — отримати з-за кордону",
    "/svidotstvo-pro-rozirvannya-shlyubu/": "Свідоцтво про розірвання шлюбу: як отримати з-за кордону",
    "/svidotstvo-pro-smert/": "Дублікат свідоцтва про смерть для спадщини за кордоном",
    "/vytyag-dracs/": "Витяг з ДРАЦС онлайн і з-за кордону — через адвоката",
    "/vytyag-pro-nesudymist/": "Витяг про несудимість з апостилем для подання за кордон",
    "/apostyl/": "Апостиль на свідоцтва ДРАЦС і несудимість з доставкою",
    "/dlya-ukraintsiv-za-kordonom/": "Документи з України для українців за кордоном",
    "/rnokpp/": "РНОКПП з-за кордону: отримати або відновити код",
    "/polshcha/": "Документи з України для Польщі: карта побиту, PESEL",
    "/nimechchyna/": "Документи з України для Німеччини: Standesamt, Einbürgerung",
    "/chekhiya/": "Документи з України для Чехії: matrika, trvalý pobyt",
    "/italiya/": "Документи з України для Італії: cittadinanza, matrimonio",
    "/ispaniya/": "Документи з України для Іспанії: nacionalidad, arraigo",
    "/blog/": "Блог: документи з України, ДРАЦС, апостиль",
    "/blog/apostyl-chy-podvijnyj-apostyl-tablytsya-po-krainakh/": "Апостиль чи подвійний апостиль: таблиця по країнах",
    "/blog/svidotstvo-pro-rozirvannya-shlyubu-chy-rishennya-sudu/": "Свідоцтво про розірвання шлюбу чи рішення суду",
    "/blog/diia-vidmovyla-u-povtornij-vydachi/": "Дія відмовила у повторній видачі: 6 причин і що робити",
    "/privacy.html": "Політика конфіденційності — Документи з України",
    "/404.html": "Сторінку не знайдено — Документи з України",
}

# мета-описи, 70–160 символів
SEO_DESC = {
    "/": "Свідоцтва ДРАЦС, витяги й несудимість з України з апостилем і доставкою в 35+ країн. Адвокат за ордером — без довіреності й консульства. Від 80 €.",
    "/svidotstvo-pro-narodzhennya/": "Дублікат свідоцтва про народження, якщо ви за кордоном або Дія відмовила. Адвокат отримає за ордером, без довіреності, з апостилем і доставкою.",
    "/svidotstvo-pro-shlyub/": "Повторне свідоцтво про шлюб для подання за кордоном: отримання через адвоката без довіреності, апостиль, переклад і доставка в будь-яку країну.",
    "/svidotstvo-pro-rozirvannya-shlyubu/": "Свідоцтво, витяг з ДРАЦС чи рішення суду — що підтверджує розлучення за кордоном і як його отримати через адвоката без довіреності, з апостилем.",
    "/svidotstvo-pro-smert/": "Повторне свідоцтво про смерть для спадщини за кордоном: хто має право, як отримати через адвоката без довіреності, апостиль і доставка.",
    "/vytyag-dracs/": "Витяг з реєстру актів цивільного стану про шлюб, народження, розлучення чи сімейний стан — через адвоката без довіреності, з апостилем і перекладом.",
    "/vytyag-pro-nesudymist/": "Паперовий витяг про несудимість з печаткою МВС і апостилем для візи, ВНЖ, роботи чи громадянства. Отримаємо в Україні й надішлемо за кордон.",
    "/apostyl/": "Апостиль на свідоцтва ДРАЦС, витяги й несудимість: які документи апостилюють, коли потрібен подвійний апостиль, переклад і відправка за кордон.",
    "/dlya-ukraintsiv-za-kordonom/": "Свідоцтва ДРАЦС, витяги й несудимість з України, якщо ви за кордоном: адвокат за ордером, без нотаріальної довіреності, з апостилем і доставкою.",
    "/rnokpp/": "РНОКПП з-за кордону: отримати код уперше, відновити картку або оформити дитині. Довіреність за нашим зразком, паперова картка з доставкою.",
    "/polshcha/": "Українські документи для Польщі: карта побиту, транскрипція свідоцтв, шлюб в USC, громадянство. Апостиль, присяжний переклад, адвокат за ордером.",
    "/nimechchyna/": "Українські документи для Німеччини: Standesamt, Einbürgerung, возз'єднання сім'ї. Апостиль обов'язковий, переклад за ISO 9, адвокат за ордером.",
    "/chekhiya/": "Українські документи для Чехії: шлюб у матриці, trvalý pobyt, громадянство. Коли апостиль не обов'язковий, хто перекладає, адвокат за ордером.",
    "/italiya/": "Українські документи для Італії: громадянство, шлюб, возз'єднання сім'ї. Апостиль, засвідчений переклад або подвійний апостиль, адвокат за ордером.",
    "/ispaniya/": "Українські документи для Іспанії: nacionalidad, arraigo, шлюб, возз'єднання сім'ї. Апостиль і traducción jurada, отримання через адвоката за ордером.",
    "/blog/": "Практичні статті про документи з України для тих, хто за кордоном: відмови Дії, апостиль по країнах, витяги ДРАЦС, несудимість, розлучення.",
    "/blog/apostyl-chy-podvijnyj-apostyl-tablytsya-po-krainakh/": "Де українські документи приймають без апостиля, де потрібен подвійний апостиль чи легалізація. Таблиця для Польщі, Німеччини, Італії, Іспанії та інших.",
    "/blog/svidotstvo-pro-rozirvannya-shlyubu-chy-rishennya-sudu/": "Розлучені через суд після 2010 року не мають свідоцтва про розірвання шлюбу. Пояснюємо, що подавати за кордоном: рішення суду, витяг з ДРАЦС, апостиль.",
    "/blog/diia-vidmovyla-u-povtornij-vydachi/": "Чому Дія не видає повторне свідоцтво: запис не знайдено, не оцифровано, розбіжності в даних. Що робити в кожному випадку і коли потрібен адвокат.",
    "/privacy.html": "Як сайт «Документи з України» обробляє персональні дані із заявок: для чого використовуються, хто має доступ і як попросити їх видалити.",
    "/404.html": "Сторінку не знайдено. Перейдіть на головну або оберіть потрібний документ у меню сайту «Документи з України».",
}

# ---------------------------------------------------------------- partials
def head(title, desc, path, extra_ld=None, noindex=False):
    url = SITE["domain"] + path
    ld = [{
        "@context": "https://schema.org", "@type": "LegalService",
        "name": SITE["name"], "url": SITE["domain"], "image": SITE["domain"] + "/assets/og.png",
        "areaServed": "UA", "availableLanguage": ["uk"], "priceRange": "від 50 €",
        "telephone": SITE["phone_raw"],
        "sameAs": [SITE["telegram"], SITE["instagram"], SITE["facebook"], SITE["youtube"], SITE["unba"]],
        "address": {"@type": "PostalAddress", "streetAddress": "вул. А. Артинова, 46, офіс 110", "addressLocality": "Вінниця", "addressCountry": "UA"},
        "description": "Отримання повторних свідоцтв ДРАЦС, витягів з реєстру актів цивільного стану та витягу про несудимість через адвоката для українців за кордоном. Апостиль, переклад, доставка.",
    }]
    if SITE["email"]: ld[0]["email"] = SITE["email"]
    if extra_ld: ld += extra_ld
    robots = '<meta name="robots" content="noindex,nofollow">\n' if noindex else ""
    title = SEO_TITLES.get(path, title.split(" | ")[0])
    assert len(title) <= 60, f"title > 60: {path} ({len(title)})"
    desc = SEO_DESC.get(path, desc)
    assert 70 <= len(desc) <= 160, f"description {len(desc)}: {path}"
    t, d = html.escape(title), html.escape(desc)
    return f"""<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f3ebdf">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="uk_UA">
<meta property="og:image" content="{SITE['domain']}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Документи з України — без поїздки і довіреності">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE['domain']}/assets/og.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/montserrat-cyrillic-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts.css?v={ASSET_V["fonts"]}">
<link rel="stylesheet" href="/assets/style.css?v={ASSET_V["css"]}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="deco" aria-hidden="true"><i class="dome"></i><i class="s1"></i><i class="s2"></i><i class="s3"></i><i class="k k1"></i><i class="k k2"></i></div>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="mark" viewBox="0 0 64 64">{MARK_PATHS}</symbol></defs></svg>
"""

def brand():
    return f'<a class="brand" href="/" aria-label="{SITE["name"]} — на головну"><span class="logo">{MARK}</span><span><b>Документи</b><span> з України</span></span></a>'

def header():
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f"""<header class="top"><div class="nav glass">
{brand()}
<nav class="menu" aria-label="Головне меню">{nav}</nav>
<div class="navr"><a class="btn sm" href="#form"><span class="full">Залишити заявку</span><span class="short">Заявка</span></a>
<button class="burger" aria-label="Меню" aria-expanded="false" aria-controls="mnav"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div>
<nav class="mnav" id="mnav" aria-label="Меню">{nav}<a href="/dlya-ukraintsiv-za-kordonom/">Якщо ви за кордоном</a><a href="/apostyl/">Апостиль</a></nav>
</div></header>
"""

def lead_form(selected=None, country=None, ids=True):
    opts = "".join(f'<option value="{v}"{" selected" if v == selected else ""}>{t}</option>' for v, t, _ in DOC_OPTIONS)
    copts = '<option value="">Країна, де ви зараз</option>' + "".join(f'<option{" selected" if c == country else ""}>{c}</option>' for c in COUNTRIES)
    return f"""<form class="lead-form{' glass' if ids else ''}" data-lead method="post" action="#">
<input type="text" name="name" placeholder="Ім'я" autocomplete="name" aria-label="Ім'я">
<select name="doc" aria-label="Який документ потрібен">{opts}</select>
<select name="country" aria-label="Країна, де ви зараз">{copts}</select>
<input type="text" name="contact" placeholder="Telegram, WhatsApp або телефон" required autocomplete="tel" aria-label="Ваш контакт">
<input class="honey" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="form-status" role="status" aria-live="polite"></div>
<div class="fb"><span class="note">Надсилаючи заявку, ви погоджуєтесь на <a href="/privacy.html">обробку персональних даних</a>.</span><button class="btn" type="submit">Надіслати →</button></div>
</form>"""

def messengers():
    return f'<a href="{SITE["telegram"]}" target="_blank" rel="noopener">Telegram</a><a href="{SITE["whatsapp"]}" target="_blank" rel="noopener">WhatsApp</a><a href="{SITE["viber"]}">Viber</a>'

def form_section(selected=None, country=None):
    return f"""<section class="s" id="form"><div class="wrap fgrid">
<div><span class="eyebrow">Заявка</span><h2>Опишіть ситуацію — відповімо за 15 хвилин</h2><p class="muted" style="max-width:420px">У робочий час, у вашому месенджері. Напишемо точну ціну, строк і чи варто взагалі платити — іноді вистачить Дії.</p>
<div class="msgs">або напишіть одразу: {messengers()}</div></div>
{lead_form(selected, country)}
</div></section>
"""

def cfg(selected="narodzhennya", country="Польща"):
    """Картка-конфігуратор: документ + країна → строк і ціна → дії."""
    if selected == "kilka": selected = "narodzhennya"
    opts = "".join(f'<option value="{v}" data-k="{k}"{" selected" if v == selected else ""}>{t}</option>' for v, t, k in DOC_OPTIONS if v != "kilka")
    copts = "".join(f'<option{" selected" if c == country else ""}>{c}</option>' for c in COUNTRIES)
    k = next(k for v, _, k in DOC_OPTIONS if v == selected)
    return f"""<div class="cfg solid">
<div class="cfghead"><span>Заявка</span><span class="live">відповімо за 15 хвилин</span></div>
<p class="cfgt">Що і куди потрібно отримати</p>
<div class="sel2">
<label class="pin"><select id="cDoc" aria-label="Документ">{opts}</select></label>
<label class="pin"><select id="cCountry" aria-label="Країна">{copts}</select></label>
</div>
<div class="term" aria-live="polite"><div><small>Строк</small><b id="cTerm">від 1 <span>роб. дня</span></b></div><div><small>Ціна</small><b id="cPrice">від {PRICE[k]} <span>€</span></b></div><div class="meta" id="cMeta">За ордером адвоката, без довіреності й консульства.</div></div>
<div class="acts"><a class="btn" href="#form">Залишити заявку</a>
<div class="mrow"><a class="btn ghost msg" href="{SITE['telegram']}" target="_blank" rel="noopener" id="cTg">{ICO_TG}Telegram</a><a class="btn ghost msg" href="{SITE['whatsapp']}" target="_blank" rel="noopener" id="cWa">{ICO_WA}WhatsApp</a><a class="btn ghost msg" href="{SITE['viber']}" id="cVb">{ICO_VB}Viber</a></div></div>
<div class="who">Адвокат {SITE['person']} · свідоцтво № {SITE['cert']} · <a href="{SITE['unba']}" target="_blank" rel="noopener">перевірити в ЄРАУ</a></div>
</div>"""

def lawyer_block():
    return f"""<section class="s" id="lawyer"><div class="wrap">
<div class="law dark">
<div class="ph"><img src="/assets/img/lawyer.webp" width="200" height="200" alt="Адвокат {SITE['person']}" loading="lazy" decoding="async"></div>
<div style="flex:1;min-width:230px"><span class="eyebrow">Ваш адвокат</span><h2 style="margin-bottom:.3em">{SITE['person']}</h2><p>Адвокат з 2017 року, керівник {SITE['lawyer'].replace('Адвокатське бюро', 'Адвокатського бюро')}. Свідоцтво про право на заняття адвокатською діяльністю № {SITE['cert']}. Офіси у Вінниці, Києві та Харкові.</p><p>З 2022 року надсилаємо документи українцям за кордоном — уже в 35+ країн. Усе листування захищене адвокатською таємницею.</p><div class="chips"><a href="{SITE['unba']}" target="_blank" rel="noopener">Перевірити в ЄРАУ ↗</a><span>Адвокатська таємниця</span><span>Договір і ордер</span><span>{SITE['offices']}</span></div></div>
</div>
<div class="trust">
<div class="glass"><b>Фотозвіт</b><span>Надсилаємо фото готового документа одразу після отримання і квитанцію про відправку з трек-номером.</span></div>
<div class="glass"><b>Оплата 50 / 50</b><span>Половина на старті, друга половина — після того, як ви побачите фото готового документа.</span></div>
<div class="glass"><b>Відгуки клієнтів</b><span>Понад вісім років бюро веде справи онлайн. <a href="{SITE['reviews']}" target="_blank" rel="noopener">Відгуки про нашу роботу</a> — на сайті сервісу розлучень.</span></div>
<div class="glass"><b>Чесна відмова</b><span>Якщо документ можна отримати в Дії безкоштовно або його немає в реєстрах — скажемо одразу, до оплати.</span></div>
</div>
</div></section>
"""

def services_strip():
    return f"""<section class="s"><div class="wrap">
<span class="eyebrow">Інші сервіси бюро</span>
<h2 style="font-size:clamp(1.5rem,3.5vw,2.1rem)">Нам уже довіряють онлайн</h2>
<div class="svc">
<a class="glass" href="https://razvod-online.com.ua" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">💔</span><span><b>РозірванняШлюбу.Online</b><span>Розлучення через суд дистанційно, зокрема коли один із подружжя за кордоном</span></span></a>
<a class="glass" href="https://alimenty-online.com.ua" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">👨‍👧</span><span><b>Аліменти.Online</b><span>Стягнення аліментів без вашої присутності в суді</span></span></a>
<a class="glass" href="https://deposit-documents.com/" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">🗂️</span><span><b>Deposit Documents</b><span>Підготовка документів для повернення депозиту</span></span></a>
</div>
</div></section>
"""

def footer(selected=None, country=None):
    email = f'<li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>' if SITE["email"] else ""
    return f"""<footer class="ft"><div class="wrap">
<div class="fcols">
<div>{brand()}
<p style="margin:12px 0 0">{SITE['lawyer']}, свідоцтво про право на заняття адвокатською діяльністю № {SITE['cert']}. <a href="{SITE['unba']}" target="_blank" rel="noopener" style="text-decoration:underline">Профіль у реєстрі адвокатів НААУ</a>.</p></div>
<div><b>Документи</b><ul>
<li><a href="/svidotstvo-pro-narodzhennya/">Свідоцтво про народження</a></li>
<li><a href="/svidotstvo-pro-shlyub/">Свідоцтво про шлюб</a></li>
<li><a href="/svidotstvo-pro-rozirvannya-shlyubu/">Розірвання шлюбу</a></li>
<li><a href="/svidotstvo-pro-smert/">Свідоцтво про смерть</a></li>
<li><a href="/vytyag-dracs/">Витяг з ДРАЦС</a></li>
<li><a href="/vytyag-pro-nesudymist/">Витяг про несудимість</a></li>
<li><a href="/rnokpp/">РНОКПП</a></li>
<li><a href="/apostyl/">Апостиль</a></li></ul></div>
<div><b>Сайт</b><ul>
<li><a href="/dlya-ukraintsiv-za-kordonom/">Якщо ви за кордоном</a></li>
<li><a href="/polshcha/">Документи для Польщі</a></li>
<li><a href="/#price">Вартість</a></li>
<li><a href="/blog/">Блог</a></li>
<li><a href="/privacy.html">Політика конфіденційності</a></li>
<li><a href="https://razvod-online.com.ua" rel="noopener">Розірвання шлюбу онлайн</a></li>
<li><a href="https://alimenty-online.com.ua" rel="noopener">Аліменти онлайн</a></li></ul></div>
<div><b>Контакти</b><ul>
<li>{SITE['city']}</li>
<li>Офіси: {SITE['offices']}</li>
<li><a href="tel:{SITE['phone_raw']}">{SITE['phone']}</a></li>{email}
<li><a href="{SITE['telegram']}" target="_blank" rel="noopener">Telegram</a> · <a href="{SITE['whatsapp']}" target="_blank" rel="noopener">WhatsApp</a> · <a href="{SITE['viber']}">Viber</a></li>
<li><a href="{SITE['instagram']}" target="_blank" rel="noopener">Instagram</a> · <a href="{SITE['facebook']}" target="_blank" rel="noopener">Facebook</a> · <a href="{SITE['youtube']}" target="_blank" rel="noopener">YouTube</a></li></ul></div>
</div>
<div class="copy">© 2017–{datetime.date.today().year} {SITE['lawyer_short']}. Ми не є державним органом і не продаємо документи — адвокат отримує їх для вас у встановленому законом порядку. Повторна видача свідоцтв і витягів ДРАЦС та витяг про несудимість є державними послугами, доступними на порталі Дія.</div>
</div></footer>
<div class="sticky"><a class="btn ghost" href="{SITE['telegram']}" target="_blank" rel="noopener">Telegram</a><a class="btn" href="#form">Залишити заявку</a></div>
<template id="lead-form-tpl">{lead_form(selected, country, ids=False)}</template>
<script src="/assets/main.js?v={ASSET_V["js"]}" defer></script>
</body>
</html>
"""

def faq_block(items, title="Питання, які ставлять перед оплатою", open_first=True):
    ds = "".join(f'<details class="glass"{" open" if (i == 0 and open_first) else ""}><summary>{html.escape(q)}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))
    return f"""<section class="s" id="faq"><div class="wrap narrow"><span class="eyebrow">FAQ</span><h2>{title}</h2>{ds}</div></section>
"""

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a).replace("<strong>", "").replace("</strong>", "")}} for q, a in items]}

SCENE_STEPS = [
    ("Заявка і договір онлайн", "Підписуємо договір дистанційно. Нотаріальна довіреність не потрібна — діємо за ордером адвоката."),
    ("Отримуємо за ордером", "Звертаємось до ДРАЦС чи МВС від вашого імені. Дія і консульство не потрібні."),
    ("Апостиль, переклад, відправка", "Надсилаємо фото готового документа, ставимо апостиль і відправляємо з трек-номером."),
    ("Документ у вас", "Оригінал доставлено до дверей. Другу половину оплати ви вносите після фото документа."),
]

def scene():
    """Скрол-анімація шляху документа: Україна праворуч → країна клієнта ліворуч."""
    lis = "".join(f'<li class="st"><span class="n">{i+1}</span><div><b>{t}</b><span class="d">{d}</span></div></li>' for i, (t, d) in enumerate(SCENE_STEPS))
    return f"""<div class="scene" id="scene">
<div class="stage">
<ol class="steps">{lis}</ol>
<svg viewBox="0 0 440 320" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<defs>
<linearGradient id="gE" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdfaf2"/><stop offset="1" stop-color="#e5dac3"/></linearGradient>
<linearGradient id="gF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf7"/><stop offset="1" stop-color="#ebe0c9"/></linearGradient>
<linearGradient id="gB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d4c7ab"/><stop offset="1" stop-color="#b9aa8a"/></linearGradient>
<linearGradient id="gP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#f3eee2"/></linearGradient>
<radialGradient id="gS" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#7aa3f5"/><stop offset="1" stop-color="#2250ad"/></radialGradient>
<radialGradient id="gSh"><stop offset="0" stop-color="#4a3820" stop-opacity=".4"/><stop offset="1" stop-color="#4a3820" stop-opacity="0"/></radialGradient>
</defs>
<path id="route" class="route" d="M330 236 Q 215 120 100 236" stroke="rgba(60,45,25,.35)" stroke-width="2.5" style="stroke-dasharray:2 8"/>
<path id="prog" class="route" d="M330 236 Q 215 120 100 236" stroke="#2f66d0" stroke-width="3.5"/>
<g><circle cx="330" cy="236" r="12" fill="rgba(47,102,208,.16)"/><circle cx="330" cy="236" r="5" fill="#2f66d0"/><text class="lbl" x="330" y="294" text-anchor="middle">Україна</text></g>
<g id="dest" opacity=".55"><circle id="destRing" cx="100" cy="236" r="12" fill="rgba(47,102,208,.16)"/><circle cx="100" cy="236" r="5" fill="#2f66d0"/><text class="lbl" id="destT" x="100" y="294" text-anchor="middle">Ваша країна</text></g>
<g id="pack" transform="translate(330,236)">
 <ellipse cx="0" cy="34" rx="52" ry="7" fill="url(#gSh)"/>
 <g id="envg" opacity="0"><rect x="-46" y="-30" width="92" height="62" rx="7" fill="url(#gB)"/><path id="flapb" d="M-46 -30 L46 -30 L0 6Z" fill="url(#gB)" stroke="#a69877" stroke-width="1" stroke-linejoin="round"/></g>
 <g id="doc">
  <rect x="-48" y="-120" width="96" height="124" rx="5" fill="url(#gP)" stroke="#d6cdb8"/>
  <text x="0" y="-98" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="9" font-weight="600" fill="#2a2724">СВІДОЦТВО</text>
  <g stroke="#d3cbbb" stroke-width="2.5" stroke-linecap="round"><line x1="-34" y1="-82" x2="34" y2="-82"/><line x1="-34" y1="-70" x2="26" y2="-70"/><line x1="-34" y1="-58" x2="34" y2="-58"/><line x1="-34" y1="-46" x2="14" y2="-46"/></g>
  <path id="sig" d="M-32 -22 c 6 -14 10 6 16 -4 s 8 -12 14 -2 s 10 10 18 -6 s 6 8 12 2" fill="none" stroke="#2a2724" stroke-width="1.8" stroke-linecap="round"/>
  <g id="order" opacity="0" transform="translate(12,-36) rotate(-12)"><rect x="-30" y="-10" width="60" height="20" rx="4" fill="#fff" fill-opacity=".85" stroke="#2f66d0" stroke-width="2"/><text x="0" y="4" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="9" font-weight="600" fill="#2f66d0">ОРДЕР</text></g>
  <g id="apo" opacity="0" transform="translate(-24,-30)"><circle r="14" fill="url(#gS)" stroke="rgba(0,0,0,.15)"/><text y="-1" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="5.5" font-weight="700" fill="#fff">APOSTILLE</text><text y="7" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="6" font-weight="700" fill="#fff">UA</text></g>
 </g>
 <g id="envf" opacity="0">
  <path d="M-46 32 L46 32 L46 -30 L0 6 L-46 -30Z" fill="url(#gE)" stroke="#cdbf9f" stroke-width="1" stroke-linejoin="round"/>
  <path id="flap" d="M-46 -30 L46 -30 L0 6Z" fill="url(#gF)" stroke="#cdbf9f" stroke-width="1" stroke-linejoin="round"/>
  <g id="seal" opacity="0"><circle cx="0" cy="6" r="9" fill="url(#gS)" stroke="rgba(0,0,0,.2)"/><text x="0" y="9" text-anchor="middle" font-size="7" font-weight="700" fill="#fff" font-family="Montserrat,sans-serif">UA</text></g>
 </g>
 <g id="done" opacity="0" transform="translate(0,-56)"><rect x="-44" y="-11" width="88" height="22" rx="11" fill="#2a2724"/><text x="0" y="4" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="9" font-weight="600" fill="#fff">ДОСТАВЛЕНО ✓</text></g>
</g>
<text id="noteT" x="215" y="40" font-family="Montserrat,sans-serif" font-size="11" font-weight="600" fill="#2a2724" text-anchor="middle"></text>
</svg>
<div class="cap glass" aria-live="polite"><b id="ct"></b><span id="cd"></span></div>
<div class="bar" id="bar"></div>
</div>
</div>
"""

def steps_static(poa=False):
    s2 = ("Довіреність за нашим зразком", "Надсилаємо готовий текст. Ви посвідчуєте довіреність у нотаріуса за кордоном або в консульстві й пересилаєте оригінал нам; переклад організовуємо ми.") if poa else ("Договір онлайн", "Підписуємо договір про правову допомогу дистанційно. На його підставі адвокат виписує ордер — довіреність не потрібна.")
    s3 = ("Отримуємо документ", "Подаємо заяву до ДПС, за потреби — про внесення змін. Фото документа надсилаємо одразу після отримання.") if poa else ("Отримуємо документ", "Звертаємось у ДРАЦС або МВС, за потреби — в архів. Фото документа надсилаємо одразу після отримання.")
    s4 = ("Доставка", "За потреби робимо нотаріальну копію з перекладом і відправляємо оригінал кур'єром з трек-номером.") if poa else ("Апостиль, переклад, доставка", "Ставимо апостиль, організовуємо переклад і відправляємо оригінал кур'єром з трек-номером.")
    items = [("Заявка й розрахунок", "Ви описуєте ситуацію. Ми перевіряємо, чи є запис у реєстрі, і надсилаємо точну ціну, строк та список потрібних даних."), s2, s3, s4]
    lis = "".join(f'<li class="glass"><span class="n">{i+1}</span><strong>{t}</strong><p>{d}</p></li>' for i, (t, d) in enumerate(items))
    sub = "Один візит до нотаріуса з вашого боку — решту робимо ми." if poa else "Жодних поїздок, нотаріусів і черг з вашого боку."
    return f"""<section class="s" id="how"><div class="wrap"><span class="eyebrow">Процес</span><h2>Як це працює</h2><p class="lead">{sub}</p><ol class="steps4">{lis}</ol></div></section>
"""

# ---------------------------------------------------------------- головна
INDEX_FAQ = [
    ("Справді не потрібна нотаріальна довіреність?", "Так. Адвокат представляє клієнта на підставі договору про правову допомогу й ордера — це передбачено статтею 26 Закону «Про адвокатуру та адвокатську діяльність». ДРАЦС, МВС і архіви приймають ордер без нотаріуса. Виняток — РНОКПП: податкова вимагає нотаріальну довіреність, її можна зробити в іноземного нотаріуса, зразок надамо."),
    ("Чи потрібно йти в консульство або їхати в Україну?", "Ні. Договір підписуємо дистанційно, усе інше адвокат робить в Україні. Це особливо важливо для чоловіків 18–60 років, яким консульство надає послуги лише за наявності військово-облікового документа."),
    ("Чому не Дія?", "Якщо ви в Україні, маєте Дія.Підпис і ваш запис є в електронному реєстрі — замовляйте в Дії. Але Дія не бачить записи з паперових книг і дає електронний витяг, який за кордоном часто не приймають. У цих випадках потрібен паперовий документ, який отримує адвокат."),
    ("Скільки це коштує?", f"Повторне свідоцтво або витяг з ДРАЦС — від {PRICE['svid']} €, витяг про несудимість — від {PRICE['nes']} €, РНОКПП — від {PRICE['rnokpp']} €, апостиль — від {PRICE['apostyl']} €. Державні збори й доставка включені. Точну ціну фіксуємо в договорі після консультації."),
    ("Скільки часу це займе?", "Повторне свідоцтво, витяг з ДРАЦС або РНОКПП — від одного робочого дня. Витяг про несудимість — від п'яти робочих днів, регламентний строк МВС — до 30 днів. Апостиль — 4–10 робочих днів. Точний строк під вашу ситуацію напишемо у відповіді на заявку."),
    ("Як я зрозумію, що ви не шахраї?", f"Перевірте свідоцтво № {SITE['cert']} у Єдиному реєстрі адвокатів України. Ми підписуємо договір від імені адвокатського бюро, надсилаємо фото готового документа і квитанцію про відправку, а другу половину оплати беремо тільки після фото документа."),
    ("Як оплатити з-за кордону?", "Будь-яким зручним способом: карткою через платіжне посилання, переказом на рахунок бюро в гривні чи євро. Оплата двома частинами — 50 % на старті і 50 % після фото готового документа."),
    ("Що, якщо мого запису немає в реєстрі?", "Це найчастіша причина відмови в Дії для записів до початку 2000-х. Ми звертаємося до архіву відділу ДРАЦС, де реєстрували акт, і запис вносять до реєстру. Якщо книга втрачена — поновлюємо актовий запис."),
]

COUNTRY_ROWS = [
    ("🇵🇱 Польща", "/polshcha/", '<span class="so">за договором не потрібен</span>, на практиці установи часто просять', '<span class="so">бажано</span>', "присяжний перекладач у Польщі", '<span class="no">зазвичай не приймають</span>'),
    ("🇩🇪 Німеччина", "/nimechchyna/", '<span class="yes">обов\'язково</span>', '<span class="yes">обов\'язково</span>', "присяжний перекладач у Німеччині; український переклад не приймають", '<span class="no">не приймають</span>'),
    ("🇨🇿 Чехія", "/chekhiya/", '<span class="so">за договором не потрібен</span>, часто просять', '<span class="so">бажано</span>', "судовий перекладач у Чехії", '<span class="no">зазвичай не приймають</span>'),
    ("🇮🇹 Італія", "/italiya/", '<span class="yes">обов\'язково</span>, часто подвійний', '<span class="yes">обов\'язково</span>', "акредитований при консульстві Італії перекладач", '<span class="no">не приймають</span>'),
    ("🇪🇸 Іспанія", "/ispaniya/", '<span class="yes">обов\'язково</span>, або подвійний', '<span class="yes">обов\'язково</span>', "traductor jurado", '<span class="no">не приймають</span>'),
]

BLOG_PLAN = [
    ("Дія та е-документи", ["diia-vidmovyla-u-povtornij-vydachi"], ["Е-витяг з Дії не прийняли за кордоном: чим він відрізняється від паперового", "«Запис не знайдено»: як отримати документ з паперової книги ДРАЦС"]),
    ("По країнах", ["apostyl-chy-podvijnyj-apostyl-tablytsya-po-krainakh"], ["Документи з України для карти побиту і громадянства в Польщі", "Німеччина: Standesamt, Aufenthaltstitel і які переклади приймають", "Чехія, Італія, Іспанія: що вимагають установи"]),
    ("Документи", ["svidotstvo-pro-rozirvannya-shlyubu-chy-rishennya-sudu"], ["Витяг про несудимість за кордоном: паперовий, електронний і строк дії", "РНОКПП з-за кордону: чому тут потрібна довіреність і як її оформити в іноземного нотаріуса", "Свідоцтво про смерть для спадщини за кордоном: повний комплект"]),
    ("Довіра і процес", [], ["Ордер адвоката замість довіреності: що це, чому законно і як перевірити адвоката в ЄРАУ", "Чоловікам 18–60: що робити, якщо консульство не приймає", "Як не заплатити шахраям за документи з України: 7 перевірок"]),
]

def is_live(slug):
    return any(p["slug"] == slug and not p.get("draft") for p in PAGES)

def countries_table():
    def name(n, href):
        return f'<a href="{href}">{n}</a>' if is_live(href.strip("/")) else n
    labels = ["", "Апостиль на свідоцтво", "Апостиль на несудимість", "Переклад", "Е-витяг з Дії"]
    rows = "".join("<tr>" + f"<td>{name(r[0], r[1])}</td>" + "".join(f'<td data-label="{labels[i+1]}">{c}</td>' for i, c in enumerate(r[2:])) + "</tr>" for r in COUNTRY_ROWS)
    return f"""<div class="tblwrap glass"><table aria-label="Вимоги до українських документів по країнах">
<thead><tr><th scope="col">Країна</th><th scope="col">Апостиль на свідоцтво</th><th scope="col">Апостиль на несудимість</th><th scope="col">Переклад</th><th scope="col">Е-витяг з Дії</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""

def blog_plan_block():
    by = {p["slug"]: p for p in POSTS}
    cols = ""
    for rub, pub, plan in BLOG_PLAN:
        lis = "".join(f'<li class="pub"><a href="/blog/{s}/">{html.escape(by[s]["h1"])}</a><small>Опубліковано</small></li>' for s in pub if s in by)
        lis += "".join(f"<li>{html.escape(t)}<small>Незабаром</small></li>" for t in plan)
        cols += f'<div class="card glass"><span class="tag">Рубрика</span><h3>{rub}</h3><ol>{lis}</ol></div>'
    return f'<div class="blog">{cols}</div>'

def doc_card(tag, tagcls, title, href, text, term_l, term, price):
    return f'<div class="card glass"><span class="tag{tagcls}">{tag}</span><h3><a href="{href}">{title}</a></h3><p>{text}</p><div class="foot"><span>{term_l} <b>{term}</b></span><span><b>від {price} €</b></span></div></div>'

def build_index():
    h = head(f"Документи з України за кордон — без поїздки і довіреності | {SITE['name']}",
             "Повторні свідоцтва ДРАЦС, витяги, витяг про несудимість, апостиль і доставка в 35+ країн. Адвокат отримує документ за ордером — нотаріальна довіреність і консульство не потрібні. Від 80 €.",
             "/", [faq_ld(INDEX_FAQ)])
    docs = "".join([
        doc_card("За ордером", "", "Повторні свідоцтва ДРАЦС", "/svidotstvo-pro-narodzhennya/", 'Про <a href="/svidotstvo-pro-narodzhennya/">народження</a>, <a href="/svidotstvo-pro-shlyub/">шлюб</a>, <a href="/svidotstvo-pro-rozirvannya-shlyubu/">розірвання шлюбу</a>, <a href="/svidotstvo-pro-smert/">смерть</a>, зміну імені. Документ нового зразка, придатний для апостиля.', "Строк", "від 1 роб. дня", PRICE["svid"]),
        doc_card("За ордером", "", "Витяг з ДРАЦС", "/vytyag-dracs/", "Підтверджує факт реєстрації акта і містить дані, яких немає у свідоцтві. Його найчастіше просять для шлюбу й спадщини за кордоном.", "Строк", "від 1 роб. дня", PRICE["vyt"]),
        doc_card("За ордером", "", "Витяг про несудимість", "/vytyag-pro-nesudymist/", "Паперовий, з печаткою МВС і апостилем. Електронний витяг з Дії для карти побиту, громадянства чи роботи за кордоном зазвичай не приймають.", "Строк", "від 5 роб. днів", PRICE["nes"]),
        doc_card("Потрібна довіреність", " warn", "РНОКПП", "/rnokpp/", "Код платника податків. Тут закон вимагає нотаріальну довіреність — її можна оформити в іноземного нотаріуса, зразок надамо.", "Строк", "від 1 роб. дня", PRICE["rnokpp"]),
        doc_card("Додатково", "", "Апостиль", "/apostyl/", "У Мін'юсті, МЗС або МОН залежно від документа. Для Італії та Іспанії — подвійний апостиль, якщо його вимагає установа.", "Строк", "4–10 роб. днів", PRICE["apostyl"]),
        doc_card("Додатково", "", "Переклад і доставка", "/dlya-ukraintsiv-za-kordonom/", "Підкажемо, який переклад приймуть у вашій країні. Оригінал відправляємо кур'єром до дверей з трек-номером.", "Доставка", "3–7 днів", PRICE["delivery"]),
    ])
    body = f"""{header()}
<main id="top">
<section class="hero"><div class="wrap">
<div class="hgrid">
<div>
<span class="pill glass">{SITE['lawyer_short']} · свідоцтво № {SITE['cert']} · з 2017</span>
<h1>Документи з України — без поїздки і довіреності</h1>
<p class="lead">Повторні свідоцтва ДРАЦС, витяги, витяг про несудимість, апостиль і доставка в 35+ країн. <strong>Адвокат отримує документ за ордером</strong> — нотаріальна довіреність і похід у консульство не потрібні.</p>
<div class="row"><a class="btn" href="#form">Дізнатись вартість і строк</a><a class="btn ghost" href="#scene">Як це працює</a></div>
</div>
{cfg()}
</div>
<div class="proof">
<div class="glass"><b>Ордер адвоката</b>Законна підстава представництва за ст. 26 Закону «Про адвокатуру та адвокатську діяльність». Нотаріус не потрібен.</div>
<div class="glass"><b>Свідоцтво № {SITE['cert']}</b><a href="{SITE['unba']}" target="_blank" rel="noopener">Перевірити в ЄРАУ →</a></div>
<div class="glass"><b>{SITE['cases']} документів</b>отримуємо щороку для клієнтів з України і з-за кордону</div>
<div class="glass"><b>35+ країн</b>доставки: Польща, Німеччина, Чехія, Італія, Іспанія, Канада, США та інші</div>
</div>
</div></section>

{scene()}
<section class="s" id="docs"><div class="wrap">
<span class="eyebrow">Що ми отримуємо</span>
<h2>Документи, строки і ціни</h2>
<p class="lead">Усе, крім РНОКПП, отримуємо за ордером адвоката — від вас потрібні лише скан паспорта і дані про документ. Державні збори включені в ціну, точну суму фіксуємо в договорі після консультації.</p>
<div class="grid">{docs}</div>
<p class="note" style="margin-top:18px">Не знайшли свій документ? Напишіть — скажемо чесно, чи можливо його отримати і чи потрібні ми взагалі.</p>
</div></section>

<section class="s" id="diia"><div class="wrap">
<span class="eyebrow">Коли Дія не допоможе</span>
<h2>Три ситуації, з якими до нас приходять найчастіше</h2>
<p class="lead">Якщо ви в Україні, маєте Дія.Підпис і ваш актовий запис є в електронному реєстрі — замовляйте в Дії, це майже безкоштовно. Ми потрібні, коли цей шлях не працює.</p>
<div class="grid3">
<div class="card glass"><p class="q">Дія каже «запис не знайдено» або відмовляє у повторній видачі</p><p>Так буває з актами до 2000-х років, зміненими даними або коли паперова книга ще не оцифрована.</p><p class="ans">Адвокат звертається у відділ ДРАЦС чи архів напряму, з ордером, і отримує документ з паперової книги. <a href="/blog/diia-vidmovyla-u-povtornij-vydachi/" style="color:var(--blue)">Шість причин відмови</a>.</p></div>
<div class="card glass"><p class="q">Електронний витяг з Дії не прийняли в установі за кордоном</p><p>Електронний документ без мокрої печатки за кордоном часто не визнають — потрібен паперовий оригінал з апостилем.</p><p class="ans">Отримуємо паперовий документ, ставимо апостиль і відправляємо кур'єром. Ви отримуєте те, що приймуть.</p></div>
<div class="card glass"><p class="q">Консульство записує на місяці вперед або не приймає взагалі</p><p>Черги на запис, вимога особистої присутності, а чоловікам 18–60 років послуги надають лише з військово-обліковим документом.</p><p class="ans">У консульство йти не треба: ордер адвоката діє в Україні без вашої участі й без нотаріуса.</p></div>
</div>
</div></section>

<section class="s"><div class="wrap"><div class="men dark">
<div><span class="eyebrow">Чоловікам 18–60</span><h2 style="margin-bottom:.4em">Консульство не приймає без військово-облікового документа. Нам він не потрібен</h2><p>З 2024 року консульські установи надають послуги чоловікам призовного віку лише за наявності оновлених військово-облікових даних. Нотаріальну довіреність за кордоном теж не завжди вдається оформити. Ордер адвоката вирішує обидві проблеми: ви нікуди не йдете, документ отримує адвокат в Україні.</p><a class="btn blue" href="#form">Описати ситуацію</a></div>
<ul>
<li><b>Без консульства</b>Ордер подається безпосередньо у ДРАЦС чи МВС в Україні.</li>
<li><b>Без нотаріуса</b>Договір підписуємо дистанційно. Виняток — РНОКПП.</li>
<li><b>Без вашої присутності</b>Від вас — скан паспорта і контакт у месенджері.</li>
<li><b>Конфіденційно</b>Усе листування захищене адвокатською таємницею.</li>
</ul>
</div></div></section>

<section class="s" id="countries"><div class="wrap">
<span class="eyebrow">Куди відправляємо</span>
<h2>Що потрібно саме у вашій країні</h2>
<p class="lead">Вимоги залежать від країни, а не від документа. Нижче — п'ять країн, де живе найбільше українців. Докладніше — у статті <a href="/blog/apostyl-chy-podvijnyj-apostyl-tablytsya-po-krainakh/" style="color:var(--blue)">про апостиль по країнах</a>.</p>
{countries_table()}
<p class="note" style="margin-top:14px">Інша країна? Відправляємо в 35+ країн, зокрема в Канаду, США, Велику Британію та Ізраїль. Вкажіть країну в заявці — підкажемо вимоги.</p>
<div class="chipsl" aria-label="Служби доставки"><span>Нова Пошта</span><span>DHL</span><span>Укрпошта</span><span>Meest</span><span class="note" style="background:none;box-shadow:none;padding-left:4px">— обираємо службу, яка швидше доставить у вашу країну</span></div>
</div></section>

<section class="s" id="price"><div class="wrap">
<span class="eyebrow">Вартість</span>
<h2>Три пакети замість «ціна за запитом»</h2>
<p class="lead">Державні збори й доставка включені. Точну ціну фіксуємо в договорі після консультації. Оплата двома частинами: 50 % на старті, 50 % — після фото готового документа.</p>
<div class="pk">
<div class="card glass"><span class="tag">Пакет 1</span><h3>Документ</h3><p>Отримуємо документ в Україні й надсилаємо фото. Оригінал відправляємо на вашу адресу або зберігаємо до наступного кроку.</p><div class="price">від {PACK['p1']} €</div><div class="per">за один документ · від 1 роб. дня</div><ul><li>Договір і ордер</li><li>Повторне свідоцтво або витяг</li><li>Фото документа одразу</li></ul><a class="btn ghost" href="#form">Обрати</a></div>
<div class="card bluecard"><span class="tag">Найчастіше</span><h3>Документ + апостиль</h3><p>Те, що приймають за кордоном: паперовий оригінал з апостилем, відправлений кур'єром до ваших дверей.</p><div class="price">від {PACK['p2']} €</div><div class="per">за один документ · 5–11 роб. днів</div><ul><li>Усе з пакета 1</li><li>Апостиль Мін'юсту, МЗС або МОН</li><li>Доставка з трек-номером</li></ul><a class="btn white" href="#form">Обрати</a></div>
<div class="card glass"><span class="tag">Пакет 3</span><h3>Під ключ</h3><p>Для тих, хто хоче віддати одне завдання і отримати готовий комплект для установи.</p><div class="price">від {PACK['p3']} €</div><div class="per">за комплект · строк залежить від країни</div><ul><li>Усе з пакета 2</li><li>Переклад, який приймуть у вашій країні</li><li>Подвійний апостиль за потреби</li><li>Супровід до подачі в установу</li></ul><a class="btn ghost" href="#form">Обрати</a></div>
</div>
<p class="note" style="margin-top:16px">Відповідь із точною ціною і строком — за 15 хвилин у робочий час. Якщо документ можна отримати в Дії безкоштовно, ми так і скажемо.</p>
</div></section>

{lawyer_block()}
{services_strip()}
{faq_block(INDEX_FAQ)}
<section class="s" id="blog"><div class="wrap">
<span class="eyebrow">Блог</span>
<h2>Розбираємо реальні ситуації з документами</h2>
<p class="lead">Чотири рубрики, кожна відповідає на запит, з яким люди приходять у пошук. <a href="/blog/" style="color:var(--blue)">Усі статті</a>.</p>
{blog_plan_block()}
</div></section>
{form_section()}
</main>
{footer()}"""
    write("index.html", h + body)

# ---------------------------------------------------------------- внутрішні сторінки
def cases_block(cases):
    if not cases: return ""
    c = cases["cols"]
    rows = "".join(f'<tr><td>{a}</td><td data-label="{c[1]}">{b}</td><td data-label="{c[2]}">{d}</td></tr>' for a, b, d in cases["rows"])
    return f"""<section class="s"><div class="wrap"><h2>{cases['title']}</h2>
<div class="tblwrap glass"><table aria-label="{html.escape(cases['title'])}"><thead><tr><th scope="col">{c[0]}</th><th scope="col">{c[1]}</th><th scope="col">{c[2]}</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note" style="margin-top:14px">{cases.get('note','')}</p></div></section>
"""

def build_page(p):
    path = f"/{p['slug']}/"
    draft = p.get("draft", False)
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Головна", "item": SITE["domain"] + "/"},
        {"@type": "ListItem", "position": 2, "name": p["h1"], "item": SITE["domain"] + path}]}
    h = head(f"{p['title']} | {SITE['name']}", p["desc"], path, [faq_ld(p["faq"]), crumbs_ld], noindex=draft)
    diia = "".join(f"<li>{s}</li>" for s in p["diia"])
    lawyer = "".join(f"<div class='tile glass'><strong>{t}</strong><p>{d}</p></div>" for t, d in p["lawyer"])
    need = "".join(f"<li>{n}</li>" for n in p["need"])
    country = p.get("country", "Польща")
    note = '<div class="draft"><strong>Чернетка на перевірці адвоката.</strong> Сторінка закрита від пошуковиків і не має посилань із сайту.</div>' if draft else ""
    body = f"""{header()}
<main>
<section class="phero"><div class="wrap">
<nav class="crumbs" aria-label="Хлібні крихти"><a href="/">Головна</a><span>›</span><span>{html.escape(p['h1'])}</span></nav>
{note}<div class="hgrid">
<div><h1>{p['h1']}</h1><p class="lead">{p['lead']}</p>
<div class="row"><a class="btn" href="#form">Дізнатись вартість і строк</a><a class="btn ghost" href="#diia">Як зробити самому</a></div></div>
{cfg(p['doc'], country)}
</div></div></section>

<section class="s"><div class="wrap narrow"><div class="prose solid">{p['intro']}</div></div></section>
{cases_block(p.get('cases'))}
<section class="s" id="diia"><div class="wrap narrow">
<span class="eyebrow">Самостійно</span><h2>Як отримати самому</h2><p class="lead">Якщо ви в Україні і маєте Дія.Підпис — спробуйте спершу цей шлях.</p>
<ol class="olist">{diia}</ol>
<p class="callout" style="margin-top:16px">{p['diia_note']}</p>
</div></section>

<section class="s"><div class="wrap"><span class="eyebrow">Через адвоката</span><h2>Коли потрібен адвокат</h2><div class="grid2">{lawyer}</div></div></section>

<section class="s"><div class="wrap narrow"><span class="eyebrow">Від вас</span><h2>Що потрібно від вас</h2>
<ul class="nlist">{need}</ul>
<p class="note" style="margin-top:14px">Жодних оригіналів пересилати не потрібно. Усе спілкування — у месенджері.</p>
</div></section>

{steps_static(poa=p.get('poa', False))}
{lawyer_block()}
{faq_block(p['faq'], "Часті питання")}
{form_section(p['doc'], p.get('country'))}
</main>
{footer(p['doc'], p.get('country'))}"""
    write(f"{p['slug']}/index.html", h + body)

# ---------------------------------------------------------------- блог
def fmt_date(d):
    y, m, dd = d.split("-"); months = ["січня","лютого","березня","квітня","травня","червня","липня","серпня","вересня","жовтня","листопада","грудня"]
    return f"{int(dd)} {months[int(m)-1]} {y}"

def post_card(post):
    return f"""<article class="card glass"><span class="pmeta">{fmt_date(post['date'])} · {post['minutes']} хв читання</span><h3><a href="/blog/{post['slug']}/">{html.escape(post['h1'])}</a></h3><p>{html.escape(post['lead'][:180])}…</p><a class="more" href="/blog/{post['slug']}/" aria-label="Читати: {html.escape(post['h1'])}">Читати →</a></article>"""

def build_blog_index():
    h = head(f"Блог: документи з України, ДРАЦС, апостиль, несудимість | {SITE['name']}",
             "Практичні статті про отримання документів з України для тих, хто за кордоном: відмови Дії, апостиль по країнах, витяги ДРАЦС, несудимість, розлучення.", "/blog/")
    cards = "".join(post_card(p) for p in sorted(POSTS, key=lambda x: x["date"], reverse=True))
    body = f"""{header()}
<main>
<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Хлібні крихти"><a href="/">Головна</a><span>›</span><span>Блог</span></nav>
<h1>Блог</h1><p class="lead">Розбираємо реальні ситуації з документами ДРАЦС, апостилем і несудимістю — так, щоб ви могли або зробити самі, або точно знати, що замовляти.</p></div></section>
<section class="s" style="padding-top:10px"><div class="wrap"><div class="grid3">{cards}</div></div></section>
<section class="s"><div class="wrap"><span class="eyebrow">План публікацій</span><h2>Рубрики й найближчі статті</h2>{blog_plan_block()}</div></section>
{form_section()}
</main>
{footer()}"""
    write("blog/index.html", h + body)

def build_post(post):
    path = f"/blog/{post['slug']}/"
    ld = [{"@context":"https://schema.org","@type":"Article","headline":post["h1"],"description":post["desc"],
           "datePublished":post["date"],"dateModified":post["date"],"inLanguage":"uk","image":SITE["domain"]+"/assets/og.png",
           "author":{"@type":"Person","name":SITE["person"],"url":SITE["unba"]},
           "publisher":{"@type":"Organization","name":SITE["name"],"url":SITE["domain"]},
           "mainEntityOfPage":SITE["domain"]+path},
          {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
           {"@type":"ListItem","position":1,"name":"Головна","item":SITE["domain"]+"/"},
           {"@type":"ListItem","position":2,"name":"Блог","item":SITE["domain"]+"/blog/"},
           {"@type":"ListItem","position":3,"name":post["h1"],"item":SITE["domain"]+path}]}]
    h = head(f"{post['title']} | {SITE['name']}", post["desc"], path, ld)
    rel_pages = [pp for pp in PAGES if pp["slug"] in post.get("related", []) and not pp.get("draft")]
    related = "".join(f'<a class="tile glass" href="/{pp["slug"]}/"><strong>{html.escape(pp["h1"])}</strong><p>{html.escape(pp["lead"][:120])}…</p></a>' for pp in rel_pages)
    others = [pp for pp in POSTS if pp["slug"] != post["slug"]][:3]
    more = "".join(post_card(pp) for pp in others)
    body_html = post["body"].replace("<table", '<div class="tblwrap"><table').replace("</table>", "</table></div>")
    body = f"""{header()}
<main>
<article>
<section class="phero"><div class="wrap narrow"><nav class="crumbs" aria-label="Хлібні крихти"><a href="/">Головна</a><span>›</span><a href="/blog/">Блог</a></nav>
<span class="pmeta">{fmt_date(post['date'])} · {post['minutes']} хв читання · адвокат {SITE['person']}</span><h1 style="margin-top:10px">{html.escape(post['h1'])}</h1><p class="lead" style="max-width:none">{post['lead']}</p></div></section>
<section class="s" style="padding-top:10px"><div class="wrap narrow"><div class="prose solid">{body_html}</div></div></section>
</article>
<section class="s"><div class="wrap"><span class="eyebrow">Пов'язані послуги</span><h2>Не виходить самостійно?</h2><p class="lead">Опишіть ситуацію — скажемо чесно, чи варто платити, і якщо так, назвемо ціну та строк.</p><div class="grid3">{related}</div></div></section>
<section class="s"><div class="wrap"><h2>Ще з блогу</h2><div class="grid3">{more}</div></div></section>
{form_section(post['cta_doc'])}
</main>
{footer(post['cta_doc'])}"""
    write(f"blog/{post['slug']}/index.html", h + body)

# ---------------------------------------------------------------- службові файли
def build_misc():
    urls = ["/"] + [f"/{p['slug']}/" for p in PAGES if not p.get("draft")] + ["/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE['domain']}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{'1.0' if u == '/' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")
    write("assets/favicon.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A33E3"/><stop offset="1" stop-color="#3A8CD8"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="url(#g)"/><g transform="translate(7 7) scale(.78)"><path fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" d="M58 30L34.29 42.77Q32 44 29.71 42.77L6 30L6 52Q6 56 10 56L54 56Q58 56 58 52L58 30L48 30Q45 30 45 27L45 9.2Q45 6 41.8 6L22.2 6Q19 6 19 9.2L19 27Q19 30 16 30L6 30"/></g></svg>')
    h = head(f"Сторінку не знайдено | {SITE['name']}", "Сторінку не знайдено.", "/404.html", noindex=True)
    write("404.html", h + header() + '<main><section class="s"><div class="wrap narrow"><h1>Сторінку не знайдено</h1><p class="lead">Можливо, адресу змінено. Перейдіть на <a href="/" style="color:var(--blue)">головну</a> або оберіть документ у меню.</p></div></section>' + form_section() + '</main>' + footer())
    h = head(f"Політика конфіденційності | {SITE['name']}", "Політика обробки персональних даних сайту «Документи з України».", "/privacy.html")
    contact = SITE["email"] or f'у Telegram або за телефоном {SITE["phone"]}'
    write("privacy.html", h + header() + f'''<main><section class="s"><div class="wrap narrow"><div class="prose solid">
<h1 style="font-size:clamp(1.8rem,4.5vw,2.6rem)">Політика конфіденційності</h1>
<p>Цей сайт належить {SITE['lawyer']} ({SITE['city']}). Персональні дані, які ви залишаєте у формі заявки (ім'я, контакт, країна, документ), використовуються виключно для підготовки відповіді та укладення договору про правову допомогу. Дані не передаються третім особам, крім випадків, передбачених законом, і зберігаються не довше, ніж потрібно для надання послуги.</p>
<p>Заявки з форми обробляє сервіс Formspree, який пересилає їх адвокату. Сайт не використовує рекламних cookies.</p>
<p>Відомості, отримані адвокатом у зв'язку з наданням правової допомоги, є адвокатською таємницею відповідно до Закону України «Про адвокатуру та адвокатську діяльність».</p>
<p>Ви можете в будь-який момент запросити видалення своїх даних, написавши {contact}.</p>
</div></div></section></main>''' + footer())

def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)

if __name__ == "__main__":
    build_index()
    for p in PAGES:
        build_page(p)
    build_blog_index()
    for p in POSTS:
        build_post(p)
    build_misc()
