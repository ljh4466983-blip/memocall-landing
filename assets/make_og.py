from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1200, 630
BG = (7, 8, 10)

base = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(base)

# --- radial mint glow ---
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
cx, cy, rad = 220, -60, 620
for i in range(rad, 0, -6):
    t = 1 - i / rad
    a = int(38 * (t ** 2.2))
    gd.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(7 + a, 8 + a, 10 + int(a * 0.9)))
glow = glow.filter(ImageFilter.GaussianBlur(40))
base = Image.blend(base, glow, 0.85)
d = ImageDraw.Draw(base)

# violet glow bottom right
glow2 = Image.new("RGB", (W, H), BG)
g2 = ImageDraw.Draw(glow2)
cx, cy, rad = 1120, 640, 520
for i in range(rad, 0, -6):
    t = 1 - i / rad
    g2.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(7 + int(16 * t ** 2), 8, 10 + int(32 * t ** 2)))
glow2 = glow2.filter(ImageFilter.GaussianBlur(50))
base = Image.blend(base, glow2, 0.6)
d = ImageDraw.Draw(base)

# --- grid ---
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gr = ImageDraw.Draw(grid)
step = 60
for x in range(0, W + step, step):
    gr.line([(x, 0), (x, H)], fill=(255, 255, 255, 9), width=1)
for y in range(0, H + step, step):
    gr.line([(0, y), (W, y)], fill=(255, 255, 255, 9), width=1)
# fade grid
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
for y in range(H):
    v = int(255 * max(0.0, 1 - y / (H * 0.95)))
    md.line([(0, y), (W, y)], fill=v)
base = Image.composite(Image.alpha_composite(base.convert("RGBA"), grid).convert("RGB"), base, mask)
d = ImageDraw.Draw(base)

FONT = "/usr/share/fonts/pickle-hwp/NotoSansCJKkr-Regular.otf"
def f(sz): return ImageFont.truetype(FONT, sz)

MINT = (62, 224, 161)
MINT_L = (123, 243, 198)
MINT_D = (52, 211, 153)
WHITE = (244, 245, 247)
GREY = (154, 163, 171)
DIM = (122, 129, 137)

# --- logo mark ---
x0, y0, s = 80, 62, 46
mark = Image.new("RGBA", (s * 3, s * 3), (0, 0, 0, 0))
for yy in range(s * 3):
    for xx in range(s * 3):
        mark.putpixel((xx, yy), (0, 0, 0, 0))
grad = Image.new("RGB", (s, s))
gp = grad.load()
for yy in range(s):
    for xx in range(s):
        t = (xx + yy) / (2 * s)
        r = int(52 + (14 - 52) * t * -1)
        gp[xx, yy] = (int(52 + (46 - 52) * t), int(211 + (163 - 211) * t) + 13, int(153 + (113 - 153) * t) + 10)
m = Image.new("L", (s, s), 0)
ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1], radius=13, fill=255)
base.paste(grad, (x0, y0), m)
# waveform bars inside mark
for i, (bx, bh) in enumerate([(13, 12), (20, 24), (27, 17), (34, 8)]):
    bx += 0
    d.rounded_rectangle([x0 + bx - 2, y0 + s // 2 - bh // 2, x0 + bx + 1, y0 + s // 2 + bh // 2],
                        radius=1.5, fill=(6, 35, 26))

d.text((x0 + s + 16, y0 + 2), "메모콜", font=f(27), fill=WHITE, stroke_width=0)
d.text((x0 + s + 16 + 82, y0 + 12), "MemoCall", font=f(15), fill=DIM)

# --- headline ---
hx, hy = 80, 208
d.text((hx, hy), "통화가 끝나면,", font=f(56), fill=WHITE, stroke_width=1)
line2 = "일정과 발주서가 완성됩니다."
lh = 74
# gradient text for line 2
big = f(56)
tmp = Image.new("L", (W, H), 0)
ImageDraw.Draw(tmp).text((hx, hy + lh), line2, font=big, fill=255, stroke_width=1)
gw = 900
gimg = Image.new("RGB", (W, H), (0, 0, 0))
for xx in range(W):
    t = min(1.0, max(0.0, (xx - hx) / 760))
    r = int(MINT_L[0] + (142 - MINT_L[0]) * t)
    g = int(MINT_L[1] + (230 - MINT_L[1]) * t)
    b = int(MINT_L[2] + (255 - MINT_L[2]) * t)
    ImageDraw.Draw(gimg).line([(xx, 0), (xx, H)], fill=(r, g, b))
base.paste(gimg, (0, 0), tmp)
d = ImageDraw.Draw(base)

# --- subline ---
d.text((hx, hy + lh * 2 + 12), "소상공인·프리랜서·영업직을 위한 온디바이스 AI 통화 비서",
       font=f(21), fill=GREY)

# --- chips ---
chips = ["Whisper STT", "OpenAI 요약", "캘린더 자동 등록", "발주서 PDF · CSV"]
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
cx = hx
cy = 492
for label in chips:
    fnt = f(16)
    tw = od.textlength(label, font=fnt)
    w = int(tw + 50)
    od.rounded_rectangle([cx, cy, cx + w, cy + 40], radius=20, fill=(255, 255, 255, 15),
                         outline=(255, 255, 255, 40), width=1)
    od.ellipse([cx + 16, cy + 17, cx + 23, cy + 24], fill=MINT + (255,))
    od.text((cx + 32, cy + 10), label, font=fnt, fill=(214, 219, 225, 255))
    cx += w + 12
base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
d = ImageDraw.Draw(base)

# --- right side decorative card ---
cw, ch = 250, 190
cxp, cyp = W - cw - 70, 250
card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=20, fill=(255, 255, 255, 16), outline=(255, 255, 255, 34), width=1)
base = base.convert("RGBA")
base.paste(card, (cxp, cyp), card)
base = base.convert("RGB")
d = ImageDraw.Draw(base)
d.text((cxp + 24, cyp + 22), "발주서", font=f(13), fill=(140, 148, 156))
d.text((cxp + 24, cyp + 46), "삼겹살 20kg × 2", font=f(15), fill=(228, 231, 235))
d.line([(cxp + 24, cyp + 72), (cxp + cw - 24, cyp + 72)], fill=(255, 255, 255, 26), width=1)
d.text((cxp + 24, cyp + 84), "대패 10kg × 1", font=f(15), fill=(228, 231, 235))
d.line([(cxp + 24, cyp + 110), (cxp + cw - 24, cyp + 110)], fill=(255, 255, 255, 26), width=1)
d.text((cxp + 24, cyp + 124), "합계", font=f(14), fill=(140, 148, 156))
d.text((cxp + cw - 100, cyp + 118), "800,000원", font=f(19), fill=MINT, stroke_width=1)

# --- bottom hairline ---
d.line([(80, 578), (W - 80, 578)], fill=(255, 255, 255, 22), width=1)
d.text((80, 594), "IMG Story  ·  메모콜 MemoCall  ·  ljh4466983@gmail.com", font=f(14), fill=(105, 112, 120))

base.save("/workspace/memocall-landing/assets/og-image.png", "PNG", optimize=True)
print("saved", base.size)
