execute unless score #nocd ig.cool matches 1 if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute unless score #unlimited ig.energy matches 1 if score @s ig.energy matches ..24 run return run function ichigo:no_energy
execute unless score #unlimited ig.energy matches 1 run scoreboard players remove @s ig.energy 25
execute unless score #nocd ig.cool matches 1 run scoreboard players set @s ig.cool 80
playsound ichigo:shunpo player @a[distance=..48] ~ ~ ~ 1 .8
particle minecraft:poof ~ ~1 ~ .8 .7 .8 .05 45 normal @a[distance=..40]
particle minecraft:cloud ~ ~1 ~ .7 .7 .7 .05 32 normal @a[distance=..40]
function ichigo:skill/kage_spawn
