#!/usr/bin/env python3
"""Builds the Steal My Itinerary pages for finessehumxn.com.
Add a city: copy the LIMA dict, change the data, add it to TRIPS, re-run.
"""
import html, os

OUT = "site"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">')

def head(title, desc, canon, css="itinerary.css"):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="canonical" href="{canon}" />
{FONTS}
<link rel="stylesheet" href="{css}">
</head>
<body>'''

NAV = '''
<nav class="site">
  <div class="nav-inner">
    <a href="index.html" class="logo">L.<em>Finesse</em> Humxn</a>
    <div class="nav-links">
      <a href="workshop.html">Workshop</a>
      <a href="learn.html">Learn</a>
      <a href="itinerary.html" class="on">Cities</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    </div>
    <a href="contact.html" class="btn-book">Book Me</a>
    <div class="ham" onclick="toggleNav()"><span></span><span></span><span></span></div>
  </div>
</nav>
<div class="mob-menu" id="mobMenu">
  <a href="workshop.html" class="mm-a">Free Workshop</a>
  <a href="learn.html" class="mm-a">Learn</a>
  <a href="itinerary.html" class="mm-a">Cities I Work In</a>
  <a href="about.html" class="mm-a">About</a>
  <a href="contact.html" class="mm-a">Contact</a>
  <a href="contact.html" class="mm-book">Book or Hire Me</a>
</div>'''

FOOT = r'''
<footer>
  <div class="ft">
    <div class="fl">L.<em>Finesse</em> Humxn</div>
    <div class="flinks">
      <a href="workshop.html">Free Workshop</a>
      <a href="learn.html">Learn</a>
      <a href="itinerary.html">Cities I Work In</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
      <a href="https://millennialscreatives.com" target="_blank">Millennials Creatives</a>
    </div>
  </div>
  <p class="fnote">Hours, prices and phone numbers were verified at the time of writing and change without warning. Call ahead for anything you are counting on.</p>
  <p class="fcopy">&#169; 2026 L.Finesse Humxn &#183; Millennials Creatives LLC &#183; California &#183; HQ: Phoenix, AZ &#183; contact@millennialscreatives.com</p>
