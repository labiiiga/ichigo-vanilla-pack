execute if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..11 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 12
scoreboard players set @s ig.cool 20
scoreboard players set #kind ig.kind 1
function ichigo:projectile/spawn
playsound ichigo:slash player @a[distance=..48] ~ ~ ~ 1 1
