function ichigo:projectile/find_visual
kill @e[type=item_display,tag=ig.follow]
particle minecraft:poof ~ ~ ~ .4 .4 .4 .01 6 normal @a[distance=..48]
kill @s
