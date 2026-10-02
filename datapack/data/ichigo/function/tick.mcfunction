execute as @a[tag=!ig.init] run function ichigo:init
execute as @a[scores={ig.dead=1..},tag=ig.active] at @s run function ichigo:off
scoreboard players set @a[scores={ig.dead=1..}] ig.dead 0
execute as @a[scores={ichigo=1..}] at @s run function ichigo:select
scoreboard players set @a[scores={ichigo=1..}] ichigo 0
scoreboard players enable @a ichigo
scoreboard players remove @a[scores={ig.cool=1..}] ig.cool 1
scoreboard players remove @a[scores={ig.dash=1..}] ig.dash 1
scoreboard players remove @a[scores={ig.ult=1..}] ig.ult 1
execute as @a[tag=ig.active] at @s run function ichigo:player_tick
execute as @a[scores={ig.use=1..},tag=ig.active] at @s if items entity @s weapon.mainhand *[minecraft:custom_data~{ichigo:"sword"}] run function ichigo:cast
scoreboard players set @a[scores={ig.use=1..}] ig.use 0
execute in minecraft:overworld as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick
execute in minecraft:the_nether as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick
execute in minecraft:the_end as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick
