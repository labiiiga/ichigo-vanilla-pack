scoreboard players add @s ig.age 1
execute if score @s ig.age matches 3..22 rotated ~ 0 run tp @s ^ ^ ^0.11
execute if score @s ig.age matches 3..22 run particle minecraft:dust{color:[0.95,0.42,0.08],scale:0.7} ~ ~1 ~ .18 .42 .18 .01 2 normal @a[distance=..32]
execute if score @s ig.age matches 8 run data merge entity @s {Pose:{RightArm:[-150f,0f,-8f],LeftArm:[-55f,0f,28f],Body:[-8f,0f,0f]}}
execute if score @s ig.age matches 13 run data merge entity @s {Pose:{RightArm:[-32f,0f,-118f],LeftArm:[-18f,0f,18f],Body:[-5f,0f,0f]}}
execute if score @s ig.age matches 18 run data merge entity @s {Pose:{RightArm:[-122f,0f,-18f],LeftArm:[-38f,0f,22f],Body:[4f,0f,0f]}}
execute if score @s ig.age matches 18 run function ichigo:skill/clone_strike
execute if score @s ig.age matches 38 run particle minecraft:poof ~ ~1 ~ .35 .7 .35 .05 18 normal @a[distance=..32]
execute if score @s ig.age matches 38.. run kill @s
