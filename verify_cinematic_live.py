"""Integration checks run only against our isolated server on port 25595."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,r'C:\Users\LEGION 5\Documents\mc-server')
import rcon
rcon.PORT=25595
password=(ROOT/'.test-server/.rcon-pass').read_text()
def run(*cmds):return rcon.batch(password,list(cmds),.01)
def one(cmd):return run(cmd)[0]
def count(selector):
    run('scoreboard players set #qa ig.fxage 0',f'execute as {selector} run scoreboard players add #qa ig.fxage 1')
    return int(one('scoreboard players get #qa ig.fxage').split(' has ')[1].split(' ')[0])

run('tick freeze','kill @e[tag=ig.qa]','kill @e[tag=ig.fx]','summon armor_stand 0 1 0 {Tags:["ig.qa"],NoGravity:1b,Invulnerable:1b}',
    'scoreboard players set @e[tag=ig.qa,limit=1] ig.id 90001')
try:
    for form in ['shikai','bankai','hollow','vasto','true','mugetsu']:
        for kind in ['pulse','slash','ghost','burst']:
            response=one(f'execute as @e[tag=ig.qa,limit=1] at @s run function ichigo:fx/{kind}_{form}')
            assert 'Unknown' not in response and 'error' not in response.lower(),response
    assert count('@e[tag=ig.fx]')==24
    run('tick step 20');time.sleep(1.2)
    assert count('@e[tag=ig.fx]')==0,'Expired VFX leaked'
    # Both owner ids coexist; cleanup must never delete the other player's attachments.
    run('execute as @e[tag=ig.qa,limit=1] at @s run function ichigo:fx/attach_bankai')
    assert count('@e[tag=ig.attached]')==2
    run('scoreboard players set @e[tag=ig.qa,limit=1] ig.id 90002','execute as @e[tag=ig.qa,limit=1] at @s run function ichigo:fx/attach_vasto')
    assert count('@e[tag=ig.attached]')==4
    run('execute as @e[tag=ig.qa,limit=1] at @s run function ichigo:fx/cleanup')
    assert count('@e[tag=ig.attached]')==2
    run('tick step 2');time.sleep(.2)
    assert count('@e[tag=ig.attached]')==0,'Offline-owner attachments leaked'
    # Verify each projectile kind actually creates, follows and cleans its display.
    for kind in range(1,5):
        run('scoreboard players set @e[tag=ig.qa,limit=1] ig.pid 99999',f'scoreboard players set @e[tag=ig.qa,limit=1] ig.kind {kind}',
            'scoreboard players set @e[tag=ig.qa,limit=1] ig.form 2','execute as @e[tag=ig.qa,limit=1] at @s run function ichigo:projectile/visual')
        assert count('@e[tag=ig.visual]')==1
        run('execute as @e[tag=ig.qa,limit=1] at @s positioned ~3 ~ ~ run function ichigo:projectile/update_visual')
        position=one('data get entity @e[tag=ig.visual,limit=1] Pos')
        assert count('@e[tag=ig.visual,x=3.5,y=1,z=0.5,distance=..0.01]')==1,position
        run('kill @e[tag=ig.visual]')
    log=(ROOT/'.test-server/logs/latest.log').read_text(encoding='utf-8')
    assert 'Failed to load function ichigo:' not in log
    print('PASS: 24 VFX lifecycle checks, two-owner isolation, orphan cleanup, four projectile visuals and clean function load.')
finally:
    run('kill @e[tag=ig.qa]','kill @e[tag=ig.fx]','kill @e[tag=ig.visual]','tick unfreeze')
