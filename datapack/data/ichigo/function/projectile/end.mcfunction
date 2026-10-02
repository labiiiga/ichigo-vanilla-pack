function ichigo:projectile/find_visual
kill @e[type=item_display,tag=ig.follow]
playsound ichigo:impact player @a[distance=..40] ~ ~ ~ .5 1
particle minecraft:poof ~ ~ ~ .4 .4 .4 .01 6 normal @a[distance=..48]
kill @s
