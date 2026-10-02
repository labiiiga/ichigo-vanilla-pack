"""Launch installed vanilla client into the localhost-only QA server.
Uses an offline QA identity; never reads launcher accounts or authentication tokens.
"""
from pathlib import Path
import json,subprocess,os,uuid
root=Path(__file__).resolve().parent
install=Path(r'C:\Users\LEGION 5\curseforge\minecraft\Install')
meta=json.loads((install/'versions/26.2/26.2.json').read_text())
game=root/'.test-client';game.mkdir(exist_ok=True)
libraries=[]
for lib in meta['libraries']:
    allowed='rules' not in lib
    for rule in lib.get('rules',[]):
        osrule=rule.get('os',{})
        if osrule.get('name','windows')=='windows' and osrule.get('arch','x86_64') in ['x86_64','amd64']:
            allowed=rule['action']=='allow'
    if allowed:
        artifact=lib.get('downloads',{}).get('artifact')
        if artifact:
            path=install/'libraries'/artifact['path'];assert path.exists(),path
            libraries.append(str(path))
libraries.append(str(install/'versions/26.2/26.2.jar'))
java=Path(r'C:\Users\LEGION 5\Documents\mc-server\jdk\jdk-25.0.4.1+1\bin\java.exe')
args=[str(java),'-Xms512M','-Xmx1536M','--enable-native-access=ALL-UNNAMED','--sun-misc-unsafe-memory-access=allow',r'-Djdk.net.unixdomain.tmpdir=C:\Users\LEGION 5\Documents\mc-server\tmp','-cp',os.pathsep.join(libraries),meta['mainClass'],
      '--username','IchigoQA','--uuid',uuid.uuid3(uuid.NAMESPACE_DNS,'IchigoQA').hex,'--accessToken','0','--version','26.2','--gameDir',str(game),'--assetsDir',str(install/'assets'),'--assetIndex',meta['assetIndex']['id'],'--width','1280','--height','720','--quickPlayMultiplayer','127.0.0.1:25585']
(game/'options.txt').write_text('renderDistance:6\nsimulationDistance:5\nmaxFps:60\nmipmapLevels:2\nsoundCategory_master:0.5\nonboardAccessibility:false\njoinedFirstServer:true\n')
with (game/'launcher.log').open('w') as log:
    process=subprocess.Popen(args,cwd=game,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
(game/'pid').write_text(str(process.pid))
print('Started isolated vanilla QA client; PID',process.pid)
