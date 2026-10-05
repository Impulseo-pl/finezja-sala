# -*- coding: utf-8 -*-
"""Podstrony odtwarzające strukturę finezja.org (27 stron + blog z 22 wpisami).
Treść: ich teksty z _src/tresci.json (wyciagnij.py), oczyszczone z SEO-pogrubień i emoji, z poprawionymi błędami kopiuj-wklej."""
import os, re, json, html as H
import build as B
from build import pic, head, header, footer, phead, faq, faq_ld, contact_band, reviews, write, TEL1, TEL1H, TEL2, TEL2H, MAIL, ADR

T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tresci.json'), encoding='utf-8'))

# --- poprawki błędów z ich strony (kopiuj-wklej między podstronami) ---
FIX = {
    'oferta/szescdziesiatka/': [('organizację 30 urodzin', 'organizację 60. urodzin')],
    'oferta/czterdziestka/': [('organizację 30 urodzin', 'organizację 40. urodzin')],
    'oferta/piedziesiatka/': [('wiele czterdziestek', 'wiele pięćdziesiątek'), ('by czterdzieste urodziny', 'by pięćdziesiąte urodziny')],
    'oferta/siedemdziesiatka/': [('Kaczkach Starych', 'Kaczkach Średnich')],
    'oferta/komunia-swieta/': [('i zaangażowani,', 'i zaangażowaniu,')],
    'oferta/urodziny/': [('Bogate menu:</b> Jako sala weselna specjalizujemy się również w organizacji uroczystych przyjęć, takich jak osiemnaste urodziny', 'Bogate menu:</b> Jako sala weselna specjalizujemy się również w organizacji uroczystych przyjęć, takich jak urodziny i jubileusze'),
                         ('Dzieje się tak z dwóch powodów: po pierwsze pasja do gotowania a po drugie uczestniczą w szkoleniach kulinarnych.', 'Dzieje się tak z dwóch powodów: nasi kucharze gotują z pasją i regularnie uczestniczą w szkoleniach kulinarnych.')],
    'oferta/chrzest/': [('No więc, powiedzmy sobie szczerze – chrzest', 'Chrzest')],
}
# teksty, które na ich stronie były przyciskami albo pustymi nagłówkami
DROP = {'Zapytaj o wolny termin', 'Rezerwuję miejsca', 'Zobacz galerię dekoracji', 'Pobierz przykładowe menu na osiemnastkę', 'Zapytaj o DJ-a na osiemnastkę',
        'Rezerwuję miejsca na Bal Andrzejkowy 2026', 'Organizacja chrzcin krok po kroku', 'Zadzwoń do nas', 'Chcesz zamówić gotowe porcje na imprezę….'}
EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿️‍]+')

def clean(t, li=False):
    t = EMOJI.sub('', t).strip()
    lead = re.match(r'^<b>(.*?)</b>(\s*(<br>|:|–|-))', t)
    if lead:
        rest = re.sub(r'</?b>', '', t[lead.end(1) + 4:])
        t = f'<b>{lead.group(1).strip()}</b>{rest}'
    else:
        t = re.sub(r'</?b>', '', t)
    t = re.sub(r'\s+([,.;:!?])', r'\1', t).replace('  ', ' ')
    return t.strip()

def blocks(path):
    out = []
    for b in T[path]['blocks']:
        if b['t'] == 'ul':
            out.append({'t': 'ul', 'x': [clean(x, True) for x in b['x']]})
        else:
            x = clean(b['x'])
            if re.sub('<[^>]+>', '', x).strip() in DROP: continue
            out.append({'t': b['t'], 'x': x})
    for a, b2 in FIX.get(path, []):
        for b in out:
            if b['t'] == 'ul': b['x'] = [y.replace(a, b2) for y in b['x']]
            else: b['x'] = b['x'].replace(a, b2)
    return out

def split(bl):
    """Bloki -> (h1, sekcje). Sekcja = nagłówek h2 + elementy."""
    h1 = next((b['x'] for b in bl if b['t'] == 'h1'), None)
    secs, cur = [], {'h': None, 'items': []}
    for b in bl:
        if b['t'] == 'h1': continue
        if b['t'] == 'h2':
            if cur['h'] or cur['items']: secs.append(cur)
            cur = {'h': b['x'], 'items': []}
        else:
            cur['items'].append(b)
    if cur['h'] or cur['items']: secs.append(cur)
    # nagłówki bez treści pod spodem (u nich były to kafelki-linki) – wylatują
    for sec in secs:
        it = sec['items']
        sec['items'] = [b for i, b in enumerate(it) if not (b['t'] in ('h3', 'h4', 'h5') and (i + 1 == len(it) or it[i + 1]['t'] in ('h3', 'h4', 'h5')))]
    return h1, [s for s in secs if any(b['t'] in ('p', 'ul') for b in s['items'])]

