execute if entity @s[tag=aot.shifted] run return run tellraw @s {"text":"กลับร่างไททันก่อน","color":"red"}
execute if entity @s[tag=bl.bankai] run function bleach:unbankai
execute unless entity @s[tag=ig.active] run function ichigo:stash
clear @s *[minecraft:custom_data~{ichigo:"sword"}]
clear @s *[minecraft:custom_data~{ichigo:"offhand"}]
scoreboard players set @s ig.form 5
scoreboard players set @s ig.formtime 0
give @s carrot_on_a_stick[custom_name={"text":"TRUE SHIKAI · Dual Zangetsu","color":"aqua","italic":false},item_model="ichigo:true_zangetsu",custom_data={ichigo:"sword"},unbreakable={},enchantments={vanishing_curse:1},attribute_modifiers=[{type:"minecraft:attack_damage",amount:14,operation:"add_value",id:"ichigo:sword",slot:"mainhand"},{type:"minecraft:attack_speed",amount:-2,operation:"add_value",id:"ichigo:speed",slot:"mainhand"}]]
give @s carrot_on_a_stick[custom_name={"text":"Zangetsu · Short Blade","color":"aqua","italic":false},item_model="ichigo:true_short",custom_data={ichigo:"offhand"},unbreakable={},enchantments={vanishing_curse:1},attribute_modifiers=[{type:"minecraft:attack_damage",amount:0,operation:"add_value",id:"ichigo:sword",slot:"mainhand"},{type:"minecraft:attack_speed",amount:-2,operation:"add_value",id:"ichigo:speed",slot:"mainhand"}]]
attribute @s minecraft:movement_speed modifier remove ichigo:speed
attribute @s minecraft:armor modifier remove ichigo:armor
attribute @s minecraft:movement_speed modifier add ichigo:speed 0.05 add_value
attribute @s minecraft:armor modifier add ichigo:armor 11 add_value
item replace entity @s armor.chest with leather_chestplate[custom_data={ichigo:"gear"},unbreakable={},enchantments={binding_curse:1,vanishing_curse:1},equippable={slot:"chest",asset_id:"ichigo:true"}]
item replace entity @s armor.legs with leather_leggings[custom_data={ichigo:"gear"},unbreakable={},enchantments={binding_curse:1,vanishing_curse:1},equippable={slot:"legs",asset_id:"ichigo:true"}]
item replace entity @s armor.feet with leather_boots[custom_data={ichigo:"gear"},unbreakable={},enchantments={binding_curse:1,vanishing_curse:1},equippable={slot:"feet",asset_id:"ichigo:true"}]
item replace entity @s armor.head with carved_pumpkin[item_model="ichigo:ichigo_hair",custom_data={ichigo:"gear"},equippable={slot:"head"},enchantments={binding_curse:1,vanishing_curse:1}]
title @s times 4 22 10
title @s title {"text": "TRUE SHIKAI", "color": "aqua", "bold": true}
title @s subtitle {"text":"REIATSU RELEASE","color":"white"}
scoreboard players set @s ig.tx 32
function ichigo:fx/attach_true
function ichigo:fx/pulse_true
playsound ichigo:charge player @a[distance=..48] ~ ~ ~ .7 1.1
