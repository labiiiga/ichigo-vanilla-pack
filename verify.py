from pathlib import Path
import json, math, zipfile
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parent
rp=root/'resourcepack'
models=list((rp/'assets/ichigo/models/item').glob('*.json'))
for p in list(rp.rglob('*.json'))+list((root/'datapack').rglob('*.json')):
    json.loads(p.read_text(encoding='utf-8'))
for p in models:
    data=json.loads(p.read_text())
    for e in data['elements']:
        assert all(-16<=n<=32 for n in e['from']+e['to']),p
        assert all(a<b for a,b in zip(e['from'],e['to'])),p
    for texture in data['textures'].values():
        ns,name=texture.split(':')
        assert (rp/f'assets/{ns}/textures/{name}.png').is_file(),(p,texture)
for p in (rp/'assets/ichigo/items').glob('*.json'):
    target=json.loads(p.read_text())['model']['model'].split(':')[1]
    assert (rp/f'assets/ichigo/models/{target}.json').is_file()
for p in (rp/'assets/ichigo/equipment').glob('*.json'):
    for layer,values in json.loads(p.read_text())['layers'].items():
        for value in values:
            ns,name=value['texture'].split(':')
            assert (rp/f'assets/{ns}/textures/entity/equipment/{layer}/{name}.png').is_file()
for p in (root/'dist').glob('*.zip'):
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        assert 'pack.mcmeta' in z.namelist()

# Catch missing frames, blank alpha, frozen animation and accidental opaque cards.
for name in ('getsuga','blue_getsuga'):
    p=rp/f'assets/ichigo/textures/item/{name}.png'
    sheet=Image.open(p).convert('RGBA')
    assert sheet.size==(512,4096)
    meta=json.loads(p.with_suffix('.png.mcmeta').read_text())
    assert meta['animation']['frametime']==1
    frames=[sheet.crop((0,i*512,512,(i+1)*512)) for i in range(8)]
    assert len({im.tobytes() for im in frames})==8, 'Frozen animation'
    for im in frames:
        alpha=im.getchannel('A')
        assert alpha.getextrema()==(0,255)
        bbox=alpha.getbbox()
        assert bbox and 0<bbox[0]<bbox[2]<512 and 0<bbox[1]<bbox[3]<512,'Clipped artwork'

# Geometry preview: this is an asset preview, not a screenshot from Minecraft.
palette=[(13,15,23),(34,38,51),(193,211,220),(248,247,232),(182,21,42),(245,59,73),(204,153,64),(73,196,246),(236,126,39),(80,84,99),(121,20,39),(255,255,255)]
im=Image.new('RGB',(1400,980),(21,24,33));d=ImageDraw.Draw(im)
try:
    title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',34)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
except OSError:title=font=ImageFont.load_default()
d.text((40,25),'ICHIGO  /  ORIGINAL VANILLA ASSET PREVIEW',font=title,fill=(237,234,225))
d.text((42,75),'Java 26.2  |  3D JSON geometry + custom equipment textures  |  v1',font=font,fill=(154,165,183))
names=['zangetsu','tensa_zangetsu','true_zangetsu','true_short','hollow_mask','vasto_mask','mugetsu_head','jujisho']
for index,name in enumerate(names):
    col=index%4;row=index//4;cx=col*340+30;cy=row*385+125
    d.rounded_rectangle((cx,cy,cx+320,cy+365),radius=15,fill=(30,34,46),outline=(51,57,72),width=1)
    data=json.loads((rp/f'assets/ichigo/models/item/{name}.json').read_text())
    def proj(v):
        x,y,z=v
        return ((x-8)*.9+(z-8)*.45, -y+(x-8)*.12+(z-8)*.15)
    faces=[]
    for e in data['elements']:
        a,b=e['from'],e['to'];x0,y0,z0=a;x1,y1,z1=b
        uv=e['faces']['north']['uv'];pi=int(uv[0]//4)+4*int(uv[1]//4);color=palette[pi]
        for factor,vertices in [(1,[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)]),(.65,[(x1,y0,z0),(x1,y0,z1),(x1,y1,z1),(x1,y1,z0)]),(1.18,[(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)])]:
            if 'rotation' in e:
                rotation=e['rotation'];ox,oy,oz=rotation['origin'];t=math.radians(rotation['angle'])
                assert rotation['axis']=='z'
                vertices=[(ox+(x-ox)*math.cos(t)-(y-oy)*math.sin(t),oy+(x-ox)*math.sin(t)+(y-oy)*math.cos(t),z) for x,y,z in vertices]
            depth=sum(v[2]-v[0]*.2-v[1]*.02 for v in vertices)/4
            faces.append((depth,[proj(v) for v in vertices],tuple(min(255,int(c*factor)) for c in color)))
    points=[point for _,verts,_ in faces for point in verts]
    xmin=min(p[0] for p in points);xmax=max(p[0] for p in points);ymin=min(p[1] for p in points);ymax=max(p[1] for p in points)
    scale=min(240/(xmax-xmin),275/(ymax-ymin))
    for _,verts,color in sorted(faces,reverse=True):
        screen=[(cx+160+(x-(xmin+xmax)/2)*scale,cy+160+(y-(ymin+ymax)/2)*scale) for x,y in verts]
        d.polygon(screen,fill=color)
    d.text((cx+18,cy+326),name.replace('_',' ').upper(),font=font,fill=(229,230,235))
d.text((42,928),'Six forms: Shikai / Bankai / Hollow / Vasto Lorde / True Shikai / Mugetsu',font=font,fill=(211,218,228))
im.save(root/'dist/asset-preview.png')
print(f'PASS: JSON, {len(models)} geometries, textures, equipment references, ZIP integrity. Preview saved.')
