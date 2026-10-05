# -*- coding: utf-8 -*-
"""Generator dema Finezja (sala bankietowa, Kaczki Średnie). Uruchom: python _src/build.py (z dowolnego miejsca)."""
import os, re, json
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://impulseo-pl.github.io/finezja-sala/'
IMG = os.path.join(ROOT, 'img')
TEL1, TEL1H = '665 188 619', '+48665188619'
TEL2, TEL2H = '601 637 397', '+48601637397'
MAIL = 'biuro@finezja.org'
ADR = 'Kaczki Średnie 10c, 62-700 Turek'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Finezja+Sala+bankietowa+Kaczki+%C5%9Arednie+10c+Turek'
EMBED = ('https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d15606.95162728655!2d18.52099567459853!3d51.971505459897536'
         '!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x471b1ef02f4fde83%3A0x8beb946e786d75f9!2sFinezja.%20Sala%20bankietowa-%20sala%20na%20wesele'
         '!5e0!3m2!1spl!2spl!4v1731493576537!5m2!1spl!2spl')
GOOGLE = 'https://maps.google.com/?cid=10082315392986740217'
FB = 'https://www.facebook.com/Finezja.sala.bankietowa'
IG = 'https://www.instagram.com/sala.bankietowa.finezja/'
YT = 'https://www.youtube.com/watch?v=g2kK5KW1re4'

# ---------- obrazy ----------
def variants(name):
    out = []
    for f in os.listdir(IMG):
        m = re.fullmatch(re.escape(name) + r'-(\d+)\.webp', f)
        if m:
            w, h = Image.open(os.path.join(IMG, f)).size
            out.append((w, f, h))
    if not out:
        raise SystemExit('brak obrazu ' + name)
    return sorted(out)

def pic(p, name, alt, sizes='(max-width:860px) 100vw, 50vw', lazy=True, high=False, cls=''):
    v = variants(name)
    src = ([x for x in v if x[0] >= 1100] or [v[-1]])[0]
    srcset = ', '.join(f'{p}img/{f} {w}w' for w, f, h in v)
    a = f'<img src="{p}img/{src[1]}" srcset="{srcset}" sizes="{sizes}" width="{src[0]}" height="{src[2]}" alt="{alt}"'
    if lazy: a += ' loading="lazy" decoding="async"'
    if high: a += ' fetchpriority="high"'
    if cls: a += f' class="{cls}"'
    return a + '>'

def big(p, name):
    return p + 'img/' + variants(name)[-1][1]

# ---------- wspólne ----------
NAV = [('wesele/', 'Wesele'), ('przyjecia/', 'Przyjęcia'), ('catering/', 'Catering'),
       ('bal-andrzejkowy/', 'Bal Andrzejkowy'), ('galeria/', 'Galeria'), ('kontakt/', 'Kontakt')]

ORG = {
    "@type": ["EventVenue", "Restaurant"], "@id": BASE + "#finezja",
    "name": "Finezja – sala weselna i bankietowa",
    "description": "Sala weselna i bankietowa dla 60–160 gości w Kaczkach Średnich, 4 km od Turku. Własna kuchnia, catering, noclegi, bezpłatny parking. Od 2010 roku.",
    "url": BASE, "image": BASE + "img/og.jpg", "telephone": TEL1H, "email": MAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "Kaczki Średnie 10c", "postalCode": "62-700",
                "addressLocality": "Turek", "addressRegion": "wielkopolskie", "addressCountry": "PL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 51.9715, "longitude": 18.5210},
    "maximumAttendeeCapacity": 160, "servesCuisine": "polska", "priceRange": "330–380 zł/os. (menu weselne 2026)",
    "vatID": "7391718282",
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "10:00", "closes": "13:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "09:00", "closes": "13:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday", "Sunday"], "opens": "09:00", "closes": "21:00"}],
    "sameAs": [FB, IG],
    "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True}
                       for n in ["Bezpłatny parking", "Klimatyzacja", "Noclegi", "Własna kuchnia", "Fotobudka", "Kamera 360"]],
}

def head(p, path, title, desc, ld=None, preload=None, cls=''):
    lds = [dict({"@context": "https://schema.org"}, **ORG)] + (ld or [])
    ldh = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    pre = ''
    if preload:
        v = variants(preload)
        pre = f'<link rel="preload" as="image" imagesrcset="{", ".join(f"{p}img/{f} {w}w" for w, f, h in v)}" imagesizes="(max-width:860px) 100vw, 45vw">'
    return f'''<!doctype html>
<html lang="pl" class="{cls}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}img/og.jpg">
<meta name="theme-color" content="#3d1620">
<meta name="view-transition" content="same-origin">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add('js');try{{if(!sessionStorage.getItem('fz_intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{document.documentElement.classList.add('intro');sessionStorage.setItem('fz_intro','1')}}}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
{pre}
<link rel="stylesheet" href="{p}assets/styles.css">
{ldh}
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
<div class="intro-screen" aria-hidden="true"><div class="mono"><i></i><b>F</b><i></i></div><span class="mono-word">Finezja</span><span class="mono-sub">Turek / Kaczki Średnie</span></div>
'''

def logo(p, sub='sala weselna i bankietowa'):
    return f'<a class="brand" href="{p}" aria-label="Finezja – strona główna"><span class="brand-f" aria-hidden="true"><i></i><b>F</b><i></i></span><span class="brand-t"><b>Finezja</b><span>{sub}</span></span></a>'

def header(p, cur, dark=True):
    links = ''.join(f'<a href="{p}{u}"{" aria-current=page" if u == cur else ""}>{n}</a>' for u, n in NAV)
    big = ''.join(f'<a href="{p}{u}" style="--i:{i}">{n}</a>' for i, (u, n) in enumerate([('', 'Strona główna')] + NAV))
    return f'''<header class="top{' on-dark' if dark else ''}"><div class="wrap">
{logo(p)}
<nav class="nav" aria-label="Menu główne">{links}</nav>
<a class="top-cta" href="{p}kontakt/#zapytanie">Zapytaj o termin</a>
<button class="burger" aria-label="Otwórz menu" aria-expanded="false" aria-controls="menu"><span>Menu</span><i></i></button>
</div></header>
<div class="menu" id="menu" aria-hidden="true"><div class="menu-in">
<nav aria-label="Menu">{big}</nav>
<div class="menu-side"><p><a href="tel:{TEL1H}">{TEL1}</a><br><a href="tel:{TEL2H}">{TEL2}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p><p>{ADR}</p></div>
</div></div>
<main id="tresc">
'''

def footer(p):
    return f'''</main>
<footer class="foot"><div class="wrap">
<div class="foot-top">
<p class="foot-say">Zobaczcie salę na żywo – <a href="{p}kontakt/#zapytanie">umówcie wizytę</a> albo zadzwońcie: <a href="tel:{TEL1H}">{TEL1}</a></p>
</div>
<div class="cols">
<div>{logo(p, 'Turek / Kaczki Średnie')}
<p style="margin-top:22px">{ADR}<br>4 km od centrum Turku, woj. wielkopolskie</p>
<p><a class="u" href="{MAPS}" target="_blank" rel="noopener">Pokaż na mapie Google</a></p></div>
<div><h4>Kontakt</h4><ul>
<li><a href="tel:{TEL1H}">{TEL1}</a></li><li><a href="tel:{TEL2H}">{TEL2}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li>
<li style="margin-top:12px"><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{YT}" target="_blank" rel="noopener">YouTube</a></li></ul></div>
<div><h4>Biuro sali</h4><ul><li>Poniedziałek 10:00–13:00</li><li>Czwartek 9:00–13:00</li><li>Piątek–niedziela 9:00–21:00</li><li class="dim">Wizyty w sali – po umówieniu, także w weekend</li></ul></div>
<div><h4>Oferta</h4><ul>{''.join(f'<li><a href="{p}{u}">{n}</a></li>' for u, n in NAV[:5])}<li><a href="{p}przyjecia/#konsolacja">Konsolacje</a></li></ul></div>
</div>
<div class="kpo"><img src="{p}img/kpo.webp" width="340" height="55" alt="Fundusze Europejskie, Rzeczpospolita Polska, Unia Europejska – NextGenerationEU" loading="lazy">
<p>F.U. Finezja realizuje projekt dofinansowany ze środków Krajowego Planu Odbudowy, inwestycja A1.2.1 „Inwestycje dla przedsiębiorstw w produkty, usługi i kompetencje pracowników oraz kadry związane z dywersyfikacją działalności”. Przedsięwzięcie: „Dywersyfikacja usług FINEZJI poprzez zieloną transformację, zakup środków trwałych, cyfryzację oraz doradztwo i szkolenia w województwie wielkopolskim”. Kwota wsparcia: 485 235 zł.</p></div>
<div class="legal"><span>© 2026 Finezja Sala Bankietowa · NIP 739 171 82 82</span><span>Projekt demonstracyjny strony – Impulseo</span></div>
</div></footer>
<nav class="callbar" aria-label="Szybki kontakt"><a href="tel:{TEL1H}">Zadzwoń</a><a href="{p}kontakt/#zapytanie">Zapytaj o termin</a></nav>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="{p}assets/app.js" defer></script>
<script src="{p}assets/licznik.js" defer></script>
</body></html>
'''

def phead(p, img, crumb, h1, lead, kicker='', actions=''):
    return f'''<section class="phead"><div class="wrap phead-in">
<div class="ph-txt"><div class="crumbs"><a href="{p}">Finezja</a><span>/</span>{crumb}</div>
{f'<p class="kicker">{kicker}</p>' if kicker else ''}<h1 data-split>{h1}</h1><p class="lead">{lead}</p>{actions}</div>
<figure class="arch ph-img">{pic(p, img, '', sizes='(max-width:860px) 100vw, 42vw', lazy=False, high=True)}</figure>
</div></section>
'''

def faq(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="faq-a"><div><p>{a}</p></div></div></details>' for q, a in items) + '</div>'

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in items]}

