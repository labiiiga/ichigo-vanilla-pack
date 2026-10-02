scoreboard players operation #owner ig.owner = @s ig.id
scoreboard players operation #form ig.form = @s ig.form
scoreboard players add #next ig.pid 1
execute anchored eyes positioned ^ ^ ^1.8 run summon marker ~ ~ ~ {Tags:["ig.projectile","ig.new"]}
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players operation @s ig.pid = #next ig.pid
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players operation @s ig.owner = #owner ig.owner
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players operation @s ig.kind = #kind ig.kind
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players operation @s ig.form = #form ig.form
execute as @e[type=marker,tag=ig.new,limit=1] run scoreboard players set @s ig.age 0
tag @s add ig.launch
execute as @e[type=marker,tag=ig.new,limit=1] at @s rotated as @a[tag=ig.launch,limit=1] run tp @s ~ ~ ~ ~ ~
tag @s remove ig.launch
execute as @e[type=marker,tag=ig.new,limit=1] at @s run function ichigo:projectile/visual
tag @e[type=marker,tag=ig.new] remove ig.new