def items_html(items):
    o = ''
    for b in items:
        if b['t'] in ('h3', 'h4', 'h5'): o += f'<h3>{b["x"]}</h3>'
        elif b['t'] == 'ul': o += '<ul class="dots">' + ''.join(f'<li>{x}</li>' for x in b['x']) + '</ul>'
        else:
            x = b['x']
            m = re.match(r'^<b>(.*?)</b><br>(.*)$', x)
            o += f'<p class="pt"><b>{m.group(1)}</b>{m.group(2)}</p>' if m else f'<p>{x}</p>'
    return o

def is_faq(sec):
    return sec['h'] and re.search(r'pytania|FAQ', sec['h'], re.I) and sum(1 for b in sec['items'] if b['t'] == 'h3') >= 2

def faq_items(sec):
    q, out = None, []
    for b in sec['items']:
        if b['t'] == 'h3': q = b['x']
        elif q and b['t'] == 'p': out.append((q, b['x'])); q = None
    return out

def body(p, secs, imgs, alts=None):
    """Sekcje tekstu na przemian ze zdjęciami. Zwraca (html, lista_faq)."""
    o, faqs, k = '', [], 0
    imgs = list(imgs)
    for i, s in enumerate(secs):
        if is_faq(s):
            faqs += faq_items(s); continue
        h = f'<h2>{s["h"]}</h2>' if s['h'] else ''
        txt = h + items_html(s['items'])
        long = len(re.sub('<[^>]+>', '', txt)) > 1400
        if imgs and not long:
            im = imgs.pop(0)
            o += f'<div class="row{" flip" if k % 2 else ""} txt-row"><div>{txt}</div><figure>{pic(p, im, "")}</figure></div>'
            k += 1
        elif imgs and long:
            im = imgs.pop(0)
            o += f'<div class="two long-row{" flip" if k % 2 else ""}"><div class="sticky-fig"><figure>{pic(p, im, "")}</figure></div><div>{txt}</div></div>'
            k += 1
        else:
            o += f'<div class="prose">{txt}</div>'
    return o, faqs

def cut_lead(t, n=200):
    """Lead do nagłówka: pełne zdania do ~n znaków; reszta wraca do treści."""
    zd = re.split(r'(?<=[.!?…])\s+', t.strip())
    lead = ''
    while zd and (not lead or len(lead) + len(zd[0]) < n):
        lead = (lead + ' ' + zd.pop(0)).strip()
    return lead, ' '.join(zd)

def lead_of(secs):
    """Pierwszy akapit przed pierwszym h2 jako lead nagłówka (krótki); dłuższa część zostaje w treści."""
    if secs and secs[0]['h'] is None and secs[0]['items'] and secs[0]['items'][0]['t'] == 'p':
        ld = re.sub('<[^>]+>', '', secs[0]['items'].pop(0)['x'])
        ld, rest = cut_lead(ld)
        if rest: secs[0]['items'].insert(0, {'t': 'p', 'x': rest})
        if not secs[0]['items']: secs.pop(0)
        return ld
    return ''

def short(t, n=230):
    t = re.sub('<[^>]+>', '', t)
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'

def desc(t):
    return H.escape(short(t, 155), quote=True)

def related(p, cur):
    """Pasek z innymi okazjami."""
    L = [(u, n) for u, n in OFERTA if u != cur]
    return '<section class="paper rel"><div class="wrap"><p class="kicker">Inne okazje w Finezji</p><div class="rel-links">' + ''.join(
        f'<a href="{p}{u}">{n}</a>' for u, n in L) + '</div></div></section>'

OFERTA = [('wesele/', 'Wesele'), ('oferta/osiemnastka/', 'Osiemnastka'), ('oferta/urodziny/', 'Urodziny'), ('oferta/30-ste-urodziny/', '30. urodziny'),
          ('oferta/czterdziestka/', 'Czterdziestka'), ('oferta/piedziesiatka/', 'Pięćdziesiątka'), ('oferta/szescdziesiatka/', 'Sześćdziesiątka'),
          ('oferta/siedemdziesiatka/', 'Siedemdziesiątka'), ('oferta/chrzest/', 'Chrzest święty'), ('oferta/komunia-swieta/', 'Komunia święta'),
          ('oferta/spotkania-firmowe/', 'Spotkania firmowe'), ('oferta/konsolacja/', 'Konsolacja')]