def contact_band(p, h='Najlepiej zobaczyć salę na miejscu', t='Umów się na wizytę – pokażemy salę, kuchnię, pokoje i parking, a przy okazji opowiemy, jak wyglądają przyjęcia u nas. Spotkania także w weekend.'):
    return f'''<section class="cband"><div class="wrap contact-grid">
<div><p class="kicker">Rezerwacje i wizyty</p><h2>{h}</h2><p>{t}</p>
<dl class="cdl"><dt>Telefon</dt><dd><a href="tel:{TEL1H}">{TEL1}</a> · <a href="tel:{TEL2H}">{TEL2}</a></dd>
<dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd><dt>Adres</dt><dd>{ADR}</dd></dl>
<div class="actions"><a class="btn light" href="{p}kontakt/#zapytanie">Zapytaj o wolny termin</a><a class="btn line-light" href="tel:{TEL1H}">Zadzwoń</a></div></div>
<div class="map-wrap"><iframe class="map" src="{EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa dojazdu do sali Finezja"></iframe></div>
</div></section>
'''

REVIEWS = [
    ('Organizowałam tu wesele syna, ponieważ urzekł mnie klimat tego miejsca i fantastyczna obsługa. Największym potwierdzeniem doskonałego wyboru były zachwyty gości nad podanymi daniami.', 'Dominika K.', 'wesele'),
    ('Wesele w Finezji było dla nas niezapomnianym przeżyciem. Sala była pięknie oświetlona, a aranżacje kwiatowe dodawały uroku całemu miejscu. Jedzenie było po prostu przepyszne.', 'Jolanta G.', 'wesele'),
    ('Robiliśmy u Państwa niejedną imprezę i jak zawsze jesteśmy bardzo zadowoleni. Jedzenie przepyszne, dużo i te wasze devolaje. Z cateringu również jesteśmy zadowoleni – przede wszystkim ciepły.', 'Wioletta W.', 'przyjęcia i catering'),
    ('Pozytywna opinia z osiemnastki mojej córki. Jedzenie było przepyszne, świeże, a panie w obsłudze i kuchni przemiłe. To nie była moja pierwsza impreza na tej sali i nic mnie nie zawiodło.', 'Nina K.', 'osiemnastka'),
    ('Zamówiony udziec z dodatkami dla 20 osób plus kilka sałatek na zimno – pierwsza klasa wykonanie, bardzo smaczne, każdy gość zadowolony. Na pewno powtórzę zamówienie.', 'Andrej K.', 'catering'),
    ('Catering na czas, wszystko ciepłe i pyszne. Polecam!', 'Marcin T.', 'catering'),
]

def reviews(sel):
    q = ''.join(f'<figure class="rev{" on" if j == 0 else ""}"><blockquote>{t}</blockquote><figcaption>{n} <span>· {k} · opinia z Google</span></figcaption></figure>' for j, (t, n, k) in enumerate(REVIEWS[i] for i in sel))
    return f'''<section class="revs"><div class="wrap revs-in">
<div class="revs-side"><p class="kicker">Opinie gości</p><h2>Co piszą po przyjęciu</h2>
<p>Ocena „doskonała” na podstawie 300 opinii w Google.</p><p><a class="u" href="{GOOGLE}" target="_blank" rel="noopener">Wszystkie opinie w Google</a></p></div>
<div class="revs-stage" data-revs>{q}
<div class="revs-nav"><button type="button" class="rv-prev" aria-label="Poprzednia opinia">←</button><span class="revs-count">1 / {len(sel)}</span><button type="button" class="rv-next" aria-label="Następna opinia">→</button></div></div>
</div></section>
'''

