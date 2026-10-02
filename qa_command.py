"""Send arguments to the isolated localhost QA server only."""
import sys
from pathlib import Path
sys.path.insert(0,r'C:\Users\LEGION 5\Documents\mc-server')
import rcon
rcon.PORT=25595
print('\n'.join(rcon.batch((Path(__file__).parent/'.test-server/.rcon-pass').read_text(),sys.argv[1:])))
