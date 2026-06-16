"""Generate Event IQ favicon set (PNG + ICO + Apple touch) from the brand mark."""
from PIL import Image, ImageDraw

GOLD_TOP = (232, 201, 122)   # #E8C97A
GOLD_BOT = (201, 168, 76)    # #C9A84C
INK = (13, 13, 13)           # #0D0D0D
S = 1024                     # master render size (supersampled)
U = S / 32.0                 # design is in 32-unit space

def gold_gradient(size):
    g = Image.new("RGB", (1, size))
    for y in range(size):
        t = y / max(size - 1, 1)
        g.putpixel((0, y), tuple(round(GOLD_TOP[i] + (GOLD_BOT[i] - GOLD_TOP[i]) * t) for i in range(3)))
    return g.resize((size, size))

def bars_mask(size):
    """White rounded bars on black, in 32-unit coords scaled to `size`."""
    u = size / 32.0
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    bars = [(7, 12, 3, 8), (12, 8, 3, 16), (17, 6, 3, 20), (22, 10, 3, 12)]
    for x, y, w, h in bars:
        d.rounded_rectangle([x*u, y*u, (x+w)*u, (y+h)*u], radius=1.5*u, fill=255)
    return m

def render(size, rounded=True, transparent=True):
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0) if transparent else INK + (255,))
    d = ImageDraw.Draw(bg)
    u = size / 32.0
    if rounded:
        d.rounded_rectangle([0, 0, size-1, size-1], radius=7*u, fill=INK + (255,))
        # subtle gold border
        d.rounded_rectangle([3.5*u, 3.5*u, size-3.5*u, size-3.5*u], radius=5.5*u,
                            outline=GOLD_BOT + (90,), width=max(1, round(0.6*u)))
    grad = gold_gradient(size).convert("RGBA")
    bg.paste(grad, (0, 0), bars_mask(size))
    return bg

master = render(S, rounded=True)

def save_png(name, size, **kw):
    render(size, **kw).resize((size, size), Image.LANCZOS) if False else None
    img = render(size, **kw) if size > 64 else master.resize((size, size), Image.LANCZOS)
    img.save(name)
    print("wrote", name, img.size)

# PNG favicons (transparent rounded corners)
for sz in (16, 32, 48, 192, 512):
    out = master.resize((sz, sz), Image.LANCZOS)
    out.save(f"favicon-{sz}.png")
    print("wrote", f"favicon-{sz}.png")

# Multi-size ICO
master.resize((256, 256), Image.LANCZOS).save("favicon.ico", sizes=[(16,16),(32,32),(48,48)])
print("wrote favicon.ico")

# Apple touch icon — opaque dark square (iOS rounds it itself)
apple = render(S, rounded=False, transparent=False).resize((180, 180), Image.LANCZOS)
apple.save("apple-touch-icon.png")
print("wrote apple-touch-icon.png (180)")
