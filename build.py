# -*- coding: utf-8 -*-
"""
Static site generator for oniks16 (ОНИКС — стройматериалы, Набережные Челны).
Generates a multi-page SEO-friendly static site into ./site (web root: site_src -> site).
"""
import json, re, os, shutil, html, unicodedata, datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "site_src")
OUT = os.path.join(ROOT, "site")
BASE_URL = "https://oniks16.ru"  # canonical base (same domain, new site replaces old)

PHONE_MAIN = "+7 (906) 122-29-99"
PHONE_MAIN_HREF = "+79061222999"
PHONE_SECOND = "+7 (906) 119-47-32"
PHONE_SECOND_HREF = "+79061194732"
WHATSAPP = "79061222999"
EMAIL = "onikstroy@mail.ru"
ADDRESS = "г. Набережные Челны, Казанский проспект, 234, строение 7"
WORK_HOURS = "Пн–Пт: 08:00–16:00 (перерыв 12:00–13:00), Сб: 08:00–12:00"
ORG_NAME = "ОНИКС"
ORG_FULL = "Компания «ОНИКС» — строительные и отделочные материалы в Набережных Челнах"
INN = "ИНН 1650367329"
OGRN = "ОГРН 1181690062465"

# ---------------------------------------------------------------- categories
CATEGORIES = [
    {"slug": "shtukaturki", "name": "Штукатурки", "short": "Гипсовые и цементные составы",
     "title": "Штукатурка гипсовая и цементная — купить в Набережных Челнах",
     "desc": "Гипсовые и цементные штукатурки KNAUF, OBERFIX, Декоратор, PLITONIT оптом и в розницу. Машинного и ручного нанесения. Склад в Набережных Челнах, быстрая отгрузка.",
     "text": "Штукатурка — базовый материал черновой и чистовой отделки стен и потолков. В каталоге «ОНИКС» — гипсовые штукатурки машинного и ручного нанесения (KNAUF, OBERFIX, GipsPLAST), цементные составы для фасадов и влажных помещений (Декоратор DK, PLITONIT, CemPLAST), а также декоративные фактурные смеси. Поможем рассчитать расход на вашу площадь и подобрать состав под основание: бетон, кирпич, газобетон."},
    {"slug": "dekorativnaya", "name": "Декоративная штукатурка", "short": "Фактурные покрытия для стен и фасадов",
     "title": "Декоративная штукатурка — купить в Набережных Челнах | ОНИКС",
     "desc": "Декоративные штукатурки Декоратор: венецианская, короед, травертино, арт-бетон, марокканская. В наличии на складе в Набережных Челнах. Поможем с выбором и расчётом.",
     "text": "Декоративная штукатурка превращает стены в готовое финишное покрытие: венецианская классика и мраморная, фактурные «короед» и «апельсиновая корка», травертино, арт-бетон, вельвет и «китайский шёлк». Линейка Декоратор DK подходит для интерьеров и фасадов, колеруется в любой цвет. Подскажем по технике нанесения и расходу на квадратный метр."},
    {"slug": "shpaklevki", "name": "Шпатлёвки", "short": "Стартовые и финишные смеси",
     "title": "Шпатлёвка гипсовая, цементная, финишная — Набережные Челны",
     "desc": "Шпатлёвки Декоратор DK и TopSILK: гипсовые универсальные, финишные полимерные, цементные фасадные. Опт и розница в Набережных Челнах.",
     "text": "Шпатлёвка доводит поверхность до состояния «под покраску» или «под обои». У нас — гипсовые универсальные и полимерные составы для сухих помещений, цементные фасадные шпатлёвки для улицы и влажных зон, финишные смеси с тонким слоем нанесения. Подберём связку «штукатурка + шпатлёвка» под ваш тип основания."},
    {"slug": "nalivnoi-pol", "name": "Наливные полы", "short": "Ровнители и самонивелирующиеся смеси",
     "title": "Наливной пол и ровнители — купить в Набережных Челнах | ОНИКС",
     "desc": "Наливные полы Декоратор DK: быстротвердеющие, финишные, для тёплых полов. Склад в Набережных Челнах, отгрузка в день заказа.",
     "text": "Наливной пол создаёт идеально ровное основание под ламинат, плитку, линолеум и паркет. В наличии быстротвердеющие ровнители (по полу можно ходить уже через 3–4 часа), базовые и финишные самонивелирующиеся смеси Декоратор DK с толщиной слоя от 1 до 100 мм."},
    {"slug": "gipsokarton", "name": "Гипсокартон", "short": "Листы, профили и комплектующие",
     "title": "Гипсокартон и профиль — купить в Набережных Челнах | ОНИКС",
     "desc": "Гипсокартон ГКЛ, ГКЛВ, ГКЛО 9,5 и 12,5 мм и профили для каркаса. Оптом и в розницу со склада в Набережных Челнах. Доставка по городу.",
     "text": "Гипсокартон — основа перегородок, потолков и обшивки стен. Держим на складе листы ГКЛ (обычный), ГКЛВ (влагостойкий) и ГКЛО (огнестойкий) толщиной 9,5 и 12,5 мм, а также полный набор профилей: направляющие, стоечные, потолочные. Поможем рассчитать комплект на ваш объект."},
    {"slug": "klej", "name": "Плиточный клей", "short": "Для плитки, камня и керамогранита",
     "title": "Клей для плитки и керамогранита — Набережные Челны | ОНИКС",
     "desc": "Плиточный клей Декоратор DK, KeraMax, GraniFIX, KeraFix: стандартный, усиленный, для керамогранита и мозаики. В наличии в Набережных Челнах.",
     "text": "Правильный клей — залог того, что плитка не отвалится через год. У нас — базовые и усиленные клеи для керамической плитки, керамогранита и натурального камня, белый клей для мозаики и стеклянной плитки, монтажные клеи для пенополистирола и ГКЛ, штукатурно-клеевые смеси для фасадов. Подскажем класс клея под формат плитки и основание."},
    {"slug": "kraski", "name": "Краски и грунтовки", "short": "Для внутренних и фасадных работ",
     "title": "Краски и грунтовки — купить в Набережных Челнах | ОНИКС",
     "desc": "Грунтовки глубокого проникновения, бетонконтакт, кварц-грунт, интерьерные и фасадные краски. Склад в Набережных Челнах.",
     "text": "Грунтовка укрепляет основание и сокращает расход финишных материалов, краска завершает отделку. В каталоге — грунты глубокого проникновения, адгезионный бетонконтакт, кварц-грунт под декоративные покрытия, влагостойкие интерьерные и атмосферостойкие фасадные краски."},
    {"slug": "potolochnye-paneli", "name": "Потолочные панели", "short": "Готовые решения для отделки потолка",
     "title": "Потолочные панели GIPSCOLOR — Набережные Челны | ОНИКС",
     "desc": "Потолочные панели GIPSCOLOR Universal и Medical 600×600. Быстрый монтаж, влагостойкость. Купить в Набережных Челнах.",
     "text": "Потолочные панели GIPSCOLOR — готовое решение для офисов, магазинов, медицинских и жилых помещений. Панели 600×600 мм серий Universal и Medical монтируются на стандартную подвесную систему, не требуют финишной отделки и легко моются."},
    {"slug": "zatirki", "name": "Затирки", "short": "Цементные и эпоксидные составы",
     "title": "Затирка для плитки — купить в Набережных Челнах | ОНИКС",
     "desc": "Затирки PLITONIT Colorit: цементные и эпоксидные, широкая палитра цветов. В наличии в Набережных Челнах.",
     "text": "Затирка защищает швы от влаги и загрязнений и завершает облик облицовки. Предлагаем цементные затирки PLITONIT Colorit Premium и трёхкомпонентную эпоксидную затирку Colorit Easy Fill — устойчивую к влаге, грибку и бытовой химии."},
    {"slug": "steklooboi", "name": "Стеклообои", "short": "Армирующие покрытия под покраску",
     "title": "Стеклообои под покраску Profitex — Набережные Челны | ОНИКС",
     "desc": "Стеклотканевые обои Profitex: рогожка, ёлочка, паутинка. Прочное покрытие под многократную покраску. Купить в Набережных Челнах.",
     "text": "Стеклообои — армирующее покрытие стен и потолков под покраску: скрывают мелкие трещины, выдерживают до 10–15 циклов перекрашивания, не горят и не боятся влаги. Фактуры Profitex — от мелкой «паутинки» до выразительных «рогожки» и «ёлочки»."},
    {"slug": "raznoe", "name": "Разное", "short": "Сетки, крепёж и сопутствующие товары",
     "title": "Сетки, дюбели, углы и комплектующие — Набережные Челны | ОНИКС",
     "desc": "Фасадные сетки, дюбель-гвозди для изоляции, штукатурные углы и маяки. Комплектующие для отделки в Набережных Челнах.",
     "text": "Мелочей в отделке не бывает: фасадная сетка, углы с армирующей сеткой, штукатурные маяки, дюбель-гвозди для теплоизоляции. Все сопутствующие материалы — в одном заказе вместе со смесями и гипсокартоном."},
]

