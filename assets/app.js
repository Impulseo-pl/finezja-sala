(function(){
  var d=document, html=d.documentElement, $=function(s,c){return (c||d).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
  var MAIL='biuro@finezja.org', TEL='+48665188619';
  var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var zl=function(n){return n.toLocaleString('pl-PL',{maximumFractionDigits:0})+' zł'};
  var clamp=function(v,a,b){return Math.max(a,Math.min(b,v))};

  /* płynne przewijanie */
  var lenis=null;
  if(window.Lenis&&!RM){lenis=new Lenis({lerp:.11,wheelMultiplier:1});(function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(performance.now())}
  function scrollTo(el){if(lenis)lenis.scrollTo(el,{offset:-80});else el.scrollIntoView({behavior:RM?'auto':'smooth'})}

  /* nagłówki – słowa wjeżdżają od dołu */
  $$('[data-split], main h2').forEach(function(h){
    if(h.closest('.menu'))return;
    var i=0;
    (function walk(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(n){
        if(n.nodeType===3){
          var parts=n.textContent.split(/([ \t\n]+)/),f=d.createDocumentFragment();
          parts.forEach(function(w){
            if(!w)return;
            if(/^[ \t\n]+$/.test(w)){f.appendChild(d.createTextNode(' '));return}
            var o=d.createElement('span');o.className='sw';var s=d.createElement('span');s.style.setProperty('--d',i++);s.textContent=w;o.appendChild(s);f.appendChild(o);
          });
          n.parentNode.replaceChild(f,n);
        }else if(n.nodeType===1&&!n.classList.contains('sw'))walk(n);
      });
    })(h);
    h.classList.add('split');
  });

  /* start po ekranie wejścia */
  var delay=html.classList.contains('intro')?1750:60;
  setTimeout(function(){
    html.classList.add('ready');
    $$('.hero [data-split], .phead [data-split]').forEach(function(h){h.classList.add('split-in')});
    setTimeout(function(){html.classList.remove('intro')},1200);
  },delay);

  /* odsłanianie przy przewijaniu */
  var sel='main section:not(.hero):not(.phead) figure, main .strip';
  $$(sel).forEach(function(f){if(f.closest('.hs-track')||f.closest('[data-revs]')||f.closest('.vx'))return;f.classList.add('rv-img')});
  var txt='main section:not(.hero):not(.phead) .kicker, main section:not(.hero):not(.phead) p:not(.lede), main .spec, main .list, main .steps li, main .faq, main .actions, main .calc, main .cart, main .occ, main .three>div, main .cdl, main .bal-dl, main .hint, main .form, main .masonry a';
  $$(txt).forEach(function(el){if(el.closest('[data-revs]')||el.closest('.rv-img')||el.closest('.vx'))return;el.classList.add('rv')});
  $$('.steps, .three, .hs-track').forEach(function(g){$$(':scope > *',g).forEach(function(c,i){c.style.setProperty('--rd',(i%3)*0.12+'s')})});
  if('IntersectionObserver' in window&&!RM){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');if(e.target.classList.contains('split'))e.target.classList.add('split-in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    /* element w całości przycięty clip-path nigdy nie „przecina” ekranu – obserwujemy rodzica */
    var pmap=new Map(),pio=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){(pmap.get(e.target)||[]).forEach(function(c){c.classList.add('in')});pio.unobserve(e.target)}})},{rootMargin:'0px 0px -10% 0px',threshold:0});
    $$('.rv').forEach(function(el){io.observe(el)});
    $$('.rv-img').forEach(function(el){var par=el.parentElement;if(!pmap.has(par)){pmap.set(par,[]);pio.observe(par)}pmap.get(par).push(el)});
    $$('main h2.split').forEach(function(h){if(!h.closest('.hero')&&!h.closest('.phead'))io.observe(h)});
  }else{
    $$('.rv, .rv-img').forEach(function(el){el.classList.add('in')});$$('.split').forEach(function(h){h.classList.add('split-in')});
  }

  /* pokaz zdjęć w łuku */
  $$('[data-slides]').forEach(function(box){
    var im=$$('img',box);if(im.length<2||RM)return;var k=0;
    setInterval(function(){im[k].classList.remove('on');k=(k+1)%im.length;var n=im[k];if(n.loading==='lazy')n.loading='eager';n.classList.add('on')},5200);
  });

  /* lede – słowa zapalają się */
  var lede=$('[data-words]'),words=[];
  if(lede){
    lede.innerHTML=lede.textContent.trim().split(/\s+/).map(function(w){return '<span class="w">'+w+'</span>'}).join(' ');
    words=$$('.w',lede);if(RM)words.forEach(function(w){w.classList.add('lit')});
  }

  /* poziome przewijanie okazji */
  var hs=$('[data-hs]'),track=hs&&$('.hs-track',hs),hsOn=false;
  function hsSetup(){
    if(!hs)return;
    hsOn=innerWidth>860&&!RM;
    hs.classList.toggle('pinned',hsOn);
    if(hsOn){var extra=track.scrollWidth-innerWidth;hs.style.setProperty('--hs-h',(innerHeight+extra)+'px');hs._extra=extra}
    else{track.style.transform='';hs.style.removeProperty('--hs-h')}
  }

  /* parallax, nagłówek, wideo, lede – jedna pętla */
  var top=$('.top'),lastY=0,par=$$('[data-par]'),vx=$('[data-vx]'),vid=vx&&$('video',vx),ticking=false;
  function frame(){
    ticking=false;
    var y=scrollY,vh=innerHeight;
    if(top){
      var dark=$('.hero, .phead');var limit=dark?dark.offsetHeight-80:40;
      top.classList.toggle('solid',y>limit);
      top.classList.toggle('hide',y>lastY&&y>400&&!d.body.classList.contains('menu-open'));
      lastY=y;
    }
    if(!RM){
      par.forEach(function(el){var r=el.getBoundingClientRect();if(r.bottom<-100||r.top>vh+100)return;var c=(r.top+r.height/2-vh/2);el.style.transform='translate3d(0,'+(c*parseFloat(el.dataset.par)).toFixed(1)+'px,0)'});
      if(hsOn){var r=hs.getBoundingClientRect(),p=clamp(-r.top/(hs._extra||1),0,1);track.style.transform='translate3d('+(-p*hs._extra).toFixed(1)+'px,0,0)';hs.style.setProperty('--hp',p.toFixed(3))}
      if(vx&&innerWidth>860){var rv=vx.getBoundingClientRect(),pv=clamp((-rv.top+vh*.35)/(vh*.95),0,1);vx.style.setProperty('--vp',(1-pv).toFixed(3))}
      if(words.length){var rl=lede.getBoundingClientRect(),pl=clamp((vh*.85-rl.top)/(rl.height+vh*.35),0,1),n=Math.round(pl*words.length);words.forEach(function(w,i){w.classList.toggle('lit',i<n)})}
    }
  }
  function onScroll(){if(!ticking){ticking=true;requestAnimationFrame(frame)}}
  addEventListener('scroll',onScroll,{passive:true});
  addEventListener('resize',function(){hsSetup();onScroll()});
  hsSetup();frame();
  if(track&&!hsOn)track.addEventListener('scroll',function(){if(hsOn)return;var m=track.scrollWidth-track.clientWidth;hs.style.setProperty('--hp',m?(track.scrollLeft/m).toFixed(3):0)},{passive:true});
  if(vid&&'IntersectionObserver' in window){
    new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){vid.preload='auto';var pr=vid.play();if(pr&&pr.catch)pr.catch(function(){})}else vid.pause()})},{threshold:.15}).observe(vid);
  }

  /* menu */
  var bg=$('.burger'),menu=$('#menu');
  function setMenu(o){d.body.classList.toggle('menu-open',o);bg.setAttribute('aria-expanded',o);menu.setAttribute('aria-hidden',!o);if(lenis){o?lenis.stop():lenis.start()}else d.body.style.overflow=o?'hidden':''}
  if(bg)bg.addEventListener('click',function(){setMenu(!d.body.classList.contains('menu-open'))});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.body.classList.contains('menu-open'))setMenu(false)});

  /* kotwice na tej samej stronie */
  d.addEventListener('click',function(e){
    var a=e.target.closest('a[href*="#"]');if(!a)return;
    var u=new URL(a.href,location.href);if(u.pathname!==location.pathname||!u.hash)return;
    var t=d.getElementById(decodeURIComponent(u.hash.slice(1)));if(!t)return;
    e.preventDefault();if(d.body.classList.contains('menu-open'))setMenu(false);scrollTo(t);history.replaceState(null,'',u.hash);
  });
  if(location.hash){var th=d.getElementById(decodeURIComponent(location.hash.slice(1)));if(th)setTimeout(function(){scrollTo(th)},delay+200)}

  /* przejście między podstronami tam, gdzie przeglądarka nie ma View Transitions */
  if(!('PageRevealEvent' in window)&&!RM){
    d.addEventListener('click',function(e){
      var a=e.target.closest('a[href]');if(!a||e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey||a.target==='_blank'||a.hasAttribute('download')||a.hasAttribute('data-lb'))return;
      var u=new URL(a.href,location.href);if(u.origin!==location.origin||(u.pathname===location.pathname&&u.hash))return;if(!/^https?:/.test(u.protocol))return;
      e.preventDefault();d.body.classList.add('leaving');setTimeout(function(){location.href=a.href},330);
    });
    addEventListener('pageshow',function(){d.body.classList.remove('leaving')});
  }

  /* opinie */
  $$('[data-revs]').forEach(function(st){
    var it=$$('.rev',st),k=0,cnt=$('.revs-count',st),timer;
    function go(n){it[k].classList.remove('on');k=(n+it.length)%it.length;it[k].classList.add('on');cnt.textContent=(k+1)+' / '+it.length}
    function auto(){clearInterval(timer);if(!RM)timer=setInterval(function(){go(k+1)},7000)}
    $('.rv-prev',st).addEventListener('click',function(){go(k-1);auto()});
    $('.rv-next',st).addEventListener('click',function(){go(k+1);auto()});
    auto();
  });

  /* FAQ – płynne rozwijanie */
  $$('.faq details').forEach(function(dt){
    var s=$('summary',dt);
    s.addEventListener('click',function(e){
      e.preventDefault();
      if(dt.open){dt.classList.remove('op');setTimeout(function(){if(!dt.classList.contains('op'))dt.open=false},RM?0:520)}
      else{dt.open=true;requestAnimationFrame(function(){requestAnimationFrame(function(){dt.classList.add('op')})})}
    });
  });

  /* dni do balu */
  $$('[data-countdown]').forEach(function(el){
    var t=new Date(el.getAttribute('data-countdown')+'T19:00:00'), now=new Date();
    var days=Math.ceil((t-now)/864e5);
    if(days>1)el.textContent='za '+days+' dni';
    else if(days===1)el.textContent='jutro';
    else if(days===0)el.textContent='dziś';
    else el.textContent='odbył się';
  });

  /* galeria: filtr */
  var fl=$('.filters');
  if(fl){
    fl.addEventListener('click',function(e){
      var b=e.target.closest('button');if(!b)return;
      $$('button',fl).forEach(function(x){x.setAttribute('aria-pressed',x===b)});
      var k=b.getAttribute('data-f'),items=$$('.masonry a');
      items.forEach(function(a){a.classList.add('out')});
      setTimeout(function(){items.forEach(function(a){a.hidden=!(k==='all'||a.getAttribute('data-k')===k)});requestAnimationFrame(function(){items.forEach(function(a){if(!a.hidden){a.classList.remove('out');a.classList.add('in')}})});if(lenis)lenis.resize()},RM?0:320);
    });
  }

  /* podgląd zdjęć – powiększenie z miniatury */
  var links=$$('[data-lb]');
  if(links.length){
    var lb=$('.lb');
    if(!lb){lb=d.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-label','Podgląd zdjęcia');lb.innerHTML='<button class="x" aria-label="Zamknij">×</button><button class="pv" aria-label="Poprzednie">‹</button><img alt=""><button class="nx" aria-label="Następne">›</button><p></p>';d.body.appendChild(lb)}
    var img=$('img',lb),cap=$('p',lb),i=0;
    function vis(){return links.filter(function(a){return !a.hidden})}
    function show(n,from){
      var v=vis();if(!v.length)return;i=(n+v.length)%v.length;var a=v[i];
      img.src=a.getAttribute('href');img.alt=a.getAttribute('data-alt')||'';cap.textContent=img.alt;
      lb.classList.add('on');if(lenis)lenis.stop();else d.body.style.overflow='hidden';
      if(from&&!RM&&img.animate){
        var t=from.getBoundingClientRect();
        var go=function(){var r=img.getBoundingClientRect();if(!r.width)return;img.animate([{transform:'translate('+(t.left+t.width/2-r.left-r.width/2)+'px,'+(t.top+t.height/2-r.top-r.height/2)+'px) scale('+(t.width/r.width)+')',opacity:.6},{transform:'none',opacity:1}],{duration:650,easing:'cubic-bezier(.22,.8,.2,1)'})};
        if(img.complete&&img.naturalWidth)go();else img.onload=function(){img.onload=null;go()};
      }
    }
    links.forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();show(vis().indexOf(a),a.querySelector('img'))})});
    function close(){lb.classList.remove('on');if(lenis)lenis.start();else d.body.style.overflow=''}
    $('.x',lb).addEventListener('click',close);
    $('.pv',lb).addEventListener('click',function(){show(i-1)});
    $('.nx',lb).addEventListener('click',function(){show(i+1)});
    lb.addEventListener('click',function(e){if(e.target===lb)close()});
    d.addEventListener('keydown',function(e){if(!lb.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
  }

  /* kalkulator menu weselnego – ceny sezonu 2026 z finezja.org */
  var wc=$('#wcalc');
  if(wc){
    var r=$('input[type=range]',wc),o=$('output',wc);
    var shown={min:0,max:0};
    function tween(el,key,to){if(RM){el.textContent=zl(to);shown[key]=to;return}var from=shown[key],t0=performance.now();shown[key]=to;(function st(t){var k=clamp((t-t0)/450,0,1),e=1-Math.pow(1-k,3);el.textContent=zl(Math.round((from+(to-from)*e)/10)*10);if(k<1)requestAnimationFrame(st)})(t0)}
    function calc(){
      var g=+r.value;o.textContent=g;
      tween($('#w-min'),'min',g*330);tween($('#w-max'),'max',g*380);
      var l=$('#w-link');if(l)l.href='../kontakt/?okazja=wesele&goscie='+g+'#zapytanie';
    }
    r.addEventListener('input',calc);calc();
  }

  /* catering – zamówienie z menu 2026 */
  var cat=$('#catering');
  if(cat){
    var cart={},items={};
    $$('.item',cat).forEach(function(it){items[it.dataset.id]={n:it.dataset.n,p:+it.dataset.p,u:it.dataset.u,el:it}});
    function render(){
      var ul=$('#cart-list'),sum=0,cnt=0,h='';
      Object.keys(cart).forEach(function(id){var q=cart[id],x=items[id];if(!q)return;sum+=q*x.p;cnt+=q;h+='<li><span>'+q+' × '+x.n+'</span><b>'+zl(q*x.p)+'</b></li>'});
      ul.innerHTML=h||'<li class="empty">Dodaj pozycje z menu przyciskiem +</li>';
      $('#cart-sum').textContent=zl(sum);
      var note=$('#cart-note');
      if(!sum){note.className='note';note.textContent='Dowóz do 5 km gratis przy zamówieniu od 300 zł.'}
      else if(sum>=300){note.className='note ok';note.textContent='Dowóz do 5 km gratis – zamówienie przekracza 300 zł.'}
      else{note.className='note';note.textContent='Brakuje '+zl(300-sum)+' do darmowego dowozu (do 5 km). Odbiór własny – bez dopłaty.'}
      $$('.item',cat).forEach(function(it){var q=cart[it.dataset.id]||0;$('.qty span',it).textContent=q;it.classList.toggle('in',q>0)});
      var bar=$('.cart-bar');if(bar){bar.classList.toggle('on',cnt>0);$('b',bar).textContent=zl(sum)}
      $$('.cart [data-send]').forEach(function(b){b.toggleAttribute('disabled',!sum);b.style.opacity=sum?1:.45});
      return sum;
    }
    cat.addEventListener('click',function(e){
      var b=e.target.closest('.qty button');if(!b)return;
      var id=b.closest('.item').dataset.id;cart[id]=Math.max(0,(cart[id]||0)+(b.dataset.d==='+'?1:-1));render();
    });
    function text(){
      var t='Dzień dobry, chcę zamówić catering:\n';
      Object.keys(cart).forEach(function(id){if(cart[id])t+='- '+cart[id]+' × '+items[id].n+' ('+items[id].u+')\n'});
      t+='Razem wg cennika: '+$('#cart-sum').textContent+'\n';
      var dt=$('#c-date').value,how=$('#c-how').value;
      t+='Termin: '+(dt||'do ustalenia')+'\nOdbiór: '+how+'\n';
      return t;
    }
    $$('.cart [data-send]').forEach(function(b){b.addEventListener('click',function(){
      if(!render())return;
      var t=text();
      if(b.dataset.send==='sms')location.href='sms:'+TEL+'?body='+encodeURIComponent(t);
      else location.href='mailto:'+MAIL+'?subject='+encodeURIComponent('Zamówienie cateringu')+'&body='+encodeURIComponent(t);
    })});
    var cd=$('#c-date');
    if(cd){
      cd.min=new Date(Date.now()+864e5).toISOString().slice(0,10);
      cd.addEventListener('change',function(){
        var h=$('#c-hint');if(!cd.value){h.classList.remove('on');return}
        var t=new Date(cd.value+'T12:00:00'),wd=t.getDay();
        var back=(wd+7-3)%7; if(back===0)back=7;
        var wed=new Date(t);wed.setDate(t.getDate()-back);
        var today=new Date();today.setHours(0,0,0,0);
        var f='środy, '+wed.toLocaleDateString('pl-PL',{day:'numeric',month:'long'});
        h.innerHTML=(wed<today?'<b>Termin zamówień minął</b> – zamówienia na ten dzień przyjmowaliśmy do '+f+'. Zadzwoń, sprawdzimy, czy da się jeszcze coś zrobić.':'Zamówienie na ten dzień złóż najpóźniej do <b>'+f+'</b>.');
        h.classList.add('on');
      });
    }
    render();
  }

  /* formularz zapytania o termin */
  var q=$('#zapytanie form');
  if(q){
    var ps=new URLSearchParams(location.search);
    if(ps.get('okazja')&&q.okazja)q.okazja.value=ps.get('okazja');
    if(ps.get('goscie')&&q.goscie)q.goscie.value=ps.get('goscie');
    var dt=q.data;
    if(dt){
      dt.min=new Date().toISOString().slice(0,10);
      dt.addEventListener('change',function(){
        var h=$('#t-hint',q.parentNode);if(!dt.value){h.classList.remove('on');return}
        var t=new Date(dt.value+'T12:00:00'),m=t.getMonth(),wd=t.getDay();
        var day=t.toLocaleDateString('pl-PL',{weekday:'long',day:'numeric',month:'long',year:'numeric'});
        var months=Math.round((t-new Date())/(864e5*30.44));
        var s='<b>'+day.charAt(0).toUpperCase()+day.slice(1)+'</b> – za ok. '+(months<1?'kilka tygodni':months+' mies.')+(months<1?'. ':' ');
        if(wd===6&&m>=4&&m<=8)s+='To sobota w sezonie weselnym: takie terminy rozchodzą się zwykle 12–18 miesięcy wcześniej, warto zapytać od razu.';
        else if(wd===5||m<4||m>8)s+='Piątki i terminy poza sezonem są zwykle dostępne z krótszym wyprzedzeniem, często w niższej cenie.';
        else s+='Potwierdzimy dostępność telefonicznie lub mailowo.';
        h.innerHTML=s;h.classList.add('on');
      });
    }
    q.addEventListener('submit',function(e){
      e.preventDefault();
      var msg=$('.form-msg',q);
      if(!q.imie.value.trim()||!(q.tel.value.trim()||q.email.value.trim())){msg.className='form-msg on err';msg.textContent='Podaj imię i telefon albo e-mail – odezwiemy się z odpowiedzią.';return}
      if(!q.zgoda.checked){msg.className='form-msg on err';msg.textContent='Zaznacz zgodę na kontakt w sprawie zapytania.';return}
      msg.className='form-msg on ok';
      msg.textContent='Dziękujemy, '+q.imie.value.trim()+'. Odezwiemy się w godzinach pracy biura. (Wersja demonstracyjna – formularz jeszcze nie wysyła wiadomości.)';
      q.reset();var h=$('#t-hint',q.parentNode);if(h)h.classList.remove('on');
    });
  }
})();
