"""Vanilla 26.2 VFX geometry. Arbitrary cuboid angles verified against its parser.
Rounded forms are overlapping tangent segments, not disconnected axis-aligned cubes.
The exact same geometry is imported into Blender for editable source and previews.
"""
import json, math, random
from pathlib import Path

PALETTE=[(9,11,19),(31,38,53),(151,169,184),(238,235,217),(149,7,31),(255,39,64),(219,170,82),(42,184,255),(235,104,24),(65,77,98),(58,4,21),(239,251,255), (77,21,120),(164,77,244),(15,70,129),(118,228,255)]
FORMS=['shikai','bankai','hollow','vasto','true','mugetsu','naruto']
ACCENTS=[7,5,5,8,15,13,8]

def build(rp):
    from PIL import Image, ImageDraw
    def write(name,elements,display=None):
        data={'ambientocclusion':False,'textures':{'palette':'ichigo:item/cinematic_palette','particle':'ichigo:item/cinematic_palette'},'elements':elements}
        if display:data['display']=display
        (rp/f'assets/ichigo/models/item/{name}.json').write_text(json.dumps(data,separators=(',',':')))
        (rp/f'assets/ichigo/items/{name}.json').write_text(json.dumps({'model':{'type':'minecraft:model','model':f'ichigo:item/{name}'}}))
    def box(center,size,c=0,angle=0,axis='z',glow=False):
        u=(c%4)*4;v=(c//4)*4
        d={'from':[round(a-b/2,5) for a,b in zip(center,size)],'to':[round(a+b/2,5) for a,b in zip(center,size)],
           'faces':{f:{'texture':'#palette','uv':[u+.75,v+.75,u+3.25,v+3.25]} for f in ['north','south','east','west','up','down']}}
        if angle:d['rotation']={'origin':list(center),'axis':axis,'angle':round(angle,5)}
        if glow:d.update(shade=False,light_emission=15)
        return d
    def arc(radius,width,depth,c,start=-100,end=100,center=(8,8,8),axis='z',segments=64,taper=True):
        out=[]
        for i in range(segments):
            u=(i+.5)/segments;t=math.radians(start+(end-start)*u)
            w=width*(max(.012,math.sin(math.pi*u))**.65 if taper else 1)
            pos=list(center)
            if axis=='z':
                pos[0]+=radius*math.cos(t);pos[1]+=radius*math.sin(t)
                size=[w,radius*abs(math.radians(end-start))/segments*1.045,depth]
                angle=math.degrees(t)
            else:
                pos[0]+=radius*math.cos(t);pos[2]+=radius*math.sin(t)
                size=[w,depth,radius*abs(math.radians(end-start))/segments*1.045]
                angle=-math.degrees(t)
            out.append(box(pos,size,c,angle,axis,True))
        return out
    atlas=Image.new('RGBA',(64,64));d=ImageDraw.Draw(atlas)
    for i,color in enumerate(PALETTE):
        x=(i%4)*16;y=(i//4)*16
        d.rectangle((x,y,x+15,y+15),fill=color+(255,))
    atlas.save(rp/'assets/ichigo/textures/item/cinematic_palette.png')
    for name,c in [('getsuga',5),('blue_getsuga',7),('mugetsu_wave',13)]:
        parts=arc(11,3.2,2.2,0,center=(3,8,8))
        parts+=arc(12.4,.30,1.3,c,center=(3,8,8))
        parts+=arc(12.6,.10,.65,11,start=-87,end=87,center=(3,8,8),segments=48)
        parts+=arc(9.8,.23,2.35,c,start=-86,end=86,center=(3,8,8),segments=48)
        for offset in [-1.25,1.25]:
            parts+=arc(10.6,.08,.10,c,start=-60,end=64,center=(3,8,8+offset),segments=28)
        write(name,parts,{'gui':{'scale':[.55,.55,.55]}})
    # Two curved crossing blades, with real depth and four tapered ends.
    parts=[]
    for rot in [-45,45]:
        for e in arc(10.5,1.9,1.5,0,start=-88,end=88,center=(2,8,8),segments=48)+arc(11.4,.24,1.6,15,start=-88,end=88,center=(2,8,8),segments=48):
            origin=e['rotation']['origin'];x,y=origin[0]-8,origin[1]-8;t=math.radians(rot)
            new=[8+x*math.cos(t)-y*math.sin(t),8+x*math.sin(t)+y*math.cos(t),origin[2]]
            delta=[new[i]-origin[i] for i in range(3)]
            e['from']=[e['from'][i]+delta[i] for i in range(3)];e['to']=[e['to'][i]+delta[i] for i in range(3)]
            e['rotation']['origin']=new;e['rotation']['angle']+=rot
            parts.append(e)
    write('jujisho',parts)
    # Cero: rounded charge core, two perpendicular orbit rings, tapering beam.
    parts=[]
    for i in range(15):
        z=2+i*.8;r=math.sqrt(max(.1,1-((i-7)/8)**2))*3.5
        parts.append(box((8,8,z),(r*2,r*2,.84),5 if i%3 else 11,45,glow=True))
    parts+=arc(5,.16,.18,5,start=0,end=360,segments=56,taper=False)
    parts+=arc(5,.16,.18,8,start=0,end=360,segments=56,taper=False,axis='y')
    write('cero',parts)
    for c in set(ACCENTS+[11]):
        ring=arc(7.5,.13,.11,c,start=0,end=360,axis='y',segments=64,taper=False)
        ring+=arc(6.65,.045,.08,11,start=0,end=360,axis='y',segments=48,taper=False)
        for j in range(12):
            t=math.tau*j/12
            ring.append(box((8+7.05*math.cos(t),8,8+7.05*math.sin(t)),(.6,.10,.055),c,-math.degrees(t),'y',True))
        write(f'ring_{c}',ring)
        write(f'slash_{c}',arc(8,.36,.18,c,start=-145,end=140,segments=60)+arc(8.3,.10,.08,11,start=-95,end=120,segments=44))
    for index,(form,c) in enumerate(zip(FORMS,ACCENTS)):
        # Open helical aura: deliberate empty front keeps first-person sight clear.
        aura=[]
        for strand in range(3):
            def point(u):
                t=u*math.tau*.58+strand*math.tau/3;r=8.4*(1-.23*u)
                return (8+r*math.cos(t),-6+u*29,8+r*math.sin(t))
            for j in range(36):
                a=point(j/36);b=point((j+1)/36)
                delta=[b[k]-a[k] for k in range(3)];length=math.sqrt(sum(v*v for v in delta))
                center=[(a[k]+b[k])/2 for k in range(3)]
                e=box(center,(.24,length*1.04,.20),c,glow=True)
                e['rotation']={'origin':center,'x':math.degrees(math.atan2(delta[2],delta[1])),'z':math.degrees(math.asin(-delta[0]/length))}
                aura.append(e)
        for j in range(9):
            t=math.tau*j/9
            aura.append(box((8+8.8*math.cos(t),-2+(j%3)*6,8+8.8*math.sin(t)),(.28,3.1,.28),c,15*(j%3-1),'z',True))
        write('aura_'+form,aura)
        # Layered coat tails / hollow shoulder shell attached to the live player.
        coat=[]
        for side in [-1,1]:
            for j in range(5):
                coat.append(box((8+side*(2+j*.75),5+j*.75,2.5-j*.42),(1.04,12-j*.5,.38),0 if form!='vasto' else 3,side*(8+j*3)))
                coat.append(box((8+side*(2+j*.75),.0+j,2.25-j*.42),(.13,2.5,.45),c if form in ['true','mugetsu'] else 2,side*(8+j*3),glow=form=='mugetsu'))
            coat.append(box((8+side*5.0,22,7),(2.6,1.1,5.0),3 if form=='vasto' else 0,side*13))
        coat.append(box((8,15.7,10.2),(8.3,1.7,.55),3))
        if form=='vasto':
            for j in range(5):
                for side in [-1,1]:coat.append(box((8+side*(1.5+j*.3),20-j*1.3,10.2),(.16,1.8,.18),4,side*35))
        write('mantle_'+form,coat)
        # Brief attacking afterimage, actual articulated silhouette, not a billboard.
        for pose in range(3):
            ghost=[box((8,18,8),(7.5,10,3.3),1),box((8,26,8),(6.3,6.3,6.3),0),box((6,7,8),(3.4,12,3.4),0,-14),box((10,7,8),(3.4,12,3.4),0,17)]
            ghost+=[box((2.5,19,8),(3,10,3),c,-75+pose*55),box((13.5,19,8),(3,10,3),1,60-pose*50),box((8,14,10),(8,1,.4),c,glow=True)]
            ghost+=[box((0,22,8),(1,19,.9),11,-65+pose*55,glow=True)]
            write(f'ghost_{form}_{pose}',ghost)
    # Sculpted mask panels, curved tapered horns and pointed hair locks.
    for form in ['hollow','vasto','mugetsu','hair']:
        name={'hollow':'hollow_mask','vasto':'vasto_mask','mugetsu':'mugetsu_head','hair':'ichigo_hair'}[form]
        parts=[]
        if form not in ['mugetsu','hair']:
            for side in [-1,1]:
                parts.append(box((8+side*2.25,8,3.1),(4.6,9.8,.7),3,side*-9,'y'))
                parts.append(box((8+side*2.6,9.2,2.53),(2.5,1.05,.19),0,side*9))
                parts.append(box((8+side*2.6,9.2,2.4),(1.15,.32,.10),6,side*9,glow=True))
                for j in range(4):parts.append(box((8+side*(.85+j*.83),4.1,2.45),(.42,1.65-j*.17,.23),0,side*14))
                for j in range(3):parts.append(box((8+side*(1.5+j*1.05),11.6,2.52),(.35,3.0-j*.45,.18),4,side*18))
            parts.append(box((8,6.6,2.12),(1.35,2,.65),3,12,'x'))
        elif form=='mugetsu':
            for j in range(5):parts.append(box((8,3.8+j*.75,2.4),(8.7,.58,.55),1 if j%2 else 2,j%2*4))
        if form=='vasto':
            for side in [-1,1]:
                for j in range(12):
                    u=j/11;w=1.8*(1-u)+.12
                    parts.append(box((8+side*(4.5+math.sin(u*1.65)*4.2),12+u*9.5,6-u*2),(w,1.13,w),3,side*(-42+u*48)))
        # Many tapered overlapping locks instead of seven rectangular hair pillars.
        if form in ['vasto','mugetsu']:
            for j in range(17):
                t=math.pi*j/16;x=8+5*math.cos(t);z=8+4*math.sin(t)
                for k in range(3):
                    parts.append(box((x,11-k*4,z+k*.65),(1.2-k*.27,5.4,1.3-k*.22),0 if form=='mugetsu' else 8,(j%3-1)*9,'z'))
        if form in ['hair','hollow']:
            for j in range(15):
                t=math.tau*j/15
                for k in range(3):
                    parts.append(box((8+(3.5+k*.36)*math.cos(t),12.2+k*.9,8+(3.5+k*.36)*math.sin(t)),(1.35-k*.4,2.25-k*.45,1.45-k*.4),8,25*math.cos(t),'z'))
        path=rp/f'assets/ichigo/models/item/{name}.json'
        display=json.loads((rp/'assets/ichigo/models/item/hollow_mask.json').read_text())['display']
        write(name,parts,display)
    # Four-times resolution painted fabric: folds, layered collars and wraps.
    for form in FORMS:
        for layer in ['humanoid','humanoid_leggings']:
            p=rp/f'assets/ichigo/textures/entity/equipment/{layer}/{form}.png'
            im=Image.open(p).resize((256,128),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
            c=PALETTE[ACCENTS[FORMS.index(form)]]
            if layer=='humanoid':
                for x in range(80,112):
                    k=int(7+8*(.5+.5*math.sin((x-80)*.64)))
                    color=(255-k,112-k,21,255) if form=='naruto' else (k,k+2,k+8,255) if form!='vasto' else (214+k,211+k,200+k,255)
                    d.line((x,82,x,111),fill=color)
                d.line([(80,80),(95,103),(110,80)],fill=(49,99,173,255) if form=='naruto' else (237,232,220,255),width=3)
                d.line([(82,82),(95,101),(108,82)],fill=(28,53,95,255) if form=='naruto' else (83,90,108,255),width=1)
                d.rectangle((80,112,111,119),fill=(49,99,173,255) if form=='naruto' else (218,216,207,255))
                d.line((80,115,111,115),fill=(22,43,82,255) if form=='naruto' else (123,130,141,255))
                if form=='naruto':
                    d.ellipse((103,89,109,95),outline=(255,196,83,255),width=2)
                    d.ellipse((104,90,108,94),outline=(49,99,173,255),width=1)
                if form=='vasto':
                    d.ellipse((91,87,102,100),fill=(4,5,9,255),outline=(113,9,25,255),width=2)
                if form=='mugetsu':
                    for y in range(82,110,4):d.line((80,y,111,y+2),fill=(108,116,129,255),width=2)
                for y in range(82,120,6):
                    d.line((176,y,189,y+2),fill=(*c,255) if form=='true' else (63,68,83,255),width=1)
            im.save(p)
