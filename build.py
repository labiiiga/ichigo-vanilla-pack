"""Build an original vanilla-compatible Ichigo fan pack for Java 26.2.
No third-party art, anime audio, client mods, or server credentials in output.
"""
from pathlib import Path
import json, math, random, hashlib, zipfile, wave, struct, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
RP = ROOT / 'resourcepack'
DP = ROOT / 'datapack'
OUT = ROOT / 'dist'
for p in (RP, DP, OUT): p.mkdir(exist_ok=True)

def js(root, name, value):
    p = root / name; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def fn(name, commands):
    p = DP / f'data/ichigo/function/{name}.mcfunction'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(commands.strip() + '\n', encoding='utf-8')

js(RP, 'pack.mcmeta', {'pack': {'description': 'ICHIGO | Zangetsu - original fan pack | Java 26.2', 'min_format': [88,0], 'max_format': [88,0]}})
js(DP, 'pack.mcmeta', {'pack': {'description': 'ICHIGO | Six forms / multiplayer skills | Java 26.2', 'min_format': [107,1], 'max_format': [107,1]}})
js(DP, 'data/minecraft/tags/function/load.json', {'values':['ichigo:load']})
js(DP, 'data/minecraft/tags/function/tick.json', {'values':['ichigo:tick']})
for name, flag in [('sneaking','is_sneaking'),('sprinting','is_sprinting'),('ground','is_on_ground')]:
    js(DP, f'data/ichigo/predicate/{name}.json', {'condition':'minecraft:entity_properties','entity':'this','predicate':{'flags':{flag:True}}})
js(DP, 'data/ichigo/tags/block/passable.json', {'values':['#minecraft:air','#minecraft:replaceable','minecraft:water','minecraft:lava','minecraft:light','#minecraft:leaves']})
js(DP, 'data/ichigo/tags/entity_type/targets.json', {'values': ['minecraft:'+n for n in ['zombie','husk','drowned','skeleton','stray','bogged','wither_skeleton','creeper','spider','cave_spider','enderman','witch','slime','magma_cube','blaze','ghast','piglin','piglin_brute','zombified_piglin','hoglin','zoglin','pillager','vindicator','evoker','ravager','phantom','silverfish','endermite','shulker','guardian','elder_guardian','breeze','warden','wither','ender_dragon']]})

