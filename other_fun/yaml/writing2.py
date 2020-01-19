#!/usr/bin/env python3

import yaml

#users = [{'name': 'John Doe' , 'occupation':  'gardener'},{'name': 'Lucy Black', 'occupation': 'teacher'}]
users = {'name': ['John Doe',  'Lucy Black'], 'occupation': [ 'gardener', 'teacher']}

users2 = {'persons': 
{'names': 
['John Doe',  'Lucy Black'],
 'occupations': ['gardener', 'teacher']},
'data': [{'date': '12/12/2012'}, {'time': 'now'}]}

blah = {'network': [{'version': 2}
] , 'renderer': 'networkd'}
 #,
# 'ethernets':
#   {'enp30s0':
#     {{'dhcp4':  'no'},
#    { 'addresses': ['xxx.xxx.xxx.100/24', 'xxx.xxx.xxx.102/24',  'xxx.xxx.xxx.105/24', '...']},
 #    {'gateway4':  'xxx.xxx.xxx.1'}, {'nameservers': {'addresses': '[xxx.xxx.xxx.1]'}}} }}
     
     
#users = [{'name': ['John Doe',  'Lucy Black']}, {'occupation': [ 'gardener', 'teacher']}]
data = ""
with open('users.yaml', 'w') as f:
    #yaml.dump(users,f)
    data += yaml.dump(users, stream = None)
print(yaml.dump(blah, stream = None, default_flow_style = None))
#print(data.replace('- ',''))
f.close()