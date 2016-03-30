# -*- coding: utf-8 -*-

import os.path
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import operator
i=0
with open("items.json")as data_file:
    data=json.load(data_file)
for i in range(0,4831):    
    line=data[i]
    if "department" in line:
        ++i
        dep=''.join(line[u"department"])
        fo=open(dep,"a")
        content=''.join(line[u"comments"])
        fo.write(content)
        fo.close
        print line
        