# All cubes are editable vanilla JSON geometry. A palette atlas gives every face
# intentional colors without borrowing Minecraft/anime textures.
palette = [(13,15,23),(34,38,51),(193,211,220),(248,247,232),(182,21,42),(245,59,73),(204,153,64),(73,196,246),(236,126,39),(80,84,99),(121,20,39),(255,255,255)]
atlas=Image.new('RGBA',(64,64),(0,0,0,0)); draw=ImageDraw.Draw(atlas)
for i,c in enumerate(palette):
    x=(i%4)*16;y=(i//4)*16
    draw.rectangle((x,y,x+15,y+15),fill=(*c,255))
    draw.line((x,y,x+15,y),fill=tuple(min(255,v+18) for v in c)+(255,))
    draw.line((x,y+15,x+15,y+15),fill=tuple(max(0,v-16) for v in c)+(255,))
p=RP/'assets/ichigo/textures/item/palette.png';p.parent.mkdir(parents=True,exist_ok=True);atlas.save(p)

def cube(a,b,color=0,rotation=None):
    u=(color%4)*4;v=(color//4)*4
    result={'from':a,'to':b,'faces':{side:{'texture':'#palette','uv':[u+.3,v+.3,u+3.7,v+3.7]} for side in ['north','south','east','west','up','down']}}
    if rotation: result['rotation']=rotation
    return result

DISPLAY = {
 'thirdperson_righthand':{'rotation':[0,-90,45],'translation':[0,2,0],'scale':[.65,.65,.65]},
 'thirdperson_lefthand':{'rotation':[0,90,-45],'translation':[0,2,0],'scale':[.65,.65,.65]},
 'firstperson_righthand':{'rotation':[0,-90,25],'translation':[1,3,1],'scale':[.68,.68,.68]},
 'firstperson_lefthand':{'rotation':[0,90,-25],'translation':[1,3,1],'scale':[.68,.68,.68]},
 'gui':{'rotation':[0,0,-35],'translation':[0,-2,0],'scale':[.6,.6,.6]},
 'ground':{'rotation':[0,0,0],'translation':[0,3,0],'scale':[.45,.45,.45]},
 'fixed':{'rotation':[0,180,0],'translation':[0,-3,0],'scale':[.7,.7,.7]}}

def model(name,elements,display=None):
    js(RP,f'assets/ichigo/models/item/{name}.json',{'textures':{'palette':'ichigo:item/palette','particle':'ichigo:item/palette'},'elements':elements,'display':display or DISPLAY})
    js(RP,f'assets/ichigo/items/{name}.json',{'model':{'type':'minecraft:model','model':f'ichigo:item/{name}'}})

def katana(x=8, true=False):
    parts=[cube([x-.65,-7,7.35],[x+.65,1,8.65],0),cube([x-.85,-7.7,7.15],[x+.85,-6.6,8.85],2),cube([x-.65,1,7.5],[x+.65,29,8.5],0),cube([x+.45,1,7.43],[x+.8,29,8.57],2),cube([x-.45,29,7.55],[x+.65,31,8.45],0)]
    for y in range(-6,1,2):parts.append(cube([x-.7,y,7.28],[x+.7,y+.5,8.72],4 if true else 1))
    # Four open bars form the Bankai guard silhouette.
    for a,b in [([x-3,.4,7],[x+3,1.1,9]),([x-3,1,7],[x-2.3,3,9]),([x+2.3,-1.6,7],[x+3,1,9]),([x-2.4,-1.6,7],[x+2.4,-.9,9])]:parts.append(cube(a,b,0))
    # Small end chain, modeled links rather than a flat sprite.
    for i in range(4):
        y=-8-i*1.15
        parts.extend([cube([x-.5,y-.8,7.5],[x-.27,y+.3,8.5],2),cube([x+.27,y-.8,7.5],[x+.5,y+.3,8.5],2),cube([x-.5,y-.8,7.5],[x+.5,y-.57,8.5],2)])
    return parts

model('tensa_zangetsu',katana())
model('hollow_zangetsu',katana(true=True))
model('zangetsu', [cube([7,-8,7.3],[9,0,8.7],0),cube([5.2,0,7.3],[10.8,7,8.7],0),cube([4.5,7,7.3],[11.5,22,8.7],0),cube([5.2,22,7.3],[10.8,27,8.7],0),cube([6,27,7.3],[10,30,8.7],0),cube([10.8,7,7.2],[12,22,8.8],3),cube([10,22,7.2],[11,27,8.8],3),cube([9,27,7.2],[10.2,30,8.8],3),cube([6.4,-1,7.1],[9.6,1,8.9],3)] + [cube([6.8,y,7.1],[9.2,y+.5,8.9],3) for y in range(-8,0,2)])
model('true_zangetsu', [cube([6.5,-7,7.3],[8.5,1,8.7],0),cube([4,1,7.3],[10,24,8.7],0),cube([4,24,7.3],[8,29,8.7],0),cube([9.5,1,7.1],[10.5,24,8.9],3),cube([4,1,7.15],[6,9,8.85],3),cube([6,1,7.1],[8,3,8.9],4)])
model('true_short', [cube([7,-3,7.3],[9,2,8.7],0),cube([6,2,7.3],[10,16,8.7],0),cube([9.5,2,7.1],[10.5,16,8.9],3),cube([7,16,7.3],[9.5,19,8.7],0)])
model('mugetsu_blade',katana()+[cube([6.3,y,7],[9.7,y+.7,9],1) for y in range(2,28,3)])

# Head geometry surrounds the player's head; head transforms align to item equip.
head_display={'head':{'rotation':[0,180,0],'translation':[0,0,0],'scale':[1,1,1]},'gui':{'rotation':[15,-30,0],'scale':[.8,.8,.8]},'ground':{'translation':[0,3,0],'scale':[.5,.5,.5]}}
def mask(horns=False,mugetsu=False):
    if mugetsu:
        e=[cube([3.8,2,2.9],[12.2,6,3.8],0)]
        for y in [2.4,3.5,4.6]:e.append(cube([3.8,y,2.7],[12.2,y+.35,3],9))
        for x in [3,4.5,6,7.5,9,10.5,12]:e.append(cube([x,10,3],[x+1.3,16,12],0))
        e.extend([cube([2,0,8],[4,14,13],0),cube([12,0,8],[14,14,13],0)])
        return e
    e=[cube([3.6,2,2.8],[12.4,12,3.7],3),cube([4,12,3],[12,14,8],3),cube([3.5,4,3],[4.5,12,7],3),cube([11.5,4,3],[12.5,12,7],3)]
    e += [cube([4.3,8,2.65],[6.6,9.6,2.85],0),cube([9.4,8,2.65],[11.7,9.6,2.85],0),cube([5.1,8.4,2.5],[6.1,9.1,2.67],6),cube([9.9,8.4,2.5],[10.9,9.1,2.67],6),cube([7.1,5.4,2.3],[8.9,7.3,2.9],3),cube([4.5,3.2,2.6],[11.5,4.4,2.8],0)]
    for x in range(5,12):e.append(cube([x,3.3,2.35],[x+.55,4.5,2.65],3))
    for x in [9,10.2,11.4]:e.append(cube([x,9.8,2.5],[x+.6,12.8,2.9],4))
    e.append(cube([11,4.5,2.5],[11.7,7.8,2.9],4))
    if horns:
        for x in [1.5,12.5]:
            e.extend([cube([x,11,4],[x+2,16,7],3),cube([x+.3,16,4.3],[x+1.7,20,6.7],3),cube([x+.6,20,4.8],[x+1.4,23,6.2],3)])
    return e
model('hollow_mask',mask(),head_display);model('vasto_mask',mask(True),head_display);model('mugetsu_head',mask(mugetsu=True),head_display)

def crescent(color=4,cross=False):
    if cross:
        parts=[]
        for angle in [-45,45]:
            rot={'origin':[8,8,8],'axis':'z','angle':angle}
            parts.extend([cube([6.7,-7,7.5],[9.3,23,8.5],0,rot),cube([8.7,-7,7.3],[9.6,23,8.7],color,rot)])
        return parts
    parts=[]
    for sign in ([1,-1] if cross else [1]):
        for i in range(12):
            t=math.radians(-78+i*156/11)
            x=8+math.cos(t)*9; y=8+math.sin(t)*12
            if cross: x,y=8+(x-8)*.707+(y-8)*sign*.707,8+(y-8)*.707-(x-8)*sign*.707
            parts += [cube([x-1.3,y-1.2,7.5],[x+1.3,y+1.2,8.5],0),cube([x+.4,y-.8,7.3],[x+1.5,y+.8,8.7],color)]
    return parts
for name,c,cross in [('getsuga',4,False),('blue_getsuga',7,False),('jujisho',7,True),('mugetsu_wave',10,False)]:model(name,crescent(c,cross),{'gui':{'scale':[.6,.6,.6]}})
model('cero', [cube([4,4,4],[12,12,12],4),cube([6,6,2],[10,10,14],5),cube([2,6,6],[14,10,10],5),cube([6,2,6],[10,14,10],3)],{'gui':{'scale':[.65,.65,.65]}})

# Original armor painting on the standard 64x32 humanoid atlas.
for form in ['shikai','bankai','hollow','vasto','true','mugetsu']:
    for layer in ['humanoid','humanoid_leggings']:
        im=Image.new('RGBA',(64,32),(0,0,0,0));d=ImageDraw.Draw(im)
        base=(15,17,25,255) if form!='vasto' else (235,231,217,255)
        for box in [(16,16,39,31),(40,16,55,31),(0,16,15,31)]:d.rectangle(box,fill=base)
        # Body front 20..27 and back 32..39: kimono collar, fold, obi sash.
        if layer=='humanoid':
            d.line([(20,20),(23,25),(27,20)],fill=(239,235,226,255),width=1)
            d.line([(23,25),(23,31)],fill=(56,59,73,255))
            d.rectangle((20,28,27,29),fill=(239,235,226,255))
            d.rectangle((32,28,39,29),fill=(239,235,226,255))
            d.line((44,20,44,30),fill=(55,58,70,255));d.line((47,20,47,30),fill=(55,58,70,255))
            if form in ['hollow','true']:d.line((25,20,26,27),fill=(182,21,42,255),width=2)
            if form=='vasto':
                d.rectangle((22,22,25,25),fill=(12,12,17,255))
                d.line((20,26,27,26),fill=(170,28,36,255),width=1)
            if form=='mugetsu':
                for y in [20,22,24,26]: d.line((20,y,27,y),fill=(102,107,116,255))
                d.rectangle((20,28,27,31),fill=(9,10,14,255))
        else:
            for x in [4,7,12]:d.line((x,20,x,31),fill=(43,46,57,255))
            for y in [29,31]:d.rectangle((0,y,15,y),fill=(228,227,216,255))
        p=RP/f'assets/ichigo/textures/entity/equipment/{layer}/{form}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
    js(RP,f'assets/ichigo/equipment/{form}.json',{'layers':{layer:[{'texture':f'ichigo:{form}'}] for layer in ['humanoid','humanoid_leggings']}})

# Synthesized original sounds: no sampled anime/music.
random.seed(12)
sounds={}
for name,duration in [('slash',.35),('shunpo',.25),('transform',1.6),('mugetsu',1.9),('cero',.8)]:
    wav=OUT/f'{name}.wav'; rate=22050
    with wave.open(str(wav),'wb') as w:
        w.setparams((1,2,rate,0,'NONE','not compressed')); samples=[]
        for i in range(int(duration*rate)):
            t=i/rate;env=math.sin(math.pi*t/duration)**.7
            noise=random.uniform(-1,1);freq=(90 if name in ['transform','mugetsu'] else 450)*(1-.65*t/duration)
            tone=math.sin(2*math.pi*freq*t)+.35*math.sin(2*math.pi*freq*2.1*t)
            samples.append(struct.pack('<h',int(max(-1,min(1,env*(.18*tone+.18*noise)))*26000)))
        w.writeframes(b''.join(samples))
    target=RP/f'assets/ichigo/sounds/{name}.ogg';target.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(wav),'-c:a','libvorbis','-q:a','4',str(target)],check=True)
    wav.unlink()
    sounds[name]={'sounds':[{'name':f'ichigo:{name}','volume':.8}]}
