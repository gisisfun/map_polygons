#!/usr/bin/env python3

import yaml

with open('data.yaml') as f:
    
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    nd = {}
    for doc in docs:
        
        for k, v in doc.items():
            #print(k, "->", v)
            #Cool bit
            nd[k] = v
            
print(nd)