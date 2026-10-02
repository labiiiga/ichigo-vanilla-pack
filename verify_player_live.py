"""Full form/equipment/cast roundtrip with the isolated vanilla QA player."""
from pathlib import Path
import sys,time
sys.path.insert(0,r'C:\Users\LEGION 5\Documents\mc-server')
import rcon
rcon.PORT=25595
password=(Path(__file__).parent/'.test-server/.rcon-pass').read_text()
def run(*cmds):return rcon.batch(password,list(cmds),.015)
def one(cmd):return run(cmd)[0]
assert 'IchigoQA' in one('list'),'Start isolated QA client first'
run('execute as IchigoQA at @s run function ichigo:off',
    'item replace entity IchigoQA armor.head with diamond_helmet',
    'item replace entity IchigoQA armor.chest with diamond_chestplate',
    'item replace entity IchigoQA armor.legs with diamond_leggings',
    'item replace entity IchigoQA armor.feet with diamond_boots')
try:
    for index,form in enumerate(['shikai','bankai','hollow','vasto','true','mugetsu'],1):
        one(f'execute as IchigoQA at @s run function ichigo:form/{form}')
        time.sleep(.15)
        assert f'has {index} ' in one('scoreboard players get IchigoQA ig.form')
        for skill in ['getsuga','special','ultimate']:
            one(f'execute as IchigoQA at @s run function ichigo:skill/{skill}')
        assert 'has 100 ' in one('scoreboard players get IchigoQA ig.energy')
        assert 'has 0 ' in one('scoreboard players get IchigoQA ig.cool')
        one('execute as IchigoQA at @s run function ichigo:off')
        for slot,item in [('head','diamond_helmet'),('chest','diamond_chestplate'),('legs','diamond_leggings'),('feet','diamond_boots')]:
            result=one(f'execute if items entity IchigoQA armor.{slot} minecraft:{item}')
            assert 'passed' in result.lower(),(form,slot,result)
        assert 'failed' in one('execute if entity @e[tag=ig.attached]').lower()
    # Health decrease on a real target validates the actual attributed attack path.
    run('difficulty normal','execute as IchigoQA at @s run function ichigo:form/bankai',
        'tp IchigoQA 0.5 1 -4.5 0 0',
        'summon zombie 0.5 1 2.5 {Tags:["ig.qa_target"],NoAI:1b,Silent:1b,PersistenceRequired:1b}',
        'execute as IchigoQA at @s run function ichigo:skill/getsuga')
    time.sleep(.45)
    health=one('data get entity @e[tag=ig.qa_target,limit=1] Health')
    assert '20.0f' not in health,health
    print('PASS: six transformations; all armor slots restore; 18 skill casts; unlimited stamina/no cooldown; attributed projectile damage:',health)
finally:
    run('kill @e[tag=ig.qa_target]','difficulty peaceful','execute as IchigoQA at @s run function ichigo:off')
