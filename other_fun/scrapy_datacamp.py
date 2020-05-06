#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:58:02 2020
@author: me
"""
import pandas as pd
from scrapy import Selector
import matplotlib.pyplot as plt
import re

xsel_lang_list = '//div[contains(@class,"course-block__technology course-block__technology--")]'
css_course_list = 'h4.course-block__title::text'
css_dc_counts = 'strong.dc-u-m-none::text'
css_per_topic_names = 'h4.dc-u-mb-4::text' 
css_per_topic_data = 'p.dc-u-mt-0::text' #first 12
css_other_track = 'span.dc-dropdown--nav__track-name::text'
css_track_comp = 'div div h5::text'
css_track_names = 'div.track-block__main h4::text'

thefile = open('my_profile.txt','r')

html = thefile.read()
sel = Selector(text=html)

print('XP by topic')
#scape web page for content
dc_topic_names = sel.css(css_per_topic_names).extract()
dc_topic_data = sel.css(css_per_topic_data).extract()[:12]

# clean tex and convert to integer
dc_topic_data = [int(re.sub('[\sA-Z]','',test)) for test in dc_topic_data]

my_topic_xp = pd.DataFrame(list(zip(dc_topic_names,dc_topic_data)), \
               columns =['Topic','XP'])

my_topic_xp.Topic = my_topic_xp.Topic.astype("category")

plt.bar(x=my_topic_xp.Topic,height=my_topic_xp.XP)
plt.xticks(rotation=60)
plt.title("Topics by XP")
plt.show()
dc_counts = sel.css(css_dc_counts).extract()
#xp = int(re.findall('.*[0-9].*',xp)[0]
#.replace('XP','').replace(",","")
#.strip())
course_list = sel.css(css_course_list).extract()
lang_list = sel.xpath(xsel_lang_list).extract()


lang_list = [re.sub('<.*.--','',re.sub('"></div>','',x)) for x in lang_list]
#lang_list=[ test[len(test)-91:-8] for test in lang_list]

my_courses = pd.DataFrame(list(zip(lang_list,course_list)), \
               columns =['Technology','Course_Name'])
my_courses.Technology = my_courses.Technology.str.title()
my_courses.Course_Name = my_courses.Course_Name.str.title()
#print('all courses')

#print(my_courses.groupby('Course_Name', as_index=False)['Technology'].count())
#print('technology by course count')
#print(my_courses.groupby('Technology', as_index=False)['Course_Name'].count())

my_courses.groupby('Technology', as_index=False)['Course_Name'].count().plot('Technology', kind='bar')
plt.xticks(rotation=45)
plt.title("Courses by Technology")
plt.show()
print(my_courses.groupby('Technology').count())
print()
print('Python Courses')
print(my_courses
      .loc[my_courses.Technology=='Python','Course_Name']
      .sort_values().reset_index(drop=True))
print()
print('R Courses')
print(my_courses
      .loc[my_courses.Technology=='R','Course_Name']
      .sort_values().reset_index(drop=True))

print("Skill Tracks")

track_names = sel.css(css_track_names).extract()
#print(track_names)

track_comp = sel.css(css_track_comp).extract()
#print(track_comp)

other=sel.css(css_other_track).extract()
#print(other)
my_tech = my_courses.Technology.unique()