def page(path, title, desc_, h1, lead, img, crumb, kicker='', content='', ld=None, actions=None, revs=None, cband=True, rel=False, cur=None):
    depth = path.strip('/').count('/') + 1 if path.strip('/') else 0
    p = '../' * depth
    content = content.replace('{P}', p)
    if actions is None:
        actions = f'<div class="actions"><a class="btn light" href="{p}kontakt/#zapytanie">Zapytaj o wolny termin</a><a class="btn line-light" href="tel:{TEL1H}">{TEL1}</a></div>'
    h = head(p, path, title, desc_, ld=ld, preload=img)
    h += header(p, cur or path)
    h += phead(p, img, crumb, h1, lead, kicker=kicker, actions=actions) if img else f'''<section class="phead noimg"><div class="wrap"><div class="ph-txt"><div class="crumbs"><a href="{p}">Finezja</a><span>/</span>{crumb}</div><h1 data-split>{h1}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}</div></div></section>'''
    h += content
    if rel: h += related(p, path)
    if revs: h += reviews(revs)
    if cband: h += contact_band(p)
    h += footer(p)
    write(path.strip('/'), h)

def std(path, img, imgs, crumb, kicker, title, extra_before='', extra_after='', revs=None, cur=None, h1=None, faq_extra=None):
    """Strona z ich tekstem: nagłówek + sekcje na przemian ze zdjęciami + FAQ."""
    h1x, secs = split(blocks(path))
    lead = lead_of(secs)
    depth = path.strip('/').count('/') + 1
    p = '../' * depth
    bh, faqs = body(p, secs, imgs)
    faqs = (faqs or []) + (faq_extra or [])
    c = extra_before + f'<section class="paper txt"><div class="wrap">{bh}</div></section>' + extra_after
    if faqs:
        c += f'<section class="sand"><div class="wrap narrow"><p class="kicker">Pytania</p><h2>Najczęściej pytacie o</h2>{faq(faqs)}</div></section>'
    page(path, title, desc(lead or bh), h1 or h1x or T[path]['title'], lead, img, crumb, kicker=kicker, content=c,
         ld=[faq_ld(faqs)] if faqs else None, revs=revs, rel=path.startswith('oferta/'), cur=cur)

# =====================================================================
def oferta_hub():
    path = 'oferta/'
    h1x, secs = split(blocks(path))
    p = '../'
    cards = [('wesele/', 'dek-roze', 'Wesele', 'Od 60 do 160 gości, jedno wesele dziennie, własna kuchnia i koordynator.'),
             ('oferta/osiemnastka/', 'osiemnastka', 'Osiemnastka', 'Sala na wyłączność do 150 gości, parkiet, DJ, tort z fontannami iskier.'),
             ('oferta/urodziny/', 'urodziny-scianka', 'Urodziny', 'Przyjęcia urodzinowe dla osób w każdym wieku – od roczku po jubileusze.'),
             ('oferta/30-ste-urodziny/', 'scena-dj', '30. urodziny', 'Sala na wyłączność, muzyka według jubilata i menu dopasowane do gości.'),
             ('oferta/czterdziestka/', 'dek-balony', 'Czterdziestka', 'Elegancka kolacja albo dynamiczne przyjęcie z parkietem tanecznym.'),
             ('oferta/piedziesiatka/', 'urodziny-50', 'Pięćdziesiątka', 'Kameralnie w gronie najbliższych albo uroczystość z rozmachem.'),
             ('oferta/szescdziesiatka/', 'sala-okna', 'Sześćdziesiątka', 'Sala zaaranżowana według Twoich wskazówek, przy pogodzie – także plener.'),
             ('oferta/siedemdziesiatka/', 'dek-kwiaty', 'Siedemdziesiątka', 'Uroczysty obiad albo przyjęcie z przymrużeniem oka – stoły ustawione do rozmowy.'),
             ('oferta/chrzest/', 'chrzest-balony', 'Chrzest święty', 'Rodzinne przyjęcie z miejscem do zabawy dla dzieci i dekoracją dopasowaną do uroczystości.'),
             ('oferta/komunia-swieta/', 'dek-oltarz', 'Komunia święta', 'Menu dla dorosłych i dzieci, 10 minut od kościołów w Turku.'),
             ('oferta/spotkania-firmowe/', 'sala-okragle', 'Spotkania firmowe', 'Bankiety, wigilie firmowe, szkolenia i integracje – z fakturą.'),
             ('oferta/konsolacja/', 'kawa', 'Konsolacja', 'Spokojne miejsce na spotkanie po pogrzebie – ustalamy wszystko w jednej rozmowie.')]
    grid = '<div class="idx">' + ''.join(f'<a class="idx-row" href="{p}{u}"><h3>{n}</h3><p>{t}</p><span class="idx-go" aria-hidden="true">→</span><figure class="idx-img">{pic(p, im, "", sizes="(max-width:860px) 40vw, 340px")}</figure></a>' for u, im, n, t in cards) + '</div>'
    first = secs.pop(0)
    lead, rest = cut_lead(re.sub('<[^>]+>', '', first['items'][0]['x'])) if first['items'] else ('', '')
    rest_items = ([{'t': 'p', 'x': rest}] if rest else []) + first['items'][1:]
    bh, _ = body(p, ([{'h': None, 'items': rest_items}] if rest_items else []) + [s for s in secs if s['items']], ['dek-luk', 'sala-stoly', 'stol-gosci', 'slodki-regal'])
    c = f'<section class="paper"><div class="wrap"><div class="sec-head"><div><p class="kicker">Oferta</p><h2>Na jaką okazję szukasz sali?</h2></div><p>Każde przyjęcie przygotowujemy od nowa: menu, ustawienie stołów, dekoracje i przebieg wieczoru.</p></div>{grid}</div></section>'
    c += f'<section class="sand txt"><div class="wrap">{bh}</div></section>'
    page(path, 'Organizacja imprez okolicznościowych Turek – oferta | Sala Finezja', desc(lead), 'Imprezy okolicznościowe w Finezji', lead,
         'sala-okragle', 'Oferta', kicker='Kaczki Średnie · 4 km od Turku', content=c, revs=[3, 0, 2])

