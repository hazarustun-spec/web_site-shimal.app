"""Generate static catalogue pages. Never overwrite legal documents."""
import html
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'assets/app-store-manifest.json').read_text())
apps={a['slug']:a for a in manifest['apps']}
content={
'zoo-merge':dict(name='Zoo Merge',category='Games',tagline='Small animals. One big adventure.',summary='Drop, merge, and rescue your way to a zoo of your own.',intro='Two matching animals become something bigger. Keep merging, beat your best score, and bring a whole zoo to life.',about='A one-thumb puzzle with a growing world to discover. Merge your way from a tiny mouse to an elephant, unlock new habitats, and collect special animal coats. Pick it up for a quick break or stay for one more rescue.',features=[('Drop & merge','Pair matching animals and climb the chain, all the way to the elephant.'),('Build your zoo','Beat your records to unlock 40 habitats and keep every animal you rescue.'),('Discover new powers','Collect silver, gold, and purple coats with bonuses and unique abilities.')],legal=[('privacy.html','Privacy Policy'),('terms.html','Terms of Use')],note='Free to play · Optional in-app purchases',anchor='how'),
'challengebu':dict(name='ChallengeBu!',category='Sports',tagline='Your next match starts here.',summary='Challenge your rivals, play tennis, and climb the league.',intro='Turn your time on the court into a friendly rivalry. Find opponents, play matches, and see your progress in the rankings.',about='ChallengeBu brings amateur tennis into a league of its own. Arrange ranked or friendly matches, track your ELO, and compete through the season. Currently open to university communities with a .edu.tr email address.',features=[('Find your match','Challenge a rival and agree on a time and match format.'),('Climb the rankings','Track your ELO, follow your form, and work towards the season finals.'),('Follow the score','Keep the live match score on your Lock Screen and Dynamic Island.')],legal=[('gizlilik.html','Privacy Policy (TR)'),('kosullar.html','Terms of Use (TR)'),('kvkk.html','KVKK (TR)')],note='Free · University email required',anchor='ozellikler'),
'cekim-yasasi-bolluk':dict(name='Çekim Yasası: Bolluk',category='Lifestyle',tagline='A little intention, every day.',summary='Make space for daily reflection, gratitude, and motivation.',intro='Begin the day with an intention. Write down your wishes, notice the good around you, and build a daily ritual that feels like yours.',about='A Turkish-language motivation app inspired by abundance rituals. Keep a journal of your wishes, gifts, and everyday moments of gratitude. Wind down with calming audio, and follow your routine through your personal archive.',features=[('Build a daily ritual','Start with a daily thought, accept your virtual universe check, and set an intention.'),('Keep a personal journal','Record your wishes, acts of generosity, and the good things that come your way.'),('Make time for yourself','Listen to calming sounds and follow your daily practice in the archive.')],legal=[('gizlilik.html','Privacy Policy & KVKK (TR)'),('kosullar.html','Terms of Use (TR)')],note='One-time purchase · In Turkish',anchor='pratikler')
}

coming_soon={
'shimal':dict(name='Shimal',category='Astrology',summary='Personalized daily astrology, shaped by your birth chart.',icon='assets/apps/shimal/icon.png'),
'bringlight':dict(name='Bring Light',category='Photo & Video',summary='Relight dark, flat photos with thoughtful editing tools.',icon='assets/apps/bringlight/icon.png'),
'marker':dict(name='marker.',category='News',summary='A focused daily briefing on the stories shaping AI.',icon='assets/apps/marker/icon.png'),
'drappin':dict(name='drappin',category='Shopping',summary='Snap any outfit and find it in real stores.',icon='assets/apps/drappin/icon.jpg')
}

def e(s): return html.escape(str(s),quote=True)
ARROW='<span aria-hidden="true">↗</span>'
def img(src,alt='',cls='',eager=False,icon=False):
 w,h=(512,512) if icon else (598,1300)
 return f'<img src="{e(src)}" alt="{e(alt)}" class="{cls}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def brand(prefix): return f'<a class="brand" href="{prefix or "./"}" aria-label="Shimal home">shimal<span class="brand-dot">.</span></a>'
def page(title,desc,body,slug='',gallery=False,image=None):
 prefix='../' if slug else ''; url='https://shimal.app/'+(slug+'/' if slug else '')
 og=f'<meta property="og:image" content="https://shimal.app/{e(image)}">' if image else ''
 script=f'<script src="{prefix}assets/gallery.js" defer></script>' if gallery else ''
 return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title>
