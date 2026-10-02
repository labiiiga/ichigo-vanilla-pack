execute unless score #nocd ig.cool matches 1 if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute unless score #unlimited ig.energy matches 1 if score @s ig.energy matches ..11 run return run function ichigo:no_energy
execute unless score #unlimited ig.energy matches 1 run scoreboard players remove @s ig.energy 12
execute unless score #nocd ig.cool matches 1 run scoreboard players set @s ig.cool 20
scoreboard players set #kind ig.kind 1
function ichigo:fx/attack
function ichigo:projectile/spawn
playsound ichigo:slash player @a[distance=..48] ~ ~ ~ 1 1
