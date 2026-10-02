summon item_display ~ ~ ~ {Tags:["ig.fx","ig.fresh"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"ichigo:ring_7"}},item_display:"none",brightness:{block:15,sky:15},view_range:1.5f,teleport_duration:1,interpolation_duration:2,transformation:{translation:[0f,0.05f,0f],scale:[0.2f,0.2f,0.2f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[type=item_display,tag=ig.fresh,limit=1] ig.fx 1
scoreboard players set @e[type=item_display,tag=ig.fresh,limit=1] ig.life 14
scoreboard players set @e[type=item_display,tag=ig.fresh,limit=1] ig.fxage 0
scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.owner = @s ig.id
tp @e[type=item_display,tag=ig.fresh,limit=1] ~ ~ ~ ~ ~
tag @e[type=item_display,tag=ig.fresh] remove ig.fresh
