"""blender -b art/getsuga.blend --python art/bake_getsuga.py"""
import bpy
from pathlib import Path
root=Path(__file__).resolve().parent
scene=bpy.data.scenes['Ichigo - Getsuga VFX']
bpy.context.window.scene=scene
blue=[(.002,.012,.035),(.004,.14,.36),(.015,.55,1),(.20,.82,1),(.75,.95,1)]
for variant in ['getsuga','blue_getsuga']:
    if variant=='blue_getsuga':
        for i,c in enumerate(blue):
            mat=bpy.data.materials['Getsuga tone '+str(i)]
            next(n for n in mat.node_tree.nodes if n.type=='EMISSION').inputs[0].default_value=(*c,1)
    folder=root/'frames'/variant
    folder.mkdir(parents=True,exist_ok=True)
    for f in range(1,9):
        scene.frame_set(f)
        scene.render.filepath=str(folder/('%02d.png'%f))
        bpy.ops.render.render(write_still=True,scene=scene.name)
print('BAKE COMPLETE: 16 transparent frames')
