execute unless score #nocd ig.cool matches 1 if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute unless score #unlimited ig.energy matches 1 if score @s ig.energy matches ..11 run return run function ichigo:no_energy
execute unless score #unlimited ig.energy matches 1 run scoreboard players remove @s ig.energy 12
execute unless score #nocd ig.cool matches 1 run scoreboard players set @s ig.cool 25
scoreboard players set #kind ig.kind 5
function ichigo:projectile/spawn
playsound ichigo:release player @a[distance=..48] ~ ~ ~ .9 1.6
particle minecraft:dust{color:[0.19,0.42,1.0],scale:1.3} ~ ~1 ~ .3 .3 .3 .02 12 normal @a[distance=..40]
