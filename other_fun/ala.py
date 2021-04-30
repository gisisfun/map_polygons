# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 17:49:57 2021

@author: damie
"""
import requests
import pandas as pd
import json
url= 'https://biocache-ws.ala.org.au/ws/occurrences/search?q=genus:%22Macropus%22'
response = requests.get(url)

data = json.loads(response.content.decode('utf-8'))

df = pd.json_normalize(data['occurrences'])