js(RP,'assets/ichigo/sounds.json',sounds)

obj=['ig.id','ig.form','ig.energy','ig.regen','ig.cool','ig.dash','ig.ult','ig.age','ig.owner','ig.kind','ig.formtime','ig.dead']
fn('load','\n'.join([f'scoreboard objectives add {o} '+('deathCount' if o=='ig.dead' else 'dummy') for o in obj]+['scoreboard objectives add ichigo trigger','scoreboard objectives add ig.use minecraft.used:minecraft.carrot_on_a_stick','scoreboard players add #next ig.id 0','forceload add 0 0']))
fn('init','''scoreboard players add #next ig.id 1
scoreboard players operation @s ig.id = #next ig.id
scoreboard players set @s ig.energy 100
scoreboard players set @s ig.regen 0
scoreboard players set @s ig.form 0
scoreboard players set @s ig.cool 0
scoreboard players set @s ig.dash 0
scoreboard players set @s ig.ult 0
scoreboard players set @s ig.formtime 0
scoreboard players set @s ig.dead 0
tag @s add ig.init
tellraw @s {"text":"[ICHIGO] พิมพ์ /trigger ichigo set 8 เพื่อเลือกดาบและร่าง","color":"aqua"}''')
fn('tick','''execute as @a[tag=!ig.init] run function ichigo:init
execute as @a[scores={ig.dead=1..},tag=ig.active] unless entity @s[nbt={Health:0.0f}] at @s run function ichigo:off
execute as @a[scores={ig.dead=1..}] unless entity @s[nbt={Health:0.0f}] run scoreboard players set @s ig.dead 0
execute as @a[scores={ichigo=1..}] at @s run function ichigo:select
scoreboard players set @a[scores={ichigo=1..}] ichigo 0
scoreboard players enable @a ichigo
scoreboard players remove @a[scores={ig.cool=1..}] ig.cool 1
scoreboard players remove @a[scores={ig.dash=1..}] ig.dash 1
scoreboard players remove @a[scores={ig.ult=1..}] ig.ult 1
execute as @a[tag=ig.active] at @s run function ichigo:player_tick
execute as @a[scores={ig.use=1..},tag=ig.active] at @s if items entity @s weapon.mainhand *[minecraft:custom_data~{ichigo:"sword"}] run function ichigo:cast
scoreboard players set @a[scores={ig.use=1..}] ig.use 0
execute in minecraft:overworld as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick
execute in minecraft:the_nether as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick
execute in minecraft:the_end as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick''')
fn('player_tick','''scoreboard players add @s ig.regen 1
execute if score @s ig.regen matches 10.. if score @s ig.energy matches ..99 run scoreboard players add @s ig.energy 1
execute if score @s ig.regen matches 10.. run scoreboard players set @s ig.regen 0
scoreboard players remove @s[scores={ig.formtime=1..}] ig.formtime 1
execute if score @s ig.form matches 6 if score @s ig.formtime matches 0 run function ichigo:off
execute if score @s ig.form matches 4 if score @s ig.formtime matches 0 run function ichigo:form/bankai
execute if score @s ig.form matches 3 if score @s ig.formtime matches 0 run function ichigo:form/bankai
execute if score @s ig.form matches 2.. run particle minecraft:dust{color:[0.15,0.03,0.07],scale:0.8} ~ ~1 ~ .25 .6 .25 0 1 normal @a[distance=..40]
title @s actionbar [{"text":"霊圧 ","color":"aqua"},{"score":{"name":"@s","objective":"ig.energy"}},{"text":"/100  |  คลิก:Getsuga  ย่อ:Shunpo  วิ่ง:ท่าพิเศษ  กระโดด:ไม้ตาย","color":"gray"}]''')
forms=[('shikai','SHIKAI · Zangetsu','zangetsu',8,0),('bankai','BANKAI · Tensa Zangetsu','tensa_zangetsu',12,0),('hollow','HOLLOW MASK','hollow_zangetsu',15,1200),('vasto','VASTO LORDE','hollow_zangetsu',18,600),('true','TRUE SHIKAI · Dual Zangetsu','true_zangetsu',14,0),('mugetsu','FINAL GETSUGA · MUGETSU','mugetsu_blade',20,400)]
fn('select','\n'.join([f'execute if score @s ichigo matches {i} run function ichigo:form/{name}' for i,(name,*_) in enumerate(forms,1)]+['execute if score @s ichigo matches 7 run function ichigo:off','execute if score @s ichigo matches 8.. run function ichigo:menu']))
buttons=[{'text':'[ '+label+' ]\n','color':'aqua' if i<3 else 'red','click_event':{'action':'run_command','command':f'/trigger ichigo set {i}'}} for i,(_,label,*_) in enumerate(forms,1)]
buttons += [{'text':'[ คืนชุดเดิม / ยกเลิกร่าง ]\n','color':'gray','click_event':{'action':'run_command','command':'/trigger ichigo set 7'}},{'text':'คลิกขวา=Getsuga | ย่อ+คลิก=Shunpo | วิ่ง+คลิก=ท่าพิเศษ | กระโดด+คลิก=ไม้ตาย\nHollow 60 วินาที / Vasto 30 วินาที / Mugetsu 20 วินาที\nท่าโจมตีเฉพาะมอนสเตอร์ ไม่ทำลายบล็อก','color':'white'}]
fn('menu','tellraw @s '+json.dumps(buttons,ensure_ascii=False,separators=(',',':')))
fn('stash','''execute in minecraft:overworld run summon armor_stand 0 -61 0 {Tags:["ig.locker","ig.new"],Invisible:1b,Marker:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b}
execute in minecraft:overworld run scoreboard players operation @e[type=armor_stand,tag=ig.new,limit=1] ig.owner = @s ig.id
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.head from entity @s armor.head
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.chest from entity @s armor.chest
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.legs from entity @s armor.legs
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.feet from entity @s armor.feet
execute in minecraft:overworld run tag @e[tag=ig.new] remove ig.new
tag @s add ig.active''')
fn('find_locker','''scoreboard players operation #owner ig.owner = @s ig.id
execute in minecraft:overworld run tag @e[tag=ig.locker] remove ig.selected
execute in minecraft:overworld as @e[type=armor_stand,tag=ig.locker] if score @s ig.owner = #owner ig.owner run tag @s add ig.selected''')
fn('off','''execute unless entity @s[tag=ig.active] run return 0
function ichigo:find_locker
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.head from entity @e[tag=ig.selected,limit=1] armor.head
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.chest from entity @e[tag=ig.selected,limit=1] armor.chest
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.legs from entity @e[tag=ig.selected,limit=1] armor.legs
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.feet from entity @e[tag=ig.selected,limit=1] armor.feet
execute in minecraft:overworld run kill @e[tag=ig.selected]
clear @s *[minecraft:custom_data~{ichigo:"sword"}]
clear @s *[minecraft:custom_data~{ichigo:"offhand"}]
tag @s remove ig.active
scoreboard players set @s ig.form 0
attribute @s minecraft:movement_speed modifier remove ichigo:speed
attribute @s minecraft:armor modifier remove ichigo:armor
title @s actionbar {"text":"คืนชุดเดิมแล้ว","color":"gray"}''')