</footer>
<script>
function toggleNav(){document.getElementById('mobMenu').classList.toggle('open');}
document.querySelectorAll('.mm-a,.mm-book').forEach(function(e){e.addEventListener('click',function(){document.getElementById('mobMenu').classList.remove('open');});});
</script>
<script>
(function(){
  var RATE=3.37, bar=document.getElementById('planbar');
  if(!bar) return;
  var stops=[].slice.call(document.querySelectorAll('.stop')),
      filters={hard:false,splurge:false,book:false}, types=[], cur='both';
  var FEEDBACK_TO='contact@millennialscreatives.com';

  function save(){try{localStorage.setItem('smi_lima',JSON.stringify({
    f:filters,t:types,c:cur,st:stops.map(function(s){return s.dataset.status||'';}),off:stops.map(function(s,i){return s.querySelector('.pk')&&!s.querySelector('.pk').checked?i:-1;}).filter(function(i){return i>=0;})
  }));}catch(e){}}
  function load(){try{var d=JSON.parse(localStorage.getItem('smi_lima')||'null');if(!d)return;
    if(d.f)filters=d.f; if(d.t)types=d.t; if(d.c)cur=d.c;
    (d.st||[]).forEach(function(v,i){
      if(!v||!stops[i])return;
      stops[i].dataset.status=v;
      var b=stops[i].querySelector('.st[data-s="'+v+'"]'); if(b)b.classList.add('on');
    });
    (d.off||[]).forEach(function(i){var b=stops[i]&&stops[i].querySelector('.pk');if(b)b.checked=false;});
  }catch(e){}}

  function money(pen){
    var usd='$'+Math.round(pen/RATE);
    if(cur==='usd') return usd;
    if(cur==='pen') return 'S/'+pen;
    return 'S/'+pen+' ('+usd+')';
  }

  function applyCurrency(){
    document.querySelectorAll('.strip dd').forEach(function(d){
      if(!d.dataset.orig) d.dataset.orig=d.innerHTML;
      var t=d.dataset.orig;
      if(cur==='pen'){
        // drop the parenthetical dollars, keep the local price
        d.innerHTML=t.replace(/\s*\(\$[^)]*\)/g,'');
      } else if(cur==='usd'){
        // prefer the dollar figure already written beside the soles
        t=t.replace(/S\/[\d.,]+(?:\s*(?:to|a)\s*[\d.,]+)?\+?\s*\((\$[^)]*)\)/g,'$1');
        // convert anything still left in soles
        t=t.replace(/S\/(\d+(?:\.\d+)?)/g,function(m,n){
          return '$'+(Math.round(parseFloat(n)/RATE*100)/100).toFixed(2).replace(/\.00$/,'');});
        d.innerHTML=t;
      } else { d.innerHTML=t; }
    });
  }

  function render(){
    var n=0,c=0;
    stops.forEach(function(s){
      var tags=(s.dataset.tags||'').split(' ').filter(Boolean),
          fixed=s.dataset.fixed==='1',
          box=s.querySelector('.pk');
      var hidden=false;
      if(filters.hard && tags.indexOf('hard')>=0) hidden=true;
      if(filters.splurge && tags.indexOf('splurge')>=0) hidden=true;
      if(filters.book && !fixed && tags.indexOf('book')<0) hidden=true;
      if(types.length && !fixed && types.indexOf(s.dataset.type||'')<0) hidden=true;
      s.classList.toggle('dim',hidden);
      var inPlan = !hidden && (fixed || (box && box.checked));
      if(inPlan && !fixed){ n++; c+=parseInt(s.dataset.cost||0,10); }
    });
    var done=0,total=0;
    stops.forEach(function(s){
      if(s.dataset.fixed==='1') return;
      total++;
      if(s.dataset.status==='did') done++;
    });
    document.getElementById('pcount').textContent=n;
    document.getElementById('pcost').textContent=money(c);
    document.getElementById('pdone').textContent=done+' of '+total;
    save();
  }

  document.querySelectorAll('.cb[data-f]').forEach(function(b){
    b.addEventListener('click',function(){
      filters[b.dataset.f]=!filters[b.dataset.f];
      b.classList.toggle('on',filters[b.dataset.f]); render();
    });
  });
  document.querySelectorAll('.cb[data-t]').forEach(function(b){
    b.addEventListener('click',function(){
      var t=b.dataset.t, i=types.indexOf(t);
      if(i>=0) types.splice(i,1); else types.push(t);
      b.classList.toggle('on',types.indexOf(t)>=0); render();
    });
  });
  document.querySelectorAll('.cb[data-cur]').forEach(function(b){
    b.addEventListener('click',function(){
      cur=b.dataset.cur;
      document.querySelectorAll('.cb[data-cur]').forEach(function(x){x.classList.toggle('on',x===b);});
      applyCurrency(); render();
    });
  });
  document.addEventListener('change',function(e){ if(e.target.classList.contains('pk')) render(); });

  document.addEventListener('click',function(e){
    var b=e.target.closest('.st'); if(!b) return;
    var stop=b.closest('.stop'), v=b.dataset.s;
    var now = stop.dataset.status===v ? '' : v;
    stop.dataset.status=now;
    stop.querySelectorAll('.st').forEach(function(x){x.classList.toggle('on',x.dataset.s===now);});
    render();
  });

  document.getElementById('rst').addEventListener('click',function(){
    filters={hard:false,splurge:false,book:false}; types=[]; cur='both';
    document.querySelectorAll('.cb[data-f],.cb[data-t]').forEach(function(b){b.classList.remove('on');});
    document.querySelectorAll('.cb[data-cur]').forEach(function(b){b.classList.toggle('on',b.dataset.cur==='both');});
    document.querySelectorAll('.pk').forEach(function(b){b.checked=true;});
    applyCurrency(); render();
  });

  document.getElementById('pcopy').addEventListener('click',function(){
    var out=[],btn=this;
    document.querySelectorAll('.day').forEach(function(d){
      var lines=[];
      d.querySelectorAll('.stop').forEach(function(s){
        if(s.classList.contains('dim')) return;
        var box=s.querySelector('.pk');
        if(box && !box.checked) return;
        lines.push('  '+s.querySelector('.time b').textContent.trim()+'  '+
                   s.querySelector('h3').childNodes[0].textContent.trim()+
                   '  ('+s.querySelector('.where').textContent.trim()+')');
      });
      if(lines.length) out.push(d.querySelector('h2').textContent.trim().toUpperCase()+'\n'+lines.join('\n'));
    });
    var txt='MY LIMA PLAN\n\n'+out.join('\n\n')+'\n\nRoughly '+
            document.getElementById('pcost').textContent+' per person.\nfinessehumxn.com';
    function done(){btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy my plan';},1800);}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(done,done);}
    else{var t=document.createElement('textarea');t.value=txt;document.body.appendChild(t);t.select();
         try{document.execCommand('copy');}catch(e){} document.body.removeChild(t); done();}
  });

  function stopName(s){ return s.querySelector('h3').childNodes[0].textContent.trim(); }

  document.getElementById('psend').addEventListener('click',function(){
    var did=[],chg=[],skp=[],btn=this;
    stops.forEach(function(s){
      var v=s.dataset.status; if(!v) return;
      var line='- '+stopName(s);
      if(v==='did') did.push(line);
      else if(v==='changed') chg.push(line);
      else if(v==='skipped') skp.push(line);
    });
    if(!did.length && !chg.length && !skp.length){
      btn.textContent='Mark a few stops first';
      setTimeout(function(){btn.textContent='Send me your notes';},2200); return;
    }
    var b='I used the Lima itinerary. Here is how it went.\n\n';
    if(did.length) b+='WORKED\n'+did.join('\n')+'\n\n';
    if(chg.length) b+='CHANGED, and what I did instead\n'+chg.join('\n')+'\n\n';
    if(skp.length) b+='SKIPPED\n'+skp.join('\n')+'\n\n';
    b+='Anything that was wrong, closed, or better than described:\n\n\n';
    b+='---\nSent from finessehumxn.com';
    var sub='Lima itinerary notes';
    var href='mailto:'+FEEDBACK_TO+'?subject='+encodeURIComponent(sub)+'&body='+encodeURIComponent(b);
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(b);}
    window.location.href=href;
    btn.textContent='Opening your email';
    setTimeout(function(){btn.textContent='Send me your notes';},2600);
  });

  document.getElementById('ppdf').addEventListener('click',function(){
    stops.forEach(function(s){
      var box=s.querySelector('.pk');
      s.classList.toggle('off', !!(box && !box.checked));
    });
    window.print();
  });
  window.addEventListener('afterprint',function(){
    stops.forEach(function(s){ s.classList.remove('off'); });
  });

  load();
  document.querySelectorAll('.cb[data-f]').forEach(function(b){b.classList.toggle('on',!!filters[b.dataset.f]);});
  document.querySelectorAll('.cb[data-t]').forEach(function(b){b.classList.toggle('on',types.indexOf(b.dataset.t)>=0);});
  document.querySelectorAll('.cb[data-cur]').forEach(function(b){b.classList.toggle('on',b.dataset.cur===cur);});
  applyCurrency(); render();
})();
</script>
</body>
</html>'''

def ticker(items):
    row = "".join('<span class="tick">%s</span>' % i for i in items)
    return '<div class="ticker"><div class="ticker-t">%s%s</div></div>' % (row, row)


# Official first-party links only. No aggregators, no resellers, no affiliate rails.
# "social" marks a venue that genuinely has no website of its own.
LINKS = {
 "Delta One, ATL to LIM":("https://www.delta.com/us/en/onboard/onboard-experience/delta-one",""),
 "Getting out of the airport":("https://www.lima-airport.com/en",""),
 "Aloft Lima Miraflores":("https://www.marriott.com/en-us/hotels/limra-aloft-lima-miraflores/overview/",""),
 "KFC, and the delivery app problem":("https://www.rappi.com.pe/",""),
 "Helarte":("https://www.helarte.com.pe/",""),
 "Huaca Pucllana":("https://museos.cultura.pe/museos/museo-de-sitio-pucllana",""),
 "Al Toke Pez":("https://www.facebook.com/ALTOKEPEZ/","social"),
 "Circuito M&#225;gico del Agua":("https://www.circuitomagicodelagua.com.pe/",""),
 "Clon":("https://www.clonrest.com/",""),
 "Machu Picchu, the Lima version":("https://leyendas.gob.pe/",""),
 "Dansa":("https://www.instagram.com/dansa.peru/","social"),
 "ChocoMuseo workshop":("https://chocomuseo.com/",""),
 "Horneando Ando":("https://www.instagram.com/horneandoando110a/","social"),
 "Larcomar and the malec&#243;n":("https://www.larcomar.com/",""),
 "Astrid y Gast&#243;n":("https://www.astridygaston.com/",""),
 "WeWork Jos&#233; Larco":("https://www.wework.com/buildings/jose-larco-1232--lima",""),
 "Ra&#237;z Coffee":("https://www.facebook.com/RaizCoffeeoficial/","social"),
 "Terrua Caf&#233;":("https://terruacafe.com",""),
}


# Every trip is three trips. This tags which one each stop belongs to.
TYPES = {
 "La Mar Cebicher&#237;a":"leisure",
 "Huaca Pucllana":"leisure",
 "Terrua Caf&#233;":"adventure",
 "Ursa Coffee Roasters":"leisure",
 "Ra&#237;z Coffee":"leisure",
 "Breakfast at the hotel":"leisure",
 "WeWork Jos&#233; Larco":"work",
 "Street interviews, Miraflores":"work",
 "Finesse Our Minds, on the road":"work",
 "Millennials Creatives connections":"work",
 "Huaca Pucllana":"leisure",
 "Al Toke Pez":"adventure",
 "Barranco on foot":"adventure",
 "Circuito M&#225;gico del Agua":"leisure",
 "Clon":"leisure",
 "Machu Picchu, the Lima version":"adventure",
 "La Mar Cebicher&#237;a":"leisure",
 "Dansa":"leisure",
 "ChocoMuseo workshop":"adventure",
 "Inka Market":"leisure",
 "Horneando Ando":"adventure",
 "Larcomar and the malec&#243;n":"leisure",
 "Astrid y Gast&#243;n":"leisure",
 "Helarte":"leisure",
 "Plaza Norte":"leisure",
}
TYPE_LABEL = {"work":"Work","leisure":"Leisure","adventure":"Adventure"}

# name -> (cost per person in soles, tags)
# tags: hard = physically demanding, splurge = over S/100, book = needs a reservation
META = {
 "La Mar Cebicher&#237;a":(120,["splurge"]),
 "Breakfast, then go":(0,[]),
 "Car to the airport":(57,[]),
 "Hotel, pack, reset":(0,[]),
 "Terrua Caf&#233;":(84,["book"]),
 "Ursa Coffee Roasters":(25,[]),
 "Ra&#237;z Coffee":(30,[]),
 "Breakfast at the hotel":(0,[]),
 "WeWork Jos&#233; Larco":(0,[]),
 "Street interviews, Miraflores":(0,[]),
 "Finesse Our Minds, on the road":(0,[]),
 "Millennials Creatives connections":(60,[]),
 "Getting out of the airport":(57,[]),
 "KFC, and the delivery app problem":(40,[]),
 "Helarte":(25,[]),
 "Plaza Norte":(0,[]),
 "Huaca Pucllana":(15,[]),
 "Al Toke Pez":(30,["hard"]),
 "Barranco on foot":(0,["hard"]),
 "Circuito M&#225;gico del Agua":(4,[]),
 "Clon":(150,["splurge","book"]),
 "Machu Picchu, the Lima version":(26,["hard"]),
 "La Picanter&#237;a":(120,["splurge"]),
 "Dansa":(300,["splurge","book"]),
 "ChocoMuseo workshop":(115,["splurge","book"]),
 "Inka Market":(100,[]),
 "Horneando Ando":(90,["book"]),
 "Larcomar and the malec&#243;n":(0,[]),
 "Astrid y Gast&#243;n":(200,["splurge","book"]),
}

def stop(s):
    cost, tags = META.get(s["name"], (0, []))
    skip = s["kind"] in ("Do not skip", "Mandatory", "Base camp", "The flight", "Learn from this")
    typ = TYPES.get(s["name"], "")
    o = ['<article class="stop" data-cost="%d" data-tags="%s" data-type="%s"%s>'
         % (cost, " ".join(tags), typ, ' data-fixed="1"' if skip else '')]
    word = not s["t"][0].isdigit()
    o.append('<div class="time%s"><b>%s</b>%s</div>'
             % (" word" if word else "", s["t"], ('<span>%s</span>' % s["ap"]) if s["ap"] else ""))
    o.append('<div class="in">')
    if not skip:
        o.append('<div class="track">'
                 '<label class="pick"><input type="checkbox" class="pk" checked><span>In my plan</span></label>'
                 '<div class="status">'
                 '<button class="st" data-s="did" type="button">Did it</button>'
                 '<button class="st" data-s="changed" type="button">Changed it</button>'
                 '<button class="st" data-s="skipped" type="button">Skipped</button>'
                 '</div></div>')
    url, kindof = LINKS.get(s["name"], ("", ""))
    nm = ('<a class="dlink" href="%s" target="_blank" rel="noopener">%s<span class="ext">&#8599;</span></a>'
          % (url, s["name"])) if url else s["name"]
    o.append('<h3>%s<span class="kind">%s</span></h3>' % (nm, s["kind"]))
    if url and kindof == "social":
        o.append('<p class="lnote">No website of their own. That link goes to their own page, not a booking site.</p>')
    lab = {"hard":"Physically demanding","splurge":"Splurge","book":"Needs booking"}
    chips = ['<span class="tg ty-%s">%s</span>' % (typ, TYPE_LABEL[typ])] if typ else []
    chips += ['<span class="tg %s">%s</span>' % (t, lab[t]) for t in tags]
    if chips:
        o.append('<div class="tags">%s</div>' % "".join(chips))
    o.append('<p class="where">%s</p>' % s["where"])
    o.append('<p class="pitch">%s</p>' % s["pitch"])
    if s.get("strip"):
        o.append('<dl class="strip">')
        for k, v in s["strip"]:
            o.append('<div><dt>%s</dt><dd>%s</dd></div>' % (k, v))
        o.append('</dl>')
    if s.get("mi") is not None:
        pct = min(100, max(0, s["mi"] / 8.0 * 100))
        o.append('<div class="radius"><div class="track"><div class="dot" style="left:%.0f%%"></div></div>'
                 '<div class="scale"><span>0 MI</span><span>4</span><span>8 MI</span></div></div>' % pct)
    if s.get("notes"):
        o.append('<div class="notes">')
        for cls, lbl, txt in s["notes"]:
            o.append('<div class="note %s"><b>%s</b><p>%s</p></div>' % (cls, lbl, txt))
        o.append('</div>')
    o.append('</div></article>')
    return "".join(o)

def day(d):
    o = ['<section class="day%s" id="%s">' % (" today" if d.get("today") else "", d["id"])]
    o.append('<div class="dayhead%s"><div class="daynum">%s</div>%s<h2>%s</h2>'
             % (" istoday" if d.get("today") else "", d["num"],
                '<span class="todaytag">You are here</span>' if d.get("today") else "", d["title"]))
    o.append('<p class="daywhen">%s</p>' % d["when"])
    o.append('<div class="daynote">%s</div></div>' % d["note"])
    o.append('<div class="stops">%s</div>' % "".join(stop(s) for s in d["stops"]))
    o.append('</section>')
    return "".join(o)


# ============================== LIMA ==============================
LIMA = {
 "slug":"lima",
 "title":"Lima by the Mile | Steal My Itinerary",
 "desc":"Five days in Lima, Peru with my parents, August 30 to September 3, ranked by distance from the hotel. Real prices in soles, what to order at every restaurant, fun facts and the things nobody tells you.",
 "canon":"https://finessehumxn.com/lima.html",
 "eyebrow":"Lima, Peru &#183; Work &#183; Leisure &#183; Adventure",
 "h1":'<em>Lima</em><br><strong>by the Mile.</strong>',
 "ledes":[
   'August 30 to September 3. California to Atlanta to Lima on Delta One, one hotel we walked out of, and then five days built on a single question. <strong>How far is it from the bed, and is it worth the drive.</strong>',
   'Distance from the Aloft on Av. 28 de Julio, drive time, what it costs, what to order by name, and the one thing nobody tells you before you go. Thirty two stops. One ruined pyramid you can eat dinner next to. One food delivery app that does not work here and will catch you out on night one.',
 ],
 "ticker":["Lima, Peru","Aug 30 to Sep 3","5 Days","30 Stops","Delta One via ATL","Base: Aloft Miraflores","Furthest 9 mi","Closest 0.4 mi","S/3.37 to $1","Sea Level","Sunset 6:04 PM","Traveling with parents","No UberEats in Peru","Use Rappi","Garua season","Order this","Fun fact","Must know"],
 "proof":[("5","Days<br>On the Ground"),("30","Stops<br>Logged"),("9.0","Furthest<br>Miles Out"),("0.4","Closest<br>Miles Out"),("60","Longest<br>Drive, Min"),("S/4","Cheapest<br>Ticket")],
 "days":[
  {"id":"d1","num":"01","title":"Landing","when":"Sunday, August 30 &#183; <strong>California to Atlanta to Lima</strong> &#183; the day you lose to travel, and the hotel mistake",
   "note":"Every trip has a day that is not really a day. This was ours. It is on here anyway, because the two things that went wrong on it are the two things I would tell anyone flying into Lima.",
   "stops":[
    {"t":"All day","ap":"","name":"Delta One, ATL to LIM","kind":"The flight","where":"California to Atlanta to Jorge Ch&#225;vez International","mi":None,
     "pitch":"Two legs. West coast to Atlanta, then Atlanta straight down to Lima. Delta One is the lie flat cabin, which matters more than usual on this route because the Lima leg lands you into a full day you are expected to function in.",
     "strip":[("Route","CA &#8594; ATL &#8594; LIM"),("Cabin","Delta One"),("Arrives","Jorge Ch&#225;vez, LIM"),("Time zone","Same as US Central")],
     "notes":[("f","Fun fact","Lima runs on UTC-5 year round with no daylight saving, so from the west coast it is only a two hour shift. There is no real jet lag on this trip. What wrecks you is the flight length, not the clock."),
              ("k","Must know","Jorge Ch&#225;vez opened an entirely new terminal in June 2025 and it is still shaking out the kinks. Build a real buffer on connections, and check your flight status the night before and the morning of.")]},
    {"t":"On arrival","ap":"","name":"Getting out of the airport","kind":"Transport","where":"Jorge Ch&#225;vez International to Miraflores","mi":None,
     "pitch":"Roughly 45 to 90 minutes to Miraflores depending on traffic. Here is the part worth writing down: the hotel desk quoted us about <strong>$35 for a taxi</strong>. The Uber was about <strong>$17</strong> for the same ride. Same road, same traffic, half the money.",
     "strip":[("To Miraflores","45 to 90 min"),("Taxi, quoted","S/118 ($35)"),("Uber, actual","S/57 ($17)"),("Shuttle","S/15 ($4.40) each")],
     "notes":[("o","Do this","Take the Uber. It picks up from the designated zone at Parking E1, not curbside, so walk out and follow the signs rather than standing at arrivals wondering why nobody is coming. Cabify works the same way."),
              ("f","Fun fact","Nearly every quote you get at a desk or counter is priced for someone who has not opened the app yet. It is not a scam, it is just the tourist rate, and it roughly doubles the fare on this exact route."),
              ("k","Must know","If you do want a taxi, use the staffed counters inside Arrivals and confirm the fare is <strong>todo incluido</strong> before getting in. Never take a ride from someone who approaches you outside Arrivals. That is the one real scam at this airport and it runs constantly.")]},
    {"t":"Night","ap":"","name":"The Wyndham by the airport","kind":"Honest review","where":"Beside Jorge Ch&#225;vez, Callao","mi":None,
     "pitch":"We booked it for the arrival night on the theory that landing tired and walking straight to a bed was the smart play. <strong>The service was genuinely good and the room was not.</strong> Both of those things are true and it would be unfair to only say one of them.",
     "strip":[("Shuttle","Free, every 30 min"),("Welcome drink","Included"),("Restaurant","24 hours"),("Breakfast","Free buffet")],
     "notes":[("o","What was actually good","A free airport shuttle every thirty minutes, a welcome drink on arrival, a restaurant open around the clock, and a free buffet breakfast we absolutely took advantage of before we left. For an airport hotel that is a real package, and the staff were fine."),
              ("k","Why we left anyway","The room was old in the way you feel rather than see in photos. Rust, a smell, and that sticky, been-here-too-long surface feel. After two flights and a full travel day, that is the wrong first night. We ate the free breakfast and got out on the next thing smoking."),
              ("f","The honest verdict","Worth it for a genuine few-hour layover, where the shuttle and the 24 hour kitchen are the whole point. Not worth it as the first night of a real trip. A late arrival is not a reason to stay near the airport. Take the 45 minute ride and wake up in Miraflores.")]},
    {"t":"Dinner","ap":"","name":"KFC, and the delivery app problem","kind":"The lesson","where":"Ordered in","mi":None,
     "pitch":"First night in one of the great food cities on earth and we ate KFC in a hotel room. That is what a travel day does to you, and there is no shame in it. What there is, is a logistics lesson nobody warns you about.",
     "strip":[("UberEats","Does not exist in Peru"),("Uber rides","Works fine"),("Use instead","Rappi"),("Or","PedidosYa")],
     "notes":[("k","Must know","<strong>UberEats does not operate in Peru.</strong> Uber for rides works perfectly, which is exactly why this catches people out. For food delivery you need <strong>Rappi</strong> or <strong>PedidosYa</strong>. Download both at the airport while you still have wifi, before you are hungry and stuck."),
              ("o","Do this","Rappi is the one that covers the most restaurants in Lima and it also delivers groceries and pharmacy items. Set it up first. PedidosYa is the backup when a place is not on Rappi.")]},
   ]},
  {"id":"d2","num":"02","title":"Ice Cream and a Long Drive","when":"Monday, August 31 &#183; <strong>out of Callao, into Miraflores</strong> &#183; 0.4 miles, then 9",
   "note":"The day we got out of the airport district and into the hotel every distance on this page is measured from. A short day with a useful lesson buried in it. The best stop was four tenths of a mile away. The longest drive was to a shopping mall.",
   "stops":[
    {"t":"Midday","ap":"","name":"Aloft Lima Miraflores","kind":"Base camp","where":"Av. 28 de Julio 894, Miraflores","mi":0.0,
     "pitch":"This is the anchor for the whole trip. Miraflores is flat, walkable, well lit, and close to almost everything worth eating. Every mile figure on this page is measured from this front door.",
     "strip":[("From airport","45 to 90 min"),("District","Miraflores"),("To the cliffs","0.9 mi"),("To Barranco","2.2 mi")],
     "notes":[("o","Do this","If you are choosing a base in Lima, choose Miraflores. Barranco is more beautiful and better at night. San Isidro is quieter and emptier. Miraflores is the one that makes every other day shorter."),
              ("k","Must know","Ask for a room away from Av. 28 de Julio if you are a light sleeper. It is a real road.")]},
    {"t":"Afternoon","ap":"","name":"Helarte","kind":"Ice cream","where":"Calle Bol&#237;var 205, Miraflores","mi":0.4,
     "pitch":"Artisanal ice cream, waffles and cakes in a room built to be photographed. Nine minutes from the lobby and open until ten at night, which quietly makes it the default answer to any evening that ends early.",
     "strip":[("From Aloft","0.4 mi"),("Walk","9 min"),("Open","Daily, 8 AM to 10 PM"),("Price","Cheap")],
     "notes":[("o","Order this","<strong>L&#250;cuma.</strong> It is a native Peruvian fruit that tastes like maple and sweet potato had a very good idea, and it does not really exist outside the Andes. Chirimoya and algarrobina are the other two to try."),
              ("f","Fun fact","L&#250;cuma has been eaten in Peru for thousands of years and shows up painted on Moche pottery. It is on ice cream menus in Lima the way vanilla is everywhere else.")]},
    {"t":"Afternoon","ap":"","name":"Plaza Norte","kind":"Mall","where":"Av. Alfredo Mendiola 1400, Independencia","mi":9.0,
     "pitch":"One of the largest malls in Lima, about 200,000 square meters, up in Independencia in the north of the city. Nine miles from the hotel and close to an hour each way in traffic.",
     "strip":[("From Aloft","9.0 mi"),("Drive","~60 min"),("Open","Daily, mall hours"),("Cost","Free entry")],
     "notes":[("k","Must know","<strong>Two hours of driving for a mall.</strong> If you want a mall in Lima, Larcomar is on a cliff over the Pacific and it is 0.9 miles from Miraflores. Plaza Norte is bigger and more local, but the drive is the whole story and I would not do it twice."),
              ("f","Fun fact","Plaza Norte sits next to one of Lima's biggest bus terminals, which is why it is enormous. It is built for the whole north of the city, not for visitors staying in Miraflores.")]},
   ]},
  {"id":"d3","num":"03","title":"Coffee and the Work Half","today":True,"when":"Tuesday, September 1 &#183; <strong>today</strong> &#183; breakfast at 7:30, then a coffee loop: a roastery, a 90 minute tasting, and one of the best coffee bars in South America",
   "note":"Three coffee stops before anything else, all inside half a mile of the lobby and all one walking loop. Then the other trip starts. I do not fly anywhere and only be on vacation. <strong>September is Suicide Prevention Month,</strong> which is not a coincidence for when this trip landed.",
   "stops":[
    {"t":"7:30","ap":"AM","name":"Breakfast at the hotel","kind":"Start easy","where":"Aloft, Av. 28 de Julio 894","mi":0.0,
     "pitch":"Eat here, then walk out for the coffee. Doing it the other way around means queuing for a table on an empty stomach with two people who did not sign up for that.",
     "strip":[("From Aloft","0.0 mi"),("Time","7:30 AM"),("Then","Coffee, on foot"),("Cost","Included")]},
    {"t":"9:00","ap":"AM","name":"Ursa Coffee Roasters","kind":"The technical one","where":"Alcanfores 183, Miraflores","mi":0.3,
     "pitch":"A roastery as much as a caf&#233;, and the one Lime&#241;os send you to when they want to show off what Peruvian coffee can actually do. Complex, deliberate, and run by people who will happily talk you through the method if you ask.",
     "strip":[("From Aloft","0.3 mi"),("Walk","6 min"),("Open","Daily, about 7 to 7"),("Price","Cheap")],
     "notes":[("o","Order this","A <strong>pour over</strong>, not an espresso drink. That is the whole reason to come here, and ask which origin they are pouring today. If it is hot, the cold brew is the other thing they are known for."),
              ("f","Fun fact","Peru is one of the largest exporters of organic coffee on earth, and for decades almost all the good beans left the country. Roasteries like this one keeping the best lots at home is a genuinely recent change."),
              ("k","Must know","They run tastings and brewing workshops. Ask at the counter whether anything is on while you are in town. It is the kind of thing that turns a coffee into a morning.")]},
    {"t":"10:00","ap":"AM","name":"Terrua Caf&#233;","kind":"The tasting","where":"Pasaje Tello 163, Miraflores","mi":0.5,
     "pitch":"Ninety minutes with people who actually know Peruvian coffee, tucked down a passage off Larco behind Parque Kennedy. You go through the history, the farms, harvesting, and how fermentation builds flavour, then watch a V60 poured properly and taste the same coffee three ways: espresso, Americano and cold brew. This is the stop that turns the other two into something you understand.",
     "strip":[("From Aloft","0.5 mi"),("Walk","10 min"),("Length","90 minutes"),("Price","S/84 ($25) each")],
     "notes":[("o","Book this now","Direct: <strong>terruacafe.com</strong> or call <strong>+51 989 307 864.</strong> It caps at ten people per session and runs in English or Spanish, so say which you want when you book. Ask for English if you want your parents to follow every step."),
              ("f","Fun fact","Tasting the same coffee as espresso, Americano and cold brew side by side is the fastest way to understand that brewing method changes flavour more than most people believe. Same beans, three genuinely different drinks."),
              ("k","Must know","No food included, so breakfast at the hotel is doing real work here. You can buy beans at the end, and this is the one souvenir from Lima that is genuinely better than anything at the market. Private sessions are available if you would rather not share the table.")]},
    {"t":"11:45","ap":"AM","name":"Ra&#237;z Coffee","kind":"The famous one","where":"Calle Porta 152, Miraflores","mi":0.5,
     "pitch":"Named among the top coffee shops in South America, and somehow still a small neighbourhood room on Calle Porta with good light and cozy seating. Four minutes from Terrua, so it is the sit down at the end of the loop rather than a separate trip.",
     "strip":[("From Aloft","0.5 mi"),("Walk","10 min"),("Open","Mon to Sat 7 to 8:30"),("Sunday","Opens 8 AM")],
     "notes":[("o","Order this","The <strong>cortado</strong> is what it is known for, and the chai latte is the surprise. On the pastry side, the carrot cake and the cheese and jam croissant are the two people come back for."),
              ("k","Must know","<strong>This is your third coffee of the morning.</strong> Order a chai latte or something without caffeine here if anyone has had enough, and come for the carrot cake rather than another cortado. Small room that fills up, but by noon the mid morning crowd has cleared.")]},
    {"t":"Midday","ap":"","name":"WeWork Jos&#233; Larco","kind":"The desk","where":"Av. Jos&#233; Larco 1232, Miraflores","mi":0.6,
     "pitch":"One membership, and a desk in almost every city I land in. Lima has locations in Miraflores and two in San Isidro, and walking into a WeWork in a country you have never worked in is quietly one of the best parts of this job. Same login, completely different room.",
     "strip":[("From Aloft","0.6 mi"),("Walk","12 min"),("Also in Lima","2 in San Isidro"),("Cost","Membership")],
     "notes":[("o","Do this","The Miraflores location on Av. Jos&#233; Larco is the one to use if you are staying around here, because you can walk it. Andr&#233;s Reyes 338 and Jorge Basadre 349 in San Isidro are the other two if your meetings are in the business district."),
              ("f","Fun fact","Collecting WeWork locations the way other people collect airport lounges is a real and underrated travel game. The coffee is different, the layout is different, and the people at the next desk tell you more about a city in an hour than a guidebook does in a week."),
              ("k","Must know","Book the desk in the app before you show up. Global access depends on your plan tier, so check yours covers Peru before you land rather than standing in a lobby finding out.")]},
    {"t":"Afternoon","ap":"","name":"Street interviews, Miraflores","kind":"Filming","where":"Parque Kennedy and the malec&#243;n","mi":0.8,
     "pitch":"Asking strangers real questions on camera in a city that is not yours is the fastest way to stop being a tourist in it. Parque Kennedy and the clifftop path are the two places in Miraflores where people are relaxed enough to actually stop and talk.",
     "strip":[("From Aloft","0.8 mi"),("Walk","15 min"),("Best time","Late morning"),("Cost","Free")],
     "notes":[("o","Do this","Lead in Spanish even if you switch to English after. <strong>Con permiso, le puedo hacer una pregunta</strong> gets a yes far more often than opening in English does. Parque Kennedy has benches, shade and the cats, so people are already stopped."),
              ("k","Must know","Ask before you record, every time. Peru takes image rights seriously and it is the right thing to do regardless. Keep the gear small. A phone gets honest answers where a rig gets performances, and it also keeps you from advertising your equipment on a public street.")]},
    {"t":"Afternoon","ap":"","name":"Finesse Our Minds, on the road","kind":"The mission","where":"Wherever the work is","mi":None,
     "pitch":"September is Suicide Prevention Month, and Finesse Our Minds is survivor led and global, so the work does not pause because I am in a different hemisphere. Filming and conversations for the month happened here, in Lima, in Spanish and English.",
     "strip":[("Month","September"),("Reach","Global, free"),("Peru helpline","L&#237;nea 113, option 5"),("Cost","Free to access")],
     "notes":[("o","Carry this","If you are working in mental health anywhere, learn the local number before you land. In Peru it is <strong>L&#237;nea 113, option 5</strong>, run by the Ministry of Health, free and open 24 hours. Knowing the local resource is the difference between talking about support and being able to point at it."),
              ("k","Must know","Peer support work travels differently than a keynote does. Language, stigma and what is culturally sayable all change at the border. Listen a great deal more than you talk for the first few days in a new country.")]},
    {"t":"Evening","ap":"","name":"Millennials Creatives connections","kind":"Business","where":"Coffee, wherever they are","mi":None,
     "pitch":"Every trip has at least one conversation that was not on the calendar when I booked the flight. Maximizing the opportunity is the whole point of being physically somewhere instead of on a call.",
     "strip":[("Format","Coffee or dinner"),("Prep","One clear ask"),("Follow up","Within 48 hours"),("Cost","You buy")],
     "notes":[("o","Do this","Go in with one specific ask instead of a general introduction. People help with a clear request and go quiet on a vague one. Send the follow up before you fly home, while you are still a face and not an email."),
              ("f","Fun fact","This is the part that makes the whole trip make sense on paper. The flight was going to happen anyway. The desk, the filming, the coffee and the ceviche all sit inside the same set of days.")]},
   ]},
  {"id":"d4","num":"04","title":"The Last Full Day","today":False,"when":"Wednesday, September 2 &#183; <strong>the whole trip, compressed</strong> &#183; packed on purpose, with a drop list",
   "note":"Thursday is a pre-dawn airport run, so <strong>this is the last real day.</strong> It is deliberately overfull. Every stop below carries a drop rank, so when the day runs long you cut from the bottom instead of arguing about it on a street corner. <strong>Pack tonight, not tomorrow morning.</strong>",
   "stops":[
    {"t":"7:30","ap":"AM","name":"Breakfast, then go","kind":"Fuel","where":"Aloft, Av. 28 de Julio 894","mi":0.0,
     "pitch":"Eat properly. There is one sit down meal today and it is not until quarter to two.",
     "strip":[("From Aloft","0.0 mi"),("Time","7:30 AM"),("Out the door","8:40"),("Cost","Included")]},
    {"t":"9:00","ap":"AM","name":"Huaca Pucllana","kind":"Cannot move","where":"Calle General Borgo&#241;o cuadra 8, Miraflores","mi":1.8,
     "pitch":"A 1,500 year old adobe pyramid in the middle of a modern neighbourhood, apartment blocks on all four sides. Guided walk on a raised path, about an hour.",
     "strip":[("From Aloft","1.8 mi"),("Drive","11 min"),("Entry","S/15 ($4.50)"),("Drop rank","Never")],
     "notes":[("o","Do this first","<strong>It is closed Tuesdays, so today is the only day left.</strong> That is why it opens the morning rather than the chocolate. Get the 9:00 slot and you are out by 10:15."),
              ("f","Fun fact","The bricks are stood on end like books on a shelf rather than stacked flat. That is why it has survived centuries of earthquakes. The gaps let it shake without collapsing."),
              ("k","Must know","Guided entry only, on gravel and slopes. Ask for the English guide at the ticket window or you will get Spanish by default.")]},
    {"t":"10:30","ap":"AM","name":"ChocoMuseo workshop","kind":"The one to book","where":"Inka Plaza, Av. Petit Thouars 5330, Miraflores","mi":1.2,
     "pitch":"Two hours from cacao bean to a bar you made yourself. Roast, peel, grind, taste the drink as it was drunk before sugar, then mould your own and choose what goes in.",
     "strip":[("From Aloft","1.2 mi"),("Drive","9 min"),("Length","2 hours"),("Price","S/115 ($34)")],
     "notes":[("o","Call ahead","Book the 10:30 today. Walking in on your last morning and finding the session full is how this comes off the list."),
              ("k","Must know","Your chocolate needs about 45 minutes to set, so you cannot walk straight out with it. That gap is exactly why the market is the next stop, on the same street.")]},
    {"t":"12:45","ap":"PM","name":"Inka Market","kind":"Souvenirs","where":"Av. Petit Thouars, blocks 5200 to 5400, Miraflores","mi":1.2,
     "pitch":"Blocks of artisan stalls in a row, the safest souvenir run in the city, and you walk out of the chocolate workshop straight into it.",
     "strip":[("From Aloft","1.2 mi"),("Walk","On the same street"),("Budget","45 minutes"),("Drop rank","3rd to cut")],
     "notes":[("o","Buy this","Baby alpaca, a chullo, and a retablo. Real alpaca is cool to the touch and does not squeak between your fingers."),
              ("k","Must know","Offer around 60 to 70 percent of the first price and settle in the middle. <strong>This is your last chance to buy anything,</strong> so if souvenirs matter, protect this block and cut something else.")]},
    {"t":"1:45","ap":"PM","name":"Horneando Ando","kind":"The one real meal","where":"Av. Prolongaci&#243;n San Mart&#237;n 110A, Barranco","mi":1.4,
     "pitch":"A puerta cerrada, a closed door restaurant with no sign. You arrive at a house, ring the intercom marked 110-A, and someone lets you in to eat home style Peruvian food in a family dining room. The most Lima thing on this entire list, and it sits four minutes from the Barranco walk.",
     "strip":[("From Aloft","1.4 mi"),("Drive","7 min"),("Open","Tue to Sun, 12:30 to 5"),("Drop rank","Never")],
     "notes":[("o","Order this","Whatever the house is baking. Ask instead of ordering."),
              ("k","Must know","<strong>Reserve this morning.</strong> It is small and it fills. Give your driver the number 110-A, not the name, because there is no storefront to find.")]},
    {"t":"3:15","ap":"PM","name":"Barranco on foot","kind":"Content","where":"Puente de los Suspiros and the Bajada de Ba&#241;os","mi":2.2,
     "pitch":"You are already in Barranco. Walk it. A wooden footbridge over a stone ravine running down to the ocean, murals on nearly every wall, forty minutes if you stop a lot, and you will stop a lot.",
     "strip":[("From lunch","4 min walk"),("Length","~40 min"),("Cost","Free"),("Drop rank","2nd to cut")],
     "notes":[("f","Fun fact","Hold your breath crossing the Bridge of Sighs the first time and make a wish. Everybody does it. Nobody admits it."),
              ("k","Must know","Walk down toward the water and take a car from the bottom rather than making anyone climb back up.")]},
    {"t":"4:45","ap":"PM","name":"Hotel, pack, reset","kind":"Do not skip","where":"Aloft, Av. 28 de Julio 894","mi":0.0,
     "pitch":"<strong>Bags done tonight.</strong> You are leaving before dawn and nobody packs well at three in the morning. Forty five minutes now buys you the rest of the evening.",
     "strip":[("From Aloft","0.0 mi"),("Length","45 min"),("Task","Pack, fully"),("Drop rank","Never")]},
    {"t":"5:40","ap":"PM","name":"Larcomar and the malec&#243;n","kind":"The goodbye","where":"Malec&#243;n de la Reserva 610, Miraflores","mi":0.9,
     "pitch":"An open air mall cut into the cliff, shops facing the Pacific, paragliders overhead. Walk the clifftop path to Parque del Amor. This is the last look at the ocean and it is worth protecting.",
     "strip":[("From Aloft","0.9 mi"),("Drive","5 min"),("Sunset","6:04 PM"),("Drop rank","Never")],
     "notes":[("o","Do this","Be on the path by 5:45. Shoot north with the coastline curving away, not into the sun."),
              ("k","Must know","Flat and paved the whole way, the most parent friendly walk in Lima. Bring a layer, the cliff is colder than three blocks inland.")]},
    {"t":"7:00","ap":"PM","name":"Circuito M&#225;gico del Agua","kind":"If you have the legs","where":"Parque de la Reserva, Cercado de Lima","mi":5.5,
     "pitch":"Thirteen lit fountains, a tunnel of water you walk through, and a laser show on a wall of mist. Guinness record holder, and entry is about a dollar.",
     "strip":[("From Aloft","5.5 mi"),("Drive","27 min"),("Entry","S/4 ($1.20)"),("Drop rank","1st to cut")],
     "notes":[("o","Do this","Catch the 7:15 show, then leave. Do not stay for the 8:15 or you will lose the dinner."),
              ("k","Must know","<strong>This is the first thing to cut.</strong> It is 54 minutes of driving round trip on a day that is already full, and it puts you at dinner at 8:45 rather than 8:00. If anyone is flagging by six, skip it and have a relaxed last supper instead. The tunnel also gets you wet, which is a poor way to arrive at Astrid y Gast&#243;n.")]},
    {"t":"8:45","ap":"PM","name":"Astrid y Gast&#243;n","kind":"The last supper","where":"Casa Moreyra, Av. Paz Sold&#225;n 290, San Isidro","mi":2.9,
     "pitch":"Gast&#243;n Acurio's flagship, in a restored 300 year old colonial hacienda with courtyards and gardens. More or less the restaurant that convinced the world Peruvian food was worth flying for. The trip closes here.",
     "strip":[("From Aloft","2.9 mi"),("Drive","13 min"),("Kitchen until","10:30 PM"),("Mains","S/90 ($27)")],
     "notes":[("o","Order this","<strong>&#192; la carte, not the tasting.</strong> Starters S/56 to S/86, mains around S/90, so three of you eat extremely well for a fraction of the S/809 tasting, and nobody sits through three hours of courses before a 3 AM alarm. Pisco sour, then their cebiche."),
              ("k","Must know","<strong>Book it right now.</strong> +51 1 442 2777, restaurante@astridygaston.com, or astridygaston.mesa247.pe. Tell them 8:45 and that you have an early flight. If you skip the fountains, move this to 8:00 and enjoy it properly.")]},
   ]},
  {"id":"d5","num":"05","title":"Out Before Dawn","when":"Thursday, September 3 &#183; <strong>early morning flight</strong> &#183; this is not a day, it is a transfer",
   "note":"An early morning international departure out of Lima means leaving the hotel in the dark. Nothing is open, nothing is planned, and the only thing that matters is the car being booked.",
   "stops":[
    {"t":"3:00","ap":"AM","name":"Car to the airport","kind":"The whole day","where":"Aloft to Jorge Ch&#225;vez International","mi":None,
     "pitch":"At three in the morning the road is empty and the drive that took 45 to 90 minutes on arrival takes about 35. That is the one good thing about this hour.",
     "strip":[("Drive at 3 AM","~35 min"),("Uber","S/57 ($17)"),("Shuttle","S/15 ($4.40) each"),("At airport","3 hrs before")],
     "notes":[("o","Do this","Book the Uber the night before if the app lets you schedule, or order it at 2:50 rather than 3:00, because pickups are thinner at that hour. Pickup is the designated zone, not curbside."),
              ("f","The cheap way, if the hour allows","<strong>Airport Express Lima is S/15 per person, about $4.40, when two or more book together,</strong> S/20 solo. Four Miraflores stops: Larcomar and the Marriott, the Tourist Information Centre, Parque Kennedy, and Hotel Boulevard. About 30 minutes. Book at lima-airport.com."),
              ("k","Must know","<strong>The shuttle almost certainly does not run at 3 AM.</strong> Published service is roughly daytime and evening only, and no operator lists a pre-dawn departure. Call <strong>01-517-3500</strong> to confirm before you count on it, and take the Uber if the answer is no. For three people the shuttle is about $13 against $17 for the car, so at this hour the car is worth it anyway."),
              ("k","Also","Three hours before an international departure, and the new terminal is still ironing out queues. Check in online the night before. Nothing is open in Miraflores at 3 AM, so eat airside, and settle the hotel bill Wednesday evening so checkout is just handing back a key.")]},
   ]},
    {"id":"d6","num":"06","title":"If You Are Staying On","when":"Friday, September 4 &#183; <strong>the extension</strong> &#183; for whoever is not on the Thursday flight",
   "note":"Not everyone leaves Thursday. If you are still here Friday and Saturday, <strong>the two best things that got cut come straight back,</strong> because both of them only exist on these days. Dansa runs Thursday to Saturday and nothing else in Lima is like it.",
   "stops":[
    {"t":"9:00","ap":"AM","name":"Machu Picchu, the Lima version","kind":"Back on","where":"Parque de las Leyendas, San Miguel","mi":7.3,
     "pitch":"A ten metre Machu Picchu replica hidden in a cave in the middle of Lima, reached only by boat across the park's lagoon while Andean music plays. Gloriously strange. The park around it is a full zoo with more than 3,500 animals and real archaeological mounds.",
     "strip":[("From Aloft","7.3 mi"),("Drive","35 min"),("Entry","S/20 ($6) &#183; S/4 senior"),("Boat","S/6 motorised")],
     "notes":[("o","Do this","Take the motorised boat, not the pedal one. Head straight for the Zona Costa lagoon, do the replica, then decide how much zoo anyone wants. Two and a half hours, not a full day."),
              ("f","Fun fact","Seniors 65 and over pay S/4, about a dollar twenty. Cheapest ticket in the family for once."),
              ("k","Must know","This is the stop distance killed on the compressed trip. With a spare day it is genuinely worth the 35 minutes each way.")]},
    {"t":"1:00","ap":"PM","name":"La Mar Cebicher&#237;a","kind":"Back on","where":"Av. La Mar 770, Miraflores","mi":1.5,
     "pitch":"Gast&#243;n Acurio's cebicher&#237;a, the one that exported the whole idea of a Peruvian cebicher&#237;a to the rest of the world. Open air, loud, packed with Lime&#241;os, lunch only because the fish does not sit overnight.",
     "strip":[("From Aloft","1.5 mi"),("Drive","8 min"),("Open","Lunch only"),("Per head","S/90 to 150 ($27 to 45)")],
     "notes":[("o","Order this","<strong>Cebiche cl&#225;sico</strong> to start, a <strong>tiradito</strong> for anyone unsure about raw fish, and <strong>arroz con mariscos</strong> for the table. Drink the leche de tigre left in the bowl."),
              ("k","Must know","No reservations, ever. Arrive before noon or after 2 or you will wait 45 to 90 minutes.")]},
    {"t":"6:50","ap":"PM","name":"Dansa","kind":"The one that got away","where":"Av. Rivera Navarrete 2692, Lince","mi":3.6,
     "pitch":"Not a restaurant. A staged production called Wankar where nine courses, six dishes and three cocktails, arrive while live dancers and musicians work the room and projections run the walls. Peru's regions are the structure. Each course belongs to a place and the dance that comes with it is from the same place.",
     "strip":[("From Aloft","3.6 mi"),("Drive","11 min"),("Runs","Thu to Sat only"),("Mezzanine","S/266 ($79)")],
     "notes":[("o","Book this the moment you know you are staying","Joinnus, or +51 1 219 9000. It caps and it only runs three nights a week, which is exactly why it fell off the compressed trip."),
              ("f","Fun fact","Built by Lucho Quequezana, a musician who plays dozens of traditional Peruvian instruments, and Vania Mas&#237;as, a former ballerina who left the classical world to train street dancers from Lima's outer districts. The cast comes out of that programme."),
              ("k","Must know","Check in around 6:50 for a 7:30 start, about two and a half hours. Ask for <strong>platea</strong>, the ground floor. No reason to climb stairs for a worse view of dancers.")]},
   ]},
  {"id":"d7","num":"07","title":"The Spare Saturday","when":"Saturday, September 5 &#183; <strong>the loose day</strong> &#183; everything else that got cut",
   "note":"No fixed shape. This is the day for whatever the compressed trip did not have room for, in roughly the order I would do it.",
   "stops":[
    {"t":"11:15","ap":"AM","name":"Al Toke Pez","kind":"Back on","where":"Calle Manuel Bonilla 113, Surquillo","mi":0.9,
     "pitch":"Eight or nine stools at a counter, one chef, no menu to think hard about. Toshiro Matsufuji has a doctorate in structural chemistry and gave it up to run this. One of the cheapest famous meals in Latin America.",
     "strip":[("From Aloft","0.9 mi"),("Drive","5 min"),("Open","Daily, 11 to 5"),("Plates","S/25 to 35 ($7 to 10)")],
     "notes":[("o","Order this","The <strong>combinado</strong>. Ceviche, chicharr&#243;n de pescado, arroz con mariscos and tallar&#237;n saltado on one plate, so nobody has to choose."),
              ("k","Must know","No reservations, a sidewalk queue and nowhere to wait. Be there at 11:00 sharp. Cash is smoothest. This is the least comfortable stop in Lima and it is worth it.")]},
    {"t":"7:00","ap":"PM","name":"Circuito M&#225;gico del Agua","kind":"If you skipped it","where":"Parque de la Reserva, Cercado de Lima","mi":5.5,
     "pitch":"Thirteen lit fountains, a tunnel of water you walk through, and a laser show on a wall of mist. Guinness record holder for the largest fountain complex in a public park, and entry is about a dollar.",
     "strip":[("From Aloft","5.5 mi"),("Drive","27 min"),("Shows","7:15, 8:15, 9:15"),("Entry","S/4 ($1.20)")],
     "notes":[("o","Do this","Arrive for the 7:15, then walk the T&#250;nel de las Sorpresas and the Fuente M&#225;gica once the first crowd clears."),
              ("k","Must know","The tunnel gets you wet, and Lima evenings sit around 60 degrees and damp. Bring a layer and book the ride home in the app rather than hailing at the gate.")]},
    {"t":"9:00","ap":"PM","name":"Clon","kind":"Back on","where":"Av. Almirante Miguel Grau 203A, Barranco","mi":2.2,
     "pitch":"The loose, loud younger sibling of M&#233;rito, which sits at number 26 in the World's 50 Best. Same kitchen brain, shareable plates, a third of the ceremony.",
     "strip":[("From Aloft","2.2 mi"),("Drive","11 min"),("Booking","952 992 337"),("Per head","S/150 ($45)")],
     "notes":[("o","Order this","In rounds, not all at once, and ask what came in that morning before you touch the printed menu."),
              ("k","Must know","Call to confirm they will seat you at 9 PM. Their closing time is the one thing I could not verify anywhere online.")]},
   ]},
  ],
 "dishes":[
  ("Ceviche","hot","Has heat","Raw fish cured in lime with red onion, chili and salt, served with sweet potato and giant corn. The lime liquid left in the bowl is leche de tigre and you drink it. Ask for it <strong>sin aj&#237;</strong> if anyone wants it mild."),
  ("Tiradito","mild","Milder","Ceviche's calmer cousin. Fish sliced thin like sashimi, sauced rather than marinated, no onion. This is the one to order for a parent who is unsure about raw fish."),
  ("Causa","mild","Mild","Chilled layers of yellow potato whipped with lime and aj&#237; amarillo, packed around chicken, tuna or crab. Looks like a small cake. Tastes nothing like one."),
  ("Lomo saltado","mild","Mild","Beef stir fried with onion, tomato and soy in a screaming hot wok, served over fries and rice. Chinese technique, Peruvian ingredients. The safest bet on any menu."),
  ("Aj&#237; de gallina","mild","Gentle","Shredded chicken in a creamy yellow chili and walnut sauce over rice. Comfort food, warm rather than hot."),
  ("Anticuchos","hot","Has heat","Beef heart, marinated and grilled on skewers over coals. It does not taste like organ meat, it tastes like the best steak tip you have had. The street food of Lima."),
  ("Rocoto relleno","hot","Genuinely spicy","A rocoto pepper stuffed with spiced beef and cheese and baked. The pepper is the whole dish and it is hot. Order one for the table to try, not one each."),
  ("Papa a la huanca&#237;na","mild","Mild","Boiled potato under a cold, creamy cheese and yellow chili sauce. Almost every meal starts with this somewhere."),
  ("Arroz chaufa","mild","Mild","Peruvian Chinese fried rice, born in Lima's Barrio Chino. Order it at a chifa and understand half of Lima instantly."),
  ("Pan con chicharr&#243;n","mild","Mild","Fried pork, sweet potato and salsa criolla in a roll. The national hangover breakfast, sold before noon and rarely after."),
  ("Picarones","mild","Sweet","Squash and sweet potato doughnut rings, fried and drenched in chancaca syrup. Street dessert. Eat them standing up."),
  ("Suspiro a la lime&#241;a","mild","Sweet","Caramel manjar blanco under a port spiked meringue. The name means the sigh of a woman from Lima, which tells you exactly how sweet it is."),
  ("Pisco sour","mild","Strong","Pisco, lime, syrup, egg white, bitters. Peru's national drink and a genuine argument with Chile over who invented it. Stronger than it tastes."),
  ("Chilcano","mild","Easy","Pisco, ginger ale, lime, ice. Lighter than a pisco sour and much easier to drink with food. This is what locals order on a weeknight."),
  ("Chicha morada","mild","No alcohol","Purple corn boiled with pineapple, clove and cinnamon, then chilled. Sweet, spiced, non alcoholic, and the correct drink with ceviche."),
  ("Inca Kola","mild","No alcohol","Bright yellow, tastes like bubblegum, and outsells Coca-Cola in Peru so thoroughly that Coke eventually gave up and bought a stake in it. Try it once for the story."),
 ],
 "markets":[
  ("Inka Market, Miraflores","<strong>Go.</strong> Av. Petit Thouars, blocks 5200 to 5400. Artisan goods, alpaca, silver, ceramics, all in a safe walkable strip. Already built into Day 3 because it shares a street with ChocoMuseo.","Bargain to about 70 percent of the opening price. Bundle purchases at one stall.","1.2 MI &#183; 9 MIN"),
  ("Barrio Chino","<strong>Go if you want lunch, not shopping.</strong> Calle Cap&#243;n in the historic center. Lima's Chinatown is where chifa was invented, which is arguably the most influential thing that has ever happened to Peruvian food.","Daytime only, and go for a chifa meal with arroz chaufa rather than for the shops. Watch your bag on Cap&#243;n.","~5 MI &#183; 25 MIN"),
  ("Polvos Azules","<strong>Only if you love a chaotic bazaar.</strong> An enormous informal market in the center selling electronics, clothing and a great deal of counterfeit everything. It is an experience, not a shopping trip.","Cash only in practice, crowded, and pickpocketing is the main risk. Nothing you buy here has a warranty.","~5 MI &#183; 25 MIN"),
  ("Gamarra, La Victoria","<strong>Skip on this trip.</strong> South America's largest garment district, tens of thousands of textile businesses in a few dozen blocks. Fascinating if you are sourcing clothing. Overwhelming if you are not.","La Victoria requires real street awareness, and it will eat an entire day you do not have.","~4 MI &#183; 30 MIN"),
  ("Plaza Norte","<strong>Done.</strong> You already made the nine mile, near hour long drive to Independencia. That was the mall trip. There is no reason to make that drive twice.","","9 MI &#183; ~60 MIN"),
 ],
 "cuts":[
  ("Laguna Esmeralda, Huacho",
   "This one hurts, because the photos are unreal. But it is at <strong>kilometer 137 of the Panamericana Norte, roughly three hours each way from Lima.</strong> That is six hours in a car out of a three day trip. Worse, it is not a public natural site. Access runs through a private condominium development, departures are limited and decided by them, and multiple visitors report that the tour includes a pitch to sell you a plot of land. With parents and three days left, this is a no.",
   "<strong>If the sandboarding is the part you want,</strong> the Chilca dunes are about an hour south of Miraflores, tours run at 8 AM and 2 PM daily, and operators will dial the dune buggy down to a gentle version on request. That is a half day instead of a full one."),
  ("Dansa, the Wankar dinner theatre",
   "Nine courses with live dancers and musicians, and it was the anchor of the original Thursday. <strong>It only runs Thursday to Saturday,</strong> and Thursday is now a 3 AM airport run. Wednesday is not an option for it. Genuinely the biggest loss on this trip.",
   "Book it first thing on the next Lima trip. Joinnus, or +51 1 219 9000, and ask for platea on the ground floor."),
  ("Parque de las Leyendas and the Machu Picchu replica",
   "A ten metre Machu Picchu replica in a cave you reach by boat, plus a full zoo, and seniors pay S/4 to get in. It is also <strong>7.3 miles out and needs two and a half hours,</strong> which is the entire morning that Huaca Pucllana now has to occupy because Huaca closes Tuesdays.",
   "Distance lost this one, not quality. It is the first thing I would add back with one more day."),
  ("Al Toke Pez and La Mar",
   "Both are lunch only, and there is exactly one lunch slot left. <strong>Horneando Ando took it</strong> because it sits four minutes from the Barranco walk, which saves a crossing of the city on the tightest day of the trip.",
   "Al Toke Pez was always the rough one anyway: eight stools, a sidewalk queue and nowhere to sit while you wait."),
  ("Clon, Barranco",
   "A good dinner that lost its night to Astrid y Gast&#243;n. With one evening left, the flagship wins.",
   ""),
  ("La Picanter&#237;a, Surquillo",
   "H&#233;ctor Sol&#237;s's whole-fish picanter&#237;a was the plan for Thursday lunch, and it is <strong>closed.</strong> The Surquillo location shut in May 2026. Sol&#237;s has said it returns in 2027 in a different district. Every listing still online shows it open, which is how a trip loses an afternoon.",
   "<strong>Replaced with La Mar</strong> on Av. La Mar, eight minutes from the hotel. Same job on the day, a proper sit-down seafood lunch, and the one place in Lima that arguably did more than any other to put Peruvian food on the map."),
  ("Helarte",
   "Calle Bol&#237;var 205, open daily 8 AM to 10 PM, and you already went. Worth knowing it is <strong>0.4 miles from the lobby and open until 10 PM,</strong> which makes it the default late dessert on any night that ends early. L&#250;cuma is the flavor to get if you did not.",
   ""),
 ],
 "know":[
  ("Book these two right now","<strong>Astrid y Gast&#243;n</strong> for Friday dinner: +51 1 442 2777. <strong>Dansa</strong> for Thursday: through Joinnus or +51 1 219 9000.","Both are the kind of thing that sells out while you are deciding."),
  ("Two calls to confirm","<strong>Clon</strong> at 952 992 337, to check they seat at 8:45 PM. <strong>Horneando Ando</strong> to reserve, because it is a closed door house with limited seats.",""),
  ("Money, and the ATM trap","About <strong>S/3.37 to the dollar.</strong> Every price on this page is in soles first, because that is the money you will actually be handing over.","<strong>Do not pull cash at the airport.</strong> The airport ATMs charged us close to <strong>$8 per withdrawal.</strong> Wait until Miraflores and use a bank machine, BCP, Interbank, Scotiabank or BBVA, inside the branch rather than a standalone kiosk."),
  ("One button that saves you money","When any ATM or card reader offers to charge you <strong>in dollars instead of soles, always choose soles.</strong> That offer is called dynamic currency conversion and the exchange rate baked into it is terrible.","Take out one larger amount rather than three small ones, since the fee is per withdrawal, not per sol. Tipping is about 10 percent, and check the bill for <strong>servicio</strong> first, because if it is there you do not add more."),
  ("Water","<strong>Do not drink the tap water,</strong> including in the hotel. Sealed bottles only. Ice at real restaurants is fine. At street stalls and juice carts, ask for it without ice.",""),
  ("Getting around","Uber and Cabify both work well here and are cheap. Book through the app rather than hailing on the street, especially at night and especially outside a busy attraction.","Every drive on this itinerary is under 35 minutes except the one to Plaza Norte, which is why it is not on it twice."),
  ("Food delivery, the trap","<strong>UberEats does not operate in Peru.</strong> Uber for rides works perfectly, which is exactly what makes people assume the food app does too.","Download <strong>Rappi</strong> first and <strong>PedidosYa</strong> as the backup. Do it at the airport on wifi, not at 10 PM when you are hungry."),
  ("Where to stay","Miraflores. Not the airport. The airport hotel is attached to the terminal and that is its only argument.","We booked it for the arrival night and left immediately. Eat the 45 minute ride and wake up somewhere worth waking up in."),
  ("Staying smart","Miraflores, Barranco and San Isidro are the comfortable districts and this itinerary lives almost entirely inside them.","Phone away on quiet side streets, bag in front on crowded ones, and take a car back from the center rather than walking after dark."),
  ("Weather","Around 60 to 68 degrees, grey, and damp on the coast. September is the tail of the gar&#250;a season. Bring one layer everywhere. It will not rain in any meaningful way.",""),
  ("If you need support in Peru","<strong>L&#237;nea 113, option 5.</strong> Free, 24 hours, run by Peru's Ministry of Health, for mental health support in Spanish.","Worth having in your phone before you land, whether or not you think you will need it."),
  ("Two useful phrases","<strong>La cuenta, por favor</strong> to get the bill, which never comes until you ask. <strong>Sin aj&#237;</strong> if someone wants it without the chili.",""),
 ],
}



PARTNER = '''<div class="sect" id="partner"><div class="lbl">Partnerships</div>
<h2>Every link on this page<br><em>goes straight to the business.</em></h2>
<p class="intro">No affiliate rails, no booking resellers, no Viator, no GetYourGuide. If a restaurant is on here it is because I ate there and it was worth your afternoon. When a venue has no site of its own, the link goes to their page, not to somebody selling tickets on their behalf. That is the whole editorial policy and it is not negotiable, including for paid work.</p>
<div class="cards">
  <div class="c"><h4>What a partner gets</h4><p>A named, linked placement inside a real itinerary that people use on the ground, plus the photo and video I shoot while I am there. The pages stay up and keep working. This is not a story that disappears in 24 hours.</p></div>
  <div class="c"><h4>Who this reaches</h4><p>I speak and train in eight countries. The people reading these pages are the ones who were in the room: professionals, organizers, university and government audiences, and the friends they send afterward. Smaller than a travel blog. Considerably more qualified.</p></div>
  <div class="c"><h4>What I will not do</h4><p>Write a stop I did not go to, take a link out because a competitor paid, or hide that something is sponsored. Anything paid is labeled. The cut list stays honest, and a partner can end up on it.</p></div>
  <div class="c"><h4>Work with me</h4><p>Tourism boards, hotels, airlines, restaurant groups and travel brands: I build the city guide, shoot the content, and speak at the event while I am there. Tell me the market and the dates.</p><p><a href="contact.html" class="m">Start a conversation &#8594;</a></p></div>