<meta name="description" content="{e(desc)}"><meta name="theme-color" content="#ffffff"><link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">{og}<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css">{script}</head>
<body><a class="skip" href="#main">Skip to content</a><header class="header wrap">{brand(prefix)}<nav aria-label="Main navigation"><a href="{prefix}#apps">Our apps</a><a href="{prefix}support/">Support {ARROW}</a></nav></header>{body}
<footer class="footer wrap" id="contact"><div class="footer-main">{brand(prefix)}<p>Independent apps.<br>Made in Istanbul.</p><a class="contact-email" href="mailto:hello@shimal.app">hello@shimal.app {ARROW}</a></div><div class="footer-bottom"><span>© 2026 Shimal</span><a href="{prefix}support/">App support &amp; legal</a><a href="https://apps.apple.com/developer/id1885352713">Find us on the App Store {ARROW}</a></div></footer></body></html>'''

cards=[]
for slug,c in content.items():
 a=apps[slug]
 cards.append(f'''<article class="app-card"><a class="app-card-link" href="{slug}/" aria-label="Explore {e(c['name'])}"><div class="app-card-head">{img(a['icon']['path'],cls='app-icon',eager=True,icon=True)}</div><h3>{e(c['name'])}</h3><p class="card-description">{e(c['summary'])}</p></a></article>''')
soon_cards=[]
for slug,c in coming_soon.items():
 soon_cards.append(f'''<article class="soon-card"><a href="{slug}/" aria-label="Explore {e(c['name'])}"><div class="soon-icon-wrap">{img(c['icon'],cls='app-icon',icon=True)}<span class="soon-badge">Coming soon</span></div><p class="soon-category">{e(c['category'])}</p><h3>{e(c['name'])}</h3><p class="card-description">{e(c['summary'])}</p>{ARROW}</a></article>''')
body=f'''<main id="main" class="wrap"><section class="home-intro" aria-labelledby="home-title"><div><p class="eyebrow"><span></span> INDEPENDENT APP STUDIO</p><h1 id="home-title">Made for your<br><span class="blue">everyday.</span></h1></div><p class="home-description">A little play. A new challenge. A moment for yourself.<br>Discover the apps we make at Shimal.</p></section><section class="catalogue" id="apps" aria-labelledby="apps-title"><div class="section-heading"><h2 id="apps-title">Our apps <span class="count">{len(content):02}</span></h2><span class="section-note">Available on the App Store</span></div><div class="app-grid">{''.join(cards)}</div></section><section class="coming" aria-labelledby="coming-title"><div class="section-heading"><h2 id="coming-title">Coming soon <span class="count">{len(coming_soon):02}</span></h2><span class="section-note">Currently in development</span></div><div class="soon-grid">{''.join(soon_cards)}</div></section></main>'''
(ROOT/'index.html').write_text(page('Shimal — Independent apps for your everyday','Discover Shimal’s iPhone apps: Zoo Merge, ChallengeBu! and Çekim Yasası: Bolluk. Browse screenshots and explore each app on the App Store.',body))

for slug,c in content.items():
 a=apps[slug]; n=len(a['screenshots'])
 shots=''.join(f'<a class="screenshot" href="../{s["path"]}" data-gallery-index="{i}" aria-label="Enlarge {e(c["name"])} screenshot {i+1}">{img("../"+s["path"],c["name"]+f" — App Store screenshot {i+1}",eager=i<3)}<span>{i+1:02} / {n:02}</span></a>' for i,s in enumerate(a['screenshots']))
 features=''.join(f'<article><span class="feature-number">0{i+1}</span><h3>{e(title)}</h3><p>{e(text)}</p></article>' for i,(title,text) in enumerate(c['features']))
 legal=''.join(f'<a href="{url}">{e(label)} {ARROW}</a>' for url,label in c['legal'])
 related=''.join(f'<a class="related-app" href="../{s}/">{img("../"+apps[s]["icon"]["path"],icon=True)}<span>{e(v["name"])}<small>{v["category"]}</small></span>{ARROW}</a>' for s,v in content.items() if s!=slug)
 note='<p class="app-context">For motivation and personal reflection; the app does not promise financial outcomes.</p>' if slug=='cekim-yasasi-bolluk' else ''
 body=f'''<main id="main" class="wrap"><a class="back-link" href="../#apps"><span aria-hidden="true">←</span> All apps</a><section class="product-hero" aria-labelledby="app-title"><div class="product-copy"><div class="product-identity">{img('../'+a['icon']['path'],cls='product-icon',eager=True,icon=True)}<div><p class="eyebrow">{c['category'].upper()} / IPHONE</p><h1 id="app-title">{e(c['name'])}</h1></div></div><h2 class="product-tagline">{e(c['tagline'])}</h2><p class="product-intro">{e(c['intro'])}</p><div class="download-row"><a class="button" href="{a['storeUrl']}" aria-label="View {e(c['name'])} on the App Store">View on the App Store {ARROW}</a><span>{e(c['note'])}</span></div></div></section>