TRANSLIT = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i','й':'y',
    'к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f',
    'х':'h','ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
}

def slugify(s):
    s = s.lower().replace("ё", "е")
    out = []
    for ch in s:
        if ch in TRANSLIT: out.append(TRANSLIT[ch])
        elif ch.isalnum(): out.append(ch)
        else: out.append("-")
    slug = re.sub(r"-+", "-", "".join(out)).strip("-")
    return slug[:80]

def clean_html(t):
    """Strip Tilda markup to plain paragraphs."""
    if not t: return ""
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"</p>", "\n\n", t)
    t = re.sub(r"<li>", "— ", t)
    t = re.sub(r"</li>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n\s*", "\n\n", t)
    return t.strip()

# generic fallback descriptions per category
FALLBACK = {
    "shtukaturki": "{name} — сухая штукатурная смесь для выравнивания стен и потолков. Подходит для внутренних работ по бетону, кирпичу и газобетону. Наносится ручным или машинным способом, образует ровную поверхность под шпатлёвку, покраску или декоративную отделку.",
    "dekorativnaya": "{name} — декоративное покрытие для стен с выразительной фактурой. Наносится на подготовленное основание, колеруется в нужный оттенок, после высыхания не требует дополнительной отделки. Подходит для квартир, офисов и коммерческих интерьеров.",
    "shpaklevki": "{name} — шпатлёвка для финишного выравнивания поверхности перед покраской или оклейкой обоями. Легко наносится и шлифуется, образует гладкое основание без усадки и трещин.",
    "nalivnoi-pol": "{name} — самонивелирующаяся смесь для создания ровного основания пола под финишные покрытия: ламинат, плитку, линолеум. Быстро набирает прочность, подходит для систем тёплого пола.",
    "gipsokarton": "{name} — материал для устройства перегородок, обшивки стен и подвесных потолков. Монтируется на каркас из металлического профиля, образует ровную поверхность под любую финишную отделку.",
    "klej": "{name} — клеевой состав для облицовочных работ. Обеспечивает надёжное сцепление с основанием, устойчив к сползанию плитки, подходит для внутренних и наружных работ.",
    "kraski": "{name} — материал для подготовки и финишной отделки поверхностей. Обеспечивает равномерное покрытие, стойкий цвет и долговечность отделки внутри и снаружи помещений.",
    "potolochnye-paneli": "{name} — готовое решение для отделки потолков. Монтируется на стандартную подвесную систему 600×600, не требует покраски, легко моется и при необходимости заменяется отдельными модулями.",
    "zatirki": "{name} — затирочный состав для заполнения межплиточных швов. Защищает облицовку от влаги и загрязнений, устойчив к бытовой химии, сохраняет цвет в течение всего срока службы.",
    "steklooboi": "{name} — стеклотканевое покрытие для стен и потолков под покраску. Армирует поверхность, скрывает мелкие трещины, выдерживает многократное перекрашивание. Не поддерживает горение, подходит для помещений любого назначения.",
    "raznoe": "{name} — комплектующие для строительных и отделочных работ. Применяется вместе с основными материалами из каталога: смесями, гипсокартоном и профилями.",
}

