scoreboard players add #next ig.id 1
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
tellraw @s {"text":"[ICHIGO + NARUTO] พิมพ์ /trigger ichigo set 8 เพื่อเปิดเมนูร่าง","color":"aqua"}

scoreboard players set @s ig.tx 0
scoreboard players set @s ig.combo 0
