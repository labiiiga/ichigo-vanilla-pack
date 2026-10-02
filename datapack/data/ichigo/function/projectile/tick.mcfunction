scoreboard players add @s ig.age 1
execute unless block ^ ^ ^1.5 #ichigo:passable run return run function ichigo:projectile/end
tp @s ^ ^ ^1.5
execute at @s run function ichigo:projectile/update_visual
scoreboard players operation #owner ig.owner = @s ig.owner
tag @a[tag=ig.caster] remove ig.caster
execute as @a if score @s ig.id = #owner ig.owner run tag @s add ig.caster
execute unless entity @a[tag=ig.caster,limit=1] run return run function ichigo:projectile/end
execute if score @s ig.kind matches 1 as @e[type=#ichigo:targets,distance=..2.5] run damage @s 12 minecraft:magic by @a[tag=ig.caster,limit=1]
execute if score @s ig.kind matches 2 as @e[type=#ichigo:targets,distance=..3.5] run damage @s 20 minecraft:magic by @a[tag=ig.caster,limit=1]
execute if score @s ig.kind matches 3 as @e[type=#ichigo:targets,distance=..3] run damage @s 26 minecraft:magic by @a[tag=ig.caster,limit=1]
execute if score @s ig.kind matches 4 as @e[type=#ichigo:targets,distance=..5] run damage @s 42 minecraft:magic by @a[tag=ig.caster,limit=1]
execute if score @s ig.kind matches 5 as @e[type=#ichigo:targets,distance=..2.5] run damage @s 14 minecraft:magic by @a[tag=ig.caster,limit=1]
particle minecraft:dust{color:[0.6,0.02,0.06],scale:1.3} ~ ~ ~ .35 .6 .35 0 2 normal @a[distance=..64]
execute if score @s ig.age matches 32.. run function ichigo:projectile/end
