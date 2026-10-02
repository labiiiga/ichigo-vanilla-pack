function ichigo:fx/find_owned
execute unless entity @e[type=item_display,tag=ig.owned] if score @s ig.form matches 1 run function ichigo:fx/attach_shikai
execute unless entity @e[type=item_display,tag=ig.owned] if score @s ig.form matches 2 run function ichigo:fx/attach_bankai
execute unless entity @e[type=item_display,tag=ig.owned] if score @s ig.form matches 3 run function ichigo:fx/attach_hollow
execute unless entity @e[type=item_display,tag=ig.owned] if score @s ig.form matches 4 run function ichigo:fx/attach_vasto
execute unless entity @e[type=item_display,tag=ig.owned] if score @s ig.form matches 5 run function ichigo:fx/attach_true
execute unless entity @e[type=item_display,tag=ig.owned] if score @s ig.form matches 6 run function ichigo:fx/attach_mugetsu
function ichigo:fx/find_owned
execute rotated ~ 0 run tp @e[type=item_display,tag=ig.owned] ~ ~ ~ ~ 0
execute if score #clock ig.clock matches 0 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.00000f,0f,1.00000f]}}
execute if score #clock ig.clock matches 4 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.19509f,0f,0.98079f]}}
execute if score #clock ig.clock matches 8 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.38268f,0f,0.92388f]}}
execute if score #clock ig.clock matches 12 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.55557f,0f,0.83147f]}}
execute if score #clock ig.clock matches 16 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.70711f,0f,0.70711f]}}
execute if score #clock ig.clock matches 20 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.83147f,0f,0.55557f]}}
execute if score #clock ig.clock matches 24 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.92388f,0f,0.38268f]}}
execute if score #clock ig.clock matches 28 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.98079f,0f,0.19509f]}}
execute if score #clock ig.clock matches 32 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,1.00000f,0f,0.00000f]}}
execute if score #clock ig.clock matches 36 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.98079f,0f,-0.19509f]}}
execute if score #clock ig.clock matches 40 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.92388f,0f,-0.38268f]}}
execute if score #clock ig.clock matches 44 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.83147f,0f,-0.55557f]}}
execute if score #clock ig.clock matches 48 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.70711f,0f,-0.70711f]}}
execute if score #clock ig.clock matches 52 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.55557f,0f,-0.83147f]}}
execute if score #clock ig.clock matches 56 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.38268f,0f,-0.92388f]}}
execute if score #clock ig.clock matches 60 run data merge entity @e[type=item_display,tag=ig.owned,tag=ig.aura,limit=1] {start_interpolation:0,interpolation_duration:4,transformation:{left_rotation:[0f,0.19509f,0f,-0.98079f]}}
scoreboard players remove @s[scores={ig.tx=1..}] ig.tx 1
execute if score @s ig.form matches 1 if score @s ig.tx matches 24 run function ichigo:fx/pulse_shikai
execute if score @s ig.form matches 1 if score @s ig.tx matches 18 run function ichigo:fx/pulse_shikai
execute if score @s ig.form matches 1 if score @s ig.tx matches 12 run function ichigo:fx/burst_shikai
execute if score @s ig.form matches 1 if score @s ig.tx matches 6 run function ichigo:fx/pulse_shikai
execute if score @s ig.form matches 1 if score #clock ig.clock matches 0 run function ichigo:fx/pulse_shikai
execute if score @s ig.form matches 2 if score @s ig.tx matches 24 run function ichigo:fx/pulse_bankai
execute if score @s ig.form matches 2 if score @s ig.tx matches 18 run function ichigo:fx/pulse_bankai
execute if score @s ig.form matches 2 if score @s ig.tx matches 12 run function ichigo:fx/burst_bankai
execute if score @s ig.form matches 2 if score @s ig.tx matches 6 run function ichigo:fx/pulse_bankai
execute if score @s ig.form matches 2 if score #clock ig.clock matches 0 run function ichigo:fx/pulse_bankai
execute if score @s ig.form matches 3 if score @s ig.tx matches 24 run function ichigo:fx/pulse_hollow
execute if score @s ig.form matches 3 if score @s ig.tx matches 18 run function ichigo:fx/pulse_hollow
execute if score @s ig.form matches 3 if score @s ig.tx matches 12 run function ichigo:fx/burst_hollow
execute if score @s ig.form matches 3 if score @s ig.tx matches 6 run function ichigo:fx/pulse_hollow
execute if score @s ig.form matches 3 if score #clock ig.clock matches 0 run function ichigo:fx/pulse_hollow
execute if score @s ig.form matches 4 if score @s ig.tx matches 24 run function ichigo:fx/pulse_vasto
execute if score @s ig.form matches 4 if score @s ig.tx matches 18 run function ichigo:fx/pulse_vasto
execute if score @s ig.form matches 4 if score @s ig.tx matches 12 run function ichigo:fx/burst_vasto
execute if score @s ig.form matches 4 if score @s ig.tx matches 6 run function ichigo:fx/pulse_vasto
execute if score @s ig.form matches 4 if score #clock ig.clock matches 0 run function ichigo:fx/pulse_vasto
execute if score @s ig.form matches 5 if score @s ig.tx matches 24 run function ichigo:fx/pulse_true
execute if score @s ig.form matches 5 if score @s ig.tx matches 18 run function ichigo:fx/pulse_true
execute if score @s ig.form matches 5 if score @s ig.tx matches 12 run function ichigo:fx/burst_true
execute if score @s ig.form matches 5 if score @s ig.tx matches 6 run function ichigo:fx/pulse_true
execute if score @s ig.form matches 5 if score #clock ig.clock matches 0 run function ichigo:fx/pulse_true
execute if score @s ig.form matches 6 if score @s ig.tx matches 24 run function ichigo:fx/pulse_mugetsu
execute if score @s ig.form matches 6 if score @s ig.tx matches 18 run function ichigo:fx/pulse_mugetsu
execute if score @s ig.form matches 6 if score @s ig.tx matches 12 run function ichigo:fx/burst_mugetsu
execute if score @s ig.form matches 6 if score @s ig.tx matches 6 run function ichigo:fx/pulse_mugetsu
execute if score @s ig.form matches 6 if score #clock ig.clock matches 0 run function ichigo:fx/pulse_mugetsu
