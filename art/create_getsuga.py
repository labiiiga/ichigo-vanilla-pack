"""Run in Blender through MCP. Creates an isolated, editable VFX source scene."""
import bpy, math
from pathlib import Path
from mathutils import Quaternion

ROOT = Path(r'C:\Users\LEGION 5\minecraft_server\bleach-ichigo')
scene = bpy.data.scenes.new('Ichigo - Getsuga VFX')
bpy.context.window.scene = scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'
scene.render.fps = 20
scene.frame_start, scene.frame_end = 1, 8
scene.world = bpy.data.worlds.new('Getsuga transparent world')

def material(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes.clear()
    e = m.node_tree.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*color, 1)
    e.inputs[1].default_value = 1
    out = m.node_tree.nodes.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(e.outputs[0], out.inputs[0])
    m.diffuse_color = (*color, 1)
    return m

colors = [(0.007,0.001,0.005),(0.20,0.003,0.018),(0.85,0.012,0.028),(1.0,0.15,0.19),(1.0,0.65,0.65)]
mats = [material('Getsuga tone '+str(i), c) for i,c in enumerate(colors)]

def ribbon(name, outer, inner, start, end, z, mat, ripple=0, phase=0):
    # Smooth curved strips with tapered ends; actual meshes, editable in Blender.
    verts, faces = [], []
    for i in range(161):
        u = i/160
        t = start+(end-start)*u
        taper = max(0,math.sin(math.pi*u))**0.7
        r = outer + ripple*math.sin(t*11+phase)*taper
        for rad in (r, r-(outer-inner)*taper):
            verts.append((math.cos(t)*rad-.65, math.sin(t)*rad*1.12, z + .045*math.sin(t*2)*taper))
        if i: faces.append((2*i-2,2*i-1,2*i+1,2*i))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    ob = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(ob)
    ob.data.materials.append(mats[mat])
    for p in mesh.polygons: p.use_smooth = True
    return ob

lo, hi = -1.72, 1.72
ribbon('Crimson silhouette',1.95,1.19,lo,hi,0,2,.009)
ribbon('Black cutting body',1.89,1.27,lo,hi,.06,0,.013)
ribbon('Deep red inner edge',1.37,1.29,-1.56,1.56,.09,1,.019)
ribbon('Hot cutting edge',1.946,1.913,-1.66,1.66,.11,3,.006)
ribbon('Edge highlight',1.942,1.932,-1.30,1.30,.13,4,.004)
for j in range(8):
    start=-1.67+j*.31
    ob=ribbon('Flowing ember %02d'%j,2.01+(j%3)*.055,1.99+(j%3)*.055,start,start+.37+(j%2)*.23,.04,2+(j%2),.016,j)
    for f in range(1,10):
        phase=2*math.pi*(f-1)/8+j
        ob.rotation_euler.z=.025*math.sin(phase)
        ob.scale=(1+.014*math.cos(phase),1+.014*math.cos(phase),1)
        ob.keyframe_insert(data_path='rotation_euler',frame=f)
        ob.keyframe_insert(data_path='scale',frame=f)
for j in range(5):
    ob=ribbon('Inner energy filament %02d'%j,1.48+j*.066,1.465+j*.066,-1.2+j*.14,.25+j*.2,.14,1 if j%2 else 2,.022,j)
    for f in range(1,10):
        ob.rotation_euler.z=.07*math.sin(2*math.pi*(f-1)/8+j)
        ob.keyframe_insert(data_path='rotation_euler',frame=f)

camera=bpy.data.cameras.new('Getsuga orthographic bake')
camera.type='ORTHO'
camera.ortho_scale=5.3
ob=bpy.data.objects.new('Getsuga bake camera',camera)
scene.collection.objects.link(ob)
ob.location=(0,0,10)
scene.camera=ob
scene.frame_set(1)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_rotation=Quaternion((1,0,0,0))
        area.spaces.active.region_3d.view_distance=7
        area.spaces.active.region_3d.view_location=(0,0,0)
scene['purpose']='Original smooth Getsuga meshes. Bake to animated vanilla textures; no client mods.'
(ROOT/'art').mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/getsuga.blend'),copy=True)
print('Created',scene.name,len(scene.objects),'objects; source saved')