</div></div>'''

def build_trip(T):
    o = [head(T["title"], T["desc"], T["canon"]), NAV]
    o.append('<header class="t-hero"><div class="eye">%s</div><h1>%s</h1>%s</header>'
             % (T["eyebrow"], T["h1"], "".join('<p class="t-lede">%s</p>' % l for l in T["ledes"])))
    o.append(ticker(T["ticker"]))
    o.append('<div class="proof">%s</div>' % "".join(
        '<div class="pi"><div class="pin">%s</div><div class="pil">%s</div></div>' % (n, l) for n, l in T["proof"]))

    o.append('<nav class="days"><div class="inner">')
    for d in T["days"]:
        o.append('<a href="#%s">Day %s &#183; %s</a>' % (d["id"], d["num"].lstrip("0"), d["title"]))
    o.append('<a href="#eat">What to Eat</a><a href="#markets">Markets</a>'
             '<a href="#cut">Cut List</a><a href="#know">Before You Go</a></div></nav>')

    o.append('''<div class="controls"><div class="cwrap">
 <div class="cgrp"><span class="clbl">Show me the</span>
   <button class="cb" data-t="work">Work</button>
   <button class="cb" data-t="leisure">Leisure</button>
   <button class="cb" data-t="adventure">Adventure</button>
 </div>
 <div class="cgrp"><span class="clbl">Make it yours</span>
   <button class="cb" data-f="hard">Skip the hard walking</button>
   <button class="cb" data-f="splurge">Skip the splurges</button>
   <button class="cb" data-f="book">Only what needs booking</button>
 </div>
 <div class="cgrp"><span class="clbl">Currency</span>
   <button class="cb cur" data-cur="pen">Soles only</button><button class="cb cur on" data-cur="both">Both</button><button class="cb cur" data-cur="usd">USD only</button>
 </div>
 <div class="cgrp"><button class="cb reset" id="rst">Reset</button></div>
 <div class="legend"><span class="lg o">Order this</span><span class="lg f">Fun fact</span><span class="lg k">Must know</span></div>