def sword_item(model_name,label,damage,offhand=False):
    return 'carrot_on_a_stick[custom_name='+json.dumps({'text':label,'color':'aqua','italic':False},ensure_ascii=False,separators=(',',':'))+',item_model="ichigo:'+model_name+'",custom_data={ichigo:"'+('offhand' if offhand else 'sword')+'"},unbreakable={},enchantments={vanishing_curse:1},attribute_modifiers=[{type:"minecraft:attack_damage",amount:'+str(damage)+',operation:"add_value",id:"ichigo:sword",slot:"mainhand"},{type:"minecraft:attack_speed",amount:-2,operation:"add_value",id:"ichigo:speed",slot:"mainhand"}]]'

for i,(name,label,blade,damage,duration) in enumerate(forms,1):
    commands=['execute if entity @s[tag=aot.shifted] run return run tellraw @s {"text":"กลับร่างไททันก่อน","color":"red"}', 'execute if entity @s[tag=bl.bankai] run function bleach:unbankai', 'execute unless entity @s[tag=ig.active] run function ichigo:stash','clear @s *[minecraft:custom_data~{ichigo:"sword"}]','clear @s *[minecraft:custom_data~{ichigo:"offhand"}]', f'scoreboard players set @s ig.form {i}',f'scoreboard players set @s ig.formtime {duration}',f'give @s {sword_item(blade,label,damage)}']
    if name=='true':commands.append('give @s '+sword_item('true_short','Zangetsu · Short Blade',0,True))
    commands += ['attribute @s minecraft:movement_speed modifier remove ichigo:speed','attribute @s minecraft:armor modifier remove ichigo:armor',f'attribute @s minecraft:movement_speed modifier add ichigo:speed {0.12 if i in [3,4] else .05} add_value',f'attribute @s minecraft:armor modifier add ichigo:armor {6+i} add_value']
    for slot,item in [('chest','leather_chestplate'),('legs','leather_leggings'),('feet','leather_boots')]:
        commands.append(f'item replace entity @s armor.{slot} with {item}[custom_data={{ichigo:"gear"}},unbreakable={{}},enchantments={{binding_curse:1,vanishing_curse:1}},equippable={{slot:"{slot}",asset_id:"ichigo:{name}"}}]')
    if name in ['hollow','vasto','mugetsu']:
        head={'hollow':'hollow_mask','vasto':'vasto_mask','mugetsu':'mugetsu_head'}[name]
        commands.append(f'item replace entity @s armor.head with carved_pumpkin[item_model="ichigo:{head}",custom_data={{ichigo:"gear"}},equippable={{slot:"head"}},enchantments={{binding_curse:1,vanishing_curse:1}}]')
    else:commands.append('execute in minecraft:overworld run function ichigo:restore_head')
    commands += [f'title @s title {json.dumps({"text":label,"color":"dark_red" if i>2 else "aqua","bold":True},ensure_ascii=False)}','playsound ichigo:transform player @a[distance=..48] ~ ~ ~ .8 1','particle minecraft:dust{color:[0.7,0.03,0.1],scale:1.5} ~ ~1 ~ .7 1 .7 .01 35 normal @a[distance=..48]']
    fn('form/'+name,'\n'.join(commands))
