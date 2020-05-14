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

from docx import Document


document = Document()
paragraphs = document.paragraphs

from docx.shared import Pt

style = document.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(10)

document.styles['Normal']

def doctable(data, tabletitle):
    data = pd.DataFrame(data)  # My input data is in the 2D list form
    document.add_heading(tabletitle)
    table = document.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    for i,val in enumerate(data.columns):
        hdr_cells[i].text = val
#    hdr_cells[1].text = 'Id'
    table = document.add_table(rows=(data.shape[0]), cols=data.shape[1])  # First row are table headers!
    #document.styles("Normal")
    for i, column in enumerate(data) :
        for row in range(data.shape[0]) :
            table.cell(row, i).line_spacing = 0.5
            table.cell(row, i).text = str(data[column][row])



def print_me(text='',to_docx=True, style='Normal'):
    if (to_docx):
        document.add_paragraph(text)
    print(text)


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
css_urls = 'a::attr(href)'
css_course_urls = 'a.course-block__link::attr(href)'
css_topic_urls = 'a.shim::attr(href)'
css_titles_text = 'title::text'
css_track_names ='div.track-block__main'


thefile = open('my_profile.txt','r')

html = thefile.read()
sel = Selector(text=html)
the_title = sel.css(css_titles_text).extract_first()
document.add_heading(the_title, 0)
print(the_title)
print('')

document.add_heading('XP Points by Topic', level=1)
print('XP by topic')

dc_counts = sel.css(css_dc_counts).extract()
print_me('Total XP '+dc_counts[0]+' Total Courses '+dc_counts[1] + 
         ' Total Exercises '+dc_counts[2])

#scape web page for content
dc_topic_names = sel.css(css_per_topic_names).extract()
dc_topic_data = sel.css(css_per_topic_data).extract()[:12]
dc_topic_data = just_words(dc_topic_data,nothing,['XP'])
# clean tex and convert to integer
dc_topic_data = [int(x) for x in dc_topic_data]

my_topic_xp = pd.DataFrame(list(zip(dc_topic_names,dc_topic_data)), \
               columns =['Topic','XP'])
# make category
my_topic_xp.Topic = my_topic_xp.Topic.astype("category")
my_topic_xp.sort_values(by='XP',ascending=False,inplace=True)


plt.bar(x=my_topic_xp.Topic,height=my_topic_xp.XP)
plt.xticks(rotation=90)
plt.ylabel("XP")
plt.xlabel("Topic")
plt.title("Topics by XP")
#plt.gcf().subplots_adjust(bottom=1)
plt.savefig('topic_chart.png',bbox_inches="tight")
plt.show()

document.add_picture('topic_chart.png')

document.add_page_break()
document.add_heading('All Courses', level=1)
print('All Courses')

course_list = sel.css(css_course_list).extract()
lang_raw=sel.xpath(xsel_lang_list).extract()
lang_list=just_words(lang_raw,is_amp,['0'])
course_urls=sel.css(css_course_urls).extract()

my_courses = pd.DataFrame(list(zip(lang_list,course_list,course_urls)), \
               columns =['Technology','Course_Name',"URL"])
my_courses.Technology = my_courses.Technology.str.title()
my_courses.Course_Name = my_courses.Course_Name.str.title()

my_courses.groupby('Technology', as_index=False)['Course_Name'].count().plot('Technology', kind='bar')
plt.xticks(rotation=45)
plt.title("Courses by Technology")
plt.ylabel('Courses')
#plt.gcf().subplots_adjust(bottom=1)
plt.savefig('tech_chart.png',bbox_inches="tight")
plt.show()
document.add_picture('tech_chart.png')



tech_table=my_courses. \
groupby('Technology',as_index=False)['Course_Name']. \
count().rename(columns={"Course_Name":"Course_Count"})

doctable(tech_table,"Course count by Technology (Language)")
#    row_cells[2].text = desc

print(tech_table)

document.add_page_break()
python_courses = my_courses \
      .loc[my_courses.Technology=='Python','Course_Name'] \
      .sort_values().reset_index(drop=True)
doctable(python_courses,"Python Courses List")

print('Python Courses')
print(python_courses)
r_courses = my_courses \
    .loc[my_courses.Technology=='R','Course_Name'] \
    .sort_values().reset_index(drop=True)
    
document.add_page_break()
doctable(r_courses,"R Courses List")
print('R Courses')
print(r_courses)


#
document.add_page_break()
track_names = sel.css(css_track_names).extract()

track_names = just_words(track_names,is_amp,['0'])
my_tracks = pd.DataFrame(list(track_names), \
               columns =['Skill_Track'])
my_tracks.Skill_Track = my_tracks.Skill_Track.str.replace('\n ','').str.strip()
doctable(my_tracks,"Skill Tracks")
print("Skill Tracks")
print(my_tracks)


track_comp = sel.css(css_track_comp).extract()
#print(track_comp)

other=sel.css(css_other_track).extract()
#print(other)
my_tech = my_courses.Technology.unique()



document.save('test.docx')
