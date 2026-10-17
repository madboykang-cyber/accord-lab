# 시냅스 랩 세로 포스터 컷 4장(1080x1350)을 홈페이지와 같은 Pretendard 글꼴·톤으로 생성한다. 출력: poster/cut-01~04.jpg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
W, H = 1080, 1350
FD = r"C:\Users\PC\클로드 코드\fonts"
def f(size, w="ExtraBold"): return ImageFont.truetype(os.path.join(FD, f"Pretendard-{w}.otf"), size)
INK = (11, 18, 32); YEL = (254, 229, 0); SKY = (147, 197, 253); WHITE = (255, 255, 255); MUTED = (170, 184, 220); GREEN = (52, 211, 153); BRAND = (37, 99, 235); INDIGO = (79, 70, 229)
SYM = Image.open("../synapse-lab-next/public/symbol.png").convert("RGBA")
HERO = Image.open("../synapse-lab-next/public/bg-hero.jpg").convert("RGB")
SITE = Image.open("../synapse-lab-ad/assets/site-mobile.png").convert("RGB")

def base(photo=True):
    img = Image.new("RGB", (W, H), INK)
    if photo:
        ph = HERO.resize((W, int(HERO.height * W / HERO.width)), Image.LANCZOS).crop((0, 0, W, H))
        img.paste(ph, (0, 0))
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for y in range(H):
            a = int(120 + 120 * (y / H)); od.line([(0, y), (W, y)], fill=INK + (a,))
        img = img.convert("RGBA"); img.alpha_composite(ov)
    else:
        img = img.convert("RGBA")
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([520, -300, 1400, 560], fill=INDIGO + (150,)); gd.ellipse([-340, 760, 520, 1620], fill=BRAND + (130,))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(140)))
    return img