def osiem_extra(sec):
    """Z bloku osiemnastki z dema v1: motywy imprezy i formy podania (bez FAQ – FAQ jest z ich strony)."""
    two = sec[sec.index('<div class="two"'):]
    two = re.sub(r'<div style="margin-top:28px"><div class="faq">.*?</div></div>', '', two, flags=re.S)
    two = two.replace(' style="margin-top:clamp(56px,8vw,96px)"', '')
    return f'<section class="sand"><div class="wrap"><div class="sec-head"><div><p class="kicker">Motyw i menu</p><h2>Sala jako tło, menu bez sztywnych pakietów</h2></div></div>{two}</section>'

def oferta_pages(blk):
    X, q18 = blk
    std('oferta/osiemnastka/', 'osiemnastka', ['urodziny-scianka', 'scena-dj', 'bal-parkiet', 'slodki-babeczki', 'bal-scianka', 'slodki-regal'],
        '<a href="../">Oferta</a><span>/</span>Osiemnastka', '18. urodziny · Turek i okolice',
        'Sala na osiemnastkę w Turku – 18. urodziny w Sali Finezja', h1='Osiemnastka w Sali Finezja',
        extra_after=osiem_extra(X['osiemnastka']), revs=[3, 2, 0])
    std('oferta/urodziny/', 'urodziny-scianka', ['urodziny-50', 'slodki-regal', 'urodziny-pion'], '<a href="../">Oferta</a><span>/</span>Urodziny',
        'Roczek, 18, 30, 40, 50, 60, 70 lat', 'Wynajem sali na urodziny – Turek, Kaczki Średnie | Finezja', revs=[3, 0, 2])
    for path, img, imgs, n, k in [
        ('oferta/30-ste-urodziny/', 'scena-dj', ['bal-scianka', 'slodki-babeczki'], '30. urodziny', 'Sala na 30 urodziny'),
        ('oferta/czterdziestka/', 'dek-balony', ['sala-wieczor', 'stol-gosci', 'slodki-stol'], 'Czterdziestka', 'Restauracja na 40 urodziny'),
        ('oferta/piedziesiatka/', 'urodziny-50', ['stol-gosci', 'dek-mlodzi', 'kawa'], 'Pięćdziesiątka', 'Restauracja na 50. urodziny'),
        ('oferta/szescdziesiatka/', 'sala-okna', ['kawa', 'slodki-okno'], 'Sześćdziesiątka', '60. urodziny w sali Finezja'),
        ('oferta/siedemdziesiatka/', 'dek-kwiaty', ['sala-okragle', 'slodki-regal'], 'Siedemdziesiątka', 'Sala na 70. urodziny – Turek')]:
        std(path, img, imgs, f'<a href="../">Oferta</a><span>/</span>{n}', 'Okrągłe urodziny · Kaczki Średnie pod Turkiem',
            f'{k} | Sala Finezja, Kaczki Średnie', revs=[0, 3, 2])
    std('oferta/chrzest/', 'chrzest-balony', ['chrzest-neon', 'scianka-mis', 'chrzest-pion'], '<a href="../">Oferta</a><span>/</span>Chrzest święty',
        'Chrzciny pod Turkiem', 'Sala na chrzciny Turek – jak zorganizować chrzest | Finezja', h1='Chrzest święty',
        extra_before=f'<section class="sand">{X["komunia"]}</section>', revs=[0, 2, 3])
    std('oferta/komunia-swieta/', 'dek-oltarz', ['sala-stoly', 'slodki-stol', 'dek-stol', 'stol-gosci'], '<a href="../">Oferta</a><span>/</span>Komunia święta',
        'Pierwsza Komunia Święta', 'Sala na komunię Turek – przyjęcie komunijne w Finezji', h1='Komunia święta w Finezji', revs=[0, 2, 3])
    std('oferta/spotkania-firmowe/', 'sala-okragle', ['sala-dluga', 'kawa'], '<a href="../">Oferta</a><span>/</span>Spotkania firmowe',
        'Dla firm', 'Spotkania firmowe i bankiety – Turek | Sala Finezja', h1='Spotkania firmowe',
        extra_before=f'<section class="sand">{X["firmy"]}</section>', revs=[2, 0, 1])
    std('oferta/konsolacja/', 'kawa', ['sala-okna'], '<a href="../">Oferta</a><span>/</span>Konsolacja',
        'Spotkanie po pogrzebie', 'Konsolacja (stypa) – Turek, Kaczki Średnie | Finezja', h1='Konsolacja',
        extra_before=f'<section class="sand">{X["konsolacja"]}</section>')

