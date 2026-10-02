from pathlib import Path
import shutil,secrets
root=Path(__file__).resolve().parent
src=Path(r'C:\Users\LEGION 5\Documents\mc-server')
dst=root/'.test-server';dst.mkdir(exist_ok=True)
shutil.copy2(src/'server.jar',dst/'server.jar')
shutil.copy2(src/'eula.txt',dst/'eula.txt')
secret=dst/'.rcon-pass'
if not secret.exists():secret.write_text(secrets.token_hex(18))
properties={'server-ip':'127.0.0.1','server-port':25585,'enable-rcon':'true','rcon.port':25595,'rcon.password':secret.read_text(),'online-mode':'false','max-players':4,'view-distance':5,'simulation-distance':3,'level-type':'minecraft:flat','generate-structures':'false','spawn-protection':0,'difficulty':'peaceful','gamemode':'creative','resource-pack':'http://127.0.0.1:8889/Ichigo-26.2-resourcepack.zip','resource-pack-sha1':(root/'dist/resourcepack.sha1').read_text().strip(),'require-resource-pack':'true','motd':'ICHIGO VFX LOCAL TEST','allow-flight':'true','sync-chunk-writes':'false'}
properties['pause-when-empty-seconds']=0
(dst/'server.properties').write_text('\n'.join(f'{k}={v}' for k,v in properties.items())+'\n')
shutil.copytree(root/'datapack',dst/'world/datapacks/ichigo',dirs_exist_ok=True)
print('Isolated localhost test server ready on 25585 / RCON 25595')
