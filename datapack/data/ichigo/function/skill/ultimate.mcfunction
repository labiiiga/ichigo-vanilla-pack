execute if score @s ig.ult matches 1.. run return run function ichigo:cooldown
execute if score @s ig.energy matches ..59 run return run function ichigo:no_energy
scoreboard players remove @s ig.energy 60
scoreboard players set @s ig.ult 900
scoreboard players set @s ig.cool 80
scoreboard players set #kind ig.kind 4
function ichigo:projectile/spawn
title @s title {"text":"月牙天衝","color":"dark_red","bold":true}
playsound ichigo:mugetsu player @a[distance=..64] ~ ~ ~ 1 1
execute if score @s ig.form matches 6 run scoreboard players set @s ig.formtime 50