def catering_page():
    h1x, secs = split(blocks('catering-turek/'))
    p = '../'
    # ich stary cennik na stronie zastępujemy odnośnikiem do aktualnego menu 2026 (z ich grafiki)
    keep = [s for s in secs if not (s['h'] and re.match(r'(Menu cateringowe|Mięsa|Torty|Sałatki|Zupy|Ciasta)', s['h']))]
    intro = keep.pop(0) if keep and keep[0]['h'] is None else None
    feats = [b for b in (intro['items'] if intro else [])]
    lead = re.sub('<[^>]+>', '', feats[0]['x']).replace('!', '! ', 1) if feats else ''
    hs = [(b['x'], feats[i + 1]['x']) for i, b in enumerate(feats[:-1]) if b['t'] == 'h3']
    keep2 = []
    for s in keep:
        s['items'] = [b for b in s['items'] if not (b['t'] == 'p' and re.search(r'Gęsina|Zupa krem', b['x']))]
        if s['h'] or s['items']: keep2.append(s)
    bh, faqs = body(p, keep2, ['slodki-okno', 'slodki-regal', 'kawa'])
    feat_html = ''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a, b in hs)
    c = f'''<section class="paper"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Catering z Finezji</p><h2>Wydarzenie Twoich marzeń zaczyna się tutaj</h2></div><p>Stwórz niezapomniane przeżycia z pomocą naszych ekspertów w zakresie planowania imprez i cateringu.</p></div>
<div class="feats">{feat_html}</div>
<div class="menu-cta"><div><p class="kicker">Menu cateringowe 2026</p><h3>Zupy, mięsa, dodatki, przekąski, sałatki, ciasta i torty – z cenami</h3><p>Wybierz dania, a suma policzy się sama. Zamówienie wyślesz SMS-em albo mailem. Zamówienia przyjmujemy do środy.</p></div>
<div class="actions"><a class="btn" href="{p}menu-cateringowe-2026/">Zobacz menu i zamów</a><a class="btn ghost" href="{p}wigilia/">Catering wigilijny</a></div></div>
</div></section>
<section class="sand txt"><div class="wrap">{bh}</div></section>'''
    page('catering-turek/', 'Catering Turek – dania z kuchni sali Finezja, dowóz i odbiór', desc(lead), 'Catering z kuchni Finezji', lead,
         'slodki-babeczki', 'Catering', kicker='Turek i okolice · od 5 do 100 osób', content=c, revs=[4, 5, 2],
         actions=f'<div class="actions"><a class="btn light" href="{p}menu-cateringowe-2026/">Menu 2026 i zamówienie</a><a class="btn line-light" href="tel:{TEL1H}">Zamów: {TEL1}</a></div>')

def wigilia_page(blk):
    X, _ = blk
    std('wigilia/', 'stol-gosci', ['kawa', 'slodki-okno', 'sala-wieczor'], 'Catering wigilijny', 'Odbiór 23 grudnia, 13:00–16:00',
        'Catering wigilijny Turek – Wigilia z kuchni Finezji', h1='Catering wigilijny',
        extra_after=f'<section class="paper">{X["swieta"].replace("../catering/", "{P}catering-turek/").replace("Catering Finezji", "Catering Finezji")}</section>'.replace('{P}', '../'), cur='catering-turek/')

