import sys
import json
sys.path.insert(0, '/media/robert/80C2-37E4/papers/3rdparty/xplore')
from xploreapi import XPLORE

query = XPLORE('jxbje7zvg66y37t96cydaq6v')
query.abstractText('Precup')
query.dataType('json')
data = query.callAPI()

obj = json.loads(data) 

for i in obj:
    print i
    

