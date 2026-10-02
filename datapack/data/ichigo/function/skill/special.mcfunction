execute if score @s ig.cool matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..24 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 25
scoreboard players set @s ig.cool 60
scoreboard players set #kind ig.kind 2
execute if score @s ig.form matches 4 run scoreboard players set #kind ig.kind 3
function ichigo:projectile/spawn
playsound ichigo:cero player @a[distance=..48] ~ ~ ~ 1 1
