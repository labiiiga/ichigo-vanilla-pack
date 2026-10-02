function ichigo:fx/cleanup
scoreboard players add @s ig.gen 1
summon item_display ~ ~ ~ {Tags:["ig.attached","ig.fresh","ig.aura"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"ichigo:aura_true"}},item_display:"none",brightness:{block:15,sky:15},view_range:1.5f,teleport_duration:1,interpolation_duration:2,transformation:{translation:[0f,1.0f,0f],scale:[1.15f,1.15f,1.15f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.owner = @s ig.id
scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.gen = @s ig.gen
tag @e[type=item_display,tag=ig.fresh] remove ig.fresh
summon item_display ~ ~ ~ {Tags:["ig.attached","ig.fresh","ig.mantle"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"ichigo:mantle_true"}},item_display:"none",brightness:{block:15,sky:15},view_range:1.5f,teleport_duration:1,interpolation_duration:2,transformation:{translation:[0f,0.5f,0f],scale:[1.0f,1.0f,1.0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.owner = @s ig.id
scoreboard players operation @e[type=item_display,tag=ig.fresh,limit=1] ig.gen = @s ig.gen
tag @e[type=item_display,tag=ig.fresh] remove ig.fresh
