function ichigo:fx/pulse_mugetsu
playsound ichigo:release player @a[distance=..48] ~ ~ ~ .8 1
particle minecraft:flash{color:-1} ~ ~1 ~ 0 0 0 0 1 normal @a[distance=..40]
particle minecraft:dust{color:[0.6431372549019608,0.30196078431372547,0.9568627450980393],scale:1.25} ~ ~1 ~ .65 1.1 .65 .03 32 normal @a[distance=..40]
particle minecraft:end_rod ~ ~1 ~ .5 1 .5 .09 15 normal @a[distance=..40]