def load_products():
    prods = json.load(open(os.path.join(ROOT, "products_final.json"), encoding="utf-8"))
    cat_by_name = {c["name"]: c for c in CATEGORIES}
    # map scraped category names to new slugs
    remap = {
        "Штукатурки": "shtukaturki", "Декоративная штукатурка": "dekorativnaya",
        "Шпатлёвки": "shpaklevki", "Наливные полы": "nalivnoi-pol",
        "Гипсокартон": "gipsokarton", "Плиточный клей": "klej",
        "Краски и грунтовки": "kraski", "Потолочные панели": "potolochnye-paneli",
        "Затирки": "zatirki", "Разное": "raznoe",
    }
    used = set()
    out = []
    for p in prods:
        cat_slug = remap.get(p["category"], "raznoe")
        price = p.get("page_price")
        if not price:
            try: price = int(float(p.get("price") or 0)) or None
            except Exception: price = None
        slug = slugify(p["title"])
        if not slug or slug in used:
            slug = f"{slug}-{p['uid'] % 100000}"
        used.add(slug)
        desc = clean_html(p.get("text") or "")
        if len(desc) < 60:
            desc = FALLBACK[cat_slug].format(name=p["title"])
        out.append({
            "uid": p["uid"], "name": p["title"], "slug": slug,
            "cat": cat_slug, "price": price,
            "images": p.get("local_images") or [],
            "desc": desc,
            "old_url": p.get("url") or "",
        })
    return out

