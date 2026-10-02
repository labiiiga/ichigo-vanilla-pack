scoreboard players add @s ig.fxage 1
execute if score @s ig.fx matches 1 if score @s ig.fxage matches 1 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[1.4f,0.9f,1.4f]}}
execute if score @s ig.fx matches 1 if score @s ig.fxage matches 4 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[3.6f,0.9f,3.6f]}}
execute if score @s ig.fx matches 1 if score @s ig.fxage matches 8 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[5.2f,0.9f,5.2f]}}
execute if score @s ig.fx matches 1 if score @s ig.fxage matches 11 run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{scale:[6.2f,0.05f,6.2f]}}
execute if score @s ig.fx matches 2 if score @s ig.fxage matches 1 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{left_rotation:[0f,0f,-0.57358f,0.81915f]}}
execute if score @s ig.fx matches 2 if score @s ig.fxage matches 3 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{left_rotation:[0f,0f,0.17365f,0.98481f]}}
execute if score @s ig.fx matches 2 if score @s ig.fxage matches 5 run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{left_rotation:[0f,0f,0.81915f,0.57358f]}}
execute if score @s ig.fx matches 11 if score @s ig.fxage matches 2 run item replace entity @s contents with paper[item_model="ichigo:ghost_shikai_1"]
execute if score @s ig.fx matches 11 if score @s ig.fxage matches 4 run item replace entity @s contents with paper[item_model="ichigo:ghost_shikai_2"]
execute if score @s ig.fx matches 12 if score @s ig.fxage matches 2 run item replace entity @s contents with paper[item_model="ichigo:ghost_bankai_1"]
execute if score @s ig.fx matches 12 if score @s ig.fxage matches 4 run item replace entity @s contents with paper[item_model="ichigo:ghost_bankai_2"]
execute if score @s ig.fx matches 13 if score @s ig.fxage matches 2 run item replace entity @s contents with paper[item_model="ichigo:ghost_hollow_1"]
execute if score @s ig.fx matches 13 if score @s ig.fxage matches 4 run item replace entity @s contents with paper[item_model="ichigo:ghost_hollow_2"]
execute if score @s ig.fx matches 14 if score @s ig.fxage matches 2 run item replace entity @s contents with paper[item_model="ichigo:ghost_vasto_1"]
execute if score @s ig.fx matches 14 if score @s ig.fxage matches 4 run item replace entity @s contents with paper[item_model="ichigo:ghost_vasto_2"]
execute if score @s ig.fx matches 15 if score @s ig.fxage matches 2 run item replace entity @s contents with paper[item_model="ichigo:ghost_true_1"]
execute if score @s ig.fx matches 15 if score @s ig.fxage matches 4 run item replace entity @s contents with paper[item_model="ichigo:ghost_true_2"]
execute if score @s ig.fx matches 16 if score @s ig.fxage matches 2 run item replace entity @s contents with paper[item_model="ichigo:ghost_mugetsu_1"]
execute if score @s ig.fx matches 16 if score @s ig.fxage matches 4 run item replace entity @s contents with paper[item_model="ichigo:ghost_mugetsu_2"]
execute if score @s ig.fx matches 17 if score @s ig.fxage matches 2 run item replace entity @s contents with paper[item_model="ichigo:ghost_naruto_1"]
execute if score @s ig.fx matches 17 if score @s ig.fxage matches 4 run item replace entity @s contents with paper[item_model="ichigo:ghost_naruto_2"]
execute if score @s ig.fxage >= @s ig.life run kill @s
