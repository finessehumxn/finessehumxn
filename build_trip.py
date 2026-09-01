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
      <a href="itinerary.html" class="on">Itinerary</a>
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
  <a href="itinerary.html" class="mm-a">Steal My Itinerary</a>
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
      <a href="itinerary.html">Steal My Itinerary</a>
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
      filters={hard:false,splurge:false,book:false}, cur='pen';

  function save(){try{localStorage.setItem('smi_lima',JSON.stringify({
    f:filters,c:cur,off:stops.map(function(s,i){return s.querySelector('.pk')&&!s.querySelector('.pk').checked?i:-1;}).filter(function(i){return i>=0;})
  }));}catch(e){}}
  function load(){try{var d=JSON.parse(localStorage.getItem('smi_lima')||'null');if(!d)return;
    if(d.f)filters=d.f; if(d.c)cur=d.c;
    (d.off||[]).forEach(function(i){var b=stops[i]&&stops[i].querySelector('.pk');if(b)b.checked=false;});
  }catch(e){}}

  function money(pen){ return cur==='usd' ? '$'+Math.round(pen/RATE) : 'S/'+pen; }

  function applyCurrency(){
    document.querySelectorAll('.strip dd').forEach(function(d){
      if(!d.dataset.orig) d.dataset.orig=d.innerHTML;
      if(cur==='usd'){
        d.innerHTML=d.dataset.orig.replace(/S\/(\d+(?:\.\d+)?)/g,function(m,n){
          return '$'+(Math.round(parseFloat(n)/RATE*100)/100).toFixed(2).replace(/\.00$/,'');});
      } else { d.innerHTML=d.dataset.orig; }
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
      s.classList.toggle('dim',hidden);
      var inPlan = !hidden && (fixed || (box && box.checked));
      if(inPlan && !fixed){ n++; c+=parseInt(s.dataset.cost||0,10); }
    });
    document.getElementById('pcount').textContent=n;
    document.getElementById('pcost').textContent=money(c);
    save();
  }

  document.querySelectorAll('.cb[data-f]').forEach(function(b){
    b.addEventListener('click',function(){
      filters[b.dataset.f]=!filters[b.dataset.f];
      b.classList.toggle('on',filters[b.dataset.f]); render();
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

  document.getElementById('rst').addEventListener('click',function(){
    filters={hard:false,splurge:false,book:false}; cur='pen';
    document.querySelectorAll('.cb[data-f]').forEach(function(b){b.classList.remove('on');});
    document.querySelectorAll('.cb[data-cur]').forEach(function(b){b.classList.toggle('on',b.dataset.cur==='pen');});
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

  load();
  document.querySelectorAll('.cb[data-f]').forEach(function(b){b.classList.toggle('on',!!filters[b.dataset.f]);});
  document.querySelectorAll('.cb[data-cur]').forEach(function(b){b.classList.toggle('on',b.dataset.cur===cur);});
  applyCurrency(); render();
})();
</script>
</body>
</html>'''

def ticker(items):
    row = "".join('<span class="tick">%s</span>' % i for i in items)
    return '<div class="ticker"><div class="ticker-t">%s%s</div></div>' % (row, row)

# name -> (cost per person in soles, tags)
# tags: hard = physically demanding, splurge = over S/100, book = needs a reservation
META = {
 "Getting out of the airport":(75,["book"]),
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
    o = ['<article class="stop" data-cost="%d" data-tags="%s"%s>'
         % (cost, " ".join(tags), ' data-fixed="1"' if skip else '')]
    word = not s["t"][0].isdigit()
    o.append('<div class="time%s"><b>%s</b>%s</div>'
             % (" word" if word else "", s["t"], ('<span>%s</span>' % s["ap"]) if s["ap"] else ""))
    o.append('<div class="in">')
    if not skip:
        o.append('<label class="pick"><input type="checkbox" class="pk" checked>'
                 '<span>In my plan</span></label>')
    o.append('<h3>%s<span class="kind">%s</span></h3>' % (s["name"], s["kind"]))
    if tags:
        lab = {"hard":"Physically demanding","splurge":"Splurge","book":"Needs booking"}
        o.append('<div class="tags">%s</div>' % "".join(
            '<span class="tg %s">%s</span>' % (t, lab[t]) for t in tags))
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
    o = ['<section class="day" id="%s">' % d["id"]]
    o.append('<div class="dayhead"><div class="daynum">%s</div><h2>%s</h2>' % (d["num"], d["title"]))
    o.append('<p class="daywhen">%s</p>' % d["when"])
    o.append('<div class="daynote">%s</div></div>' % d["note"])
    o.append('<div class="stops">%s</div>' % "".join(stop(s) for s in d["stops"]))
    o.append('</section>')
    return "".join(o)


# ============================== LIMA ==============================
LIMA = {
 "slug":"lima",
 "title":"Lima by the Mile | Steal My Itinerary",
 "desc":"Six days in Lima, Peru with my parents, August 30 to September 4, ranked by distance from the hotel. Real prices in soles, what to order at every restaurant, fun facts and the things nobody tells you.",
 "canon":"https://finessehumxn.com/lima.html",
 "eyebrow":"Steal my itinerary &#183; Lima, Peru",
 "h1":'<em>Lima</em><br><strong>by the Mile.</strong>',
 "ledes":[
   'August 30 to September 4. California to Atlanta to Lima on Delta One, one hotel we walked out of, and then five days built on a single question. <strong>How far is it from the bed, and is it worth the drive.</strong>',
   'Distance from the Aloft on Av. 28 de Julio, drive time, what it costs, what to order by name, and the one thing nobody tells you before you go. Twenty stops. One ruined pyramid you can eat dinner next to. One food delivery app that does not work here and will catch you out on night one.',
 ],
 "ticker":["Lima, Peru","Aug 30 to Sep 4","6 Days","20 Stops","Delta One via ATL","Base: Aloft Miraflores","Furthest 9 mi","Closest 0.4 mi","S/3.37 to $1","Sea Level","Sunset 6:04 PM","Traveling with parents","No UberEats in Peru","Use Rappi","Garua season","Order this","Fun fact","Must know"],
 "proof":[("6","Days<br>On the Ground"),("20","Stops<br>Logged"),("9.0","Furthest<br>Miles Out"),("0.4","Closest<br>Miles Out"),("60","Longest<br>Drive, Min"),("S/4","Cheapest<br>Ticket")],
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
     "pitch":"Roughly 45 to 90 minutes to Miraflores depending on traffic. Three ways to do it and only two of them are worth considering.",
     "strip":[("To Miraflores","45 to 90 min"),("Official taxi","S/60 to 95"),("Uber pickup","Parking E1"),("Private transfer","$22 to 27")],
     "notes":[("o","Do this","Use the staffed taxi counters inside Arrivals and confirm the price is <strong>todo incluido</strong> before you get in, or take an Uber from the designated zone at Parking E1. Uber does not pick up curbside at this airport."),
              ("k","Must know","Ignore anyone who approaches you outside Arrivals offering a ride. That is the one scam at this airport and it runs constantly. Carry small soles notes, because the no change routine is the second one.")]},
    {"t":"Night","ap":"","name":"The Wyndham by the airport","kind":"Learn from this","where":"Beside the Jorge Ch&#225;vez terminal","mi":None,
     "pitch":"We booked the airport hotel for the arrival night on the theory that landing tired and walking straight to a bed was the smart play. It is genuinely attached to the terminal, and that is the entire case for it. It was not close to the standard we like to live at, and we left immediately.",
     "strip":[("Distance to terminal","Attached"),("To Miraflores","45 to 90 min"),("Verdict","Left immediately"),("Better move","Go straight to Miraflores")],
     "notes":[("k","Must know","<strong>Do not book the airport hotel unless your layover is genuinely a few hours.</strong> A late arrival is not a reason. Eat the ride, get to Miraflores or Barranco the same night, and wake up somewhere you actually want to be. We lost most of a day undoing this."),
              ("f","Fun fact","The airport sits in Callao, which is its own port city, not Lima proper. Nothing around it is where you want to spend a night. The good districts are all 45 minutes south.")]},
    {"t":"Dinner","ap":"","name":"KFC, and the delivery app problem","kind":"The lesson","where":"Ordered in","mi":None,
     "pitch":"First night in one of the great food cities on earth and we ate KFC in a hotel room. That is what a travel day does to you, and there is no shame in it. What there is, is a logistics lesson nobody warns you about.",
     "strip":[("UberEats","Does not exist in Peru"),("Uber rides","Works fine"),("Use instead","Rappi"),("Or","PedidosYa")],
     "notes":[("k","Must know","<strong>UberEats does not operate in Peru.</strong> Uber for rides works perfectly, which is exactly why this catches people out. For food delivery you need <strong>Rappi</strong> or <strong>PedidosYa</strong>. Download both at the airport while you still have wifi, before you are hungry and stuck."),
              ("o","Do this","Rappi is the one that covers the most restaurants in Lima and it also delivers groceries and pharmacy items. Set it up first. PedidosYa is the backup when a place is not on Rappi.")]},
   ]},
  {"id":"d2","num":"02","title":"The Reset","when":"Monday, August 31 &#183; <strong>moving to Miraflores</strong> &#183; the day the trip actually starts",
   "note":"<strong>This day is still a gap in my notes.</strong> What I know is that we got out of Callao and into the Aloft on Av. 28 de Julio, which is where every distance on the rest of this page is measured from. Send me what we did and I will fill it in.",
   "stops":[
    {"t":"Midday","ap":"","name":"Aloft Lima Miraflores","kind":"Base camp","where":"Av. 28 de Julio 894, Miraflores","mi":0.0,
     "pitch":"This is the anchor for the whole trip. Miraflores is flat, walkable, well lit, and close to almost everything worth eating. Every mile figure on this page is measured from this front door.",
     "strip":[("From airport","45 to 90 min"),("District","Miraflores"),("To the cliffs","0.9 mi"),("To Barranco","2.2 mi")],
     "notes":[("o","Do this","If you are choosing a base in Lima, choose Miraflores. Barranco is more beautiful and better at night. San Isidro is quieter and emptier. Miraflores is the one that makes every other day shorter."),
              ("k","Must know","Ask for a room away from Av. 28 de Julio if you are a light sleeper. It is a real road.")]},
   ]},
  {"id":"d3","num":"03","title":"Ice Cream and a Long Drive","when":"Tuesday, September 1 &#183; <strong>0.4 miles, then 9</strong> &#183; one of these was worth it",
   "note":"A short day with a useful lesson buried in it. The best stop was four tenths of a mile away. The longest drive was to a shopping mall.",
   "stops":[
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
  {"id":"d4","num":"04","title":"Close Range","when":"Wednesday, September 2 &#183; <strong>nothing today is more than 5.5 miles out</strong> &#183; two indoor stops, one long night",
   "note":"Today exists because of one hard rule. <strong>Huaca Pucllana closes every Tuesday.</strong> Yesterday was Tuesday. So the pyramid anchors this morning, and everything else falls in around it.",
   "stops":[
    {"t":"9:30","ap":"AM","name":"Huaca Pucllana","kind":"Ruins","where":"Calle General Borgo&#241;o cuadra 8, Miraflores","mi":1.8,
     "pitch":"A 1,500 year old adobe pyramid sitting in the middle of a modern neighborhood, surrounded by apartment buildings on all four sides. You walk the site with a guide on a raised path. It takes about an hour.",
     "strip":[("From Aloft","1.8 mi"),("Drive","11 min"),("Open","Wed to Mon, 9 to 5"),("Entry","S/15 &#183; S/7.50 reduced")],
     "notes":[("f","Fun fact","It is built from millions of hand made bricks stood on end like books on a shelf, not stacked flat. That bookshelf pattern is why it has survived centuries of earthquakes. The gaps let it shake without collapsing."),
              ("k","Must know","Entry is guided only, and the tour goes at the guide's pace on gravel and slopes. There are ramps and an elevator, but the bathroom is narrow. Ask for the English guide at the ticket window or you will get Spanish by default.")]},
    {"t":"11:15","ap":"AM","name":"Al Toke Pez","kind":"Ceviche counter","where":"Calle Manuel Bonilla 113, Surquillo","mi":0.9,
     "pitch":"Eight or nine stools at a counter, one chef, no menu you need to think hard about. Toshiro Matsufuji has a doctorate in structural chemistry and gave it up to run this. It is one of the cheapest famous meals in Latin America.",
     "strip":[("From Aloft","0.9 mi"),("Drive","5 min"),("Open","Daily, 11 to 5"),("Plates","S/25 to 35")],
     "notes":[("o","Order this","The <strong>combinado</strong>. It is ceviche, chicharr&#243;n de pescado, arroz con mariscos and tallar&#237;n saltado all on one plate, so nobody has to choose. Add a chicha morada."),
              ("f","Fun fact","Netflix put this counter on television and the line got longer, but the price never moved. Locals still eat here on a lunch break."),
              ("k","Must know","This is the least comfortable stop of the whole trip. There is no waiting room, no reservations, and the queue is on the sidewalk. Getting there at 11:00 sharp is the whole strategy. If the line is already deep, one person holds the spot and the parents wait in the car. Cash is smoothest.")]},
    {"t":"1:00","ap":"PM","name":"Hotel reset","kind":"Do not skip","where":"Aloft, Av. 28 de Julio 894","mi":0.0,
     "pitch":"Two more hours out and the night falls apart. This block is doing real work.",
     "strip":[("From Aloft","0.0 mi"),("Drive","None"),("Length","2 hours"),("Cost","Free")]},
    {"t":"3:30","ap":"PM","name":"Barranco on foot","kind":"Content","where":"Puente de los Suspiros and the Bajada de Ba&#241;os, Barranco","mi":2.2,
     "pitch":"The best walking hour in the city. A wooden footbridge over a stone ravine that runs down to the ocean, murals on nearly every wall, and a slow uphill back. Roughly forty minutes of actual walking if you stop a lot, and you will stop a lot.",
     "strip":[("From Aloft","2.2 mi"),("Drive","11 min"),("Open","Always"),("Cost","Free")],
     "notes":[("f","Fun fact","The Bridge of Sighs is named for a local superstition. Hold your breath and make a wish the first time you cross it, and the wish is supposed to land. Everybody does it. Nobody admits it."),
              ("k","Must know","The Bajada de Ba&#241;os is a real descent and a real climb back. Walk down toward the water, then take a taxi from the bottom rather than making anyone hike back up. Phones stay in pockets on the quieter side streets.")]},
    {"t":"6:45","ap":"PM","name":"Circuito M&#225;gico del Agua","kind":"Fountains","where":"Parque de la Reserva, Cercado de Lima","mi":5.5,
     "pitch":"Thirteen illuminated fountains in one park, including a tunnel of water you walk through and a laser show fired onto a wall of mist. It holds the Guinness record for the largest fountain complex in a public park. Entry costs about one US dollar, which stays funny the entire time.",
     "strip":[("From Aloft","5.5 mi"),("Drive","27 min"),("Shows","7:15, 8:15, 9:15"),("Entry","S/4 &#183; about $1.20")],
     "notes":[("o","Do this","Arrive for the 7:15 show, then walk the T&#250;nel de las Sorpresas and the Fuente M&#225;gica after. The fountains photograph better once the crowd from the first show clears out."),
              ("f","Fun fact","The park sat closed and neglected for decades before the city rebuilt it in 2007. It is now one of the most visited attractions in Peru, and the crowd is overwhelmingly Lime&#241;o families, not tourists."),
              ("k","Must know","The tunnel fountain will get you wet. That is the point, but bring a layer, because Lima nights in September sit around 60 degrees and damp. Book the ride back through the app rather than hailing outside the gate.")]},
    {"t":"8:45","ap":"PM","name":"Clon","kind":"Dinner","where":"Av. Almirante Miguel Grau 203A, Barranco","mi":2.2,
     "pitch":"The loose, loud younger sibling of M&#233;rito, which sits at number 26 in the World's 50 Best. Same kitchen brain, shareable plates, a third of the ceremony. Good last stop on a night that started at a pyramid.",
     "strip":[("From Aloft","2.2 mi"),("Drive","11 min"),("Booking","952 992 337"),("Per head","Around S/150")],
     "notes":[("o","Order this","Order in rounds, not all at once, and let the kitchen pace it. Ask what came in that morning before you touch the printed menu."),
              ("k","Must know","Call ahead today and confirm they will still seat a table of three at 8:45 PM. Their closing time is the one thing I could not verify anywhere online. If the answer is no, the backup is Restaurante Huaca Pucllana, which serves until 10 PM with the lit pyramid outside the window.")]},
   ]},
  {"id":"d5","num":"05","title":"The Long Haul","when":"Thursday, September 3 &#183; <strong>one 7.3 mile push, then everything comes back close</strong> &#183; ends in a theater",
   "note":"The only day that leaves the Miraflores bubble. Get the distance done in the morning while everyone is fresh, then spend the rest of the day within four miles of the bed.",
   "stops":[
    {"t":"9:00","ap":"AM","name":"Machu Picchu, the Lima version","kind":"Replica","where":"Parque de las Leyendas, San Miguel","mi":7.3,
     "pitch":"There is a ten meter Machu Picchu replica hidden inside a cave in the middle of Lima, and the only way to reach it is by boat across the park's lagoon while Andean music plays. It is gloriously strange. The park around it is also a full zoo with more than 3,500 animals and real archaeological mounds on the grounds.",
     "strip":[("From Aloft","7.3 mi"),("Drive","35 min"),("Open","Daily, 9 to 5"),("Entry","S/20 adult &#183; S/4 senior")],
     "notes":[("o","Do this","The boat to the cave costs S/6 for the motorized one, S/12 for the pedal boat. Take the motorized one. Nobody wants to pedal their parents across a lagoon."),
              ("f","Fun fact","Seniors 65 and over pay S/4 to get in, which is about one dollar and twenty cents. The parents get the cheapest ticket in the family for once."),
              ("k","Must know","This is a large park with real walking distances between zones. Head straight for the Zona Costa lagoon first, do the replica, then decide how much zoo anyone actually wants. Budget two and a half hours, not a full day.")]},
    {"t":"1:00","ap":"PM","name":"La Picanter&#237;a","kind":"The big lunch","where":"Francisco Moreno 388, Surquillo","mi":0.5,
     "pitch":"H&#233;ctor Sol&#237;s brought northern Peruvian cooking to Lima and built it around one idea. You walk in, you look at the whole fish on ice, you pick one, and the kitchen turns that single fish into three or four different dishes for the table. Communal tables, tile floors, zero pretension, serious food.",
     "strip":[("From Aloft","0.5 mi"),("Drive","4 min"),("Open","Lunch only, closes ~5:30"),("Price","By weight of fish")],
     "notes":[("o","Order this","Pick one whole fish for the table and let them split it. Ceviche first, then sudado or a fried preparation. Add the <strong>tortilla de raya</strong>, a stingray omelette that sounds alarming and tastes like the best crab cake of your life. Chicha de jora to drink."),
              ("f","Fun fact","A picanter&#237;a is a northern Peruvian institution, historically a house where a woman cooked and sold food and chicha out of her own kitchen. Sol&#237;s built a famous restaurant by refusing to make it fancier than that."),
              ("k","Must know","Your saved hours say 2 PM to 9 PM. Every source I checked says this place is <strong>lunch only and closes around 5:30 PM.</strong> Plan for lunch, not dinner. Portions are enormous and priced by fish weight, so ask the price of the fish before you nod at it. The upstairs balcony is up a staircase, so ask for a ground floor table.")]},
    {"t":"3:30","ap":"PM","name":"Hotel reset","kind":"Mandatory","where":"Aloft, Av. 28 de Julio 894","mi":0.0,
     "pitch":"Tonight runs until 10:30. Three hours down now is what makes that possible.",
     "strip":[("From Aloft","0.0 mi"),("Drive","None"),("Length","3 hours"),("Cost","Free")]},
    {"t":"6:50","ap":"PM","name":"Dansa","kind":"Dinner theater","where":"Av. Rivera Navarrete 2692, Lince, near the San Isidro line","mi":3.6,
     "pitch":"Not a restaurant. A staged production called Wankar where nine courses, six dishes and three cocktails, land in front of you while live dancers and musicians work the room and projections run across the walls. Peru's regions are the structure. Each course belongs to a place, and the dance that arrives with it comes from the same place.",
     "strip":[("From Aloft","3.6 mi"),("Drive","11 min"),("Runs","Thu to Sat, 7:30 PM"),("Tickets","$79 mezzanine &#183; $110+ floor")],
     "notes":[("o","Book this","Tickets go through Joinnus, or call +51 1 219 9000. Book today. It only runs Thursday through Saturday, which is exactly why it sits on this night and not another one."),
              ("f","Fun fact","It was built by Lucho Quequezana, a musician who plays dozens of traditional Peruvian instruments, and Vania Mas&#237;as, a former ballerina who left the classical world to train street dancers from Lima's outer districts. The cast comes out of that program."),
              ("k","Must know","Check in is around 6:50 PM for a 7:30 start and the whole thing runs about two and a half hours. Ask for <strong>platea</strong>, the ground floor. The mezzanine is up stairs, and there is no reason to make anyone climb for a worse view of the dancers.")]},
   ]},
  {"id":"d6","num":"06","title":"The Finale","when":"Friday, September 4 &#183; <strong>chocolate, souvenirs, a secret door, and the last supper</strong> &#183; departure day",
   "note":"Everything today is stacked so that the last thing you do in Lima is sit down at Astrid y Gast&#243;n. The two morning stops sit on the same street, which is the only reason this day fits. <strong>One thing to settle: if the flight home leaves Friday night rather than after midnight, the 7:30 PM dinner has to move to lunch at 1:00 PM.</strong>",
   "stops":[
    {"t":"9:30","ap":"AM","name":"ChocoMuseo workshop","kind":"Hands on","where":"Inka Plaza, Av. Petit Thouars 5330, Miraflores","mi":1.2,
     "pitch":"Two hours from cacao bean to a bar you made yourself. You roast, peel, grind, taste the drink the way it was drunk before sugar existed, then mold your own chocolate and pick what goes in it. You leave with about 130 grams of it.",
     "strip":[("From Aloft","1.2 mi"),("Drive","9 min"),("Length","2 hours"),("Price","About $34 per person")],
     "notes":[("f","Fun fact","Peru grows more distinct varieties of cacao than any country on earth, and the original Amazonian cacao trees are native here. The bitter unsweetened drink they hand you partway through is much closer to the original than anything in a candy aisle."),
              ("k","Must know","Your chocolate needs about 45 minutes to set after the workshop ends, so you cannot walk straight out with it. That gap is exactly why the next stop is on the same street.")]},
    {"t":"11:45","ap":"AM","name":"Inka Market","kind":"Souvenirs","where":"Av. Petit Thouars, blocks 5200 to 5400, Miraflores","mi":1.2,
     "pitch":"Several blocks of artisan stalls all in a row, the easiest and safest souvenir run in the city. Alpaca, textiles, silver, ceramics, retablos. You walk out of the chocolate workshop and it is right there.",
     "strip":[("From Aloft","1.2 mi"),("Drive","9 min"),("Open","Daily, roughly 10 to 8"),("Cost","Whatever you negotiate")],
     "notes":[("o","Buy this","Real baby alpaca, a proper chullo, and a retablo, one of those little painted boxes that opens into a whole scene. Skip anything that feels plasticky and light. Real alpaca is cool to the touch and does not squeak between your fingers."),
              ("k","Must know","Prices are soft. Offer around 60 to 70 percent of the first number and settle in the middle, politely and with a smile. Buying two or three things from one stall gets you a better price than spreading it around. Bring small soles notes, because nobody will have change for a S/100 bill early in the day.")]},
    {"t":"12:45","ap":"PM","name":"Horneando Ando","kind":"Closed door lunch","where":"Av. Prolongaci&#243;n San Mart&#237;n 110A, Barranco","mi":1.4,
     "pitch":"A puerta cerrada, a closed door restaurant. There is no sign to walk toward. You arrive at a house, you ring the intercom marked 110-A, and someone lets you in to eat home style Peruvian food in what is essentially a family dining room. It is the most Lima thing on this entire list.",
     "strip":[("From Aloft","1.4 mi"),("Drive","7 min"),("Open","Tue to Sun, 12:30 to 5"),("Price","Moderate")],
     "notes":[("o","Order this","Whatever the house is baking that day. Ask instead of ordering. The name means roughly here I am, baking, and the baked things are the point."),
              ("k","Must know","Message ahead to reserve. It is small, it has gotten popular, and walking up unannounced can mean no table. Ring the intercom for 110-A when you arrive. The driver will not find a storefront, so give them the number and not the name.")]},
    {"t":"3:30","ap":"PM","name":"Larcomar and the malec&#243;n","kind":"The view","where":"Malec&#243;n de la Reserva 610, Miraflores","mi":0.9,
     "pitch":"An open air mall carved into the side of a cliff, so the shops face out over the Pacific and there is nothing above you but paragliders. Walk out from Larcomar along the clifftop path to Parque del Amor, where a giant mosaic sculpture of a couple kissing sits over the water.",
     "strip":[("From Aloft","0.9 mi"),("Drive","5 min"),("Sunset","6:04 PM"),("Cost","Free to walk")],
     "notes":[("o","Do this","Be on the clifftop path by 5:30. Shoot facing north with the coastline curving away, not straight into the sun. Paragliders launch right off the cliff edge here and cost around $60 to $90 if anyone wants to go up."),
              ("f","Fun fact","Lima spends most of the winter under a low grey ceiling the locals call the gar&#250;a. September is when it starts breaking. That flat silver light is unflattering for landscapes and unbelievably good for portraits and food, so shoot people, not skies."),
              ("k","Must know","The malec&#243;n is flat, paved and easy the whole way, which makes it the single most parent friendly walk in Lima. Bring a jacket. It is cooler and damper on the cliff than three blocks inland.")]},
    {"t":"7:30","ap":"PM","name":"Astrid y Gast&#243;n","kind":"The last supper","where":"Casa Moreyra, Av. Paz Sold&#225;n 290, San Isidro","mi":2.9,
     "pitch":"Gast&#243;n Acurio's flagship, and more or less the restaurant that convinced the world Peruvian food was worth flying for. It sits inside a restored 300 year old colonial hacienda with courtyards, gardens and its own research kitchen. This is the meal the whole trip closes on.",
     "strip":[("From Aloft","2.9 mi"),("Drive","13 min"),("Dinner","Tue to Sat, 7 to 10:30"),("Price","Mains ~S/90 &#183; tasting $240+")],
     "notes":[("o","Order this","Go &#224; la carte, not the tasting menu. Starters run S/56 to S/86 and mains around S/90, so three people eat extremely well for a fraction of the $240 per head tasting, and nobody has to sit through three hours of courses on their last night. Start with a pisco sour and their cebiche."),
              ("f","Fun fact","Acurio trained as a lawyer in Madrid and quietly switched to culinary school without telling his father, who was a senator. Astrid is his wife, a German pastry chef he met in Paris. The restaurant carries both names because both of them built it."),
              ("k","Must know","<strong>You do not have a reservation yet, so this is today's one urgent task.</strong> Call +51 1 442 2777, or email restaurante@astridygaston.com, or book at astridygaston.mesa247.pe. Closed Mondays, and Sunday is lunch only. There is an elevator and both indoor and garden seating, so it is a comfortable room for parents.")]},
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
  ("Helarte",
   "Calle Bol&#237;var 205, open daily 8 AM to 10 PM, and you already went. Worth knowing it is <strong>0.4 miles from the lobby and open until 10 PM,</strong> which makes it the default late dessert on any night that ends early. L&#250;cuma is the flavor to get if you did not.",
   ""),
 ],
 "know":[
  ("Book these two right now","<strong>Astrid y Gast&#243;n</strong> for Friday dinner: +51 1 442 2777. <strong>Dansa</strong> for Thursday: through Joinnus or +51 1 219 9000.","Both are the kind of thing that sells out while you are deciding."),
  ("Two calls to confirm","<strong>Clon</strong> at 952 992 337, to check they seat at 8:45 PM. <strong>Horneando Ando</strong> to reserve, because it is a closed door house with limited seats.",""),
  ("Money","About <strong>S/3.37 to the dollar.</strong> Cards work at every restaurant on this list. Carry small soles for taxis, markets, the fountains and the tiny places.","Tipping is about 10 percent, and check the bill for <strong>servicio</strong> first, because if it is there you do not add more."),
  ("Water","<strong>Do not drink the tap water,</strong> including in the hotel. Sealed bottles only. Ice at real restaurants is fine. At street stalls and juice carts, ask for it without ice.",""),
  ("Getting around","Uber and Cabify both work well here and are cheap. Book through the app rather than hailing on the street, especially at night and especially outside a busy attraction.","Every drive on this itinerary is under 35 minutes except the one to Plaza Norte, which is why it is not on it twice."),
  ("Food delivery, the trap","<strong>UberEats does not operate in Peru.</strong> Uber for rides works perfectly, which is exactly what makes people assume the food app does too.","Download <strong>Rappi</strong> first and <strong>PedidosYa</strong> as the backup. Do it at the airport on wifi, not at 10 PM when you are hungry."),
  ("Where to stay","Miraflores. Not the airport. The airport hotel is attached to the terminal and that is its only argument.","We booked it for the arrival night and left immediately. Eat the 45 minute ride and wake up somewhere worth waking up in."),
  ("Staying smart","Miraflores, Barranco and San Isidro are the comfortable districts and this itinerary lives almost entirely inside them.","Phone away on quiet side streets, bag in front on crowded ones, and take a car back from the center rather than walking after dark."),
  ("Weather","Around 60 to 68 degrees, grey, and damp on the coast. September is the tail of the gar&#250;a season. Bring one layer everywhere. It will not rain in any meaningful way.",""),
  ("Two useful phrases","<strong>La cuenta, por favor</strong> to get the bill, which never comes until you ask. <strong>Sin aj&#237;</strong> if someone wants it without the chili.",""),
 ],
}


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
 <div class="cgrp"><span class="clbl">Make it yours</span>
   <button class="cb" data-f="hard">Skip the hard walking</button>
   <button class="cb" data-f="splurge">Skip the splurges</button>
   <button class="cb" data-f="book">Only what needs booking</button>
 </div>
 <div class="cgrp"><span class="clbl">Currency</span>
   <button class="cb cur on" data-cur="pen">S/</button><button class="cb cur" data-cur="usd">USD</button>
 </div>
 <div class="cgrp"><button class="cb reset" id="rst">Reset</button></div>
 <div class="legend"><span class="lg o">Order this</span><span class="lg f">Fun fact</span><span class="lg k">Must know</span></div>
</div></div>
<div class="planbar" id="planbar"><div class="pwrap">
  <div class="pstat"><b id="pcount">0</b><span>stops in your plan</span></div>
  <div class="pstat"><b id="pcost">S/0</b><span>per person, roughly</span></div>
  <button class="cb copy" id="pcopy">Copy my plan</button>
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

    o.append('<div class="band"><div class="band-in">'
             '<h2>Take the whole thing. <em>Change the city.</em></h2>'
             '<p>Distance from where you are sleeping, what it costs, what to order, and the one thing nobody tells you. It works for Lima. It works for everywhere else on the list.</p>'
             '<div class="btns"><a href="itinerary.html" class="bb bb-dark">See Every Itinerary</a>'
             '<a href="contact.html" class="bb bb-ghost">Send Me a City</a></div></div></div>')
    o.append(FOOT)
    return "\n".join(o)


def build_index(trips):
    o = [head("Steal My Itinerary | L.Finesse Humxn",
              "Real itineraries from real trips, built by distance from the hotel. Prices, what to order, fun facts, and the things nobody tells you before you go.",
              "https://finessehumxn.com/itinerary.html"), NAV]
    o.append('<header class="t-hero"><div class="eye">Steal my itinerary</div>'
             '<h1><em>Take</em> the plan.<br><strong>Skip the research.</strong></h1>'
             '<p class="t-lede">These are not roundups. Every trip here got built on the ground, in the city, from a hotel lobby, and every stop is ranked the way you actually plan a day. <strong>How far is it from where I am sleeping, and is it worth the drive.</strong></p>'
             '<p class="t-lede">Real prices. What to order by name. The one thing nobody tells you before you go. Copy any of it.</p>'
             '<div class="legend"><span class="lg o">Order this</span><span class="lg f">Fun fact</span><span class="lg k">Must know</span></div>'
             '</header>')
    o.append(ticker(["Steal my itinerary","Built on the ground","Real prices","What to order","Fun facts","Must knows","Cut lists","Distance from the hotel","New cities coming"]))

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
    o.append('<section class="sect"><div class="lbl">The trips</div><div class="trips">%s</div></section>' % "".join(cards))

    o.append('<section class="sect"><div class="lbl">How these are built</div>'
             '<h2>Same format<br><em>every time.</em></h2>'
             '<p class="intro">Which is the point. Once you have read one, you know exactly where to look on the next one.</p>'
             '<div class="cards">'
             '<div class="c"><h4>Distance from the bed</h4><p>Every stop shows miles and drive time from the hotel I actually stayed in, plus a bar showing where it falls in the day&#8217;s range. You can see instantly whether something is a five minute hop or the one long push.</p></div>'
             '<div class="c"><h4>Real numbers</h4><p>Entry fees in local currency with the dollar conversion, opening hours by day, and the phone number to call. Verified the week the trip happened, with anything I could not confirm marked as unconfirmed.</p></div>'
             '<div class="c"><h4>Order this, fun fact, must know</h4><p>Three lines under every stop. What to actually order by name, one thing worth knowing about the place, and the practical detail that would have wrecked the day if I had not known it.</p></div>'
             '<div class="c"><h4>A cut list</h4><p>Every itinerary ends with what got cut and exactly why. Being honest about what does not fit is the difference between a plan and a wish list.</p></div>'
             '</div></section>')

    o.append('<div class="band"><div class="band-in"><h2>Where should I <em>go next?</em></h2>'
             '<p>Tell me the city and I will build it the same way. New itineraries land here first.</p>'
             '<div class="btns"><a href="contact.html" class="bb bb-dark">Send Me a City</a>'
             '<a href="workshop.html" class="bb bb-ghost">Free Workshop</a></div></div></div>')
    o.append(FOOT)
    return "\n".join(o)


TRIPS = [
 {"href":"lima.html","flag":"Peru &#183; Aug 30 to Sep 4","name":"Lima by the Mile","days":"6","stops":"20","drive":"60 min",
  "blurb":"Three days with my parents out of Miraflores. A pyramid in the middle of the city, a Machu Picchu replica you reach by boat, a restaurant with no sign on the door, and the fountain park that costs one dollar."},
 {"soon":True,"flag":"Coming next","name":"Asia","blurb":"Same format, new base hotel. In progress."},
]

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "lima.html"), "w").write(build_trip(LIMA))
open(os.path.join(OUT, "itinerary.html"), "w").write(build_index(TRIPS))
print("built lima.html and itinerary.html")
