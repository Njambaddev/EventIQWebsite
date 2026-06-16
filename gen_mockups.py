"""Render a contact sheet of Event IQ logo style options for comparison."""
from PIL import Image, ImageDraw, ImageFont

GOLD = (201, 168, 76)
GOLD_LT = (232, 201, 122)
CREAM = (253, 251, 246)
INK = (13, 13, 13)
PANEL = (20, 20, 20)

def font(cands, size):
    for p in cands:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

SERIF = ["/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf",
         "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"]
SANS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
SANS_B = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]

SS = 2  # supersample

# ---------- marks ----------
def mark_bars(d, x, y, s, color):
    u = s/32
    for bx,by,bw,bh in [(7,12,3,8),(12,8,3,16),(17,6,3,20),(22,10,3,12)]:
        d.rounded_rectangle([x+bx*u,y+by*u,x+(bx+bw)*u,y+(by+bh)*u], radius=1.5*u, fill=color)

def mark_wave(d, x, y, s, color):
    u = s/32
    hs = [8,14,20,26,20,14,8]; bw=2; gap=(32-len(hs)*bw)/(len(hs)+1)
    for i,h in enumerate(hs):
        bx=(i+1)*gap+i*bw; by=16-h/2
        d.rounded_rectangle([x+bx*u,y+by*u,x+(bx+bw)*u,y+(by+h)*u], radius=1*u, fill=color)

def mark_arcs(d, x, y, s, color):
    u = s/32; cx,cy=9,16
    d.ellipse([x+(cx-2)*u,y+(cy-2)*u,x+(cx+2)*u,y+(cy+2)*u], fill=color)
    for r in (6,11,16):
        d.arc([x+(cx-r)*u,y+(cy-r)*u,x+(cx+r)*u,y+(cy+r)*u], start=-52, end=52,
              fill=color, width=max(2,int(1.7*u)))

def mark_badge(d, x, y, s, bars=True):
    u = s/32
    d.rounded_rectangle([x,y,x+s,y+s], radius=7*u, fill=INK)
    d.rounded_rectangle([x+2*u,y+2*u,x+s-2*u,y+s-2*u], radius=5.5*u, outline=GOLD, width=max(1,int(0.7*u)))
    if bars:
        mark_bars(d, x, y, s, GOLD)

def mark_monogram(d, x, y, s):
    u = s/32
    d.rounded_rectangle([x,y,x+s,y+s], radius=7*u, fill=INK)
    d.rounded_rectangle([x+2*u,y+2*u,x+s-2*u,y+s-2*u], radius=5.5*u, outline=GOLD, width=max(1,int(0.7*u)))
    f = font(SERIF, int(s*0.5))
    t = "IQ"
    bb = d.textbbox((0,0), t, font=f)
    d.text((x+s/2-(bb[2]-bb[0])/2-bb[0], y+s/2-(bb[3]-bb[1])/2-bb[1]), t, font=f, fill=GOLD)

# ---------- text ----------
def track_text(d, pos, text, f, fill, tracking=0):
    x, y = pos
    for ch in text:
        d.text((x,y), ch, font=f, fill=fill)
        bb = d.textbbox((0,0), ch, font=f)
        x += (bb[2]-bb[0]) + tracking + (f.size*0.04)
    return x

def wordmark(d, x, y, size, dark_text=False, caps=False, tracking=0):
    """Draw 'Event IQ' with gold IQ. Returns baseline-ish."""
    f = font(SANS_B if caps else SERIF, size)
    ev = "EVENT " if caps else "Event "
    iq = "IQ"
    tcol = INK if dark_text else CREAM
    if caps:
        endx = track_text(d, (x,y), ev, f, tcol, tracking)
        track_text(d, (endx, y), iq, f, GOLD, tracking)
    else:
        d.text((x,y), ev, font=f, fill=tcol)
        bb = d.textbbox((0,0), ev, font=f)
        d.text((x+(bb[2]-bb[0]), y), iq, font=f, fill=GOLD)

