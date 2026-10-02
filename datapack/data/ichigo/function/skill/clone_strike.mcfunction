scoreboard players operation #owner ig.owner = @s ig.owner
tag @a remove ig.caster
execute as @a[tag=ig.active] if score @s ig.id = #owner ig.owner run tag @s add ig.caster
execute if entity @a[tag=ig.caster] as @e[type=#ichigo:targets,distance=..2.8] run damage @s 6 minecraft:magic by @a[tag=ig.caster,limit=1]
tag @a remove ig.caster
particle minecraft:crit ~ ~1 ~ .65 .8 .65 .1 12 normal @a[distance=..32]
playsound ichigo:slash player @a[distance=..32] ~ ~ ~ .7 1.4