fn('restore_head','''function ichigo:find_locker
execute if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.head from entity @e[tag=ig.selected,limit=1] armor.head''')

fn('cast','''execute if predicate ichigo:sneaking run return run function ichigo:skill/shunpo
execute unless predicate ichigo:ground run return run function ichigo:skill/ultimate
execute if predicate ichigo:sprinting run return run function ichigo:skill/special
function ichigo:skill/getsuga''')
fn('no_energy','title @s actionbar {"text":"พลังวิญญาณไม่พอ — รอให้ฟื้น","color":"red"}')
fn('cooldown','title @s actionbar {"text":"ท่ายังอยู่ในคูลดาวน์","color":"gold"}')
fn('skill/getsuga','''execute if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..11 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 12
scoreboard players set @s ig.cool 20
scoreboard players set #kind ig.kind 1
function ichigo:projectile/spawn
playsound ichigo:slash player @a[distance=..48] ~ ~ ~ 1 1''')
fn('skill/special','''execute if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..24 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 25
scoreboard players set @s ig.cool 60
scoreboard players set #kind ig.kind 2
execute if score @s ig.form matches 4 run scoreboard players set #kind ig.kind 3
function ichigo:projectile/spawn
playsound ichigo:cero player @a[distance=..48] ~ ~ ~ 1 1''')
fn('skill/ultimate','''execute if score @s ig.ult matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..59 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 60
scoreboard players set @s ig.ult 900
scoreboard players set @s ig.cool 80
scoreboard players set #kind ig.kind 4
function ichigo:projectile/spawn
title @s title {"text":"月牙天衝","color":"dark_red","bold":true}
playsound ichigo:mugetsu player @a[distance=..64] ~ ~ ~ 1 1
execute if score @s ig.form matches 6 run scoreboard players set @s ig.formtime 50''')
fn('skill/shunpo','''execute if score @s ig.dash matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..7 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 8
scoreboard players set @s ig.dash 16
playsound ichigo:shunpo player @a[distance=..32] ~ ~ ~ .8 1
particle minecraft:poof ~ ~1 ~ .3 .7 .3 .02 12 normal @a[distance=..32]
scoreboard players set #step ig.age 0
execute rotated ~ 0 run function ichigo:skill/dash_step''')
fn('skill/dash_step','''execute unless block ^ ^ ^1 #ichigo:passable run return 0
execute unless block ^ ^1 ^1 #ichigo:passable run return 0
tp @s ^ ^ ^1
particle minecraft:dust{color:[0.07,0.08,0.12],scale:1.4} ~ ~1 ~ .2 .5 .2 0 3 normal @a[distance=..32]
scoreboard players add #step ig.age 1
execute if score #step ig.age matches ..9 at @s rotated ~ 0 run function ichigo:skill/dash_step''')

