execute unless score #nocd ig.cool matches 1 if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute unless score #unlimited ig.energy matches 1 if score @s ig.energy matches ..24 run return run function ichigo:no_energy
execute unless score #unlimited ig.energy matches 1 run scoreboard players remove @s ig.energy 25
execute unless score #nocd ig.cool matches 1 run scoreboard players set @s ig.cool 60
scoreboard players set #kind ig.kind 2
execute if score @s ig.form matches 4 run scoreboard players set #kind ig.kind 3
function ichigo:fx/attack
function ichigo:projectile/spawn
playsound ichigo:cero player @a[distance=..48] ~ ~ ~ 1 1

execute if score @s ig.form matches 5 run swing @s offhand