def main():
    products = load_products()
    by_cat = {c["slug"]: [] for c in CATEGORIES}
    for p in products:
        by_cat[p["cat"]].append(p)

    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)

    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")),
                      autoescape=select_autoescape(["html"]))
    ctx_common = {
        "phone_main": PHONE_MAIN, "phone_main_href": PHONE_MAIN_HREF,
        "phone_second": PHONE_SECOND, "phone_second_href": PHONE_SECOND_HREF,
        "whatsapp": WHATSAPP, "email": EMAIL, "address": ADDRESS,
        "work_hours": WORK_HOURS, "org": ORG_NAME, "inn": INN, "ogrn": OGRN,
        "base": BASE_URL, "categories": CATEGORIES,
        "year": datetime.date.today().year,
    }

    pages = []  # (url_path, priority, changefreq) for sitemap

    def render(tpl, out_path, **kw):
        t = env.get_template(tpl)
        html_doc = t.render(**{**ctx_common, **kw})
        full = os.path.join(OUT, out_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(html_doc)

    # index
    hits = [p for p in products if p["price"] and p["images"]][:8]
    render("index.html", "index.html", page_title="Строительные материалы оптом и в розницу в Набережных Челнах — ОНИКС",
           page_desc="Штукатурки, шпатлёвки, наливные полы, гипсокартон, плиточный клей и краски со склада в Набережных Челнах. Прямые поставки от производителей, особые условия для опта. Доставка по городу.",
           canonical="/", hits=hits, total=len(products), active="index")
    pages.append(("/", "1.0", "weekly"))

    # catalog index
    render("catalog.html", "catalog/index.html", page_title="Каталог строительных материалов — ОНИКС, Набережные Челны",
           page_desc="Полный каталог строительных и отделочных материалов: штукатурки, шпатлёвки, наливные полы, гипсокартон, клей, краски, гидроизоляция. Опт и розница в Набережных Челнах.",
           canonical="/catalog/", by_cat=by_cat, active="catalog")
    pages.append(("/catalog/", "0.9", "weekly"))

    # categories + products
    for c in CATEGORIES:
        prods = by_cat[c["slug"]]
        render("category.html", f"catalog/{c['slug']}/index.html",
               page_title=f"{c['title']} | ОНИКС", page_desc=c["desc"],
               canonical=f"/catalog/{c['slug']}/", cat=c, products=prods, active="catalog")
        pages.append((f"/catalog/{c['slug']}/", "0.8", "weekly"))
        for p in prods:
            price_str = f"{p['price']} ₽" if p["price"] else "уточняйте"
            render("product.html", f"catalog/{c['slug']}/{p['slug']}/index.html",
                   page_title=f"{p['name']} — купить в Набережных Челнах | ОНИКС",
                   page_desc=(f"{p['name']} — цена {price_str}. {c['name']} со склада в Набережных Челнах. "
                              f"Быстрая отгрузка, условия для опта. Звоните: {PHONE_MAIN}.")[:300],
                   canonical=f"/catalog/{c['slug']}/{p['slug']}/", p=p, cat=c,
                   related=[x for x in prods if x["uid"] != p["uid"]][:4], active="catalog")
            pages.append((f"/catalog/{c['slug']}/{p['slug']}/", "0.6", "monthly"))

    # static pages
    render("optovikam.html", "optovikam/index.html", page_title="Стройматериалы оптом в Набережных Челнах — условия для оптовиков | ОНИКС",
           page_desc="Специальные условия для строительных компаний, бригад и прорабов: оптовые цены, персональный менеджер, отгрузка со склада в день заказа.",
           canonical="/optovikam/", active="opt")
    pages.append(("/optovikam/", "0.7", "monthly"))
    render("dostavka.html", "dostavka/index.html", page_title="Доставка и оплата — ОНИКС, Набережные Челны",
           page_desc="Доставка строительных материалов по Набережным Челнам и району. Самовывоз со склада: Казанский проспект, 234, стр. 7. Оплата наличными, картой и по счёту.",
           canonical="/dostavka/", active="dostavka")
    pages.append(("/dostavka/", "0.7", "monthly"))
    render("kontakty.html", "kontakty/index.html", page_title="Контакты — ОНИКС, Набережные Челны",
           page_desc=f"Склад и офис: {ADDRESS}. Телефоны: {PHONE_MAIN}, {PHONE_SECOND}. {WORK_HOURS}.",
           canonical="/kontakty/", active="kontakty")
    pages.append(("/kontakty/", "0.6", "monthly"))

    # sitemap + robots
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    today = datetime.date.today().isoformat()
    for url, pr, cf in pages:
        sm.append(f"<url><loc>{BASE_URL}{url}</loc><lastmod>{today}</lastmod>"
                  f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

    print(f"OK: {len(pages)} pages, {len(products)} products")

if __name__ == "__main__":
    main()
