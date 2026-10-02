scoreboard players operation #owner ig.owner = @s ig.owner
tag @a[tag=ig.owner_here] remove ig.owner_here
execute as @a[tag=ig.active,nbt=!{Health:0.0f}] if score @s ig.id = #owner ig.owner run tag @s add ig.owner_here
execute unless entity @a[tag=ig.owner_here,distance=..6] run return run kill @s
scoreboard players operation #generation ig.gen = @a[tag=ig.owner_here,limit=1] ig.gen
execute unless score @s ig.gen = #generation ig.gen run kill @s