def bale():
    p = '../'
    # Bal Noworoczny – ich tekst opisuje edycję z 17 stycznia 2026
    noworoczny = [('Start', '20:00'), ('Muzyka', 'DJ Maciej Dygas – profesjonalista z wieloletnim doświadczeniem w prowadzeniu imprez'),
                  ('W cenie', 'wszystkie posiłki, napoje i ciasta, kulinarna niespodzianka w trakcie imprezy, słodki stół'),
                  ('O północy', 'lampka szampana Dorato dla każdego gościa i pokaz fajerwerków'), ('Atrakcje', 'fotobudka 360'), ('Koniec', 'bawimy się do rana')]
    spec = '<table class="spec">' + ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in noworoczny) + '</table>'
    c = f'''<section class="paper"><div class="wrap two">
<div><p class="kicker">Ostatnia edycja · 17 stycznia 2026</p><h2>Planowanie imprezy noworocznej</h2>
<p>To jest ta jedna noc w roku, kiedy żegnamy stary rok i witamy nowy. Zanim zacznie się nowy, warto sobie postanowić, co chcemy poprawić, albo co nowego zrobić – co do tej pory nam umknęło.</p>
<p>Serdecznie zapraszamy wszystkich chętnych do wspólnej zabawy z nami. Zapewniamy fantastyczną atmosferę, świetną zabawę oraz wiele atrakcji. Liczba miejsc jest ograniczona.</p>
<div class="actions"><a class="btn" href="tel:{TEL1H}">Zapytaj o kolejny bal: {TEL1}</a></div></div>
<div><p class="kicker">Jak wyglądał bal 17 stycznia 2026</p>{spec}</div>
</div></section>
<section class="night"><div class="wrap two"><div><p class="kicker">Najbliższe wydarzenie</p><h2>Bal Andrzejkowy 2026</h2><p>Sobota, 21 listopada, od 19:00 do 4:00. Kolacja, bufet przez całą noc i DJ-konferansjer. Bilety od 220 zł za osobę.</p>
<div class="actions"><a class="btn light" href="{p}andrzejki/">Program i rezerwacja</a></div></div><figure>{pic(p, 'bal-parkiet', 'Parkiet przed balem')}</figure></div></section>'''
    page('bal-noworoczny/', 'Bal Noworoczny w Turku – Sala Finezja', 'Bal Noworoczny w Sali Finezja pod Turkiem: posiłki, słodki stół, szampan o północy, fotobudka 360, fajerwerki i zabawa do rana.',
         'Bal Noworoczny', 'Jedna noc w roku, kiedy żegnamy stary rok i witamy nowy – z DJ-em, kolacją, szampanem o północy i pokazem fajerwerków.',
         'scena-dj', 'Bal Noworoczny', kicker='Sala Finezja · Kaczki Średnie', content=c, cur='andrzejki/',
         actions=f'<div class="actions"><a class="btn light" href="tel:{TEL1H}">Zapytaj o termin: {TEL1}</a><a class="btn line-light" href="{p}andrzejki/">Najbliższy bal</a></div>')
    c = f'''<section class="paper"><div class="wrap row">
<div><p class="kicker">Ostatnia edycja · 14 lutego 2026</p><h2>Bal Karnawałowy w Finezji</h2>
<p>Karnawałowa zabawa w sali, w której na co dzień odbywają się wesela: kolacja z naszej kuchni, parkiet ze światłami i muzyka do rana. Miejsca na lutowy bal znikały błyskawicznie – rezerwacje przyjmujemy telefonicznie.</p>
<table class="spec"><tr><th>Ostatni bal</th><td>14 lutego 2026</td></tr><tr><th>Rezerwacje</th><td><a href="tel:{TEL1H}">{TEL1}</a> · <a href="tel:{TEL2H}">{TEL2}</a></td></tr><tr><th>Miejsce</th><td>{ADR}</td></tr></table>
<div class="actions"><a class="btn" href="tel:{TEL1H}">Zapytaj o kolejny bal</a><a class="btn ghost" href="{p}andrzejki/">Bal Andrzejkowy 2026</a></div></div>
<figure>{pic(p, 'bal-scianka', 'Ścianka balowa w sali Finezja')}</figure>
</div></section>'''
    page('karnawal/', 'Bal Karnawałowy w Turku – Sala Finezja', 'Bal Karnawałowy w Sali Finezja pod Turkiem: kolacja z własnej kuchni, parkiet i muzyka do rana. Rezerwacje: 665 188 619.',
         'Bal Karnawałowy', 'Karnawałowa noc w sali weselnej – kolacja, parkiet ze światłami i zabawa do rana. Zapraszamy do rezerwacji.',
         'bal-sala', 'Bal Karnawałowy', kicker='Sala Finezja · Kaczki Średnie', content=c, cur='andrzejki/',
         actions=f'<div class="actions"><a class="btn light" href="tel:{TEL1H}">Rezerwacje: {TEL1}</a><a class="btn line-light" href="{p}andrzejki/">Najbliższy bal</a></div>')

