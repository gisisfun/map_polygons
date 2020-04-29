#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:58:02 2020

@author: me
"""
import pandas as pd
from scrapy import Selector
import matplotlib.pyplot as plt
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
print('all courses')
print(my_courses.groupby('Course_Name', as_index=False)['Technology'].count())
print('technology by course count')
print(my_courses.groupby('Technology', as_index=False)['Course_Name'].count())

my_courses.groupby('Technology', as_index=False)['Course_Name'].count().plot('Technology', kind='bar')
plt.show()

print("Skill Tracks")
track_names = sel.css('div.track-block__main h4::text').extract()
print(track_names)
track_comp = sel.css('div div h5::text').extract()
print(track_comp)


other=sel.css('span.dc-dropdown--nav__track-name::text').extract()
print(other)
my_tech = my_courses.Technology.unique()
python_courses = my_courses[my_courses.Technology=="python"]['Course_Name'].sort_values().reset_index(drop=True)
r_courses = my_courses[my_courses.Technology=="r"]['Course_Name'].sort_values().reset_index(drop=True)
