function ichigo:find_locker
execute if entity @e[tag=ig.selected,limit=1] run item replace entity @s armor.head from entity @e[tag=ig.selected,limit=1] armor.head
