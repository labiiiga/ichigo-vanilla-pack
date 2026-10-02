execute as @a[tag=!ig.init] run function ichigo:init
execute as @a[scores={ig.dead=1..},tag=ig.active] unless entity @s[nbt={Health:0.0f}] at @s run function ichigo:off
execute as @a[scores={ig.dead=1..}] unless entity @s[nbt={Health:0.0f}] run scoreboard players set @s ig.dead 0
execute as @a[scores={ichigo=1..}] at @s run function ichigo:select
scoreboard players set @a[scores={ichigo=1..}] ichigo 0
scoreboard players enable @a ichigo
scoreboard players remove @a[scores={ig.cool=1..}] ig.cool 1
scoreboard players remove @a[scores={ig.dash=1..}] ig.dash 1
scoreboard players remove @a[scores={ig.ult=1..}] ig.ult 1
execute as @a[tag=ig.active,nbt=!{Health:0.0f}] at @s run function ichigo:player_tick
execute as @a[scores={ig.use=1..},tag=ig.active] at @s if items entity @s weapon.mainhand *[minecraft:custom_data~{ichigo:"sword"}] run function ichigo:cast
scoreboard players set @a[scores={ig.use=1..}] ig.use 0
execute in minecraft:overworld as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick
execute in minecraft:the_nether as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick
execute in minecraft:the_end as @e[type=marker,tag=ig.projectile] at @s run function ichigo:projectile/tick

scoreboard players add #clock ig.clock 1
execute if score #clock ig.clock matches 64.. run scoreboard players set #clock ig.clock 0
execute as @a[tag=ig.active,nbt=!{Health:0.0f}] at @s run function ichigo:fx/player
execute in minecraft:overworld as @e[type=item_display,tag=ig.fx] at @s run function ichigo:fx/tick
execute in minecraft:overworld as @e[type=item_display,tag=ig.attached] at @s run function ichigo:fx/check_owner
execute in minecraft:overworld as @e[type=armor_stand,tag=ig.clone] at @s run function ichigo:skill/clone_tick
execute in minecraft:the_nether as @e[type=item_display,tag=ig.fx] at @s run function ichigo:fx/tick
execute in minecraft:the_nether as @e[type=item_display,tag=ig.attached] at @s run function ichigo:fx/check_owner
execute in minecraft:the_nether as @e[type=armor_stand,tag=ig.clone] at @s run function ichigo:skill/clone_tick
execute in minecraft:the_end as @e[type=item_display,tag=ig.fx] at @s run function ichigo:fx/tick
execute in minecraft:the_end as @e[type=item_display,tag=ig.attached] at @s run function ichigo:fx/check_owner
execute in minecraft:the_end as @e[type=armor_stand,tag=ig.clone] at @s run function ichigo:skill/clone_tick