fn('projectile/spawn','''scoreboard players operation #owner ig.owner = @s ig.id
scoreboard players operation #form ig.form = @s ig.form
execute anchored eyes positioned ^ ^ ^1.8 run summon marker ~ ~ ~ {Tags:["ig.projectile","ig.new"]}
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players operation @s ig.owner = #owner ig.owner
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players operation @s ig.kind = #kind ig.kind
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players operation @s ig.form = #form ig.form
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players set @s ig.age 0
tag @s add ig.launch
execute as @e[type=marker,tag=ig.new,limit=1] at @s rotated as @a[tag=ig.launch,limit=1] run tp @s ~ ~ ~ ~ ~
tag @s remove ig.launch
execute as @e[type=marker,tag=ig.new,limit=1] at @s run function ichigo:projectile/visual
tag @e[type=marker,tag=ig.new] remove ig.new''')
visual=[]
for kind,name,scale in [(1,'getsuga',1.6),(2,'jujisho',1.9),(3,'cero',1.6),(4,'mugetsu_wave',3.2)]:
    nbt='{Tags:["ig.visual","ig.vnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"ichigo:'+name+'"}},item_display:"none",brightness:{block:15,sky:15},teleport_duration:1,transformation:{translation:[-0.5f,-0.5f,-0.5f],scale:['+','.join([str(scale)+'f']*3)+'],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}'
    visual.append(f'execute if score @s ig.kind matches {kind} run summon item_display ~ ~ ~ {nbt}')
