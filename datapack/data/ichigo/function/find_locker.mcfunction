scoreboard players operation #owner ig.owner = @s ig.id
execute in minecraft:overworld run tag @e[tag=ig.locker] remove ig.selected
execute in minecraft:overworld as @e[type=armor_stand,tag=ig.locker] if score @s ig.owner = #owner ig.owner run tag @s add ig.selected
