import sys, subprocess, os
from PIL import Image, ImageDraw
T=os.path.expanduser("~/.local/share/Tesseract/bin/tsrct")
proj, out, times = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
d=os.path.dirname(out); tiles=[]
for t in times:
    p=f"{d}/f_{t:05.2f}.png"
    r=subprocess.run([T,"preview","--project",proj,"--time",str(t),"--output",p],capture_output=True,text=True)
    if r.returncode: print(t, r.stdout, r.stderr[-300:]); continue
    im=Image.open(p).convert("RGB").resize((270,480)); ImageDraw.Draw(im).text((6,6),f"{t:.2f}s",fill=(255,255,0)); tiles.append(im)
cols=min(6,len(tiles)); rows=(len(tiles)+cols-1)//cols
sheet=Image.new("RGB",(cols*274,rows*484),(40,40,40))
for i,im in enumerate(tiles): sheet.paste(im,((i%cols)*274,(i//cols)*484))
sheet.save(out); print("sheet",out,len(tiles))
