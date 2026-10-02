execute unless block ^ ^ ^1 #ichigo:passable run return 0
execute unless block ^ ^1 ^1 #ichigo:passable run return 0
tp @s ^ ^ ^1
particle minecraft:dust{color:[0.07,0.08,0.12],scale:1.4} ~ ~1 ~ .2 .5 .2 0 3 normal @a[distance=..32]
scoreboard players add #step ig.age 1
execute if score #step ig.age matches ..9 at @s rotated ~ 0 run function ichigo:skill/dash_step