visual += ['execute if score @s ig.kind matches 1 if score @s ig.form matches 1 run item replace entity @e[type=item_display,tag=ig.vnew,limit=1] contents with paper[item_model="ichigo:blue_getsuga"]','tp @e[type=item_display,tag=ig.vnew,limit=1] ~ ~ ~ ~ ~','ride @e[type=item_display,tag=ig.vnew,limit=1] mount @s','tag @e[tag=ig.vnew] remove ig.vnew']
fn('projectile/visual','\n'.join(visual))
fn('projectile/tick','''scoreboard players add @s ig.age 1
execute unless block ^ ^ ^1.5 #ichigo:passable run return run function ichigo:projectile/end
tp @s ^ ^ ^1.5
scoreboard players operation #owner ig.owner = @s ig.owner
tag @a[tag=ig.caster] remove ig.caster
execute as @a if score @s ig.id = #owner ig.owner run tag @s add ig.caster
execute unless entity @a[tag=ig.caster,limit=1] run return run function ichigo:projectile/end
execute if score @s ig.kind matches 1 as @e[type=#ichigo:targets,distance=..2.5] run damage @s 12 minecraft:magic by @a[tag=ig.caster,limit=1]
execute if score @s ig.kind matches 2 as @e[type=#ichigo:targets,distance=..3.5] run damage @s 20 minecraft:magic by @a[tag=ig.caster,limit=1]
execute if score @s ig.kind matches 3 as @e[type=#ichigo:targets,distance=..3] run damage @s 26 minecraft:magic by @a[tag=ig.caster,limit=1]
execute if score @s ig.kind matches 4 as @e[type=#ichigo:targets,distance=..5] run damage @s 42 minecraft:magic by @a[tag=ig.caster,limit=1]
particle minecraft:dust{color:[0.6,0.02,0.06],scale:1.3} ~ ~ ~ .35 .6 .35 0 2 normal @a[distance=..64]
execute if score @s ig.age matches 32.. run function ichigo:projectile/end''')
fn('projectile/end','''execute on passengers run kill @s
particle minecraft:poof ~ ~ ~ .4 .4 .4 .01 6 normal @a[distance=..48]
kill @s''')