def header(img, d, idx):
    tile = Image.new("RGBA", (96, 96), WHITE + (255,)); m = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, 95, 95], 24, fill=255); tile.putalpha(m)
    w = 74; s = SYM.resize((w, int(SYM.height * w / SYM.width)), Image.LANCZOS)
    tile.alpha_composite(s, ((96 - w) // 2, (96 - s.height) // 2)); img.alpha_composite(tile, (80, 80))
    d.text((196, 84), "SYNAPSE LAB", font=f(20, "SemiBold"), fill=(165, 180, 252))
    d.text((196, 112), "시냅스 랩", font=f(34, "Black"), fill=WHITE)
    d.text((W - 80, 102), f"{idx} / 4", font=f(22, "SemiBold"), fill=MUTED, anchor="ra")

def footer(d):
    d.rounded_rectangle([80, H - 166, W - 80, H - 88], 39, fill=YEL)
    d.text((W // 2, H - 150), "대표 직통 전화 010-9286-7134", font=f(38, "Black"), fill=(17, 17, 17), anchor="ma")
    d.text((W // 2, H - 64), "madboykang-cyber.github.io/synapse-lab", font=f(22, "Medium"), fill=MUTED, anchor="ma")

def pill(d, x, y, s, size=24, bg=YEL, fg=(17, 17, 17), w="Bold"):
    tw = d.textlength(s, font=f(size, w)) + 52
    d.rounded_rectangle([x, y, x + tw, y + size + 28], (size + 28) // 2, fill=bg)
    d.text((x + 26, y + 13), s, font=f(size, w), fill=fg)
    return tw

def phone(img, x, y, w, h, scroll_css=0):
    """모바일 캡처를 폰 프레임에 넣어 합성 (scroll_css: 보여줄 시작 위치, CSS px)"""
    r = 44
    frame = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0)); fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle([0, 0, w + 23, h + 23], r + 10, fill=(22, 27, 40, 255))
    scale = w / 780
    sh = int(h / scale)
    crop = SITE.crop((0, scroll_css * 2, 780, scroll_css * 2 + sh)).resize((w, h), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); crop.putalpha(m)
    frame.alpha_composite(crop, (12, 12))
    sh_ = Image.new("RGBA", (w + 160, h + 160), (0, 0, 0, 0)); ImageDraw.Draw(sh_).rounded_rectangle([80, 110, w + 80, h + 110], r + 10, fill=(0, 0, 0, 150))
    img.alpha_composite(sh_.filter(ImageFilter.GaussianBlur(40)), (x - 92, y - 92))
    img.alpha_composite(frame, (x - 12, y - 12))

# 1. 훅 + 사이트 화면
img = base(); d = ImageDraw.Draw(img); header(img, d, 1)
d.text((80, 300), "사업·영업용 홈페이지,", font=f(74, "Black"), fill=WHITE)
d.text((80, 392), "아직 없으세요?", font=f(74, "Black"), fill=YEL)
d.text((80, 520), "사진과 소개 문구만 보내주세요.", font=f(32, "Medium"), fill=(225, 232, 255))
d.text((80, 566), "3일 안에 실제 링크로 1차 시안을 보여드립니다.", font=f(32, "Medium"), fill=(225, 232, 255))
pill(d, 80, 650, "최초 후불제 · 시안 불만족 시 착수금 환불", 24)
pill(d, 80, 724, "NO 템플릿 · 100% 맞춤형 코딩 제작", 24, bg=WHITE)
phone(img, 580, 740, 420, 424, scroll_css=0)
d = ImageDraw.Draw(img)
d.text((80, 840), "랜딩페이지", font=f(30, "SemiBold"), fill=MUTED); d.text((80, 880), "89,000원", font=f(62, "Black"), fill=SKY)
d.text((80, 980), "올인원 프리미엄 홈페이지", font=f(30, "SemiBold"), fill=MUTED); d.text((80, 1020), "289,000원", font=f(62, "Black"), fill=SKY)
d.text((80, 1110), "고정가 · 추가 비용 0원", font=f(26, "Bold"), fill=WHITE)
footer(d); img.convert("RGB").save("poster/cut-01.jpg", quality=92)

# 2. 가격
img = base(); d = ImageDraw.Draw(img); header(img, d, 2)
d.text((80, 290), "고정가입니다.", font=f(80, "Black"), fill=WHITE)
d.text((80, 386), "추가 비용 없습니다.", font=f(80, "Black"), fill=YEL)
cards = [("TYPE A", "랜딩페이지", "89,000원", "광고 · 이벤트 · 신규 오픈용 원페이지", False), ("TYPE B · BEST", "올인원 프리미엄 홈페이지", "289,000원", "가게 · 회사 소개용 다중 섹션", True)]
for i, (tag, name, price, desc, best) in enumerate(cards):
    y = 540 + i * 262
    d.rounded_rectangle([80, y, W - 80, y + 224], 30, fill=WHITE if not best else (238, 242, 255), outline=BRAND if best else None, width=4)
    d.text((120, y + 30), tag, font=f(20, "Bold"), fill=BRAND)
    d.text((120, y + 60), name, font=f(38, "ExtraBold"), fill=INK)
    d.text((120, y + 118), price, font=f(72, "Black"), fill=BRAND)
    d.text((W - 120, y + 64), desc, font=f(22, "Medium"), fill=(90, 100, 130), anchor="ra")
    d.text((W - 120, y + 100), "반응형 · 검색 등록 · 호스팅 · SSL", font=f(22, "Medium"), fill=(90, 100, 130), anchor="ra")
    d.text((W - 120, y + 136), "상담 신청 폼 · 챗봇 기능 포함", font=f(22, "Medium"), fill=(90, 100, 130), anchor="ra")
d.text((80, 1080), "예약 관리자 · 결제 · 회원제처럼 별도 시스템이 필요한 경우만 옵션입니다.", font=f(24, "Medium"), fill=MUTED)
footer(d); img.convert("RGB").save("poster/cut-02.jpg", quality=92)

# 3. 후불제 절차
img = base(); d = ImageDraw.Draw(img); header(img, d, 3)
d.text((80, 290), "시안 보고 결정하는", font=f(70, "Black"), fill=WHITE)
d.text((80, 376), "최초 후불제", font=f(96, "Black"), fill=YEL)
steps = [("착수금 3만 원", "카톡 한마디로 시작합니다"), ("3일 이내 1차 시안", "실제 웹사이트 링크로 확인하세요"), ("수정 후 잔금", "만족하실 때만 결제합니다"), ("불만족 시 전액 환불", "착수금 100% 환불 · 비용 0원")]
for i, (a, b) in enumerate(steps):
    y = 560 + i * 132
    d.ellipse([80, y, 156, y + 76], fill=BRAND); d.text((118, y + 16), str(i + 1), font=f(36, "Black"), fill=WHITE, anchor="ma")
    d.text((190, y + 2), a, font=f(42, "ExtraBold"), fill=WHITE); d.text((190, y + 54), b, font=f(26, "Medium"), fill=MUTED)
    if i < 3: d.line([(118, y + 84), (118, y + 126)], fill=(70, 90, 150), width=4)
footer(d); img.convert("RGB").save("poster/cut-03.jpg", quality=92)

# 4. 포함 항목
img = base(); d = ImageDraw.Draw(img); header(img, d, 4)
d.text((80, 290), "이 금액 하나에", font=f(72, "Black"), fill=WHITE)
d.text((80, 376), "전부 들어 있습니다", font=f(72, "Black"), fill=YEL)
items = ["PC · 모바일 반응형 맞춤 제작", "네이버 · 구글 검색 등록 무료", "서버(호스팅) · SSL 평생 0원", "월 관리비 · 약정 · 위약금 0원", "상담 신청 폼 (구글시트 연동)", "+서비스 챗봇 기능", "카톡 공유 썸네일 · 파비콘", "오픈 후 1개월 수정 무제한", "사이트 · 도메인 100% 고객 소유"]
for i, s in enumerate(items):
    y = 510 + i * 66
    d.ellipse([80, y + 12, 108, y + 40], fill=GREEN)
    d.line([(88, y + 26), (97, y + 35), (110, y + 19)], fill=INK, width=4)
    d.text((128, y + 4), s, font=f(32, "SemiBold"), fill=WHITE)
footer(d); img.convert("RGB").save("poster/cut-04.jpg", quality=92)

ims = [Image.open(f"poster/cut-0{i}.jpg").resize((360, 450)) for i in range(1, 5)]
s = Image.new("RGB", (1440, 450)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save("poster/_cuts.jpg", quality=80)
print("4 cuts ok")
