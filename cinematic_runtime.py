"""Multiplayer VFX: owner-linked attachments and short-lived interpolated displays."""
import json, math
from cinematic_assets import FORMS, ACCENTS

def build(dp, fn):
    folder=dp/'data/ichigo/function'
    def read(n):return (folder/(n+'.mcfunction')).read_text(encoding='utf-8')
    def append(n,s):fn(n,read(n)+'\n'+s)
    def display(model,tags,scale=1,y=0):
        return '{Tags:'+json.dumps(tags,separators=(',',':'))+',item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"ichigo:'+model+'"}},item_display:"none",brightness:{block:15,sky:15},view_range:1.5f,teleport_duration:1,interpolation_duration:2,transformation:{translation:[0f,'+str(float(y))+'f,0f],scale:['+','.join([str(float(scale))+'f']*3)+'],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}'
    def fresh(model,kind,life,scale=1,y=0):
        return '\n'.join(['summon item_display ~ ~ ~ '+display(model,['ig.fx','ig.fresh'],scale,y),
          f'scoreboard players set @e[type=item_display,tag=ig.fresh,limit=1] ig.fx {kind}',
          f'scoreboard players set @e[type=item_display,tag=ig.fresh,limit=1] ig.life {life}',
          'scoreboard players set @e[type=item_display,tag=ig.fresh,limit=1] ig.fxage 0',
          'scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.owner = @s ig.id',
          'tp @e[type=item_display,tag=ig.fresh,limit=1] ~ ~ ~ ~ ~',
          'tag @e[type=item_display,tag=ig.fresh] remove ig.fresh'])
    append('load','\n'.join(f'scoreboard objectives add {n} dummy' for n in ['ig.tx','ig.fxage','ig.life','ig.fx','ig.clock','ig.combo','ig.gen'])+'\nscoreboard players set #clock ig.clock 0')
    append('init','scoreboard players set @s ig.tx 0\nscoreboard players set @s ig.combo 0')
    fn('fx/cleanup','''scoreboard players operation #owner ig.owner = @s ig.id
execute in minecraft:overworld as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run kill @s
execute in minecraft:the_nether as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run kill @s
execute in minecraft:the_end as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run kill @s''')
    off=read('off').replace('function ichigo:find_locker','function ichigo:fx/cleanup\nscoreboard players set @s ig.tx 0\nfunction ichigo:find_locker')
    fn('off',off)
    for i,(form,c) in enumerate(zip(FORMS,ACCENTS),1):
        cmds=['function ichigo:fx/cleanup','scoreboard players add @s ig.gen 1']
        for model,y,scale,tag in [('aura_'+form,1.0,1.15,'ig.aura'),('mantle_'+form,.5,1.0,'ig.mantle')]:
            cmds+=['summon item_display ~ ~ ~ '+display(model,['ig.attached','ig.fresh',tag],scale,y),
                   'scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.owner = @s ig.id',
                   'scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.gen = @s ig.gen',
                   'tag @e[type=item_display,tag=ig.fresh] remove ig.fresh']
        fn('fx/attach_'+form,'\n'.join(cmds))
        fn('fx/pulse_'+form,fresh(f'ring_{c}',1,14,.2,.05))
        fn('fx/slash_'+form,fresh(f'slash_{c}',2,7,1.3,1.0))
        # Three-frame posed afterimage at the launch point; finite lifetime.
        fn('fx/ghost_'+form,fresh(f'ghost_{form}_0',10+i,7,.97,.5))
        fn('fx/burst_'+form,'\n'.join([
            f'function ichigo:fx/pulse_{form}',
            'playsound ichigo:release player @a[distance=..48] ~ ~ ~ .8 1',
            'particle minecraft:flash{color:-1} ~ ~1 ~ 0 0 0 0 1 normal @a[distance=..40]',
            f'particle minecraft:dust{{color:{json.dumps([v/255 for v in __import__("cinematic_assets").PALETTE[c]],separators=(",",":"))},scale:1.25}} ~ ~1 ~ .65 1.1 .65 .03 32 normal @a[distance=..40]',
            'particle minecraft:end_rod ~ ~1 ~ .5 1 .5 .09 15 normal @a[distance=..40]']))
        original=read('form/'+form)
        if form in ['shikai','bankai','true']:
            original=original.replace('execute in minecraft:overworld run function ichigo:restore_head','item replace entity @s armor.head with carved_pumpkin[item_model="ichigo:ichigo_hair",custom_data={ichigo:"gear"},equippable={slot:"head"},enchantments={binding_curse:1,vanishing_curse:1}]')
        original=original[:original.index('title @s title')]+f'''title @s times 4 22 10
title @s title {json.dumps({'text':form.upper().replace('TRUE','TRUE SHIKAI'),'color':'aqua' if i in [1,5] else 'dark_red','bold':True})}
title @s subtitle {{"text":"REIATSU RELEASE","color":"white"}}
scoreboard players set @s ig.tx 32
function ichigo:fx/attach_{form}
function ichigo:fx/pulse_{form}
playsound ichigo:charge player @a[distance=..48] ~ ~ ~ .7 {1.1 if i in [1,5] else .85}
'''
        fn('form/'+form,original)
    fn('fx/find_owned','''scoreboard players operation #owner ig.owner = @s ig.id
tag @e[type=item_display,tag=ig.attached] remove ig.owned
execute as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run tag @s add ig.owned''')
    player=['function ichigo:fx/find_owned']
    player += [f'execute unless entity @e[type=item_display,tag=ig.owned] if score @s ig.form matches {i} run function ichigo:fx/attach_{form}' for i,form in enumerate(FORMS,1)]
    player+=['function ichigo:fx/find_owned','execute rotated ~ 0 run tp @e[type=item_display,tag=ig.owned] ~ ~ ~ ~ 0']
    # Aura rotates independently, coat stays with the player's facing.
    for phase in range(16):
        a=phase*math.tau/16
        q=f'[0f,{math.sin(a/2):.5f}f,0f,{math.cos(a/2):.5f}f]'
        player.append(f'execute if score #clock ig.clock matches {phase*4} run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {{start_interpolation:0,interpolation_duration:4,transformation:{{left_rotation:{q}}}}}')
    player+=['scoreboard players remove @s[scores={ig.tx=1..}] ig.tx 1']
    for i,form in enumerate(FORMS,1):
        player += [f'execute if score @s ig.form matches {i} if score @s ig.tx matches {t} run function ichigo:fx/{"burst" if t==12 else "pulse"}_{form}' for t in [24,18,12,6]]
        player += [f'execute if score @s ig.form matches {i} if score #clock ig.clock matches 0 run function ichigo:fx/pulse_{form}']
    player += ['execute if score @s ig.form matches 7 run particle minecraft:dust{color:[0.95,0.42,0.08],scale:1.0} ~ ~1 ~ .3 .65 .3 .01 2 normal @a[distance=..40]',
               'execute if score @s ig.form matches 7 run particle minecraft:dust{color:[0.19,0.42,1.0],scale:0.75} ~ ~1 ~ .25 .5 .25 .01 1 normal @a[distance=..40]']
    fn('fx/player','\n'.join(player))
    # Remove a loaded attachment if its owner disconnects, dies or changes dimension.
    fn('fx/check_owner','''scoreboard players operation #owner ig.owner = @s ig.owner
tag @a[tag=ig.owner_here] remove ig.owner_here
execute as @a[tag=ig.active,nbt=!{Health:0.0f}] if score @s ig.id = #owner ig.owner run tag @s add ig.owner_here
execute unless entity @a[tag=ig.owner_here,distance=..6] run return run kill @s
scoreboard players operation #generation ig.gen = @a[tag=ig.owner_here,limit=1] ig.gen
execute unless score @s ig.gen = #generation ig.gen run kill @s''')
    fx=['scoreboard players add @s ig.fxage 1']
    for age in [1,4,8,11]:
        scale={1:1.4,4:3.6,8:5.2,11:6.2}[age]
        sy=.9 if age<11 else .05
        fx.append(f'execute if score @s ig.fx matches 1 if score @s ig.fxage matches {age} run data merge entity @s {{start_interpolation:0,interpolation_duration:3,transformation:{{scale:[{scale}f,{sy}f,{scale}f]}}}}')
    for age,ang in [(1,-70),(3,20),(5,110)]:
        rad=math.radians(ang)/2
        fx.append(f'execute if score @s ig.fx matches 2 if score @s ig.fxage matches {age} run data merge entity @s {{start_interpolation:0,interpolation_duration:2,transformation:{{left_rotation:[0f,0f,{math.sin(rad):.5f}f,{math.cos(rad):.5f}f]}}}}')
    for i,form in enumerate(FORMS,1):
        for age,pose in [(2,1),(4,2)]:fx.append(f'execute if score @s ig.fx matches {10+i} if score @s ig.fxage matches {age} run item replace entity @s contents with paper[item_model="ichigo:ghost_{form}_{pose}"]')
    fx+=['execute if score @s ig.fxage >= @s ig.life run kill @s']
    fn('fx/tick','\n'.join(fx))
    # A real vanilla hand swing is broadcast to the caster and nearby friends.
    action=['swing @s mainhand','scoreboard players add @s ig.combo 1','execute if score @s ig.combo matches 3.. run scoreboard players set @s ig.combo 0']
    for i,form in enumerate(FORMS,1):
        action += [f'execute if score @s ig.form matches {i} rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_{form}',
                   f'execute if score @s ig.form matches {i} if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_{form}']
    fn('fx/attack','\n'.join(action))
    for skill in ['getsuga','special','ultimate']:
        s=read('skill/'+skill).replace('function ichigo:projectile/spawn','function ichigo:fx/attack\nfunction ichigo:projectile/spawn')
        if skill=='special':s+='\nexecute if score @s ig.form matches 5 run swing @s offhand\n'
        fn('skill/'+skill,s)
    shunpo=read('skill/shunpo').replace('playsound ichigo:shunpo','function ichigo:fx/afterimage\nplaysound ichigo:shunpo')
    fn('skill/shunpo',shunpo)
    fn('fx/afterimage','\n'.join(f'execute if score @s ig.form matches {i} rotated ~ 0 run function ichigo:fx/ghost_{form}' for i,form in enumerate(FORMS,1)))
    dash=read('skill/dash_step').replace('tp @s ^ ^ ^1','execute if score #step ig.age matches 3 run function ichigo:fx/afterimage\nexecute if score #step ig.age matches 6 run function ichigo:fx/afterimage\ntp @s ^ ^ ^1')
    fn('skill/dash_step',dash)
    tick=read('tick')
    # Dead players do not cast or rebuild attachments while waiting for respawn.
    tick=tick.replace('execute as @a[tag=ig.active] at @s','execute as @a[tag=ig.active,nbt=!{Health:0.0f}] at @s')
    tick+='\nscoreboard players add #clock ig.clock 1\nexecute if score #clock ig.clock matches 64.. run scoreboard players set #clock ig.clock 0\nexecute as @a[tag=ig.active,nbt=!{Health:0.0f}] at @s run function ichigo:fx/player\n'
    for dimension in ['overworld','the_nether','the_end']:
        tick+=f'execute in minecraft:{dimension} as @e[type=item_display,tag=ig.fx] at @s run function ichigo:fx/tick\n'
        tick+=f'execute in minecraft:{dimension} as @e[type=item_display,tag=ig.attached] at @s run function ichigo:fx/check_owner\n'
        tick+=f'execute in minecraft:{dimension} as @e[type=armor_stand,tag=ig.clone] at @s run function ichigo:skill/clone_tick\n'
    fn('tick',tick)
    # Center every projectile correctly: the item renderer already centers its model.
    fn('projectile/visual',read('projectile/visual').replace('translation:[-0.5f,-0.5f,-0.5f]','translation:[0f,0f,0f]'))
    fn('projectile/end',read('projectile/end').replace('particle minecraft:poof','playsound ichigo:impact player @a[distance=..40] ~ ~ ~ .5 1\nparticle minecraft:poof'))
    # Old all-red ambient flecks are replaced by each form's own aura geometry.
    fn('player_tick','\n'.join(l for l in read('player_tick').splitlines() if 'run particle minecraft:dust' not in l))
