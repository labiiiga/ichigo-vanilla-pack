execute unless entity @s[tag=ig.active] run return 0
function ichigo:find_locker
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.head from entity @e[tag=ig.selected,limit=1] armor.head
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.chest from entity @e[tag=ig.selected,limit=1] armor.chest
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.legs from entity @e[tag=ig.selected,limit=1] armor.legs
execute in minecraft:overworld if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.feet from entity @e[tag=ig.selected,limit=1] armor.feet
execute in minecraft:overworld run kill @e[tag=ig.selected]
clear @s *[minecraft:custom_data~{ichigo:"sword"}]
clear @s *[minecraft:custom_data~{ichigo:"offhand"}]
tag @s remove ig.active
scoreboard players set @s ig.form 0
attribute @s minecraft:movement_speed modifier remove ichigo:speed
attribute @s minecraft:armor modifier remove ichigo:armor
title @s actionbar {"text":"คืนชุดเดิมแล้ว","color":"gray"}
