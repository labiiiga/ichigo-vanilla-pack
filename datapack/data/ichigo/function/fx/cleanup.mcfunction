scoreboard players operation #owner ig.owner = @s ig.id
execute in minecraft:overworld as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run kill @s
execute in minecraft:the_nether as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run kill @s
execute in minecraft:the_end as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run kill @s
