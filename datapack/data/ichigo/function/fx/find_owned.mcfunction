scoreboard players operation #owner ig.owner = @s ig.id
tag @e[type=item_display,tag=ig.attached] remove ig.owned
execute as @e[type=item_display,tag=ig.attached] if score @s ig.owner = #owner ig.owner run tag @s add ig.owned
