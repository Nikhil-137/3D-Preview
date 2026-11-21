"""Generates Android launcher icons from icon.png into the Capacitor android project."""
import os, sys
from PIL import Image, ImageDraw

SRC = 'icon.png'
RES = 'android/app/src/main/res'
BG = '#171b21'

if not os.path.exists(SRC):
    print('icon.png not found, keeping the default icon')
    sys.exit(0)

src = Image.open(SRC).convert('RGB')
legacy = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
fore = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}

def rounded(img, radius_ratio):
    s = img.size[0]
    mask = Image.new('L', (s * 4, s * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s * 4 - 1, s * 4 - 1), radius=int(s * 4 * radius_ratio), fill=255)
    out = img.convert('RGBA')
    out.putalpha(mask.resize((s, s), Image.LANCZOS))
    return out

for d in legacy:
    folder = f'{RES}/mipmap-{d}'
    os.makedirs(folder, exist_ok=True)
    s = legacy[d]
    sq = src.resize((s, s), Image.LANCZOS)
    rounded(sq, 0.18).save(f'{folder}/ic_launcher.png')
    rounded(sq, 0.5).save(f'{folder}/ic_launcher_round.png')
    src.resize((fore[d], fore[d]), Image.LANCZOS).save(f'{folder}/ic_launcher_foreground.png')

os.makedirs(f'{RES}/mipmap-anydpi-v26', exist_ok=True)
xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
       '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
       '    <background android:drawable="@color/ic_launcher_background"/>\n'
       '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
       '</adaptive-icon>\n')
for name in ('ic_launcher.xml', 'ic_launcher_round.xml'):
    open(f'{RES}/mipmap-anydpi-v26/{name}', 'w').write(xml)

os.makedirs(f'{RES}/values', exist_ok=True)
open(f'{RES}/values/ic_launcher_background.xml', 'w').write(
    f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{BG}</color>\n</resources>\n')
print('Icons generated')
