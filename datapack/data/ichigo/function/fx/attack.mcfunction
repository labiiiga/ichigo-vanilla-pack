swing @s mainhand
scoreboard players add @s ig.combo 1
execute if score @s ig.combo matches 3.. run scoreboard players set @s ig.combo 0
execute if score @s ig.form matches 1 rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_shikai
execute if score @s ig.form matches 1 if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_shikai
execute if score @s ig.form matches 2 rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_bankai
execute if score @s ig.form matches 2 if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_bankai
execute if score @s ig.form matches 3 rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_hollow
execute if score @s ig.form matches 3 if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_hollow
execute if score @s ig.form matches 4 rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_vasto
execute if score @s ig.form matches 4 if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_vasto
execute if score @s ig.form matches 5 rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_true
execute if score @s ig.form matches 5 if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_true
execute if score @s ig.form matches 6 rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_mugetsu
execute if score @s ig.form matches 6 if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_mugetsu
execute if score @s ig.form matches 7 rotated ~ 0 positioned ^ ^ ^.5 run function ichigo:fx/slash_naruto
execute if score @s ig.form matches 7 if score @s ig.combo matches 0 rotated ~ 0 positioned ^.45 ^ ^-.35 run function ichigo:fx/ghost_naruto
