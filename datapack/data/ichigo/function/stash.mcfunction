execute in minecraft:overworld run summon armor_stand 0 -61 0 {Tags:["ig.locker","ig.new"],Invisible:1b,Marker:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b}
execute in minecraft:overworld run scoreboard players operation @e[type=armor_stand,tag=ig.new,limit=1] ig.owner = @s ig.id
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.head from entity @s armor.head
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.chest from entity @s armor.chest
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.legs from entity @s armor.legs
execute in minecraft:overworld run item replace entity @e[type=armor_stand,tag=ig.new,limit=1] armor.feet from entity @s armor.feet
execute in minecraft:overworld run tag @e[tag=ig.new] remove ig.new
tag @s add ig.active