</div></div>
<div class="planbar" id="planbar"><div class="pwrap">
  <div class="pstat"><b id="pcount">0</b><span>stops in your plan</span></div>
  <div class="pstat"><b id="pcost">S/0</b><span>per person, roughly</span></div>
  <div class="pstat"><b id="pdone">0</b><span>done so far</span></div>
  <div class="pbtns">
    <button class="cb" id="pcopy">Copy my plan</button>
    <button class="cb pdf" id="ppdf">Save as PDF</button>
    <button class="cb copy" id="psend">Send me your notes</button>
  </div>
</div></div>''')

    for d in T["days"]:
        o.append(day(d))

    o.append('<section class="sect" id="eat"><div class="lbl">What to actually order in Peru</div>'
             '<h2>Fifteen words of a<br><em>Peruvian menu.</em></h2>'
             '<p class="intro">Heat is marked, because aj&#237; is used constantly here and some of it lands harder than it looks.</p>'
             '<div class="dishes">%s</div></section>' % "".join(
        '<div class="dish"><div class="dn">%s<i class="%s">%s</i></div><div class="dd">%s</div></div>' % (n, c, tag, d)
        for n, c, tag, d in T["dishes"]))

    o.append('<section class="sect" id="markets"><div class="lbl">The market list</div>'
             '<h2>Ranked by whether it is<br><em>worth your time.</em></h2>'
             '<p class="intro">Five markets came up. They are not equivalent, and two of them are not a good use of three remaining days.</p>'
             '<div class="cards">%s</div></section>' % "".join(
        '<div class="c"><h4>%s</h4><p>%s</p>%s<span class="m">%s</span></div>'
        % (n, a, ('<p>%s</p>' % b) if b else '', m) for n, a, b, m in T["markets"]))

    o.append('<section class="sect" id="cut"><div class="lbl">Cut from the list, and why</div>'
             '<h2>Being honest about<br><em>what does not fit.</em></h2>'
             '<p class="intro">That is the difference between an itinerary and a wish list.</p>%s</section>' % "".join(
        '<div class="cut"><h4>%s</h4><p>%s</p>%s</div>' % (n, a, ('<p>%s</p>' % b) if b else '')
        for n, a, b in T["cuts"]))

    o.append('<section class="sect" id="know"><div class="lbl">Before you go anywhere else today</div>'
             '<h2>The practical<br><em>everything.</em></h2>'
             '<div class="cards">%s</div></section>' % "".join(
        '<div class="c"><h4>%s</h4><p>%s</p>%s</div>' % (n, a, ('<p>%s</p>' % b) if b else '')
        for n, a, b in T["know"]))

    o.append(PARTNER)
    o.append('<div class="band"><div class="band-in">'
             '<h2>Take the whole thing. <em>Change the city.</em></h2>'
             '<p>Distance from where you are sleeping, what it costs, what to order, and the one thing nobody tells you. It works for Lima. It works for everywhere else on the list.</p>'
             '<div class="btns"><a href="itinerary.html" class="bb bb-dark">Every City</a>'
             '<a href="contact.html" class="bb bb-ghost">Send Me a City</a></div></div></div>')
    o.append(FOOT)
    return "\n".join(o)


def build_index(trips):
    o = [head("Every Trip Is Three Trips | Steal My Itinerary",
              "Work, leisure and adventure in every city I land in. Real itineraries built by distance from the hotel. Prices, what to order, fun facts, and the things nobody tells you before you go.",
              "https://finessehumxn.com/itinerary.html"), NAV]
    o.append('<header class="t-hero"><div class="eye">Work &#183; Leisure &#183; Adventure</div>'
             '<h1>Every trip is<br><em>three trips.</em></h1>'
             '<p class="t-lede">There is the reason I flew, whether that is a keynote, a training room or a build. There are the slow days around it. And there is the one thing I go do that has nothing to do with either, which is usually the part I remember.</p>'
             '<p class="t-lede"><strong>I have never taken a trip that was only one of the three.</strong> So every stop here is tagged, and you can filter the whole city down to the version of the trip you are actually taking. Real prices, what to order by name, and the thing nobody tells you before you go.</p>'
             '<div class="legend"><span class="lg o">Order this</span><span class="lg f">Fun fact</span><span class="lg k">Must know</span></div>'
             '</header>')
    o.append(ticker(["Work","Leisure","Adventure","8+ Countries","South Africa","Japan","Vietnam","Peru","Built on the ground","Real prices","What to order","Fun facts","Must knows","Cut lists","Steal my itinerary"]))

    cards = []
    for t in trips:
        if t.get("soon"):
            cards.append('<div class="trip soon"><div class="top"><p class="flag">%s</p><h3>%s</h3><p>%s</p></div>'
                         '<dl><div><dt>Days</dt><dd>TBD</dd></div><div><dt>Stops</dt><dd>TBD</dd></div>'
                         '<div><dt>Max drive</dt><dd>TBD</dd></div></dl></div>' % (t["flag"], t["name"], t["blurb"]))
        else:
            cards.append('<a class="trip" href="%s"><div class="top"><p class="flag">%s</p><h3>%s</h3><p>%s</p>'
                         '<span class="go">Open the itinerary &#8594;</span></div>'
                         '<dl><div><dt>Days</dt><dd>%s</dd></div><div><dt>Stops</dt><dd>%s</dd></div>'
                         '<div><dt>Max drive</dt><dd>%s</dd></div></dl></a>'
                         % (t["href"], t["flag"], t["name"], t["blurb"], t["days"], t["stops"], t["drive"]))
    o.append('<section class="sect"><div class="lbl">The cities</div><div class="trips">%s</div></section>' % "".join(cards))

    o.append('<section class="sect"><div class="lbl">How these are built</div>'
             '<h2>Same format<br><em>every time.</em></h2>'
             '<p class="intro">Which is the point. Once you have read one, you know exactly where to look on the next one.</p>'
             '<div class="cards">'
             '<div class="c"><h4>Distance from the bed</h4><p>Every stop shows miles and drive time from the hotel I actually stayed in, plus a bar showing where it falls in the day&#8217;s range. You can see instantly whether something is a five minute hop or the one long push.</p></div>'
             '<div class="c"><h4>Real numbers</h4><p>Entry fees in local currency with the dollar conversion, opening hours by day, and the phone number to call. Verified the week the trip happened, with anything I could not confirm marked as unconfirmed.</p></div>'
             '<div class="c"><h4>Order this, fun fact, must know</h4><p>Three lines under every stop. What to actually order by name, one thing worth knowing about the place, and the practical detail that would have wrecked the day if I had not known it.</p></div>'
             '<div class="c"><h4>A cut list</h4><p>Every itinerary ends with what got cut and exactly why. Being honest about what does not fit is the difference between a plan and a wish list.</p></div>'
             '<div class="c"><h4>Bend it to you</h4><p>Filter the city down to work, leisure or adventure. Uncheck what you do not want. Skip the hard walking, skip the splurges, or show only what needs booking. Prices switch between local currency and dollars, the total moves as you edit, and you can copy your version out.</p></div>'
             '<div class="c"><h4>Why I have these</h4><p>I fly for work more than anything else, but no trip has ever stayed in one lane. There is always a stage, always a slow afternoon, and always one thing I had no business doing. These pages are what I would tell a friend flying in behind me.</p></div>'
             '</div></section>')

    o.append(PARTNER)
    o.append('<div class="band"><div class="band-in"><h2>Where should I <em>go next?</em></h2>'
             '<p>Tell me the city and I will build it the same way. New itineraries land here first.</p>'
             '<div class="btns"><a href="contact.html" class="bb bb-dark">Send Me a City</a>'
             '<a href="workshop.html" class="bb bb-ghost">Free Workshop</a></div></div></div>')
    o.append(FOOT)
    return "\n".join(o)


TRIPS = [
 {"href":"lima.html","flag":"Peru &#183; Work, leisure and adventure &#183; Aug 30 to Sep 3, plus an extension","name":"Lima by the Mile","days":"5","stops":"30","drive":"60 min",
  "blurb":"Three days with my parents out of Miraflores. A pyramid in the middle of the city, a Machu Picchu replica you reach by boat, a restaurant with no sign on the door, and the fountain park that costs one dollar."},
 {"soon":True,"flag":"South Africa &#183; Work first","name":"Johannesburg","blurb":"The Hard Rock Cafe keynote, and everything I did once the mic was off. Being written now."},
 {"soon":True,"flag":"Vietnam &#183; Work first","name":"Ho Chi Minh City","blurb":"Training at Saigon International University, then the city on my own time. Being written now."},
 {"soon":True,"flag":"Japan &#183; Work first","name":"Tokyo","blurb":"The international speaking trip, and the adventure half nobody saw. Being written now."},
]

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "lima.html"), "w").write(build_trip(LIMA))
open(os.path.join(OUT, "itinerary.html"), "w").write(build_index(TRIPS))
print("built lima.html and itinerary.html")
