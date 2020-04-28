#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:58:02 2020

@author: me
"""
import pandas as pd
from scrapy import Selector

thefile = open('webpage.txt','r')
html = thefile.read()
sel = Selector(text=html)

course_list = sel.css('h4.course-block__title::text').extract()
xsel = '//div[contains(@class,"course-block__technology course-block__technology--")]'
lang_list = sel.xpath(xsel).extract()


lang_list = [x.\
             replace('<div class="course-block__technology course-block__technology--','').\
             replace('"></div>','')for
 x in lang_list]
print("length",len(course_list))
for i,course in enumerate(course_list):
    print(course_list[i])
    
my_courses = pd.DataFrame(list(zip(lang_list,course_list)), \
               columns =['Technology','Course_Name'])

my_courses.groupby('Course_Name', as_index=False)['Technology'].count()
