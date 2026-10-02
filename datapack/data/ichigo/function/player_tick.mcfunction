execute if score #unlimited ig.energy matches 1 run scoreboard players set @s ig.energy 100
scoreboard players add @s ig.regen 1
execute if score @s ig.regen matches 10.. if score @s ig.energy matches ..99 run scoreboard players add @s ig.energy 1
execute if score @s ig.regen matches 10.. run scoreboard players set @s ig.regen 0
scoreboard players remove @s[scores={ig.formtime=1..}] ig.formtime 1
execute if score @s ig.form matches 6 if score @s ig.formtime matches 0 run function ichigo:off
execute if score @s ig.form matches 4 if score @s ig.formtime matches 0 run function ichigo:form/bankai
execute if score @s ig.form matches 3 if score @s ig.formtime matches 0 run function ichigo:form/bankai
execute if score @s ig.form matches 2.. run particle minecraft:dust{color:[0.15,0.03,0.07],scale:0.8} ~ ~1 ~ .25 .6 .25 0 1 normal @a[distance=..40]
execute unless score #unlimited ig.energy matches 1 run title @s actionbar [{"text":"霊圧 ","color":"aqua"},{"score":{"name":"@s","objective":"ig.energy"}},{"text":"/100  |  คลิก:Getsuga  ย่อ:Shunpo  วิ่ง:ท่าพิเศษ  กระโดด:ไม้ตาย","color":"gray"}]
execute if score #unlimited ig.energy matches 1 run title @s actionbar [{"text":"霊圧 ∞  |  ","color":"aqua"},{"text":"คลิก:Getsuga  ย่อ:Shunpo  วิ่ง:ท่าพิเศษ  กระโดด:ไม้ตาย","color":"gray"}]
