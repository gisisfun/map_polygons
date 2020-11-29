#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:58:02 2020
@author: me
DataCamp Summary of Courses Tracks and Projects
Sourced from html from profile page (my_profile.txt) and pdf certificates 
sotored in subdirectories (Courses, Skills, Career)
"""
import pdftotext
import os
import numpy as np
import pandas as pd
from scrapy import Selector
import matplotlib.pyplot as plt
import re
import spacy
from itertools import repeat


def extract_pdf_data(page_text,c_type):
    page_lines = page_text.split('\n')
    ref=page_lines[0]
    #print(page_lines)
    #if c_type=='Courses':        
    if len(page_lines) == 5:
        course = page_lines[2].replace(' Track','')
        date = page_lines[3]
    else:
        course = page_lines[2]+' '+page_lines[3]
        date = page_lines[4]
    #else:
    #    course = page_lines[2].replace(' Track','')
    #    date=np.nan
    print(ref,course,date)
    return ref,course,date

def extract_pdf_courses(path_to_files):
    list_out=[]
    for (root,dirs,files) in os.walk(path_to_files, topdown=True):
        print(dirs,root)
        dirs_list=dirs
        for dir_name in dirs_list:
            the_path=path_to_files +'/'+ dir_name
            for (root,dirs,files) in os.walk(the_path, topdown=True):
                #print("bbbb",path_to_files,files)
                if len(root.split('/')) >2:
                    course_or_track = root.split('/')[2]
                    print(course_or_track,root)
                    if course_or_track in ['Skill','Career']:
                        c_type = course_or_track
                    else:
                        c_type = 'Course'
                if 'certificate.pdf' in files:
                    
                    the_file=''+root+'/certificate.pdf'
                    # Load your PDF
                    with open(the_file, "rb") as f:
                        pdf = pdftotext.PDF(f)

                        # Iterate over all the pages
                        for page in pdf:
                            #print(page)
                            page_text= page
                            
                            (ref, course, date) = extract_pdf_data(page_text,
                            dir_name)
                            
                            list_out.append([ref,
                                             course,
                                             date, c_type])
        return list_out


def just_words(raw_html,func,non_extra=[]):
    '''
    Finds all words in html 
    
    input:
        raw_html - list of strings returned from scrapy query
        
    returns:
        list of strings without html text
    '''

#    nlp = spacy.load('en_core_web_sm')

#   text = "I bland: , hello"
#    doc = nlp(text)
#    words = [word.text for word in doc]
#
#    print(' '.join([word for word in words if word.isalpha()]))

    non_words = ['block__main', 'class', 
                 'dc', 'div', 'h4', 'mb',
                 'mt', 'p', 'track', 'u',
                 'course','block__technology','...'] + non_extra
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

if __name__ == "__main__":
    #course_as = sel.css( 'div.course-block > a' )
    # Selecting all href attributes chaining with css
    #hrefs_from_css = course_as.css( '::attr(href)' )
    # Selecting all href attributes chaining with xpath
    #hrefs_from_xpath = course_as.xpath( './@href' )
    css_dc_counts = 'strong.dc-u-m-none::text'

    xsel_course_lang = '//div[contains(@class,"course-block__technology course-block__technology--")]'

    css_python_course_names = "div.course-block__technology--python + div.course-block__body h4.course-block__title::text"
    css_python_course_desc = "div.course-block__technology--python + div.course-block__body h4.course-block__title + p.course-block__description::text"

    css_r_course_names = "div.course-block__technology--r + div.course-block__body h4.course-block__title::text"
    css_r_course_desc = "div.course-block__technology--r + div.course-block__body h4.course-block__title + p.course-block__description::text"

    css_sql_course_names = "div.course-block__technology--sql + div.course-block__body h4.course-block__title::text"
    css_sql_course_desc = "div.course-block__technology--sql + div.course-block__body h4.course-block__title + p.course-block__description::text"

    css_scala_course_names = "div.course-block__technology--scala + div.course-block__body h4.course-block__title::text"
    css_scala_course_desc = "div.course-block__technology--scala + div.course-block__body h4.course-block__title + p.course-block__description::text"

    css_shell_course_names = "div.course-block__technology--shell + div.course-block__body h4.course-block__title::text"
    css_shell_course_desc = "div.course-block__technology--shell + div.course-block__body h4.course-block__title + p.course-block__description::text"

    css_theory_course_names = "div.course-block__technology--theory + div.course-block__body h4.course-block__title::text"
    css_theory_course_desc = "div.course-block__technology--theory + div.course-block__body h4.course-block__title + p.course-block__description::text"


    css_course_list = 'h4.course-block__title::text'
    css_course_urls = 'a.course-block__link::attr(href)'
    css_course_descriptions = 'p.course-block__description::text'
    css_per_topic_names = 'h4.dc-u-mb-4::text' 
    css_per_topic_data = 'p.dc-u-mt-0::text' #first 12
    css_other_track = 'span.dc-dropdown--nav__track-name::text'
    css_topic_urls = 'section.profile-topics a.shim::attr(href)'
    
    css_track_names ='div.track-block__main'
    css_track_urls = 'section.profile-tracks a.shim::attr(href)'
    css_track_comp = 'div div h5::text'
    #css_track_names = 'div.track-block__main h4::text'
    css_urls = 'a::attr(href)'

    css_titles_text = 'title::text'
    css_project_urls='section.profile-courses a.shim::attr(href)'
    css_project_names='section.profile-courses h5.dc-project-block__title::text'
    
    thefile = open('my_profile.txt','r')

    print('getting pdf cert data')
    cert_list = extract_pdf_courses('Datacamp')
                
    cert_df = pd.DataFrame(cert_list, columns=['ref','course','date','c_type'])
    #cert_df.ref = cert_df.ref.str.strip()
    cert_df.course = cert_df.course\
                     .str.replace('COMPLETED ON','')\
                     .str.strip()\
                     .str.replace(' Track','')
                     
    cert_df['date_fmt'] = cert_df.date
    #pd.to_datetime(cert_df.date)
    cert_df['course'] = cert_df.course.str.replace('So ware','Software')
    cert_df['course'] = cert_df.course.str.replace('E cient','Efficient')
    cert_df['course'] = cert_df.course.str.replace("Air ow","Airflow")
    #cert_df['course'] = cert_df.course.str.replace(":","")
    cert_df['course'] = cert_df.course.str.replace("Classi cation",
           "Classification")
    cert_df['course'] = cert_df.course.str.replace("Classi ers","Classifiers")
    cert_df['course_lower'] = cert_df.course.str.lower()
    
    # initalize new excel file
    writer = pd.ExcelWriter('datacamp_certs.xlsx', engine = 'xlsxwriter')

    html = thefile.read()
    sel = Selector(text=html)
    the_title = sel.css(css_titles_text).extract_first()
    print(the_title)
    print('')
    print('XP by topic')

    dc_counts = sel.css(css_dc_counts).extract()
    print('Total XP '+dc_counts[0]+' Total Courses '+dc_counts[1] + 
             ' Total Exercises '+dc_counts[2])
#    cert_counts = cert_df.c_type.value_counts()
          
#    print(cert_counts) 
    #scape web page for content
    dc_topic_names = sel.css(css_per_topic_names).extract()
    dc_topic_data = sel.css(css_per_topic_data).extract()[:12]
    dc_topic_data = just_words(dc_topic_data,nothing,['XP'])
    # clean tex and convert to integer
    dc_topic_data = [int(x) for x in dc_topic_data]

    my_topic_xp = pd.DataFrame(list(zip(dc_topic_names,dc_topic_data)), \
                               columns =['Topic','XP'])
    my_topic_xp.Topic =  my_topic_xp.Topic.str.strip()
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

    my_topic_xp.to_excel(writer, index=False, sheet_name='Topic XP')

    
    print('All Courses')
    r_course_names = sel.css(css_r_course_names).extract()
    r_course_desc = [line.strip() for line in 
                         sel.css(css_r_course_desc).extract()]
    r_course = list(zip(r_course_names,
                        r_course_desc,
                        repeat('r')))
    
    python_course_names = sel.css(css_python_course_names).extract()
    python_course_desc = [line.strip() for line in 
                         sel.css(css_python_course_desc).extract()]    
    python_course = list(zip(python_course_names,
                             python_course_desc,
                             repeat('python')))

    sql_course_names = sel.css(css_sql_course_names).extract()
    sql_course_desc = [line.strip() for line in 
                         sel.css(css_sql_course_desc).extract()]    
    sql_course = list(zip(sql_course_names,
                          sql_course_desc,
                          repeat('sql')))

    course_list = sel.css(css_course_list).extract()
    lang_raw=sel.xpath(xsel_course_lang).extract()
    lang_list=just_words(lang_raw,is_amp,['0'])
    course_urls=sel.css(css_course_urls).extract()
    course_descriptions=[line.strip() for line in 
                         sel.css(css_course_descriptions).extract()]


    my_courses = pd.DataFrame(list(zip(lang_list,course_list,course_list,\
                                       course_descriptions,course_urls)), \
                              columns =['Technology','Course_Name','Course_Raw'\
                                        ,'Description','URL'])
    
    my_courses.Technology = my_courses.Technology.str.title()
    my_courses.Course_Name = my_courses.Course_Name.str.title()
    my_courses['course_lower'] = my_courses.Course_Name.str.lower().str.strip()
    
    # add cert data
    courses_join_df = pd.DataFrame.merge(my_courses, cert_df, how='left', 
                                         on='course_lower', 
                                         sort=False, suffixes=('_x', '_y'))

    my_courses.groupby('Technology', as_index=False)['Course_Name'].count()
    
    tech_table=my_courses. \
    groupby('Technology',as_index=False)['Course_Name']. \
    count().rename(columns={"Course_Name":"Course_Count"})
    tech_table['Technology']  = tech_table.Technology.astype("category")
    tech_table.sort_values(by='Course_Count',ascending=False,inplace=True)
    tech_table.plot('Technology', kind='bar')
    plt.xticks(rotation=45)
    plt.title("Courses by Technology")
    plt.ylabel('Courses')
    #plt.gcf().subplots_adjust(bottom=1)
    plt.savefig('tech_chart.png',bbox_inches="tight")
    plt.show()

#
    #    row_cells[2].text = desc
    print(tech_table)
    tech_table.to_excel(writer, index=False, sheet_name='Courses by Technology')


    print('Python Courses')
    python_courses = courses_join_df[['ref','Course_Name','date',
                                      'Description', 'Technology']]\
    .loc[courses_join_df.Technology=='Python'] \
          .sort_values(by='Course_Name').reset_index(drop=True)
    print(python_courses[['ref','Course_Name','date']])
    python_courses.to_excel(writer, index=False, sheet_name='Python Courses')
    
    print('R Courses')    
    r_courses = my_courses \
        .loc[my_courses.Technology=='R','Course_Name'] \
        .sort_values().reset_index(drop=True)    
    r_courses = courses_join_df[['ref','Course_Name','date',
                                 'Description','Technology']]\
    .loc[courses_join_df.Technology=='R'] \
          .sort_values(by='Course_Name').reset_index(drop=True)
          
    print(r_courses[['ref','Course_Name','date']])
    r_courses.to_excel(writer, index=False, sheet_name='R Courses')

    print('SQL Courses')    
    sql_courses = my_courses \
        .loc[my_courses.Technology=='Sql','Course_Name'] \
        .sort_values().reset_index(drop=True)    
    sql_courses = courses_join_df[['ref','Course_Name','date',
                                 'Description','Technology']]\
    .loc[courses_join_df.Technology=='Sql'] \
          .sort_values(by='Course_Name').reset_index(drop=True)
          
    print(sql_courses[['ref','Course_Name','date']])
    sql_courses.to_excel(writer,index=False,sheet_name='SQL Courses')


    track_names = sel.css(css_track_names).extract()

    track_names = just_words(track_names,is_amp,['0'])
    wp_tracks = pd.DataFrame(list(track_names), \
                             columns =['Skill_Track'])
    wp_tracks.Skill_Track = wp_tracks.Skill_Track.str.\
                            replace('\n ','').\
                            str.strip()
    # add cert data
    tracks_join_df = pd.DataFrame.merge(wp_tracks, cert_df, how='left', 
                                        left_on='Skill_Track', right_on='course', 
                                        sort=False, suffixes=('_x', '_y'))

    
    my_tracks_df = tracks_join_df[['ref','course','date','c_type']]
    print("Skill Tracks")
    print(my_tracks_df)
    my_tracks_df.to_excel(writer, sheet_name='Tracks')
    writer.save()
    writer.close()    
    project_names = sel.css(css_project_names).extract()
    project_urls = sel.css(css_project_urls).extract()
    my_projects = pd.DataFrame(list(zip(project_names,project_urls)), \
                               columns =['Project','URL'])

    print("Projects")
    print(my_projects.Project)

    my_tech = my_courses.Technology.unique()