# ---------- sheet ----------
W = 1200*SS
TILE = 200*SS
N = 6
HEAD = 120*SS
H = HEAD + TILE*N
img = Image.new("RGB", (W, H), (10,10,10))
d = ImageDraw.Draw(img)

# header
hf = font(SERIF, 46*SS); sf = font(SANS, 18*SS)
d.text((50*SS, 38*SS), "Event IQ", font=hf, fill=CREAM)
bb = d.textbbox((0,0), "Event IQ", font=hf);
d.text((50*SS, 38*SS), "Event ", font=hf, fill=CREAM)
ev_w = d.textbbox((0,0),"Event ",font=hf)[2]
d.text((50*SS+ev_w, 38*SS), "IQ", font=hf, fill=GOLD)
d.text((50*SS, 90*SS), "Logo style options — pick one (or mix mark + wordmark)", font=sf, fill=(150,150,150))

labels = [
 "1  Mark + serif wordmark  (horizontal)",
 "2  Stacked  (mark over wordmark)",
 "3  Sound-wave mark + wordmark",
 "4  Monogram badge 'IQ' + wordmark",
 "5  Modern all-caps sans  (tracked)",
 "6  Light background variant",
]
lf = font(SANS_B, 15*SS)

for i in range(N):
    ty = HEAD + i*TILE
    light = (i == 5)
    bg = CREAM if light else (PANEL if i % 2 else (15,15,15))
    d.rectangle([0, ty, W, ty+TILE], fill=bg)
    d.line([0, ty, W, ty], fill=(60,60,60) if not light else (210,205,195), width=1)
    # label
    d.text((50*SS, ty+18*SS), labels[i], font=lf, fill=GOLD if not light else (150,120,30))
    cx = 70*SS
    cy = ty + 78*SS
    msize = 70*SS
    wsize = 58*SS
    if i == 0:
        mark_bars(d, cx, cy, msize, GOLD)
        wordmark(d, cx+msize+28*SS, cy+2*SS, wsize)
    elif i == 1:
        # stacked, centered in a column on the left third
        colcx = 230*SS
        mark_bars(d, colcx-msize/2, ty+44*SS, msize, GOLD)
        f = font(SERIF, 40*SS)
        ev_w = d.textbbox((0,0),"Event ",font=f)[2]; iq_w=d.textbbox((0,0),"IQ",font=f)[2]
        tot = ev_w+iq_w; sx = colcx-tot/2; sy=ty+125*SS
        d.text((sx,sy),"Event ",font=f,fill=CREAM); d.text((sx+ev_w,sy),"IQ",font=f,fill=GOLD)
    elif i == 2:
        mark_arcs(d, cx, cy, msize, GOLD)
        wordmark(d, cx+msize+28*SS, cy+2*SS, wsize)
    elif i == 3:
        mark_monogram(d, cx, cy, msize)
        wordmark(d, cx+msize+28*SS, cy+2*SS, wsize)
    elif i == 4:
        track_text(d, (cx, cy+10*SS), "EVENT ", font(SANS_B, 46*SS), CREAM, tracking=6*SS)
        # continue IQ in gold
        f=font(SANS_B,46*SS)
        # measure tracked EVENT width
        x=cx
        for ch in "EVENT ":
            x += d.textbbox((0,0),ch,font=f)[2] + 6*SS + f.size*0.04
        track_text(d,(x,cy+10*SS),"IQ",f,GOLD,tracking=6*SS)
    elif i == 5:
        mark_badge(d, cx, cy, msize, bars=True)
        wordmark(d, cx+msize+28*SS, cy+2*SS, wsize, dark_text=True)

img = img.resize((W//SS, H//SS), Image.LANCZOS)
img.save("logo-mockups.png")
print("wrote logo-mockups.png", img.size)
