"""Creative Event IQ logo concepts — round 2."""
import math
from PIL import Image, ImageDraw, ImageFont

GOLD = (203, 170, 78)
GOLD_LT = (232, 201, 122)
CREAM = (253, 251, 246)
INK = (13, 13, 13)

def font(cands, size):
    for p in cands:
        try: return ImageFont.truetype(p, size)
        except Exception: pass
    return ImageFont.load_default()

SERIF = ["/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf",
         "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"]
SANS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
SANS_B = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]

SS = 3

def wordmark(d, x, y, size, dark=False):
    f = font(SERIF, size)
    ev = "Event "
    d.text((x, y), ev, font=f, fill=INK if dark else CREAM)
    w = d.textbbox((0,0), ev, font=f)[2]
    d.text((x+w, y), "IQ", font=f, fill=GOLD)
    return x + w + d.textbbox((0,0),"IQ",font=f)[2]

# ---- creative marks (s = box size) ----
def m_mixer(d, x, y, s, c):
    """Fader + knob — mixing console controls."""
    u = s/32
    # fader track + cap
    d.rounded_rectangle([x+8*u, y+4*u, x+10*u, y+28*u], radius=1*u, fill=c)
    d.rounded_rectangle([x+4*u, y+9*u, x+14*u, y+13*u], radius=1.5*u, fill=GOLD_LT)
    # knob
    kx, ky, r = 22*u, 16*u, 8*u
    d.ellipse([x+kx-r, y+ky-r, x+kx+r, y+ky+r], outline=c, width=max(2,int(1.8*u)))
    d.line([x+kx, y+ky, x+kx, y+ky-r], fill=GOLD_LT, width=max(2,int(1.8*u)))
    d.ellipse([x+kx-1.6*u, y+ky-1.6*u, x+kx+1.6*u, y+ky+1.6*u], fill=GOLD_LT)

def m_speaker(d, x, y, s, c):
    u = s/32; cx, cy = x+16*u, y+16*u
    for r in (14, 9):
        d.ellipse([cx-r*u, cy-r*u, cx+r*u, cy+r*u], outline=c, width=max(2,int(1.5*u)))
    d.ellipse([cx-3.2*u, cy-3.2*u, cx+3.2*u, cy+3.2*u], fill=GOLD_LT)

def m_radial(d, x, y, s, c):
    u = s/32; cx, cy = x+16*u, y+16*u; n = 30
    for i in range(n):
        a = 2*math.pi*i/n
        inner = 5.5*u
        outer = (9 + 5*abs(math.sin(i*1.7)))*u
        d.line([cx+math.cos(a)*inner, cy+math.sin(a)*inner,
                cx+math.cos(a)*outer, cy+math.sin(a)*outer],
               fill=c, width=max(2,int(1.3*u)))
    d.ellipse([cx-3*u, cy-3*u, cx+3*u, cy+3*u], fill=GOLD_LT)

def m_knob(d, x, y, s, c):
    u = s/32; cx, cy = x+16*u, y+16*u; R = 11*u
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=c, width=max(2,int(1.7*u)))
    for i in range(11):
        a = math.radians(120 + i*30)
        d.line([cx+math.cos(a)*(R+2*u), cy+math.sin(a)*(R+2*u),
                cx+math.cos(a)*(R+5*u), cy+math.sin(a)*(R+5*u)],
               fill=c, width=max(1,int(1.0*u)))
    a = math.radians(255)
    d.line([cx, cy, cx+math.cos(a)*R*0.65, cy+math.sin(a)*R*0.65], fill=GOLD_LT, width=max(2,int(1.9*u)))
    d.ellipse([cx-2*u, cy-2*u, cx+2*u, cy+2*u], fill=GOLD_LT)

def m_negbadge(d, x, y, s):
    """Solid gold tile with equalizer bars knocked out (negative space)."""
    u = s/32
    d.rounded_rectangle([x, y, x+s, y+s], radius=7*u, fill=GOLD)
    for bx,by,bw,bh in [(7,12,3,8),(12,8,3,16),(17,6,3,20),(22,10,3,12)]:
        d.rounded_rectangle([x+bx*u, y+by*u, x+(bx+bw)*u, y+(by+bh)*u], radius=1.5*u, fill=INK)

def wavebars(d, x, y, w, c):
    n = 52
    bw = w/(n*1.7); gap = bw*0.7
    for i in range(n):
        t = i/(n-1)
        amp = 3 + 15*math.exp(-((t-0.68)**2)/0.03) + 2.5*abs(math.sin(t*22))
        bx = x + i*(bw+gap)
        d.rounded_rectangle([bx, y-amp, bx+bw, y+amp], radius=bw/2, fill=c)

# ---- sheet ----
W = 1200*SS; TILE = 215*SS; N = 6; HEAD = 130*SS
H = HEAD + TILE*N
img = Image.new("RGB", (W, H), (10,10,10))
d = ImageDraw.Draw(img)

hf = font(SERIF, 46*SS); sf = font(SANS, 18*SS)
d.text((50*SS, 40*SS), "Event ", font=hf, fill=CREAM)
ew = d.textbbox((0,0),"Event ",font=hf)[2]
d.text((50*SS+ew, 40*SS), "IQ", font=hf, fill=GOLD)
d.text((50*SS, 95*SS), "Creative concepts — round 2  (sound / mixing-console motifs)", font=sf, fill=(150,150,150))

labels = [
 "A  Mixing-console mark  (fader + knob)",
 "B  Waveform underline  (audio signature)",
 "C  Speaker-cone mark  (concentric driver)",
 "D  Sound-burst emblem  (radial EQ)",
 "E  Rotary knob mark  (with level ticks)",
 "F  Filled gold badge  (negative-space bars)",
]
lf = font(SANS_B, 15*SS)

for i in range(N):
    ty = HEAD + i*TILE
    bg = (18,18,18) if i % 2 else (13,13,13)
    d.rectangle([0, ty, W, ty+TILE], fill=bg)
    d.line([0, ty, W, ty], fill=(55,55,55), width=1)
    d.text((50*SS, 18*SS+ty), labels[i], font=lf, fill=GOLD)
    cx = 72*SS; cy = ty + 84*SS; ms = 72*SS; ws = 58*SS
    if i == 0:
        m_mixer(d, cx, cy, ms, GOLD); wordmark(d, cx+ms+30*SS, cy+4*SS, ws)
    elif i == 1:
        endx = wordmark(d, 72*SS, ty+58*SS, ws)
        wavebars(d, 80*SS, ty+170*SS, endx-72*SS-10*SS, GOLD)
    elif i == 2:
        m_speaker(d, cx, cy, ms, GOLD); wordmark(d, cx+ms+30*SS, cy+4*SS, ws)
    elif i == 3:
        m_radial(d, cx, cy, ms, GOLD); wordmark(d, cx+ms+30*SS, cy+4*SS, ws)
    elif i == 4:
        m_knob(d, cx, cy, ms, GOLD); wordmark(d, cx+ms+30*SS, cy+4*SS, ws)
    elif i == 5:
        m_negbadge(d, cx, cy, ms); wordmark(d, cx+ms+30*SS, cy+4*SS, ws)

img = img.resize((W//SS, H//SS), Image.LANCZOS)
img.save("logo-mockups-2.png")
print("wrote logo-mockups-2.png", img.size)
