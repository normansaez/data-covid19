import glob
from pathlib import Path
import os

for path in Path('.').rglob('*.json'):
    cut = path.name.split('_')[0]
    cut = cut+'.json'
#    cmd = 'cp "{}" {}'.format(path, cut)
#    print(cmd)
    path.rename(cut)


