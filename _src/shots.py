"""Zrzuty ekran po ekranie (animacje przewijania). python shots.py home,wesele/ 1440 [intro]"""
import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image
pages=sys.argv[1].split(',');w=int(sys.argv[2]);h=900 if w>800 else 844
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'sh')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1,is_mobile=w<800,has_touch=w<800)
    pg=ctx.new_page()
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    for name in pages:
        url='http://127.0.0.1:8124/finezja-sala/'+(name if name!='home' else '')+'?team=1'
        pg.goto(url,wait_until='networkidle',timeout=60000)
        if len(sys.argv)>3:
            for t in (300,900,1500,2400):
                pg.wait_for_timeout(t if t==300 else 600);pg.screenshot(path=f'{OUT}/intro_{t}.png')
        pg.wait_for_timeout(2600)
        H=pg.evaluate('document.documentElement.scrollHeight');frames=[];y=0
        while y<H and len(frames)<40:
            pg.mouse.wheel(0,0);pg.evaluate(f'window.scrollTo(0,{y})');pg.wait_for_timeout(1300)
            f=f'{OUT}/_f{len(frames)}.png';pg.screenshot(path=f);frames.append(f);y+=int(h*.85)
            H=pg.evaluate('document.documentElement.scrollHeight')
        n=name.strip('/').replace('/','_') or 'home'
        sc=0.5 if w>800 else 0.55
        ims=[Image.open(f) for f in frames];tw,th=int(w*sc),int(h*sc)
        per=4 if w>800 else 5
        for k in range(0,len(ims),per*2):
            grp=ims[k:k+per*2];cols=min(len(grp),per);rows=(len(grp)+per-1)//per
            sheet=Image.new('RGB',(cols*tw+(cols-1)*6,rows*th+(rows-1)*6),'white')
            for j,im in enumerate(grp):sheet.paste(im.resize((tw,th)),((j%per)*(tw+6),(j//per)*(th+6)))
            sheet.save(f'{OUT}/{n}_{w}_{k//(per*2)}.png')
        for f in frames:os.remove(f)
        print(n,w,'H',H,'frames',len(frames))
    print('ERR',errs[:8])
    b.close()