def write(path, html):
    fp = os.path.join(ROOT, path, 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    hd, body = html.split('</head>', 1)
    body = re.sub(r'>([^<]+)<', lambda t: '>' + re.sub(r'(?<=[\s(])(w|z|i|o|u|a|do|na|od|po|za|we|ze|ok\.) ', lambda m: m.group(1) + '&nbsp;', t.group(1)) + '<', body)  # sierotki tylko w tekście
    html = hd + '</head>' + body
    open(fp, 'w', encoding='utf-8', newline='\n').write(html)

# =====================================================================
#  STRONA GŁÓWNA
# =====================================================================
def home():
    p = ''
    occ = [
        ('wesele/', 'dek-roze', 'Wesele', 'Od 60 do 160 gości, jedno wesele dziennie, menu z własnej kuchni i koordynator od podpisania umowy do ostatniego tańca.'),
        ('przyjecia/#osiemnastka', 'urodziny-scianka', 'Osiemnastka i urodziny', 'Sala na wyłączność, parkiet, DJ, tort z fontannami iskier. Roczek, 18-tka, 30, 40, 50, 60 i 70 lat.'),
        ('przyjecia/#komunia', 'chrzest-neon', 'Komunia i chrzciny', 'Rodzinne przyjęcie w jasnej sali, menu dla dorosłych i dzieci, dekoracje dopasowane do uroczystości.'),
        ('przyjecia/#firmy', 'sala-okragle', 'Spotkania firmowe', 'Bankiety, wigilie firmowe, szkolenia i integracje – z fakturą, obsługą i menu ustalonym pod grupę.'),
        ('przyjecia/#konsolacja', 'kawa', 'Konsolacja', 'Spokojne miejsce na spotkanie po pogrzebie. Obiad, kawa, ciasto – ustalamy wszystko w jednej rozmowie.'),
        ('catering/', 'slodki-babeczki', 'Catering na wynos', 'Dania z tej samej kuchni co na weselach – od 5 do 100 osób. Menu 2026 z cenami i zamówieniem online.'),
    ]
    occ_html = ''.join(f'<a class="occ" href="{p}{u}"><figure>{pic(p, im, "", sizes="(max-width:860px) 80vw, 30vw")}</figure><h3>{h}</h3><p>{t}</p><span class="u">Zobacz</span></a>' for u, im, h, t in occ)
    slides = [('dek-roze', 'Kwiaty za stołem Pary Młodej w sali Finezja'), ('sala-zyrandole', 'Wnętrze sali z żyrandolami i lustrzanym sufitem'),
              ('dek-mlodzi', 'Stół Pary Młodej ze świecami'), ('slodki-stol', 'Słodki stół z ciastami z naszej kuchni')]
    sl = ''.join(pic(p, n, a, sizes='(max-width:860px) 100vw, 46vw', lazy=i > 0, high=i == 0, cls='on' if i == 0 else '') for i, (n, a) in enumerate(slides))
    ld = [{"@context": "https://schema.org", "@type": "Event", "name": "Bal Andrzejkowy 2026 w Finezji",
           "startDate": "2026-11-21T19:00:00+01:00", "endDate": "2026-11-22T04:00:00+01:00",
           "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
           "location": {"@id": BASE + "#finezja"}, "url": BASE + "bal-andrzejkowy/",
           "offers": {"@type": "Offer", "price": "220", "priceCurrency": "PLN", "url": BASE + "bal-andrzejkowy/"}}]
    h = head(p, '', 'Finezja – sala weselna i bankietowa pod Turkiem | Kaczki Średnie',
             'Sala weselna i bankietowa dla 60–160 gości, 4 km od Turku. Od 2010 roku ponad 350 wesel. Własna kuchnia, noclegi, bezpłatny parking, catering.',
             ld=ld, preload='dek-roze')
    h += header(p, '')
    h += f'''<section class="hero"><div class="wrap hero-in">
<div class="hero-txt">
<p class="kicker">Kaczki Średnie · 4 km od Turku</p>
<h1 data-split><span class="h1-small">Sala weselna i bankietowa</span> <em>Finezja</em></h1>
<p class="lead">Wesela, osiemnastki, komunie i przyjęcia firmowe od 2010 roku. Jedno przyjęcie dziennie, kuchnia na miejscu, zabawa do rana z dala od zabudowań.</p>
<div class="actions"><a class="btn light" href="kontakt/#zapytanie">Zapytaj o wolny termin</a><a class="btn line-light" href="tel:{TEL1H}">{TEL1}</a></div>
</div>
<figure class="arch hero-img" data-slides>{sl}</figure>
</div>
<div class="wrap"><p class="hero-facts">Od 2010 roku<span></span>ponad 350 wesel<span></span>60–160 gości<span></span>ok. 48 miejsc noclegowych<span></span>300 opinii w Google, ocena „doskonała”</p></div>
</section>

<section class="lede-sec"><div class="wrap">
<p class="lede" data-words>Jasne wnętrze z wysokimi oknami, kryształowymi żyrandolami i lustrzanym sufitem. Kuchnia, która gotuje na miejscu. Cisza wokół sali, więc zabawa trwa do rana. Każde przyjęcie przygotowujemy od nowa – menu, ustawienie stołów, dekoracje i przebieg wieczoru.</p>
</div></section>

<section class="pair"><div class="wrap">
<div class="pair-row">
<div class="pair-img"><figure class="tall" data-par="-0.06">{pic(p, 'sala-kwiaty', 'Wnętrze sali Finezja z kwiatami, żyrandolami i lustrzanym sufitem')}</figure>
<figure class="pair-small" data-par="0.12">{pic(p, 'sala-zyrandole', 'Kryształowe żyrandole nad stołami', sizes='22vw')}</figure></div>
<div class="pair-txt"><p class="kicker">Sala</p><h2>Jasne wnętrze, które dopasujemy do Waszego przyjęcia</h2>
<p>Wysokie okna, kryształowe żyrandole, lustrzany sufit z oświetleniem LED i białe pokrowce na krzesłach. Wnętrze jest spokojnym tłem – tak samo dobrze wygląda wesele w stylu glamour, boho, jak i elegancka komunia.</p>
<p>Układ stołów, dekoracje i światło ustalamy pod okazję i liczbę gości. Sala jest klimatyzowana, ma wentylację mechaniczną, osobne wejście dla gości i miejsce na słodki stół, drink bar czy fotobudkę.</p>
<p><a class="u" href="galeria/">Zobacz galerię sali</a></p></div>
</div>
<div class="pair-row flip">
<div class="pair-img"><figure class="tall" data-par="-0.05">{pic(p, 'slodki-stol', 'Słodki stół z ciastami i deserami z kuchni Finezji')}</figure>
<figure class="pair-small" data-par="0.1">{pic(p, 'slodki-babeczki', 'Babeczki i desery z naszej kuchni', sizes='22vw')}</figure></div>
<div class="pair-txt"><p class="kicker">Kuchnia</p><h2>Gotujemy na miejscu, nie wozimy cateringu z zewnątrz</h2>
<p>Każde danie powstaje w naszej kuchni – ze świeżych, w większości lokalnych składników. Torty na śmietanie i lodowe, ciasta domowe i monoporcje na słodki stół też robimy sami, więc tort nie jedzie w upale.</p>
<p>Menu układamy razem z Wami: klasyka kuchni polskiej dla rodziców i dziadków obok nowocześniejszych dań dla młodszych gości. Dania wegetariańskie, wegańskie, bezglutenowe i bez laktozy przygotowujemy jako pełnowartościowe posiłki.</p>
<p><a class="u" href="catering/">Menu cateringowe 2026</a></p></div>
</div>
</div></section>

<section class="hs" data-hs><div class="hs-pin">
<div class="wrap hs-head"><div><p class="kicker">Oferta</p><h2>Na jaką okazję szukasz sali?</h2></div><p>Każde przyjęcie przygotowujemy od nowa: menu, ustawienie stołów, dekoracje i przebieg wieczoru.</p></div>
<div class="hs-track">{occ_html}</div>
<div class="wrap"><div class="hs-bar"><i></i></div></div>
</div></section>

<section class="night bal-home"><div class="wrap bal-grid">
<div class="bal-txt"><p class="kicker">Najbliższe wydarzenie</p><h2>Bal Andrzejkowy 2026</h2>
<p class="bal-date">Sobota, 21 listopada<span data-countdown="2026-11-21"></span></p>
<p>Ostatnia wielka zabawa przed świętami. Kolacja serwowana do stołu, bufet przez całą noc, drugie ciepłe danie po północy i DJ-konferansjer do czwartej rano. Przyjeżdżają pary, grupy znajomych i całe zespoły z pracy.</p>
<dl class="bal-dl"><dt>Start i koniec</dt><dd>19:00 – 4:00</dd><dt>Bilet</dt><dd>od 220 zł za osobę, wszystko w cenie</dd></dl>
<div class="actions"><a class="btn light" href="bal-andrzejkowy/">Program i rezerwacja</a><a class="btn line-light" href="tel:{TEL1H}">Rezerwuj: {TEL1}</a></div></div>
<figure class="bal-img" data-par="-0.05">{pic(p, 'bal-parkiet', 'Sala Finezja przygotowana na bal – parkiet, światła i ścianka')}<figcaption>Sala przed Balem Andrzejkowym 2024</figcaption></figure>
</div></section>

<section class="vx" data-vx><div class="vx-pin">
<div class="vx-frame"><video src="media/wieczor.mp4" poster="img/wieczor-1280.webp" muted loop playsinline preload="none" aria-label="Budynek sali Finezja wieczorem – podświetlone wejście i napis LOVE"></video></div>
<div class="wrap vx-txt"><p class="kicker">Dojazd i noclegi</p><h2>Cisza wokół sali, Turek kilka minut samochodem</h2></div>
</div></section>

<section class="paper"><div class="wrap two dojazd">
<div><p>Sala stoi z dala od zabudowań, więc zabawa trwa do rana bez ściszania muzyki. Przed budynkiem jest bezpłatny parking, a wokół zieleń – miejsce na zdjęcia i przerwę na świeżym powietrzu.</p>
<p><a class="u" href="wesele/#noclegi">Szczegóły noclegów</a> &nbsp; <a class="u" href="{MAPS}" target="_blank" rel="noopener">Wyznacz trasę</a></p></div>
<table class="spec"><tr><th>Turek</th><td>4 km, ok. 10 minut do kościołów i USC</td></tr>
<tr><th>Konin, Koło</th><td>dojazd drogą DK92 bez przesiadek</td></tr>
<tr><th>Kalisz</th><td>niecała godzina samochodem</td></tr>
<tr><th>Noclegi</th><td>ok. 48 miejsc: w sali, w Barze Kaczki Średnie za ścianą i w Lawendowej Willi</td></tr></table>
</div></section>
'''
    h += reviews([0, 2, 3, 1])
    h += f'''<section class="paper"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Jak zacząć</p><h2>Od telefonu do przyjęcia</h2></div><p>Sześć kroków – od pierwszego pytania o termin do ostatniego tańca.</p></div>
<ol class="steps">
<li><b>Dzwonisz albo piszesz</b><span>Podajesz okazję, datę i przybliżoną liczbę gości. Sprawdzamy, czy termin jest wolny.</span></li>
<li><b>Oglądasz salę</b><span>Umawiamy wizytę – także w weekend. Pokazujemy salę, kuchnię, pokoje i parking.</span></li>
<li><b>Rezerwujesz termin</b><span>Podpisujemy umowę, która opisuje wszystko, co zawiera cena. Przy weselu zaliczka 1000 zł blokuje datę.</span></li>
<li><b>Ustalamy menu i przebieg</b><span>Wybieracie dania, dekoracje i harmonogram. Przy większych przyjęciach – degustacja.</span></li>
<li><b>Potwierdzamy szczegóły</b><span>Liczba gości, diety, rozsadzenie, plan wieczoru z DJ-em i fotografem.</span></li>
<li><b>Świętujecie</b><span>Sala jest gotowa przed przyjazdem gości. Obsługa, sprzątanie i demontaż są po naszej stronie.</span></li>
</ol></div></section>
'''
    h += contact_band(p)
    h += footer(p)
    write('', h)

# =====================================================================
#  WESELE
# =====================================================================
WFAQ = [
    ('Ilu gości pomieści sala weselna Finezja?', 'Od 60 do 160 osób przy stołach, z zachowaniem dużego parkietu. Przy mniejszych weselach salę aranżujemy tak, żeby nie wydawała się pusta.'),
    ('Ile kosztuje wesele w Finezji?', 'Menu weselne w sezonie 2026 kosztuje od 330 do 380 zł za osobę. W cenie: obiad serwowany, zimne przekąski, ciepłe kolacje, słodki stół, napoje bezalkoholowe, obsługa kelnerska, podstawowa dekoracja stołów i koordynator. Dla wesela na 100 osób to orientacyjnie 33 000–38 000 zł za pełne menu.'),
    ('Czy można przywieźć własny alkohol?', 'Tak – tak wygląda u nas standard. Nie pobieramy opłaty korkowej. Obsługa schłodzi alkohol i zadba o uzupełnianie na stołach.'),
    ('Czy sala organizuje tylko jedno wesele dziennie?', 'Tak. W dniu Waszego ślubu cała sala, kuchnia i obsługa pracują tylko dla Was.'),
    ('Do której można się bawić?', 'Do rana – sala jest oddalona od zabudowań, więc nie ma ograniczeń hałasu.'),
    ('Jak wcześnie trzeba rezerwować termin?', 'Soboty w sezonie maj–wrzesień rozchodzą się zwykle 12–18 miesięcy wcześniej. Piątki i terminy poza sezonem są dostępne z krótszym wyprzedzeniem i często w niższej cenie.'),
    ('Czy jest degustacja menu?', 'Tak, po rezerwacji terminu zapraszamy Parę Młodą na degustację wybranych dań.'),
    ('Czy sala robi tort weselny?', 'Tak. Torty na śmietanie i lodowe przygotowujemy we własnej kuchni, w wybranym kształcie i dekoracji. Na słodki stół robimy także deserki i monoporcje. Jeśli wolicie cukiernię, polecamy Krainę Słodkości (603 615 263).'),
    ('Czy w sali jest fotobudka i kamera 360?', 'Tak, oba urządzenia są nasze i obsługuje je nasza ekipa. Fotobudka drukuje zdjęcia na miejscu, kamera 360 nagrywa filmiki w zwolnionym tempie, które goście od razu dostają na telefon. Cenę podajemy przy ustalaniu menu.'),
    ('Czy można przyjść z własnym DJ-em, fotografem lub dekoratorem?', 'Tak, bez żadnych opłat. Możecie też skorzystać z wykonawców, którzy regularnie pracują w Finezji – lista z telefonami jest wyżej na tej stronie.'),
    ('Czy można zorganizować poprawiny?', 'Tak – w sali lub w plenerze następnego dnia, z osobnym menu.'),
    ('Na ile przed weselem podajemy diety gości?', 'Liczbę gości z dietą wegetariańską, wegańską, bezglutenową lub bez laktozy wystarczy podać 14 dni przed weselem.'),
]

def partners_table(rows):
    return '<table class="list"><thead><tr><th>Wykonawca</th><th>Telefon</th></tr></thead><tbody>' + ''.join(
        f'<tr><td>{n}</td><td><a href="tel:+48{t.replace(" ", "")}">{t}</a></td></tr>' for n, t in rows) + '</tbody></table>'

def wesele():
    p = '../'
    h = head(p, 'wesele/', 'Sala weselna pod Turkiem – wesele w Finezji, 60–160 gości | Menu 2026',
             'Wesele w sali Finezja, 4 km od Turku: 60–160 gości, menu 330–380 zł/os. w 2026, alkohol własny bez korkowego, noclegi, fotobudka i kamera 360. Od 2010 roku ponad 350 wesel.',
             ld=[faq_ld(WFAQ)], preload='stol-mlodych')
    h += header(p, 'wesele/')
    h += phead(p, 'stol-mlodych', 'Wesele', 'Wesele w Finezji', 'Od 2010 roku zorganizowaliśmy ponad 350 wesel. Wiemy, jak rozłożyć ciepłe kolacje, kiedy zaplanować tort, żeby nie kolidował z blokiem tanecznym, i gdzie ustawić fotografa, żeby pierwszy taniec wyszedł na zdjęciach.',
               kicker='Sala weselna · Kaczki Średnie pod Turkiem',
               actions='<div class="actions"><a class="btn light" href="#kalkulator">Policz koszt menu</a><a class="btn line-light" href="../kontakt/?okazja=wesele#zapytanie">Zapytaj o termin</a></div>')
    h += f'''<section><div class="wrap two">
<div><p class="kicker">W skrócie</p><h2>Sala Finezja w liczbach</h2><p class="muted">Wszystko, o co pary pytają przy pierwszym telefonie – w jednej tabeli.</p>
<figure style="margin:28px 0 0">{pic(p, 'dek-luk', 'Stół Pary Młodej pod złotym łukiem z kwiatami')}</figure></div>
<table class="spec">
<tr><th>Doświadczenie</th><td>od 2010 roku, ponad 350 wesel</td></tr>
<tr><th>Liczba gości</th><td>od 60 do 160 osób przy stołach</td></tr>
<tr><th>Menu weselne 2026</th><td>330–380 zł za osobę</td></tr>
<tr><th>Alkohol</th><td>własny, bez opłaty korkowej</td></tr>
<tr><th>Rezerwacja</th><td>zaliczka 1000 zł blokuje datę</td></tr>
<tr><th>Kuchnia</th><td>własna, gotujemy na miejscu</td></tr>
<tr><th>Tort i desery</th><td>z własnej kuchni: na śmietanie, lodowe, monoporcje</td></tr>
<tr><th>Atrakcje na miejscu</th><td>własna fotobudka i kamera 360</td></tr>
<tr><th>Zabawa</th><td>do rana – bez ograniczeń hałasu</td></tr>
<tr><th>Parking</th><td>bezpłatny, przy sali</td></tr>
<tr><th>Noclegi</th><td>ok. 48 miejsc w Kaczkach Średnich – <a href="#noclegi">szczegóły</a></td></tr>
<tr><th>Poprawiny</th><td>w sali lub w plenerze następnego dnia</td></tr>
<tr><th>Adres</th><td>{ADR}</td></tr>
</table></div></section>

<section class="white"><div class="wrap">
<div class="row">
<div><p class="kicker">Dlaczego pary wybierają Finezję</p><h2>Jedno wesele dziennie</h2>
<p>W dniu Waszego ślubu sala, kuchnia i obsługa pracują tylko dla Was. Nie dzielicie parkingu, kuchni ani parkietu z inną imprezą.</p>
<h3 style="margin-top:1.4em">Koordynacja w cenie</h3>
<p>Od podpisania umowy macie jedną osobę do kontaktu. Pilnuje harmonogramu, ustaleń z DJ-em, florystą i fotografem oraz przebiegu przyjęcia. Obsługa jest na sali od przyjazdu pierwszych gości do wyjścia ostatnich.</p>
<h3 style="margin-top:1.4em">Fotobudka, kamera 360 i tort – u nas</h3>
<p>Zamiast trzech dodatkowych umów z podwykonawcami zamawiacie atrakcje i słodki stół w jednym miejscu. Fotobudka i kamera 360 stoją tak, żeby nie kolidowały z parkietem i stanowiskiem DJ-a.</p></div>
<figure class="tall">{pic(p, 'sala-pion', 'Długie stoły weselne w sali Finezja')}</figure>
</div></div></section>

<section><div class="wrap two">
<div><p class="kicker">Menu weselne</p><h2>Co i jak podajemy</h2>
<p>Menu ustalamy indywidualnie z każdą Parą Młodą. Standardowy przebieg kolacji weselnej w Finezji wygląda tak:</p>
<table class="list" style="margin-top:18px"><tbody>
<tr><td><b>Powitanie</b></td><td>chlebem i solą, toast – lampka szampana lub wina dla wszystkich gości</td></tr>
<tr><td><b>Obiad</b></td><td>serwowany do stołu: zupa i danie główne z kilkoma rodzajami mięs, rybą i opcją wegetariańską, z dodatkami i surówkami</td></tr>
<tr><td><b>Zimne przekąski</b></td><td>deski mięs, sery, sałatki, pasztety, ryby, marynaty – uzupełniane przez całą noc</td></tr>
<tr><td><b>Ciepłe kolacje</b></td><td>kilka dań w ciągu nocy, np. pieczone mięsa, strogonow, żurek, barszcz z pasztecikiem</td></tr>
<tr><td><b>Słodki stół</b></td><td>tort z naszej kuchni, ciasta domowe, desery, owoce, kawa i herbata bez ograniczeń</td></tr>
<tr><td><b>Napoje</b></td><td>woda, soki, napoje gazowane bez limitu; alkohol własny, bez korkowego</td></tr>
</tbody></table>
<p class="muted small" style="margin-top:16px">Dodatki na życzenie: wiejski stół, drink bar z barmanem, fontanna czekoladowa, tort z fontannami iskier, ciężki dym na pierwszy taniec, animator dla dzieci.</p></div>

<div id="kalkulator" style="scroll-margin-top:100px"><div class="calc" id="wcalc">
<p class="kicker">Kalkulator</p><h3>Ile kosztuje menu na Wasze wesele?</h3>
<p class="muted small">Liczymy według cennika sezonu 2026: od 330 do 380 zł za osobę. Różnica między wariantami to liczba ciepłych kolacji, rodzaj mięs i ryb oraz dodatki.</p>
<label class="f" for="w-g" style="margin-top:18px">Liczba gości</label>
<div class="range"><input id="w-g" type="range" min="60" max="160" step="5" value="100"><output for="w-g">100</output></div>
<div class="out"><div><b id="w-min">33 000 zł</b>wariant od 330 zł/os.</div><div><b id="w-max">38 000 zł</b>wariant do 380 zł/os.</div></div>
<p class="small" style="margin-bottom:8px"><b>W każdym wariancie:</b></p>
<ul class="ticks"><li>obiad serwowany</li><li>zimne przekąski całą noc</li><li>ciepłe kolacje</li><li>ciasta, kawa i herbata</li><li>napoje bezalkoholowe</li><li>obsługa kelnerska</li><li>podstawowa dekoracja stołów</li><li>koordynator wesela</li></ul>
<p class="small muted" style="margin-top:14px">Alkohol przywozicie własny – 0 zł korkowego. Wynik to orientacyjny koszt menu, dokładną ofertę przygotujemy po rozmowie.</p>
<div class="actions"><a class="btn" id="w-link" href="../kontakt/?okazja=wesele#zapytanie">Zapytaj o termin i menu</a></div>
</div></div>
</div></section>

<section class="sand"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Krok po kroku</p><h2>Jak wygląda współpraca</h2></div><p>Od pierwszej wizyty do rozliczenia – bez niespodzianek w umowie.</p></div>
<ol class="steps">
<li><b>Oglądacie salę</b><span>Umawiamy spotkanie, także w weekend. Pokazujemy salę, kuchnię, plener, pokoje i parking.</span></li>
<li><b>Rezerwujecie termin</b><span>Zaliczka 1000 zł blokuje datę. Umowa opisuje wszystko, co zawiera cena.</span></li>
<li><b>Ustalamy menu i harmonogram</b><span>Zwykle 3–6 miesięcy przed ślubem. Degustacja wybranych dań.</span></li>
<li><b>Potwierdzamy szczegóły</b><span>Dwa tygodnie przed weselem: liczba gości, rozsadzenie, diety, plan dnia z DJ-em i fotografem.</span></li>
<li><b>Dzień wesela</b><span>Sala udekorowana i gotowa przed przyjazdem gości. Koordynator czuwa nad przebiegiem, Wy się bawicie.</span></li>
<li><b>Poprawiny i rozliczenie</b><span>Opcjonalne poprawiny na miejscu. Rozliczenie końcowe następnego dnia po weselu.</span></li>
</ol></div></section>

<section><div class="wrap">
<div class="strip">
<a href="{big(p, 'dek-roze')}" data-lb data-alt="Dekoracja kwiatowa za stołem Pary Młodej">{pic(p, 'dek-roze', 'Dekoracja kwiatowa za stołem Pary Młodej', sizes='(max-width:760px) 100vw, 50vw')}</a>
<a href="{big(p, 'nakrycie')}" data-lb data-alt="Nakrycia na stołach weselnych">{pic(p, 'nakrycie', 'Nakrycia na stołach weselnych', sizes='25vw')}</a>
<a href="{big(p, 'dek-milosc')}" data-lb data-alt="Podświetlany napis Miłość na ściance">{pic(p, 'dek-milosc', 'Podświetlany napis Miłość na ściance', sizes='25vw')}</a>
<a href="{big(p, 'slodki-regal')}" data-lb data-alt="Słodki stół z deserami z naszej kuchni">{pic(p, 'slodki-regal', 'Słodki stół z deserami z naszej kuchni', sizes='25vw')}</a>
<a href="{big(p, 'love')}" data-lb data-alt="Napis LOVE w ogrodzie przy sali">{pic(p, 'love', 'Napis LOVE w ogrodzie przy sali', sizes='25vw')}</a>
</div>
<p style="margin-top:18px"><a class="link" href="../galeria/">Cała galeria sali</a></p>
</div></section>

<section class="white"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Partnerzy</p><h2>Sprawdzeni wykonawcy, którzy znają salę</h2></div>
<p>Grali, dekorowali i fotografowali w Finezji wielokrotnie – znają akustykę, wymiary sali i nasz harmonogram podawania dań. Terminy i ceny ustalacie bezpośrednio z nimi.</p></div>
<div class="three">
<div><h3>DJ-e weselni</h3>{partners_table([('Jacek Kujawa', '888 548 650'), ('Klaudiusz', '537 718 851'), ('Maciej Dygas', '785 961 525'), ('Mariusz Kominiarczyk', '693 969 367')])}
<p class="small muted" style="margin-top:12px">W sezonie soboty u dobrych DJ-ów rozchodzą się równie szybko jak terminy sal – warto zadzwonić zaraz po rezerwacji.</p></div>
<div><h3>Floryści i dekoratorzy</h3>{partners_table([('Zakręcona', '665 073 452'), ('Amor', '603 107 092'), ('Czarnek', '798 980 534'), ('Joanna', '691 074 619'), ('Balwit', '504 121 509'), ('Mateusz Adamiak', '783 298 205')])}</div>
<div><h3>Fotografowie</h3>{partners_table([('Natalia Krauze', '693 233 022'), ('Darek Kowalski', '606 374 408'), ('Natalia Okoń', '505 947 401'), ('Kuźnia Kadru', '603 448 740')])}
<h3 style="margin-top:28px">Pozostali</h3>{partners_table([('Kraina Słodkości – cukiernia', '603 615 263'), ('Wesoły Duecik – animatorzy dla dzieci', '781 066 273'), ('Barman – drink bar', '697 217 044')])}</div>
</div>
<p class="muted" style="margin-top:28px">Możecie też przyjechać z własną ekipą – DJ-em, zespołem, fotografem, dekoratorem czy barmanem. Nie pobieramy za to żadnych opłat.</p>
</div></section>

<section id="noclegi" style="scroll-margin-top:80px"><div class="wrap">
<div class="row">
<div><p class="kicker">Noclegi</p><h2>Goście z daleka nie muszą wracać w nocy</h2>
<p>W Kaczkach Średnich, kilka minut pieszo od sali, jest łącznie około 48 miejsc noclegowych. Pokoje w Finezji zwykle rezerwuje Para Młoda i najbliższa rodzina, pozostałych gości warto skierować do sąsiednich obiektów. Większe grupy nocują też w hotelach w Turku, 4 km od sali.</p>
<div class="tbl-scroll"><table class="list"><thead><tr><th>Obiekt</th><th>Miejsca</th><th>Gdzie</th><th>Telefon</th></tr></thead><tbody>
<tr><td>Sala Finezja</td><td>8 miejsc</td><td>na miejscu</td><td><a href="tel:{TEL1H}">{TEL1}</a></td></tr>
<tr><td>Bar Kaczki Średnie</td><td>4 pokoje</td><td>za ścianą</td><td><a href="tel:+48607254797">607 254 797</a></td></tr>
<tr><td>Lawendowa Willa</td><td>15 pokoi</td><td>ok. 700 m</td><td><a href="tel:+48786226322">786 226 322</a></td></tr>
</tbody></table></div>
<p class="small muted" style="margin-top:14px">Przy potwierdzaniu szczegółów podpowiemy, jak rozdzielić miejsca. Na życzenie organizujemy też transport dla gości.</p></div>
<figure>{pic(p, 'budynek-dzien', 'Budynek sali Finezja w Kaczkach Średnich')}</figure>
</div></div></section>

<section class="sand"><div class="wrap narrow">
<p class="kicker">Pytania</p><h2>Najczęściej pytacie o</h2>
{faq(WFAQ)}
</div></section>
'''
    h += reviews([0, 1, 2])
    h += contact_band(p, 'Umówcie się na obejrzenie sali', 'Pokażemy salę, plener, kuchnię i pokoje, a przy okazji opowiemy, czego nauczyło nas ponad 350 wesel.')
    h += footer(p)
    write('wesele', h)

# =====================================================================
#  PRZYJĘCIA
# =====================================================================
def przyjecia():
    p = '../'
    q18 = [
        ('Ile kosztuje osiemnastka w Finezji?', 'Cena zależy od liczby gości, menu i atrakcji. Przygotowujemy indywidualną wycenę – po kontakcie ofertę dostaniesz w ciągu 24 godzin.'),
        ('Ile osób pomieści sala?', 'Komfortowo do 150 gości przy osiemnastce z parkietem. Organizujemy też mniejsze, kameralne przyjęcia.'),
        ('Czy można przynieść własny tort lub alkohol?', 'Tak – szczegóły ustalamy przy rezerwacji.'),
        ('Do której może trwać impreza?', 'Sala stoi z dala od zabudowań mieszkalnych, więc zabawa może trwać do późnych godzin nocnych – godzinę ustalamy przy rezerwacji.'),
    ]
    h = head(p, 'przyjecia/', 'Sala na osiemnastkę, urodziny, komunię i chrzciny – Turek | Finezja',
             'Przyjęcia okolicznościowe pod Turkiem: osiemnastki, okrągłe urodziny, komunie, chrzciny, konsolacje i spotkania firmowe. Sala na wyłączność, własna kuchnia, parking.',
             ld=[faq_ld(q18)], preload='urodziny-scianka')
    h += header(p, 'przyjecia/')
    h += phead(p, 'urodziny-scianka', 'Przyjęcia', 'Przyjęcia rodzinne i firmowe', 'Osiemnastki, okrągłe urodziny, komunie, chrzciny, konsolacje, bankiety firmowe. Salę wynajmujemy na wyłączność – w dniu przyjęcia nikt inny z niej nie korzysta.',
               kicker='Turek i okolice',
               actions='<div class="actions" style="gap:6px 22px"><a class="link" style="color:#e9dcc3" href="#osiemnastka">Osiemnastka</a><a class="link" style="color:#e9dcc3" href="#urodziny">Urodziny</a><a class="link" style="color:#e9dcc3" href="#komunia">Komunia i chrzciny</a><a class="link" style="color:#e9dcc3" href="#firmy">Firmy</a><a class="link" style="color:#e9dcc3" href="#konsolacja">Konsolacja</a></div>')
    h += f'''<section id="osiemnastka" style="scroll-margin-top:80px"><div class="wrap">
<div class="row">
<div><p class="kicker">18. urodziny</p><h2>Osiemnastka, o której będą mówić</h2>
<p>Dwa pokolenia w jednej sali: znajomi jubilata, którzy chcą tańczyć, i rodzina, która czeka na porządny ciepły obiad. Układamy przebieg wieczoru tak, żeby obie strony wyszły zadowolone.</p>
<table class="spec">
<tr><th>Sala</th><td>na wyłączność, do 150 gości, klimatyzowana</td></tr>
<tr><th>Parkiet</th><td>profesjonalne nagłośnienie i światła LED, miejsce dla DJ-a lub zespołu</td></tr>
<tr><th>Ekran i rzutnik</th><td>pokaz zdjęć z dzieciństwa, wideo-życzenia</td></tr>
<tr><th>Efekty</th><td>ciężki dym na pierwszy taniec, fontanny iskier do wjazdu tortu</td></tr>
<tr><th>Słodki stół</th><td>tort i ciasta z naszej kuchni lub własny tort</td></tr>
<tr><th>Diety</th><td>dania wegetariańskie, wegańskie, bezglutenowe – zgłoszenie 7 dni wcześniej</td></tr>
</table></div>
<figure class="tall">{pic(p, 'osiemnastka', 'Ścianka na osiemnastkę z balonami i cyfrą 18')}</figure>
</div>

<div class="two" style="margin-top:clamp(56px,8vw,96px)">
<div><h3>Motyw imprezy – sala jako tło</h3>
<p class="muted">Wystrój Finezji jest neutralny i łatwo go „przebrać”. Przynieś zdjęcia z Pinteresta, ulubione kolory i listę zainteresowań – przełożymy to na aranżację.</p>
<table class="list"><tbody>
<tr><td><b>Glamour</b></td><td>złote balony, cekinowe tła, świece, elegancka kolacja i taneczna druga część</td></tr>
<tr><td><b>Hollywood</b></td><td>czerwony dywan, ścianka jak na premierze, „gwiazdy” z imionami gości</td></tr>
<tr><td><b>Podróże</b></td><td>flagi odwiedzonych krajów, mapy, stoły nazwane miastami</td></tr>
<tr><td><b>Gaming / film</b></td><td>plakaty ulubionych gier i filmów, neony, muzyka w klimacie</td></tr>
<tr><td><b>Boho</b></td><td>suszone kwiaty, pampasy, drewno, lampiony i ciepłe światło</td></tr>
</tbody></table></div>
<div><h3>Forma podania</h3>
<p class="muted">Menu układamy z Tobą – proponujemy 2–3 warianty w różnych cenach, bez sztywnych pakietów.</p>
<table class="list"><thead><tr><th>Forma</th><th>Dla kogo</th><th>Jak to działa</th></tr></thead><tbody>
<tr><td><b>Serwowana</b></td><td>osiemnastka z rodziną</td><td>dania podawane do stołu przez kelnerów</td></tr>
<tr><td><b>Bufet</b></td><td>impreza taneczna ze znajomymi</td><td>goście jedzą, kiedy chcą</td></tr>
<tr><td><b>Mix</b></td><td>najczęstszy wybór</td><td>ciepły obiad do stołu, potem kolejne dania i słodki stół na całą noc</td></tr>
</tbody></table>
<div style="margin-top:28px">{faq(q18)}</div></div>
</div></div></section>

<section id="urodziny" class="white" style="scroll-margin-top:80px"><div class="wrap">
<div class="row flip">
<div><p class="kicker">Roczek, 30, 40, 50, 60, 70 lat</p><h2>Okrągłe urodziny i jubileusze</h2>
<p>Na poważnie i uroczyście albo z przymrużeniem oka – z wystawnym obiadem i tortem albo kolacją z tańcami. Kameralne przyjęcie w gronie najbliższych i większa uroczystość z rozmachem wyglądają u nas inaczej, bo każde ustawiamy od nowa.</p>
<p>Doradzimy w kwestii menu, ustawienia sali i harmonogramu. Przy przyjęciach dla dzieci wydzielimy strefę do zabawy, przy sześćdziesiątce czy siedemdziesiątce – ustawimy stoły tak, żeby dało się swobodnie rozmawiać.</p>
<p>Przy sprzyjającej pogodzie część przyjęcia może odbyć się na zewnątrz.</p>
<div class="actions"><a class="btn ghost" href="../kontakt/?okazja=urodziny#zapytanie">Zapytaj o termin</a></div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<figure style="margin:0">{pic(p, 'urodziny-50', 'Dekoracja na 50. urodziny z podświetlaną cyfrą', sizes='25vw')}</figure>
<figure style="margin:0">{pic(p, 'urodziny-pion', 'Dekoracja urodzinowa z balonami', sizes='25vw')}</figure></div>
</div></div></section>

<section id="komunia" style="scroll-margin-top:80px"><div class="wrap">
<div class="row">
<figure>{pic(p, 'chrzest-balony', 'Dekoracja na chrzest z neonem i balonami')}</figure>
<div><p class="kicker">Komunia święta i chrzciny</p><h2>Rodzinne przyjęcie w jasnej sali</h2>
<p>Pierwsza Komunia i chrzest to dni, w których przy jednym stole siedzą dziadkowie, rodzice i najmłodsi. Przygotowujemy menu dla dorosłych i dla dzieci, układ stołów z miejscem do zabawy i dekoracje dopasowane do uroczystości – od białych kwiatów po podświetlane napisy.</p>
<p>Do kościołów w Turku jest około 10 minut samochodem, a przed salą czeka bezpłatny parking.</p>
<p class="muted small">Na komunie warto rezerwować salę z dużym wyprzedzeniem – majowe niedziele znikają pierwsze.</p>
<div class="actions"><a class="btn ghost" href="../kontakt/?okazja=komunia#zapytanie">Zapytaj o termin komunii</a><a class="btn ghost" href="../kontakt/?okazja=chrzciny#zapytanie">Chrzciny</a></div></div>
</div></div></section>

<section id="firmy" class="sand" style="scroll-margin-top:80px"><div class="wrap">
<div class="row flip">
<div><p class="kicker">Dla firm</p><h2>Bankiety, wigilie firmowe, szkolenia</h2>
<p>Kolacje biznesowe, jubileusze firm, integracje, wigilie pracownicze i szkolenia. Sala z nagłośnieniem, rzutnikiem i klimatyzacją, parking dla wszystkich uczestników, obsługa kelnerska i faktura.</p>
<p>Menu ustalamy pod grupę, z uwzględnieniem diet i alergii. Na Andrzejki możemy przygotować zamknięty bal tylko dla Waszej firmy w innym listopadowym terminie.</p>
<div class="actions"><a class="btn ghost" href="../kontakt/?okazja=firma#zapytanie">Zapytaj o ofertę dla firmy</a></div></div>
<figure>{pic(p, 'sala-okragle', 'Sala z okrągłymi stołami ustawiona na przyjęcie')}</figure>
</div></div></section>

<section id="konsolacja" style="scroll-margin-top:80px"><div class="wrap narrow">
<p class="kicker">Konsolacja</p><h2>Spokojne miejsce na spotkanie po pogrzebie</h2>
<p>Konsolacja to czas, w którym rodzina i bliscy mogą usiąść razem przy posiłku i wspominać zmarłego. Wiemy, że w tych dniach nie ma siły na organizację – ustalimy wszystko w jednej rozmowie telefonicznej: liczbę osób, godzinę, obiad, kawę i ciasto.</p>
<p>Salę przygotujemy tak, żeby było cicho i kameralnie, a obsługa pozostanie dyskretna.</p>
<div class="actions"><a class="btn" href="tel:{TEL1H}">Zadzwoń: {TEL1}</a><a class="btn ghost" href="tel:{TEL2H}">{TEL2}</a></div>
</div></section>

<section class="white"><div class="wrap two">
<div><p class="kicker">Święta</p><h2>Wielkanoc i Wigilia bez gotowania</h2>
<p>Świąteczny obiad w sali w gronie rodziny albo tradycyjne potrawy na wynos – pierogi z kapustą i grzybami, barszcz czerwony z uszkami, smażony karp, kompot z suszu. Catering wigilijny odbierasz 23 grudnia w godzinach 13:00–16:00.</p>
<p class="muted">Świąteczne terminy rozchodzą się szybko – zamówienia warto składać z kilkutygodniowym wyprzedzeniem.</p>
<div class="actions"><a class="btn ghost" href="../catering/">Catering Finezji</a></div></div>
<figure style="margin:0">{pic(p, 'kawa', 'Stół z kawą, herbatą i ciastami w sali Finezja')}</figure>
</div></section>
'''
    h += reviews([3, 2, 0])
    h += contact_band(p)
    h += footer(p)
    write('przyjecia', h)

# =====================================================================
#  CATERING – menu 2026 (z grafiki menu na finezja.org)
# =====================================================================
MENU = [
    ('zupy', 'Zupy', 'cena za litr', 'l', [
        ('Żurek', 24), ('Barszczyk biały', 22), ('Rosół', 18), ('Zupa gulaszowa', 22), ('Strogonow', 54)]),
    ('miesa', 'Mięsa', 'cena za porcję', 'porcja', [
        ('Schab tradycyjny', 13), ('Schab pod pierzynką', 15), ('Kotlet ułański', 15, 'pieczarki i ser'), ('Kotlet schabowy z farszem węgierskim', 15),
        ('Schab zawijany ze szpinakiem i serem', 15), ('Zagłoba', 15, 'ser pleśniowy i brokuł'), ('Dewolaje', 16, 'masło i ser'),
        ('Sznycel drobiowy z ananasem i serem', 14), ('Karkówka pieczona', 13), ('Karkówka zapiekana', 15, 'sos pieczarkowy i ser'),
        ('Karkówka z kapustą', 15), ('Kotlet mielony', 12), ('Bryzol z cebulką', 13), ('Zrazy wieprzowe', 15), ('Szaszłyk wieprzowy', 12),
        ('Schab w sosie musztardowym', 13), ('Polędwica wieprzowa w sosie kurkowym', 19), ('Gołąbki w sosie pomidorowym', 15),
        ('Filet z kurczaka z suszonymi pomidorami', 32, 'w sosie kaparowym'), ('Filet parowany z żurawiną', 32, 'w sosie serowym'),
        ('Nuggetsy z kurczaka', 14), ('Kotlet po parysku', 15, 'z mozzarellą i pomidorami'), ('Żeberka w sosie', 15), ('Noga z kaczki', 26)]),
    ('dodatki', 'Dodatki', 'półmisek 400 g', 'półmisek', [
        ('Ziemniaki z koperkiem', 7), ('Ziemniaki pieczone w ziołach', 15), ('Frytki', 15), ('Kluski śląskie', 15), ('Kopytka', 15),
        ('Marchewka z groszkiem', 10), ('Buraczki na ciepło', 10), ('Pieczarki duszone', 15), ('Surówka z białej kapusty', 10),
        ('Surówka z czerwonej kapusty', 10), ('Surówka z selera i rodzynek', 10), ('Surówka z kapusty pekińskiej', 10), ('Surówka z kiszonej kapusty', 10)]),
    ('przekaski', 'Przekąski', 'cena za zestaw', 'zestaw', [
        ('Przekąski na lustrze', 150, '24 szt.'), ('Rolada szpinakowa z łososiem', 32, '6 szt.'), ('Roladki z tortilli', 30, '6 szt.'),
        ('Pierś z kurczaka w cieście francuskim', 35), ('Pstrąg faszerowany z warzywami', 60), ('Minihamburgery', 36, '6 szt.'),
        ('Wrapy', 35, '6 szt.'), ('Szarpane udko na bagietce', 30, '6 szt.'), ('Rożki naleśnikowe z nadzieniem', 30, '6 szt.'), ('Tacosy', 25, '6 szt.')]),
    ('salatki', 'Sałatki', 'cena za 500 g', '500 g', [
        ('Gyros', 32), ('Jarzynowa', 26), ('Grecka', 27), ('Z tuńczykiem', 25), ('Cezar', 37), ('Brokułowa', 32), ('Śledziowa z burakami', 30)]),
    ('udziec', 'Na większe spotkanie', '', 'szt.', [
        ('Udziec z dodatkami', 350, 'do 15 osób')]),
    ('ciasta', 'Ciasta i torty', '', 'szt.', [
        ('Ciasto domowe – blacha', 130, 'malinowa chmurka, sernik, makosernik, orzechowiec, szarlotka, góra lodowa, 3 bit, popraniec, miodownik, balladyna'),
        ('Tort na śmietanie', 130, 'za 1 kg'), ('Tort lodowy', 150, 'za 1 kg')]),
]

def catering():
    p = '../'
    items = ''
    nav = ''
    n = 0
    for gid, gname, gnote, unit, rows in MENU:
        nav += f'<a href="#{gid}">{gname}</a>'
        items += f'<div class="menu-group" id="{gid}"><h3>{gname}<small>{gnote}</small></h3>'
        for r in rows:
            n += 1
            name, price = r[0], r[1]
            sub = r[2] if len(r) > 2 else ''
            u = unit if not sub or unit not in ('zestaw', 'szt.') else (sub if len(sub) < 12 else unit)
            items += (f'<div class="item" data-id="m{n}" data-n="{name}" data-p="{price}" data-u="{u}">'
                      f'<div class="n">{name}{f"<small>{sub}</small>" if sub else ""}</div><div class="p">{price} zł</div>'
                      f'<div class="qty"><button type="button" data-d="-" aria-label="Mniej: {name}">−</button><span>0</span><button type="button" data-d="+" aria-label="Więcej: {name}">+</button></div></div>')
        items += '</div>'
    items += '<p class="small muted">Deserki na słodki stół – od 9 zł za sztukę, zamówienie telefonicznie.</p>'
    cq = [
        ('Do kiedy trzeba złożyć zamówienie?', 'Zamówienia przyjmujemy do środy. Świąteczne – na Wigilię i Wielkanoc – warto składać z kilkutygodniowym wyprzedzeniem.'),
        ('Czy dowozicie catering?', 'Tak, z dopłatą za dowóz. Do 5 km dowozimy gratis przy zamówieniu od 300 zł. Możesz też odebrać zamówienie osobiście w sali.'),
        ('Dokąd dowozicie?', 'Turek i okolice, m.in. Brudzew, Tuliszków, Dobra, Malanów, Kawęczyn, Przykona, Uniejów, Koło i Konin. Przy większych zamówieniach dowozimy też dalej.'),
        ('Na ile osób przygotujecie catering?', 'Od 5 do 100 osób. Przy większych przyjęciach pomożemy dobrać ilości do liczby gości.'),
        ('Czy uwzględniacie diety?', 'Tak – dania wegetariańskie i bez alergenów przygotujemy po wcześniejszym uzgodnieniu.'),
    ]
    h = head(p, 'catering/', 'Catering Turek – menu 2026 z cenami, dowóz i odbiór | Finezja',
             'Catering z kuchni sali Finezja pod Turkiem: zupy, mięsa, sałatki, przekąski, ciasta i torty. Menu 2026 z cenami, zamówienie online, dowóz do 5 km gratis od 300 zł.',
             ld=[faq_ld(cq)], preload='slodki-babeczki')
    h += header(p, 'catering/')
    h += phead(p, 'slodki-babeczki', 'Catering', 'Catering z kuchni Finezji', 'Te same dania, które podajemy na weselach – na urodziny w domu, spotkanie firmowe albo rodzinny obiad. Od 5 do 100 osób, z dowozem lub odbiorem w sali.',
               kicker='Turek i okolice · menu 2026',
               actions='<div class="actions"><a class="btn light" href="#catering">Złóż zamówienie</a><a class="btn line-light" href="tel:' + TEL1H + '">Zamów telefonicznie</a></div>')
    h += f'''<section class="tight white"><div class="wrap">
<table class="spec"><tr><th>Zamówienia</th><td>przyjmujemy do środy</td></tr>
<tr><th>Odbiór</th><td>własny w sali albo z dowozem (dopłata)</td></tr>
<tr><th>Dowóz gratis</th><td>do 5 km przy zamówieniu od 300 zł</td></tr>
<tr><th>Telefon</th><td><a href="tel:{TEL1H}">{TEL1}</a> · <a href="tel:{TEL2H}">{TEL2}</a></td></tr></table>
</div></section>

<section id="catering" style="scroll-margin-top:76px"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Menu cateringowe 2026</p><h2>Wybierz dania i wyślij zamówienie</h2></div><p>Dodaj pozycje przyciskiem +, a suma policzy się sama. Zamówienie wyślesz SMS-em albo mailem – potwierdzimy je telefonicznie.</p></div>
<div class="cat-layout">
<div><nav class="cat-nav" aria-label="Kategorie menu">{nav}</nav>{items}</div>
<aside class="cart" id="koszyk" aria-live="polite">
<h3>Twoje zamówienie</h3>
<ul id="cart-list"></ul>
<div class="sum"><span>Razem</span><span id="cart-sum">0 zł</span></div>
<p class="note" id="cart-note"></p>
<label class="f">Na kiedy?<input type="date" id="c-date"></label>
<p class="hint small" id="c-hint" style="margin-top:10px"></p>
<label class="f" style="margin-top:12px">Odbiór<select id="c-how"><option>odbiór osobisty w sali</option><option>dowóz</option></select></label>
<button class="btn" type="button" data-send="sms" style="margin-top:16px">Wyślij SMS-em</button>
<button class="btn ghost" type="button" data-send="mail">Wyślij mailem</button>
<p class="small muted" style="margin:12px 0 0">Ceny według menu cateringowego Finezji na 2026 rok.</p>
</aside>
</div></div></section>
<a class="cart-bar" href="#koszyk"><span>Zobacz zamówienie</span><b>0 zł</b></a>

<section class="sand"><div class="wrap two">
<div><p class="kicker">Pytania</p><h2>Zamawianie i dowóz</h2>{faq(cq)}</div>
<figure style="margin:0">{pic(p, 'slodki-okno', 'Ciasta i desery z kuchni Finezji na słodkim stole')}<figcaption>Ciasta i desery z naszej kuchni – te same trafiają na zamówienia cateringowe.</figcaption></figure>
</div></section>
'''
    h += reviews([4, 5, 2])
    h += footer(p)
    write('catering', h)

# =====================================================================
#  BAL ANDRZEJKOWY
# =====================================================================
def bal():
    p = '../'
    bq = [
        ('Ile kosztuje bilet?', 'Od 220 zł za osobę. W cenie: kolacja, bufet, drugie ciepłe danie, napoje bezalkoholowe, DJ i program wieczoru.'),
        ('Czy można przyjść samemu lub w nieparzystej grupie?', 'Tak. Dosadzamy do stolików według życzeń, a większość gości i tak poznaje się na parkiecie.'),
        ('Jaki strój?', 'Elegancki wieczorowy – to bal. Nie sprawdzamy dress code’u przy drzwiach.'),
        ('Do której trwa zabawa?', 'Do 4:00. Sala jest oddalona od zabudowań.'),
        ('Czy firma może zorganizować własny bal?', 'Tak – wynajmujemy salę na wyłączność w innym listopadowym terminie, z programem dopasowanym do grupy. Wystawiamy fakturę.'),
        ('Gdzie zaparkować?', 'Bezpłatny parking przy sali. Gościom bez kierowcy podamy kontakt do sprawdzonych przewoźników z Turku.'),
    ]
    ld = [faq_ld(bq), {"@context": "https://schema.org", "@type": "Event", "name": "Bal Andrzejkowy 2026 w Finezji",
          "startDate": "2026-11-21T19:00:00+01:00", "endDate": "2026-11-22T04:00:00+01:00",
          "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
          "location": {"@id": BASE + "#finezja"}, "image": BASE + "img/og.jpg",
          "description": "Bal andrzejkowy w sali Finezja pod Turkiem: kolacja serwowana, bufet, DJ-konferansjer, zabawa do 4:00.",
          "offers": {"@type": "Offer", "price": "220", "priceCurrency": "PLN", "availability": "https://schema.org/InStock", "url": BASE + "bal-andrzejkowy/"}}]
    h = head(p, 'bal-andrzejkowy/', 'Bal Andrzejkowy 2026 w Turku – 21 listopada, Sala Finezja',
             'Bal Andrzejkowy 21 listopada 2026 w Sali Finezja pod Turkiem: kolacja, bufet przez całą noc, DJ-konferansjer, zabawa do 4:00. Bilety od 220 zł/os.',
             ld=ld, preload='bal-sala')
    h += header(p, 'bal-andrzejkowy/')
    h += phead(p, 'bal-sala', 'Bal Andrzejkowy', 'Bal Andrzejkowy 2026', 'Ostatnia wielka zabawa przed świętami. Elegancka kolacja, DJ, który zna parkiet, i sala, w której bawi się do 150 osób. Z Turku, Konina, Koła, Dobrej i Władysławowa przyjeżdża się tu na jedną noc, żeby zapomnieć o kalendarzu.',
               kicker='Sobota, 21 listopada 2026 · <span data-countdown="2026-11-21"></span>',
               actions=f'<div class="actions"><a class="btn light" href="tel:{TEL1H}">Rezerwuj: {TEL1}</a><a class="btn line-light" href="#rezerwacja">Jak zarezerwować</a></div>')
    h += f'''<section class="night"><div class="wrap two">
<div><p class="kicker">Program wieczoru</p><h2>21 listopada, od 19:00 do rana</h2>
<table class="list" style="margin-top:20px"><tbody>
<tr><td style="width:90px"><b>19:00</b></td><td>powitanie gości, zajmowanie miejsc</td></tr>
<tr><td><b>19:15</b></td><td>uroczysta kolacja serwowana do stołu</td></tr>
<tr><td><b>20:10</b></td><td>słodkości, kawa i herbata</td></tr>
<tr><td><b>21:30</b></td><td>zimne przekąski</td></tr>
<tr><td><b>22:30</b></td><td>żurek</td></tr>
<tr><td><b>23:20</b></td><td>kulinarna niespodzianka</td></tr>
<tr><td><b>1:00</b></td><td>druga ciepła kolacja</td></tr>
<tr><td><b>do 4:00</b></td><td>zabawa do rana</td></tr>
</tbody></table>
<p class="muted" style="margin-top:16px">Między daniami – bloki muzyczne. Parkiet otwiera się po kolacji i nie pustoszeje do końca.</p></div>
<div><p class="kicker">W cenie biletu</p><h2>Przyjeżdżasz i siadasz do stołu</h2>
<table class="spec" style="margin-top:20px">
<tr><th>Bilet</th><td>od 220 zł za osobę</td></tr>
<tr><th>Jedzenie</th><td>kolacja serwowana, bufet uzupełniany całą noc, drugie ciepłe danie po północy – z tej samej kuchni co na weselach</td></tr>
<tr><th>Napoje</th><td>bezalkoholowe bez limitu</td></tr>
<tr><th>Muzyka</th><td>DJ-konferansjer, od aktualnych hitów po klasyki; przed balem zbieramy życzenia muzyczne</td></tr>
<tr><th>Parkiet</th><td>kolorowe światła, efekty LED, ciężki dym na otwarcie tańców</td></tr>
<tr><th>Atrakcje</th><td>konkursy z nagrodami – bez przymusu; fotobudka opcjonalnie</td></tr>
<tr><th>Wystrój</th><td>jesienno-świąteczny, elegancki – bez plastikowych kotylionów</td></tr>
</table></div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><div><p class="kicker">Dla kogo</p><h2>Pary, znajomi, firmy, grupy</h2></div></div>
<div class="three">
<div><h3>Pary i znajomi</h3><p class="muted">Kupujecie bilety, siadacie razem przy stoliku, resztę robimy my.</p></div>
<div><h3>Firmy</h3><p class="muted">Andrzejki to naturalna integracja przed świętami. Rezerwujemy stoły dla zespołu i wystawiamy fakturę. Na życzenie – zamknięty bal tylko dla Waszej firmy w innym terminie.</p></div>
<div><h3>Grupy zorganizowane</h3><p class="muted">Sołectwa, koła gospodyń, kluby sportowe: rabat przy większej liczbie osób i pomoc w transporcie.</p></div>
</div>
<div class="strip" style="margin-top:clamp(40px,6vw,72px)">
<a href="{big(p, 'bal-parkiet')}" data-lb data-alt="Parkiet i stanowisko DJ-a przed balem">{pic(p, 'bal-parkiet', 'Parkiet i stanowisko DJ-a przed balem', sizes='(max-width:760px) 100vw, 50vw')}</a>
<a href="{big(p, 'bal-scianka')}" data-lb data-alt="Ścianka balowa w sali">{pic(p, 'bal-scianka', 'Ścianka balowa w sali', sizes='25vw')}</a>
<a href="{big(p, 'scena-dj')}" data-lb data-alt="Scena z oświetleniem">{pic(p, 'scena-dj', 'Scena z oświetleniem', sizes='25vw')}</a>
<a href="{big(p, 'sala-zyrandole')}" data-lb data-alt="Sala z żyrandolami">{pic(p, 'sala-zyrandole', 'Sala z żyrandolami', sizes='25vw')}</a>
<a href="{big(p, 'wejscie')}" data-lb data-alt="Wejście do sali Finezja">{pic(p, 'wejscie', 'Wejście do sali Finezja', sizes='25vw')}</a>
</div></div></section>

<section id="rezerwacja" class="sand" style="scroll-margin-top:80px"><div class="wrap two">
<div><p class="kicker">Rezerwacja</p><h2>Jak zarezerwować miejsca</h2>
<ol class="steps" style="grid-template-columns:1fr">
<li><b>Zadzwoń lub napisz</b><span>Podaj liczbę osób i czy chcecie siedzieć razem.</span></li>
<li><b>Wpłać zaliczkę</b><span>Zaliczka blokuje miejsce, resztę wpłacasz do 14 listopada 2026.</span></li>
<li><b>Zgłoś diety i życzenia muzyczne</b><span>Trafiają do kuchni i do DJ-a.</span></li>
<li><b>Przyjedź 21 listopada o 19:00</b><span>Dekoracje, obsługa i sprzątanie są po naszej stronie.</span></li>
</ol>
<p class="muted" style="margin-top:20px">W ubiegłych latach stoliki rozchodziły się na kilka tygodni przed terminem.</p>
<div class="actions"><a class="btn" href="tel:{TEL1H}">{TEL1}</a><a class="btn ghost" href="mailto:{MAIL}?subject=Bal%20Andrzejkowy%202026%20-%20rezerwacja">Napisz maila</a></div></div>
<div><p class="kicker">Pytania</p><h2>Zanim zadzwonisz</h2>{faq(bq)}</div>
</div></section>
'''
    h += footer(p)
    write('bal-andrzejkowy', h)

# =====================================================================
#  GALERIA
# =====================================================================
GAL = [
    ('sala', 'hero', 'Sala przygotowana na wesele'), ('sala', 'sala-kwiaty', 'Wnętrze z kwiatami i żyrandolami'),
    ('dekoracje', 'dek-roze', 'Kwiaty za stołem Pary Młodej'), ('sala', 'stol-mlodych', 'Stoły weselne ze złotymi świecznikami'),
    ('slodki', 'slodki-stol', 'Słodki stół'), ('okolica', 'budynek-wieczor', 'Sala Finezja wieczorem'),
    ('dekoracje', 'dek-luk', 'Złoty łuk z kwiatami'), ('sala', 'sala-pion', 'Długie stoły weselne'),
    ('dekoracje', 'chrzest-neon', 'Dekoracja na chrzest'), ('sala', 'scena-dj', 'Scena i stanowisko DJ-a'),
    ('slodki', 'slodki-babeczki', 'Babeczki i desery z naszej kuchni'), ('okolica', 'love', 'Napis LOVE w ogrodzie'),
    ('dekoracje', 'dek-milosc', 'Neon „Miłość” na ściance'), ('sala', 'sala-dluga', 'Sala z nakrytymi stołami'),
    ('dekoracje', 'osiemnastka', 'Ścianka na osiemnastkę'), ('sala', 'sala-zyrandole', 'Kryształowe żyrandole'),
    ('slodki', 'slodki-regal', 'Desery na słodkim stole'), ('dekoracje', 'dek-oltarz', 'Kompozycje z białych kwiatów'),
    ('okolica', 'budynek-dzien', 'Budynek sali'), ('sala', 'nakrycie', 'Nakrycia stołów'),
    ('dekoracje', 'urodziny-scianka', 'Ścianka urodzinowa z balonami'), ('sala', 'sala-okna', 'Sala z wysokimi oknami'),
    ('dekoracje', 'dek-kwiaty', 'Dekoracja stołu Pary Młodej'), ('slodki', 'slodki-okno', 'Ciasta przy oknie'),
    ('sala', 'stol-gosci', 'Stół gości'), ('okolica', 'wejscie', 'Wejście do sali'), ('dekoracje', 'urodziny-50', 'Pięćdziesiątka'),
    ('sala', 'bal-parkiet', 'Parkiet przed balem'), ('dekoracje', 'dek-mlodzi', 'Stół Pary Młodej ze świecami'),
    ('sala', 'sala-okragle', 'Okrągłe stoły'), ('slodki', 'kawa', 'Kawa i herbata dla gości'), ('dekoracje', 'chrzest-pion', 'Chrzest – dekoracja z neonem'),
    ('okolica', 'budynek-front', 'Front budynku'), ('dekoracje', 'dek-balony', 'Dekoracja z balonami'), ('sala', 'sala-wieczor', 'Sala wieczorem'),
    ('dekoracje', 'scianka-mis', 'Ścianka z balonami i misiami'), ('okolica', 'budynek-plac', 'Parking przed salą'), ('sala', 'bal-scianka', 'Ścianka balowa'),
    ('dekoracje', 'dek-stol', 'Kwiaty na stole'), ('okolica', 'budynek-ogrod', 'Sala od strony ogrodu'), ('dekoracje', 'chrzest-balony', 'Balony i neon „Chrzest Święty”'),
]

def galeria():
    p = '../'
    fl = [('all', 'Wszystkie'), ('sala', 'Sala'), ('dekoracje', 'Dekoracje'), ('slodki', 'Słodki stół'), ('okolica', 'Budynek i okolica')]
    fh = ''.join(f'<button type="button" data-f="{k}" aria-pressed="{str(k == "all").lower()}">{n}</button>' for k, n in fl)
    g = ''.join(f'<a href="{big(p, im)}" data-lb data-k="{k}" data-alt="{alt}">{pic(p, im, alt, sizes="(max-width:700px) 100vw, 33vw")}</a>' for k, im, alt in GAL)
    h = head(p, 'galeria/', 'Galeria – sala weselna Finezja pod Turkiem, zdjęcia sali i dekoracji',
             'Zdjęcia sali Finezja: wnętrze przygotowane na wesela i przyjęcia, dekoracje, słodkie stoły, budynek i otoczenie.', preload='sala-dluga')
    h += header(p, 'galeria/')
    h += phead(p, 'sala-dluga', 'Galeria', 'Galeria sali', f'{len(GAL)} zdjęć z przyjęć w Finezji – bez stocku i bez filtrów. Kliknij zdjęcie, żeby je powiększyć.', kicker='Zdjęcia z naszych przyjęć')
    h += f'''<section><div class="wrap">
<div class="filters" role="group" aria-label="Filtruj zdjęcia">{fh}</div>
<div class="masonry">{g}</div>
<p class="muted" style="margin-top:28px">Więcej zdjęć i filmów: <a class="link" href="{FB}" target="_blank" rel="noopener">Facebook</a>, <a class="link" href="{IG}" target="_blank" rel="noopener">Instagram</a>, <a class="link" href="{YT}" target="_blank" rel="noopener">YouTube</a>.</p>
</div></section>
<div class="lb" role="dialog" aria-label="Podgląd zdjęcia"><button class="x" aria-label="Zamknij">×</button><button class="pv" aria-label="Poprzednie">‹</button><img alt=""><button class="nx" aria-label="Następne">›</button><p></p></div>
'''
    h += contact_band(p)
    h += footer(p)
    write('galeria', h)

# =====================================================================
#  KONTAKT
# =====================================================================
def kontakt():
    p = '../'
    h = head(p, 'kontakt/', 'Kontakt i rezerwacje – Sala Finezja, Kaczki Średnie 10c, Turek',
             f'Sala Finezja, {ADR}. Telefon {TEL1}, {TEL2}, e-mail {MAIL}. Zapytaj o wolny termin wesela, osiemnastki, komunii lub przyjęcia firmowego.', preload='budynek-front')
    h += header(p, 'kontakt/')
    h += phead(p, 'budynek-front', 'Kontakt', 'Kontakt i rezerwacje', 'Zadzwoń, napisz albo przyjedź obejrzeć salę. Na zapytania odpowiadamy w godzinach pracy biura.', kicker='Kaczki Średnie 10c, Turek')
    h += f'''<section><div class="wrap two">
<div>
<h2>Dane kontaktowe</h2>
<table class="spec">
<tr><th>Telefon</th><td><a href="tel:{TEL1H}">{TEL1}</a><br><a href="tel:{TEL2H}">{TEL2}</a></td></tr>
<tr><th>E-mail</th><td><a href="mailto:{MAIL}">{MAIL}</a></td></tr>
<tr><th>Adres</th><td>Finezja Sala Bankietowa<br>{ADR}<br><a href="{MAPS}" target="_blank" rel="noopener">Wyznacz trasę w Google Maps</a></td></tr>
<tr><th>Biuro</th><td>poniedziałek 10:00–13:00<br>czwartek 9:00–13:00<br>piątek–niedziela 9:00–21:00</td></tr>
<tr><th>Dojazd</th><td>4 km od centrum Turku; z Konina i Koła drogą DK92; bezpłatny parking przy sali</td></tr>
<tr><th>NIP</th><td>739 171 82 82</td></tr>
</table>
<p class="muted small" style="margin-top:18px">Obserwuj nas: <a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{YT}" target="_blank" rel="noopener">YouTube</a></p>
</div>
<div id="zapytanie" style="scroll-margin-top:100px">
<h2>Zapytaj o wolny termin</h2>
<p class="muted">Podaj okazję i datę – sprawdzimy, czy sala jest wolna, i odezwiemy się z propozycją menu.</p>
<form class="form" novalidate>
<label class="f">Okazja<select name="okazja">
<option value="wesele">Wesele</option><option value="osiemnastka">Osiemnastka</option><option value="urodziny">Urodziny / jubileusz</option>
<option value="komunia">Komunia</option><option value="chrzciny">Chrzciny</option><option value="firma">Spotkanie firmowe</option>
<option value="konsolacja">Konsolacja</option><option value="catering">Catering</option><option value="inne">Inna okazja</option></select></label>
<label class="f">Liczba gości<input name="goscie" type="number" min="5" max="160" inputmode="numeric" placeholder="np. 100"></label>
<label class="f full">Data przyjęcia<input name="data" type="date"></label>
<p class="hint full" id="t-hint"></p>
<label class="f">Imię i nazwisko<input name="imie" autocomplete="name" required></label>
<label class="f">Telefon<input name="tel" type="tel" autocomplete="tel" inputmode="tel"></label>
<label class="f full">E-mail<input name="email" type="email" autocomplete="email"></label>
<label class="f full">Wiadomość<textarea name="tresc" placeholder="Dodatkowe pytania, np. o noclegi, menu, dekoracje"></textarea></label>
<label class="check full"><input type="checkbox" name="zgoda"> Zgadzam się na przetwarzanie moich danych przez Finezja Sala Bankietowa, {ADR}, w celu odpowiedzi na zapytanie.</label>
<div class="full"><button class="btn" type="submit">Wyślij zapytanie</button><p class="form-msg" role="status"></p></div>
</form>
</div>
</div></section>
<section class="sand" style="padding:0"><iframe class="map" style="min-height:460px;display:block" src="{EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa dojazdu do sali Finezja"></iframe></section>
'''
    h += footer(p)
    write('kontakt', h)

# ---------- pliki pomocnicze ----------
def extras():
    open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#3d1620"/>'
        '<text x="32" y="46" text-anchor="middle" font-family="Georgia,serif" font-size="42" fill="#f5efe6">F</text></svg>')
    urls = ['', 'wesele/', 'przyjecia/', 'catering/', 'bal-andrzejkowy/', 'galeria/', 'kontakt/']
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(f'<url><loc>{BASE}{u}</loc></url>' for u in urls) + '</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    open(os.path.join(ROOT, '.nojekyll'), 'w').write('')

if __name__ == '__main__':
    home(); wesele(); przyjecia(); catering(); bal(); galeria(); kontakt(); extras()
    print('ok')
