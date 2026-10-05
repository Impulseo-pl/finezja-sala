# -*- coding: utf-8 -*-
"""Wyciąga treść stron i wpisów z finezja.org (zrzut API WP z dema v1) do _src/tresci.json jako bloki."""
import json, os, re, html
from html.parser import HTMLParser

SRC = r'C:\Users\kluch\finezja\_src'
OUT = os.path.dirname(os.path.abspath(__file__))

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.blocks = []; s.cur = None; s.buf = ''; s.lst = None; s.skip = 0
    def handle_starttag(s, t, a):
        if t in ('script', 'style', 'noscript', 'form', 'select', 'button'): s.skip += 1
        if s.skip: return
        if t in ('h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li'):
            s.flush(); s.cur = t
        elif t in ('ul', 'ol'):
            s.flush(); s.lst = []
        elif t == 'br' and s.cur:
            s.buf += '\n'
        elif t in ('strong', 'b') and s.cur: s.buf += '<b>'
    def handle_endtag(s, t):
        if t in ('script', 'style', 'noscript', 'form', 'select', 'button'):
            s.skip = max(0, s.skip - 1); return
        if s.skip: return
        if t in ('strong', 'b') and s.cur: s.buf += '</b>'
        if t == s.cur: s.flush()
        if t in ('ul', 'ol') and s.lst is not None:
            s.flush()
            if s.lst: s.blocks.append({'t': 'ul', 'x': s.lst})
            s.lst = None
    def handle_data(s, d):
        if s.skip: return
        if s.cur: s.buf += d
    def flush(s):
        if not s.cur: return
        t = re.sub(r'[ \t\r\f\v\u00a0]+', ' ', s.buf).strip()
        t = re.sub(r'<b>\s*</b>', '', t).replace(' </b>', '</b> ').replace('<b> ', ' <b>')
        t = re.sub(r'\s*\n\s*', '<br>', t).strip()
        plain = re.sub('<[^>]+>', '', t).strip()
        if plain:
            if s.cur == 'li':
                if s.lst is not None: s.lst.append(t)
                else: s.blocks.append({'t': 'p', 'x': t})
            else:
                s.blocks.append({'t': s.cur, 'x': t})
        s.cur = None; s.buf = ''

def blocks(h):
    p = P(); p.feed(h); p.flush()
    out = []
    for b in p.blocks:
        if out and b == out[-1]: continue
        out.append(b)
    return out

res = {}
for fn, kind in (('pages.json', 'page'), ('posts.json', 'post')):
    for x in json.load(open(os.path.join(SRC, fn), encoding='utf-8')):
        path = x['link'].replace('https://www.finezja.org/', '')
        res[path] = {'kind': kind, 'title': html.unescape(x['title']['rendered']), 'slug': x['slug'], 'blocks': blocks(x['content']['rendered'])}
json.dump(res, open(os.path.join(OUT, 'tresci.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
with open(os.path.join(OUT, 'tresci.txt'), 'w', encoding='utf-8') as f:
    for k, v in res.items():
        f.write(f'\n######## /{k} | {v["title"]} | {v["kind"]}\n')
        for b in v['blocks']:
            if b['t'] == 'ul': f.write('  - ' + '\n  - '.join(b['x']) + '\n')
            else: f.write(f'[{b["t"]}] {b["x"]}\n')
print(len(res))
