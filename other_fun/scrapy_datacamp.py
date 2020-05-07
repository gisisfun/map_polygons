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


def just_words(raw_html,func,non_extra=[]):
    '''
    Finds all words in html 
    
    input:
        raw_html - list of strings returned from scrapy query
        
    returns:
        list of strings without html text
    '''
    non_words = ['block__main', 'class', 
                 'dc', 'div', 'h4', 'mb',
                 'mt', 'p', 'track', 'u',
                 'course','block__technology'] + non_extra
    final_list=[]
    for y in raw_html:
        words_l=[]
        html_words =re.findall('[\w]+',y)
        for x in html_words:
            if x not in non_words:
                words_l.append(func(x))
        final_list.append(' '.join(words_l))
    return final_list

def nothing(value):
    return value

def is_amp(f_value):
    output=f_value
    if f_value=="amp":
        output='&'   
    return output

xsel_lang_list = '//div[contains(@class,"course-block__technology course-block__technology--")]'
css_course_list = 'h4.course-block__title::text'
css_dc_counts = 'strong.dc-u-m-none::text'
css_per_topic_names = 'h4.dc-u-mb-4::text' 
css_per_topic_data = 'p.dc-u-mt-0::text' #first 12
css_other_track = 'span.dc-dropdown--nav__track-name::text'
css_track_comp = 'div div h5::text'
#css_track_names = 'div.track-block__main h4::text'

thefile = open('my_profile.txt','r')

html = thefile.read()
sel = Selector(text=html)

print('XP by topic')
#scape web page for content
dc_topic_names = sel.css(css_per_topic_names).extract()
dc_topic_data = sel.css(css_per_topic_data).extract()[:12]
dc_topic_data = just_words(test,nothing,['XP'])
# clean tex and convert to integer
dc_topic_data = [int(re.sub('[\sA-Z]','',test)) 
                 for test in dc_topic_data]

my_topic_xp = pd.DataFrame(list(zip(dc_topic_names,dc_topic_data)), \
               columns =['Topic','XP'])
# make category
my_topic_xp.Topic = my_topic_xp.Topic.astype("category")
my_topic_xp.sort_values(by='XP',ascending=False,inplace=True)


plt.bar(x=my_topic_xp.Topic,height=my_topic_xp.XP)
plt.xticks(rotation=60)
plt.ylabel("XP")
plt.xlabel("Topic")
plt.title("Topics by XP")
plt.savefig('topic_chart.png')
plt.show()
dc_counts = sel.css(css_dc_counts).extract()
print('Total XP',dc_counts[0])
print('Total Courses',dc_counts[1])
print('Total Exercises',dc_counts[2])

print()
print('all courses')
course_list = sel.css(css_course_list).extract()
lang_raw=sel.xpath(xsel_lang_list).extract()
lang_list=just_words(lang_raw,is_amp,['0'])

my_courses = pd.DataFrame(list(zip(lang_list,course_list)), \
               columns =['Technology','Course_Name'])
my_courses.Technology = my_courses.Technology.str.title()
my_courses.Course_Name = my_courses.Course_Name.str.title()

my_courses.groupby('Technology', as_index=False)['Course_Name'].count().plot('Technology', kind='bar')
plt.xticks(rotation=45)
plt.title("Courses by Technology")
plt.ylabel('Courses')
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
#
css_track_names ='div.track-block__main'
track_names = sel.css(css_track_names).extract()

track_names = just_words(track_names,is_amp,['0'])
my_tracks = pd.DataFrame(list(track_names), \
               columns =['Skill_Track'])
my_tracks.Skill_Track = my_tracks.Skill_Track.str.replace('\n ','').str.strip()
print(my_tracks)


track_comp = sel.css(css_track_comp).extract()
#print(track_comp)

other=sel.css(css_other_track).extract()
#print(other)
my_tech = my_courses.Technology.unique()
