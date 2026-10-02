"""Import the actual Minecraft VFX meshes into a separate editable Blender scene."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
ROOT=Path(r'C:\Users\LEGION 5\minecraft_server\bleach-ichigo')
import sys
sys.path.insert(0,str(ROOT))
from cinematic_assets import PALETTE,FORMS
scene=bpy.data.scenes.new('Ichigo - Cinematic Arsenal')
bpy.context.window.scene=scene
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.world=bpy.data.worlds.new('Cinematic World');scene.world.color=(.035,.035,.045)
mats=[]
for i,rgb in enumerate(PALETTE):
    mat=bpy.data.materials.new('Cinematic tone '+str(i));mat.use_nodes=True
    nodes=mat.node_tree.nodes;nodes.clear()
    emit=nodes.new('ShaderNodeEmission');emit.inputs[0].default_value=tuple((c/255)**2.2 for c in rgb)+(1,);emit.inputs[1].default_value=1
    out=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(emit.outputs[0],out.inputs[0]);mat.diffuse_color=tuple(c/255 for c in rgb)+(1,)
    mats.append(mat)

def import_model(name,location=(0,0,0),scale=1):
    data=json.loads((ROOT/f'resourcepack/assets/ichigo/models/item/{name}.json').read_text())
    verts=[];faces=[];indices=[]
    for e in data['elements']:
        a=e['from'];b=e['to'];start=len(verts)
        for x,y,z in [(a[0],a[1],a[2]),(b[0],a[1],a[2]),(b[0],b[1],a[2]),(a[0],b[1],a[2]),(a[0],a[1],b[2]),(b[0],a[1],b[2]),(b[0],b[1],b[2]),(a[0],b[1],b[2])]:
            v=Vector((x,y,z))
            if 'rotation' in e:
                r=e['rotation'];o=Vector(r['origin'])
                if 'axis' in r:
                    axis={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[r['axis']]
                    v=Quaternion(axis,math.radians(r['angle']))@(v-o)+o
                else:
                    m=Matrix.Rotation(math.radians(r.get('x',0)),3,'X')@Matrix.Rotation(math.radians(r.get('y',0)),3,'Y')@Matrix.Rotation(math.radians(r.get('z',0)),3,'Z')
                    v=m@(v-o)+o
            verts.append(((v.x-8)/16,-(v.z-8)/16,v.y/16))
        uv=next(iter(e['faces'].values()))['uv'];c=int(uv[0]//4)+int(uv[1]//4)*4
        for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)]:faces.append(tuple(start+j for j in f));indices.append(c)
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);scene.collection.objects.link(ob)
    for mat in mats:mesh.materials.append(mat)
    for face,c in zip(mesh.polygons,indices):face.material_index=c
    ob.location=location;ob.scale=(scale,)*3
    return ob

# Every mesh below is the exact cuboid model shipped to Minecraft, no render-only bevels.
for i,form in enumerate(FORMS):
    x=(i%3-1)*3.2;y=(i//3)*4
    import_model('ghost_'+form+'_1',(x,y,0))
    import_model('mantle_'+form,(x,y,0))
    import_model('aura_'+form,(x,y,.45),1.15)
    if form in ['hollow','vasto','mugetsu']:
        model={'hollow':'hollow_mask','vasto':'vasto_mask','mugetsu':'mugetsu_head'}[form]
        import_model(model,(x,y-.05,1.12))
    import_model('ring_'+str([7,5,5,8,15,13][i]),(x,y,-.5),1.7)
for i,name in enumerate(['getsuga','blue_getsuga','jujisho','cero','mugetsu_wave']):
    import_model(name,((i-2)*2.1,-3.6,.35),.85)
camera=bpy.data.cameras.new('Arsenal Camera');camera.type='ORTHO';camera.ortho_scale=16
ob=bpy.data.objects.new('Arsenal Camera',camera);scene.collection.objects.link(ob)
ob.location=(7,20,11);ob.rotation_euler=(Vector((0,.3,1))-ob.location).to_track_quat('-Z','Y').to_euler();scene.camera=ob
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=15
        area.spaces.active.region_3d.view_location=(0,0,1)
scene['preview_note']='Exact shipped VFX meshes on posed ghost mannequins. Live players retain vanilla body animation and equipment textures.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/cinematic-arsenal.blend'),copy=True)
scene.render.filepath=str(ROOT/'dist/cinematic-arsenal.png')
print('Imported exact Minecraft assets:',len(scene.objects),'objects')
