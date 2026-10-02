"""Compose Blender renders for review; no glow or other effects added."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',30)
frames=[]
for i in range(1,9):
    canvas=Image.new('RGBA',(1060,650),(18,22,31,255))
    d=ImageDraw.Draw(canvas)
    d.text((30,18),'GETSUGA TENSHO / BLENDER BAKE',font=title,fill=(239,237,227))
    for j,(name,label) in enumerate([('getsuga','BANKAI / BLACK + CRIMSON'),('blue_getsuga','SHIKAI / BLUE')]):
        panel=Image.new('RGBA',(512,512),(28,33,44,255))
        panel.alpha_composite(Image.open(root/f'frames/{name}/{i:02}.png').convert('RGBA'))
        canvas.alpha_composite(panel,(14+j*520,70))
        d.text((30+j*520,588),label,font=font,fill=(211,218,233))
    d.text((30,620),'Source render preview - not an in-game screenshot',font=font,fill=(132,145,164))
    frames.append(canvas.convert('RGB'))
frames[0].save(root.parent/'dist/getsuga-preview.png')
frames[0].save(root.parent/'dist/getsuga-animation.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
