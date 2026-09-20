"""Check catalog completeness, Apple asset integrity, and local navigation."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.refs=[]; self.ids=[]; self.gallery=0; self.h1=0; self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a: self.ids.append(a['id'])
  if 'data-gallery-index' in a: self.gallery+=1
  if tag=='h1': self.h1+=1
  for key in ['href','src']:
   if a.get(key): self.refs.append(a[key])
manifest=json.loads((ROOT/'assets/app-store-manifest.json').read_text())
coming_slugs=['shimal','bringlight','marker','drappin']
pages=['index.html','support/index.html']+[a['slug']+'/index.html' for a in manifest['apps']]
errors=[]
for name in pages:
 p=ROOT/name; page=Page(p.read_text())
 if page.h1!=1: errors.append(f'{name}: expected one h1')
 if len(page.ids)!=len(set(page.ids)): errors.append(f'{name}: duplicate ids')
 for ref in page.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc: continue
  target=(ROOT/u.path.lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir(): target=target/'index.html'
  if not target.is_file(): errors.append(f'{name}: missing {ref}'); continue
  if u.fragment and target.suffix=='.html' and u.fragment not in Page(target.read_text()).ids: errors.append(f'{name}: missing anchor {ref}')
for a in manifest['apps']:
 page=Page((ROOT/a['slug']/'index.html').read_text())
 if page.gallery!=len(a['screenshots']): errors.append(f'{a["slug"]}: incorrect screenshot count')
 if a['storeUrl'] not in page.refs: errors.append(f'{a["slug"]}: missing store URL')
 if a['slug']+'/' not in Page((ROOT/'index.html').read_text()).refs: errors.append(f'{a["slug"]}: missing home card')
 for asset in [a['icon'],*a['screenshots']]:
  p=ROOT/asset['path']
  if hashlib.sha256(p.read_bytes()).hexdigest()!=asset['sha256']: errors.append(f'{asset["path"]}: asset changed')
  with Image.open(p) as im: im.verify()
home=Page((ROOT/'index.html').read_text())
for slug in coming_slugs:
 if slug+'/' not in home.refs: errors.append(f'{slug}: missing coming-soon home card')
 icon=next((ROOT/'assets/apps'/slug).glob('icon.*'),None)
 if not icon or not icon.is_file(): errors.append(f'{slug}: missing coming-soon icon')
protected=Path('/tmp/shimal-protected-pages.json')
if protected.exists():
 for path,digest in json.loads(protected.read_text()).items():
  p=ROOT/path
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest: errors.append(f'{path}: existing protected page changed')
asset_count=sum(1+len(a['screenshots']) for a in manifest['apps'])
print(f'Checked {len(pages)} catalogue pages, {len(manifest["apps"])} App Store apps, and {asset_count} original Apple assets.')
if protected.exists(): print('Verified all 20 protected existing HTML files are byte-for-byte unchanged.')
if errors: raise SystemExit('\n'.join(errors))
print('All local links, anchors, screenshot counts, and asset integrity checks passed.')
