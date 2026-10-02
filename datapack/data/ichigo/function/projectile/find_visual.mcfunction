scoreboard players operation #pid ig.pid = @s ig.pid
tag @e[type=item_display,tag=ig.follow] remove ig.follow
execute as @e[type=item_display,tag=ig.visual] if score @s ig.pid = #pid ig.pid run tag @s add ig.follow
