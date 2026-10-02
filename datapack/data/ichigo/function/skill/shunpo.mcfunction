execute if score @s ig.dash matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..7 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 8
scoreboard players set @s ig.dash 16
playsound ichigo:shunpo player @a[distance=..32] ~ ~ ~ .8 1
particle minecraft:poof ~ ~1 ~ .3 .7 .3 .02 12 normal @a[distance=..32]
scoreboard players set #step ig.age 0
execute rotated ~ 0 run function ichigo:skill/dash_step
