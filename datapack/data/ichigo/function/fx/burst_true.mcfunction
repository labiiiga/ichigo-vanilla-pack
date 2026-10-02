function ichigo:fx/pulse_true
playsound ichigo:release player @a[distance=..48] ~ ~ ~ .8 1
particle minecraft:flash{color:-1} ~ ~1 ~ 0 0 0 0 1 normal @a[distance=..40]
particle minecraft:dust{color:[0.4627450980392157,0.8941176470588236,1.0],scale:1.25} ~ ~1 ~ .65 1.1 .65 .03 32 normal @a[distance=..40]
particle minecraft:end_rod ~ ~1 ~ .5 1 .5 .09 15 normal @a[distance=..40]
