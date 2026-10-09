#!/usr/bin/env python3
# ------------------------------------------------------------------
# v4 — Scarica le immagini remote, le ridimensiona, le CONVERTE IN WEBP
# e aggiunge width/height nell'HTML. Rende il sito indipendente da
# Base44 e molto più veloce (formato moderno + peso ridotto).
#
# USO (nella cartella vesta-sito, con internet):
#   python3 self-host-immagini.py
#
# Richiede Pillow (lo installa da solo se manca).
# ------------------------------------------------------------------
import os, re, glob, hashlib, ssl, urllib.request, subprocess, sys

CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
MAXW = 1600      # larghezza massima px
QUALITY = 80     # qualità WebP

try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    try:
        subprocess.run([sys.executable,"-m","pip","install","Pillow","--quiet","--break-system-packages"],check=False)
        from PIL import Image; HAVE_PIL=True
    except Exception:
        HAVE_PIL=False
        print("!! Pillow non disponibile: scarico le immagini senza convertirle in WebP.")

IMGDIR='images'; os.makedirs(IMGDIR,exist_ok=True)
pat=re.compile(r'https://(?:media\.base44\.com|cdn\.krossbooking\.com|images\.unsplash\.com)/[^"\'\)\s]+')

htmls=glob.glob('**/*.html',recursive=True)
urls=set()
for h in htmls:
    urls|=set(pat.findall(open(h,encoding='utf-8').read()))
print('Trovate %d immagini.\n'%len(urls))

mapping={}   # url -> (local_path, w, h)
for u in sorted(urls):
    origext=os.path.splitext(u.split('?')[0])[1].lower()
    if origext not in ('.jpg','.jpeg','.png','.webp'): origext='.jpg'
    h12=hashlib.md5(u.encode()).hexdigest()[:12]
    tmp=os.path.join(IMGDIR,h12+origext)
    ok=False; last=None
    for _ in range(3):
        try:
            req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Macintosh)'})
            with urllib.request.urlopen(req,timeout=45,context=CTX) as r, open(tmp,'wb') as fp:
                fp.write(r.read())
            ok=True; break
        except Exception as e: last=e
    if not ok:
        print('  ERRORE',u[:56],'->',last); continue
    before=os.path.getsize(tmp)

    if HAVE_PIL:
        try:
            im=Image.open(tmp)
            has_alpha = im.mode in ('RGBA','LA') or (im.mode=='P' and 'transparency' in im.info)
            im=im.convert('RGBA' if has_alpha else 'RGB')
            if im.width>MAXW:
                im=im.resize((MAXW,round(im.height*MAXW/im.width)),Image.LANCZOS)
            dest=os.path.join(IMGDIR,h12+'.webp')
            im.save(dest,'WEBP',quality=QUALITY,method=6)
            if dest!=tmp and os.path.exists(tmp): os.remove(tmp)
            w,h=im.size; local='/'+IMGDIR+'/'+h12+'.webp'
        except Exception as e:
            print('  (conversione saltata per',h12,'->',e,')')
            w=h=0; local='/'+IMGDIR+'/'+h12+origext
    else:
        w=h=0; local='/'+IMGDIR+'/'+h12+origext
    after=os.path.getsize(local.lstrip('/')) if os.path.exists(local.lstrip('/')) else before
    mapping[u]=(local,w,h)
    print('  OK  %-20s %5d KB -> %4d KB  (%sx%s)'%(os.path.basename(local),before//1024,after//1024,w or '?',h or '?'))

# riscrive HTML: url->locale + width/height
for hf in htmls:
    s=open(hf,encoding='utf-8').read()
    for u,(local,w,h) in mapping.items():
        s=s.replace(u,local)
        if w and h:
            # aggiunge width/height all'<img> che punta a questo file (se non li ha già)
            def add_wh(m):
                tag=m.group(0)
                if ' width=' in tag: return tag
                return tag[:4]+f' width="{w}" height="{h}"'+tag[4:]
            s=re.sub(r'<img\b[^>]*\bsrc="'+re.escape(local)+r'"[^>]*>', add_wh, s)
    s=s.replace(' onerror="this.remove()"','')
    open(hf,'w',encoding='utf-8').write(s)

tot=sum(os.path.getsize(os.path.join(IMGDIR,x)) for x in os.listdir(IMGDIR))//1024
print('\nFatto: %d immagini WebP locali. Peso totale /images: %d KB.'%(len(mapping),tot))
print('Il sito è indipendente da Base44, in formato moderno e leggero.')