def polecamy():
    p = '../'
    G = [('Zespoły weselne', [('Bravo', '663 678 555'), ('Tequila', '603 171 660')]),
         ('DJ-e', [('Jacek Kujawa', '888 548 650'), ('Klaudiusz', '537 718 851'), ('Maciej Dygas', '785 961 525'), ('Mariusz Kominiarczyk', '693 969 367')]),
         ('Dekoracje', [('Zakręcona', '665 073 452'), ('Amor', '603 107 092'), ('Czarnek', '798 980 534'), ('Joanna', '691 074 619'), ('Balwit', '504 121 509'), ('Mateusz Adamiak', '783 298 205')]),
         ('Fotografowie', [('Natalia Krauze', '693 233 022'), ('Darek Kowalski', '606 374 408'), ('Natalia Okoń', '505 947 401'), ('Kuźnia Kadru', '603 448 740')]),
         ('Pozostali', [('Kraina Słodkości – cukiernia', '603 615 263'), ('Wesoły Duecik – animatorzy dla dzieci', '781 066 273'), ('Barman – drink bar', '697 217 044')])]
    cols = ''.join(f'<div class="pgrp"><h3>{n}</h3>{B.partners_table(r)}</div>' for n, r in G)
    c = f'''<section class="paper"><div class="wrap"><div class="sec-head"><div><p class="kicker">Sprawdzeni wykonawcy</p><h2>Znają salę, akustykę i nasz harmonogram</h2></div>
<p>Grali, dekorowali i fotografowali w Finezji wielokrotnie. Terminy i ceny ustalacie bezpośrednio z nimi. Możecie też przyjechać z własną ekipą – nie pobieramy za to opłat.</p></div>
<div class="pgrid">{cols}</div></div></section>'''
    page('polecamy/', 'Polecamy – DJ, zespół, fotograf i dekoracje na wesele w Turku | Finezja',
         'Sprawdzeni wykonawcy, którzy pracowali w Sali Finezja: zespoły i DJ-e weselni, dekoratorzy, fotografowie z Turku i okolic – z telefonami.',
         'Polecamy', 'Poniżej przedstawiamy naszych lokalnych wykonawców. To są sprawdzone osoby.', 'scena-dj', 'Polecamy', kicker='Wykonawcy z Turku i okolic', content=c)

def lokalne():
    for path, img, imgs, crumb, title in [
        ('sala-weselna-kalisz/', 'sala-dluga', ['dek-roze', 'slodki-stol', 'budynek-ogrod'], 'Sala weselna: Kalisz', 'Sala weselna Kalisz – wesele w Finezji niedaleko Kalisza'),
        ('sala-weselna-konin/', 'hero', ['dek-luk', 'stol-mlodych', 'budynek-front'], 'Sala weselna: Konin', 'Sala weselna Konin – wesele w Finezji, 40 minut przez DK92'),
        ('sala-bankietowa-kalisz/', 'sala-zyrandole', ['sala-okragle', 'budynek-plac', 'slodki-regal'], 'Sala bankietowa: Kalisz', 'Sala bankietowa Kalisz – przyjęcia w Finezji niedaleko Kalisza')]:
        std(path, img, imgs, crumb, 'Kaczki Średnie, gmina Turek', title, revs=[0, 1, 2], cur='wesele/' if 'weselna' in path else 'oferta/')

def polityka():
    bl = blocks('polityka-prywatnosci/')
    o = ''
    for b in bl:
        if b['t'] in ('h1',): continue
        if b['t'] in ('h2', 'h3', 'h4'): o += f'<h2>{b["x"]}</h2>' if b['t'] == 'h2' else f'<h3>{b["x"]}</h3>'
        elif b['t'] == 'ul': o += '<ul class="dots">' + ''.join(f'<li>{x}</li>' for x in b['x']) + '</ul>'
        else: o += f'<p>{b["x"]}</p>'
    page('polityka-prywatnosci/', 'Polityka prywatności – Sala Finezja', 'Polityka prywatności serwisu Sali Bankietowej Finezja, Kaczki Średnie 10c, Turek.',
         'Polityka prywatności', '', None, 'Polityka prywatności', content=f'<section class="paper"><div class="wrap narrow prose legal-text">{o}</div></section>', cband=False)

# ---------------- BLOG ----------------
CAT = {'wesela': ('Wesela', ['dek-roze', 'stol-mlodych', 'dek-kwiaty', 'sala-kwiaty', 'hero', 'dek-mlodzi']),
       'chrzciny': ('Chrzciny', ['dek-balony', 'dek-milosc', 'slodki-babeczki', 'wejscie']),
       'komunie': ('Komunie', ['dek-oltarz', 'slodki-stol', 'stol-gosci', 'sala-okragle']),
       'urodziny': ('Urodziny', ['dek-balony', 'sala-zyrandole', 'slodki-regal', 'sala-wieczor', 'slodki-babeczki']),
       'wigilia': ('Wigilia', ['stol-gosci', 'kawa', 'sala-wieczor', 'slodki-regal', 'budynek-wieczor', 'dek-mlodzi']),
       'konsolacje': ('Konsolacje', ['kawa', 'sala-okragle', 'budynek-ogrod']),
       'catering': ('Catering', ['slodki-regal', 'slodki-babeczki'])}

def posts():
    L = [(k, v) for k, v in T.items() if v['kind'] == 'post']
    used = {}
    out = []
    for path, v in L:
        cat = path.split('/')[0]
        name, pool = CAT[cat]
        i = used.get(cat, 0); used[cat] = i + 1
        out.append(dict(path=path, cat=cat, catn=name, title=v['title'], img=pool[i % len(pool)]))
    return out