# Remove pumpkin's vanilla screen overlay for our wearable 3D masks.
overlay=Image.new('RGBA',(16,16),(0,0,0,0));p=RP/'assets/minecraft/textures/misc/pumpkinblur.png';p.parent.mkdir(parents=True,exist_ok=True);overlay.save(p)
icon=Image.new('RGB',(128,128),(13,15,23));d=ImageDraw.Draw(icon);d.ellipse((10,10,118,118),outline=(192,26,48),width=7);d.line((43,104,89,19),fill=(242,238,224),width=9);d.line((38,89,68,100),fill=(192,26,48),width=6);icon.save(RP/'pack.png')

for root,name in [(RP,'Ichigo-26.2-resourcepack.zip'),(DP,'Ichigo-26.2-datapack.zip')]:
    path=OUT/name
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(root.rglob('*')):
            if f.is_file(): z.write(f,f.relative_to(root).as_posix())
    print(name, path.stat().st_size, 'SHA1', hashlib.sha1(path.read_bytes()).hexdigest())
(OUT/'resourcepack.sha1').write_text(hashlib.sha1((OUT/'Ichigo-26.2-resourcepack.zip').read_bytes()).hexdigest(),encoding='ascii')
print('Models:',len(list((RP/'assets/ichigo/models/item').glob('*.json'))),'Functions:',len(list((DP/'data/ichigo/function').rglob('*.mcfunction'))))
