execute rotated ~ 0 positioned ~1.15 ~ ~ run summon armor_stand ~ ~ ~ {Tags:["ig.clone","ig.fresh"],Invisible:1b,ShowArms:1b,NoBasePlate:1b,NoGravity:1b,Invulnerable:1b,DisabledSlots:4144959,Pose:{RightArm:[-105f,0f,-24f],LeftArm:[-25f,0f,12f],Body:[0f,0f,0f]}}
execute rotated ~ 0 positioned ~-1.15 ~ ~ run summon armor_stand ~ ~ ~ {Tags:["ig.clone","ig.fresh"],Invisible:1b,ShowArms:1b,NoBasePlate:1b,NoGravity:1b,Invulnerable:1b,DisabledSlots:4144959,Pose:{RightArm:[-105f,0f,-24f],LeftArm:[-25f,0f,12f],Body:[0f,0f,0f]}}
execute rotated ~ 0 positioned ~ ~ ~-1.5 run summon armor_stand ~ ~ ~ {Tags:["ig.clone","ig.fresh"],Invisible:1b,ShowArms:1b,NoBasePlate:1b,NoGravity:1b,Invulnerable:1b,DisabledSlots:4144959,Pose:{RightArm:[-70f,0f,-75f],LeftArm:[-65f,0f,65f],Body:[0f,0f,0f]}}
scoreboard players operation @e[type=armor_stand,tag=ig.fresh] ig.owner = @s ig.id
scoreboard players set @e[type=armor_stand,tag=ig.fresh] ig.age 0
item replace entity @e[type=armor_stand,tag=ig.fresh] armor.head with carved_pumpkin[item_model="ichigo:naruto_head"]
item replace entity @e[type=armor_stand,tag=ig.fresh] armor.chest with leather_chestplate[equippable={slot:"chest",asset_id:"ichigo:naruto"}]
item replace entity @e[type=armor_stand,tag=ig.fresh] armor.legs with leather_leggings[equippable={slot:"legs",asset_id:"ichigo:naruto"}]
item replace entity @e[type=armor_stand,tag=ig.fresh] armor.feet with leather_boots[equippable={slot:"feet",asset_id:"ichigo:naruto"}]
tag @e[type=armor_stand,tag=ig.fresh] remove ig.fresh
title @s title {"text":"影分身の術！","color":"gold","bold":true}
playsound ichigo:release player @a[distance=..48] ~ ~ ~ .9 1.2