<section class="screens-section" aria-labelledby="screens-title"><div class="section-heading"><h2 id="screens-title">A closer look</h2><div class="gallery-controls" hidden><button type="button" data-gallery-prev aria-label="Previous screenshots" aria-controls="screenshots">←</button><button type="button" data-gallery-next aria-label="Next screenshots" aria-controls="screenshots">→</button></div></div><div class="screenshots" id="screenshots" tabindex="0" role="region" aria-label="{e(c['name'])} screenshots">{shots}</div><p class="screenshot-hint">Scroll to explore. Select a screenshot to take a closer look.</p></section>
<section class="about-app" id="{c['anchor']}" aria-labelledby="about-title"><h2 id="about-title">A little more<br>about the app.</h2><div><p>{e(c['about'])}</p>{note}</div></section><div class="features">{features}</div>
<section class="app-support" id="support" aria-labelledby="support-title"><span id="destek" class="anchor-alias"></span><div><p class="eyebrow">HERE TO HELP</p><h2 id="support-title">Need a hand?</h2><p>Questions, feedback, or something not working?<br>Get in touch and tell us about it.</p><a class="support-email" href="mailto:hello@shimal.app">hello@shimal.app {ARROW}</a></div><nav class="legal-links" aria-label="{e(c['name'])} legal documents">{legal}</nav></section>
<section class="related" aria-labelledby="related-title"><div class="section-heading"><h2 id="related-title">More from Shimal</h2><a href="../#apps">All apps {ARROW}</a></div><div class="related-grid">{related}</div></section></main>
<dialog id="screenshot-dialog" aria-label="Screenshot viewer"><div class="viewer-toolbar"><p id="viewer-caption" aria-live="polite"></p><button type="button" id="close-viewer" aria-label="Close screenshot viewer">Close <span aria-hidden="true">×</span></button></div><div class="viewer-stage"><button type="button" id="viewer-prev" aria-label="Previous screenshot">←</button><img id="viewer-image" alt=""><button type="button" id="viewer-next" aria-label="Next screenshot">→</button></div></dialog>'''
 (ROOT/slug/'index.html').write_text(page(c['name']+' — Shimal',c['summary'],body,slug,True,a['icon']['path']))

rows=[]
for slug,c in content.items():
 links=[('#support','App support'),*c['legal']]
 items=''.join(f'<a href="../{slug}/{url}">{e(label)} {ARROW}</a>' for url,label in links)
 rows.append(f'<article class="support-row"><h2><a href="../{slug}/">{e(c["name"])}</a></h2><nav aria-label="{e(c["name"])} documents">{items}</nav></article>')
other={
'bringlight':('Bring Light',[('index.html#support','Support'),('privacy.html','Privacy Policy'),('terms.html','Terms of Use'),('gizlilik.html','Gizlilik (TR)'),('kosullar.html','Koşullar (TR)')]),
'shimal':('Shimal',[('index.html','App page'),('../privacy.html','Privacy Policy'),('../terms.html','Terms of Use')]),
'marker':('marker.',[('index.html','App page'),('privacy.html','Privacy Policy'),('terms.html','Terms of Use')]),
'drappin':('drappin',[('support.html','Support'),('privacy.html','Privacy Policy'),('terms.html','Terms of Use')])}
for slug,(name,links) in other.items():
 items=''.join(f'<a href="../{slug}/{url}">{e(label)} {ARROW}</a>' for url,label in links)
 rows.append(f'<article class="support-row"><h2><a href="../{slug}/">{e(name)}</a></h2><nav aria-label="{e(name)} documents">{items}</nav></article>')
body=f'''<main class="wrap support-page" id="main"><a class="back-link" href="../#apps"><span aria-hidden="true">←</span> All apps</a><div class="support-intro"><p class="eyebrow">SHIMAL SUPPORT</p><h1>Here to help.</h1><p>Find support and legal documents for each app.<br>For anything else, email <a href="mailto:hello@shimal.app">hello@shimal.app</a>.</p></div>{''.join(rows)}</main>'''
(ROOT/'support').mkdir(exist_ok=True)
(ROOT/'support/index.html').write_text(page('App support & legal — Shimal','Support, privacy policies, terms of use, and KVKK documents for Shimal apps.',body,'support'))
print('Built home, 3 verified App Store product pages, and support directory. No legal documents modified.')