def blog():
    P = posts()
    p = '../'
    cats = sorted({x['cat'] for x in P}, key=lambda c: list(CAT).index(c))
    fl = '<div class="filters" role="group" aria-label="Kategorie">' + '<button type="button" data-f="all" aria-pressed="true">Wszystkie</button>' + ''.join(
        f'<button type="button" data-f="{c}" aria-pressed="false">{CAT[c][0]}</button>' for c in cats) + '</div>'
    def ex(x):
        _, secs = split(blocks(x['path']))
        for s in secs:
            for b in s['items']:
                if b['t'] == 'p' and len(re.sub('<[^>]+>', '', b['x'])) > 80: return short(b['x'], 150)
        return ''
    cards = ''.join(f'<a class="post-card" data-k="{x["cat"]}" href="{p}{x["path"]}"><figure>{pic(p, x["img"], "", sizes="(max-width:700px) 100vw, 33vw")}</figure><span class="pc-cat">{x["catn"]}</span><h3>{x["title"]}</h3><p>{ex(x)}</p></a>' for x in P)
    c = f'<section class="paper"><div class="wrap">{fl}<div class="posts">{cards}</div></div></section>'
    page('blog/', 'Blog – porady o weselach, chrzcinach, komuniach i przyjęciach | Sala Finezja',
         'Porady Sali Finezja: jak zorganizować wesele, chrzest, komunię, osiemnastkę, Wigilię i konsolację – bez stresu i w rozsądnym budżecie.',
         'Blog Finezji', 'Porady z sali, w której od 2010 roku organizujemy wesela, chrzciny, komunie, osiemnastki i Wigilie.', 'dek-mlodzi', 'Blog',
         kicker='Porady i inspiracje', content=c, cband=True,
         actions=f'<div class="actions"><a class="btn light" href="{p}kontakt/#zapytanie">Zapytaj o wolny termin</a></div>')
    for i, x in enumerate(P):
        path = x['path']
        p2 = '../../'
        bl = blocks(path)
        _, secs = split(bl)
        lead = lead_of(secs)
        o = ''
        for s in secs:
            if s['h']: o += f'<h2>{s["h"]}</h2>'
            o += items_html(s['items'])
        more = [y for y in P if y['cat'] == x['cat'] and y['path'] != path][:2] + [y for y in P if y['cat'] != x['cat']][i % 5:i % 5 + 1]
        mh = ''.join(f'<a class="post-card" href="{p2}{y["path"]}"><figure>{pic(p2, y["img"], "", sizes="33vw")}</figure><span class="pc-cat">{y["catn"]}</span><h3>{y["title"]}</h3></a>' for y in more[:3])
        c = f'''<section class="paper"><div class="wrap narrow prose article">{f'<p class="art-lead">{lead}</p>' if lead else ''}{o}
<div class="art-end"><p>Masz pytania o przyjęcie w Finezji? Zadzwoń: <a href="tel:{TEL1H}">{TEL1}</a> albo <a class="u" href="{p2}kontakt/#zapytanie">zapytaj o wolny termin</a>.</p></div></div></section>
<section class="sand"><div class="wrap"><p class="kicker">Czytaj dalej</p><div class="posts">{mh}</div></div></section>'''
        ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": x['title'], "image": B.BASE + 'img/og.jpg',
               "publisher": {"@id": B.BASE + "#finezja"}, "mainEntityOfPage": B.BASE + path}]
        page(path, H.unescape(x['title'])[:90] + ' | Blog Finezji', desc(lead or o), x['title'], '', x['img'],
             f'<a href="{p2}blog/">Blog</a><span>/</span>{x["catn"]}', kicker=x['catn'], content=c, ld=ld, cur='blog/',
             actions=f'<div class="actions"><a class="btn light" href="{p2}kontakt/#zapytanie">Zapytaj o wolny termin</a><a class="btn line-light" href="{p2}blog/">Wszystkie wpisy</a></div>')
    return P

ALL = ['', 'oferta/', 'wesele/', 'oferta/osiemnastka/', 'oferta/urodziny/', 'oferta/30-ste-urodziny/', 'oferta/czterdziestka/', 'oferta/piedziesiatka/',
       'oferta/szescdziesiatka/', 'oferta/siedemdziesiatka/', 'oferta/chrzest/', 'oferta/komunia-swieta/', 'oferta/spotkania-firmowe/', 'oferta/konsolacja/',
       'catering-turek/', 'menu-cateringowe-2026/', 'wigilia/', 'andrzejki/', 'karnawal/', 'bal-noworoczny/', 'galeria/', 'polecamy/', 'kontakt/',
       'polityka-prywatnosci/', 'sala-weselna-kalisz/', 'sala-weselna-konin/', 'sala-bankietowa-kalisz/', 'blog/']

def run():
    blk = B.przyjecia('../../')
    oferta_hub(); oferta_pages(blk)
    catering_page(); wigilia_page(B.przyjecia('../')); bale(); polecamy(); lokalne(); polityka()
    P = blog()
    return ALL + [x['path'] for x in P]
