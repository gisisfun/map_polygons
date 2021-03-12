#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:58:02 2020
@author: Damien Clarke
DataCamp Summary of Courses Tracks and Projects
Sourced from html from profile page (my_profile.txt) and pdf certificates 
stored in subdirectories (Courses, Skills, Career)
"""
import pdftotext
import os
#import numpy as np
import pandas as pd
from scrapy import Selector
import matplotlib.pyplot as plt
import re
#import spacy
from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer 
import nltk

from itertools import repeat
import json
from datetime import datetime
from fuzzywuzzy import process


def extract_pdf_data(page_text,c_type,verbose=False):
    page_lines = page_text.split('\n')
    ref=page_lines[0]
        
    if len(page_lines) == 5:
        course = page_lines[2].replace(' Track','')
        date = page_lines[3]
    else:
        course = page_lines[2]+' '+page_lines[3]
        date = page_lines[4]

    if verbose == True:
        print(ref,course,date)
    return ref,course,date

def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    # https://stackoverflow.com/questions/13636848/is-it-possible-to-do-fuzzy-match-merge-with-python-pandas
    s = df_2[key2].tolist()
    
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    m2_list  = df_1['matches'].tolist()
    df_1['matches'] = [x.split(', ')[0] for x in m2_list]
    return df_1

def extract_pdf_courses(path_to_files, verbose=False):
    list_out=[]
    for (root,dirs,files) in os.walk(path_to_files):
        if verbose == True:
            print(dirs,root)
        dirs_list=dirs
        for dir_name in dirs_list:
            the_path=path_to_files +'/'+ dir_name
            for (root,dirs,files) in os.walk(the_path, topdown=True):
                
                if len(root.split('/')) >2:
                    course_or_track = root.split('/')[2]
                    if verbose == True:
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
                            page_text= page
                            (ref, course, date) = extract_pdf_data(page_text,
                            dir_name)
                            list_out.append([ref,course,date, c_type])
        return list_out


def just_words(raw_html,func,non_extra=[]):
    """
    Finds all words in html 
    
    input:
        raw_html - list of strings returned from scrapy query
        
    returns:
        list of strings without html text
    """

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

def list_ne(sent_list,verbose=False): 
    """Process list of course names for point of speech tags
    """
    token_sentences = [nltk.word_tokenize(sent) for sent in sent_list]
    pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences]

    chunked_sentences = nltk.ne_chunk_sents(pos_sentences,binary=True)
    ne_list=[]
    ne_raw=[]
    # Test for stems of the tree with 'NE' tags
    for sent in chunked_sentences:
        ne_line=[]
        for chunk in sent:
            ne_raw.append(chunk)
            if hasattr(chunk, "label") and chunk.label() == "NE":# and chunk[0][1] == pos:
                ne_line.append(chunk[0][0])
                if verbose == True:
                    print(chunk)
                ne_words = ' '.join(ne_line)
                ne_list.append(ne_words)        
    return ne_list


def scrape_tracks(sel,css_dict,pdf_certs):
    print("Skill Tracks")
    track_names = sel.css(css_dict['track_names']).extract()

    track_names = just_words(track_names,is_amp,['0'])
    wp_tracks = pd.DataFrame(list(track_names), \
                             columns =['Skill_Track'])
    wp_tracks.Skill_Track = wp_tracks.Skill_Track.str.\
                            replace('\n ','').\
                            str.strip()
    # add cert data
    df = pd.DataFrame.merge(wp_tracks, pdf_certs, how='left', 
                                        left_on='Skill_Track', right_on='course', 
                                        sort=False, suffixes=('_x', '_y'))
    return df

def scrape_projects(sel,css_dict):
    print("Projects") 
    names = sel.css(css_dict['project_names']).extract()
    urls = sel.css(css_dict['project_urls']).extract()
    df = pd.DataFrame(list(zip(names,urls)), columns =['Project','URL']).\
                                   reset_index(drop=True)
                                 
    return df

def lang_worksheets(df,wb,verbose=False):
    tech = df.Technology.unique()
    if verbose == True:
        print(tech)
        print(df)
    df.drop('Technology',axis=1,inplace=True)
    df.reset_index(drop=True,inplace=True)

    df.to_excel(wb, index=False, sheet_name=str(tech[0]))


if __name__ == "__main__":

    # profile page css definitions
    xpath_dict ={'course_lang': '//div[contains(@class,"course-block__technology course-block__technology--")]'}
    css_dict ={ 'python_course_names': "div.course-block__technology--python + div.course-block__body h4.course-block__title::text",
    'python_course_desc': "div.course-block__technology--python + div.course-block__body h4.course-block__title + p.course-block__description::text",
    'r_course_names': "div.course-block__technology--r + div.course-block__body h4.course-block__title::text",
    'r_course_desc': "div.course-block__technology--r + div.course-block__body h4.course-block__title + p.course-block__description::text",
    'sql_course_names': "div.course-block__technology--sql + div.course-block__body h4.course-block__title::text",
    'sql_course_desc': "div.course-block__technology--sql + div.course-block__body h4.course-block__title + p.course-block__description::text",
    'scala_course_names': "div.course-block__technology--scala + div.course-block__body h4.course-block__title::text",
    'scala_course_desc': "div.course-block__technology--scala + div.course-block__body h4.course-block__title + p.course-block__description::text",
    'shell_course_names': "div.course-block__technology--shell + div.course-block__body h4.course-block__title::text",
    'shell_course_desc': "div.course-block__technology--shell + div.course-block__body h4.course-block__title + p.course-block__description::text",
    'theory_course_names': "div.course-block__technology--theory + div.course-block__body h4.course-block__title::text",
    'theory_course_desc': "div.course-block__technology--theory + div.course-block__body h4.course-block__title + p.course-block__description::text",
    'dc_counts': 'strong.dc-u-m-none::text', 
    'course_list': 'h4.course-block__title::text',
    'course_urls': 'a.course-block__link::attr(href)',
    'course_descriptions': 'p.course-block__description::text',
    'per_topic_names': 'h4.dc-u-mb-4::text', 
    'per_topic_data':  'p.dc-u-mt-0::text',
    'track_names': 'div.track-block__main',
    'other_track': 'span.dc-dropdown--nav__track-name::text',
    'topic_urls': 'section.profile-topics a.shim::attr(href)',
    'track_urls': 'section.profile-tracks a.shim::attr(href)',
    'track_comp': 'div div h5::text',
    'urls': 'a::attr(href)',
    'titles_text': 'title::text',
    'project_urls': 'section.profile-courses a.shim::attr(href)',
    'project_names': 'section.profile-courses h5.dc-project-block__title::text'}
    
    pdf_bad =[['So ware','Software'],['E cient','Efficient'],['Air ow','Airflow']]
  
    stop_words = ['Intermediate','Introduction','to','in','working','for','and'
                  ,'with','Data', 'Science','get','use','learn','Learning',
                  'writing','programming','everyone','the','toolbox','dealing',
                  'foundations','building','efficient','part','thinking','of',
                  'oriented','level','continue','master','postg','sas',
                  'consolidate','dive','create','imitate','discover','explore',
                  'school','case','exploratory','advanced']

    profile_page = open('my_profile.txt','r')

    print('getting pdf cert data')
    cert_list = extract_pdf_courses('Datacamp')
                
    certs_pdf = pd.DataFrame(cert_list, columns=['ref','course','date','c_type'])
    #cert_df.ref = cert_df.ref.str.strip()
    certs_pdf.course = certs_pdf.course\
                     .str.replace('COMPLETED ON','')\
                     .str.strip()\
                     .str.replace(' Track','')
    for _ in range(len(pdf_bad)):
        certs_pdf['course'] = certs_pdf.course.str.replace(pdf_bad[_][0],
               pdf_bad[_][1])
                   
    certs_pdf['course_lower'] = certs_pdf.course.str.lower()

    # initalize new excel file
    writer = pd.ExcelWriter('datacamp_certs.xlsx', engine = 'xlsxwriter')

    html = profile_page.read()
    sel = Selector(text=html)
    
    the_title = sel.css(css_dict['titles_text']).extract_first()
    print(the_title)
    print('')
    print('XP by topic')

    dc_counts = sel.css(css_dict['dc_counts']).extract()
    print('Total XP '+dc_counts[0]+' Total Courses '+dc_counts[1] + 
             ' Total Exercises '+dc_counts[2])

    # scrape web page for content
    dc_topic_names = sel.css(css_dict['per_topic_names']).extract()
    dc_topic_data = sel.css(css_dict['per_topic_data']).extract()[:12]
    dc_topic_data = just_words(dc_topic_data,nothing,['XP'])
    # clean tex and convert to integer
    dc_topic_data = [int(x) for x in dc_topic_data]

    my_topic_xp = pd.DataFrame(list(zip(dc_topic_names,dc_topic_data)), \
                               columns =['Topic','XP'])
    my_topic_xp.Topic =  my_topic_xp.Topic.str.strip()
    
    # make category
    my_topic_xp.Topic = my_topic_xp.Topic.astype("category")
    my_topic_xp.sort_values(by='XP',ascending=True,inplace=True)


    fig,((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize=(15,8),
         constrained_layout=True)
    fig.suptitle('Data Camp Course Progress ' +
                 datetime.strftime(datetime.today(),format='%d/%m/%Y'),
                 fontsize=24)
    fig.text(0, 0,  
         'See the source code: https://https://github.com/gisisfun/map_polygons/blob/master/other_fun/scrapy_datacamp.py',  
         style = 'italic', 
         fontsize = 14, 
         color = "green")
    #fig.tight_layout(h_pad=15, w_pad=15)
    ax1.barh(y=my_topic_xp.Topic,width=my_topic_xp.XP)

    ax1.set_ylabel("Topic")
    ax1.set_xlabel("XP")
    ax1.set_title("Topics by XP",size=14)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    my_topic_xp.to_excel(writer, index=False, sheet_name='Topic XP')

    course_list_scraped = sel.css(css_dict['course_list']).extract()
    lang_raw=sel.xpath(xpath_dict['course_lang']).extract()
    tech_list_scraped=just_words(lang_raw,is_amp,['0'])
    urls_list_scraped=sel.css(css_dict['course_urls']).extract()
    desc_list_scraped=[line.strip() for line in 
                         sel.css(css_dict['course_descriptions']).extract()]

    courses_scraped = pd.DataFrame(list(zip(tech_list_scraped,
                                           course_list_scraped,
                                           desc_list_scraped,
                                           urls_list_scraped)), \
                            columns =['Technology','Course_Name',
                                      'Description','URL'])
    
    courses_scraped.Technology = courses_scraped.Technology.str.title()
    courses_scraped.Course_Name = courses_scraped.Course_Name.str.title()
    courses_scraped['course_lower'] = courses_scraped.Course_Name.str.lower()\
                                      .str.strip()
    
    # course_dummies = pd.get_dummies(courses_scraped.Technology)
    course_counts= pd.concat([courses_scraped,
                              pd.get_dummies(courses_scraped.Technology)],
                                  axis=1,sort=False)
 
    # fix ... issue with course names in scraped data using fuzzy wuzzy
    course_clean = fuzzy_merge(course_counts, certs_pdf, 'course_lower', 'course_lower', threshold=80)
    course_clean['course_lower']=course_clean['matches']

   # add cert data
    courses_and_certs = pd.merge(course_clean, certs_pdf, how='left',
                                 on='course_lower',sort=False)

    # add more columns
    courses_and_certs['date_completed'] = pd.to_datetime(courses_and_certs.date)
    courses_and_certs['week'] = courses_and_certs['date_completed'].dt.week
    courses_and_certs['month'] = courses_and_certs['date_completed'].dt.month
    courses_and_certs['year'] = courses_and_certs['date_completed'].dt.year
    courses_and_certs.set_index(courses_and_certs['date_completed'],inplace=True)
    courses_scraped.groupby('Technology', as_index=False)['Course_Name'].count()
    
    #data prep for chart
    tech_table = courses_scraped. \
     groupby('Technology',as_index=False)['Course_Name']. \
    count().rename(columns={"Course_Name":"Course_Count"})
    
    tech_table['Technology'] = tech_table.Technology.astype("category")
    
    tech_table.sort_values(by='Course_Count',ascending=True,inplace=True)
    tech_table.plot.barh('Technology', legend=False,ax=ax2)
    ax2.set_title("DataCamp Courses by Technology",size=14)
    ax2.set_ylabel('Courses')
    
    lemmatizer = WordNetLemmatizer()
    course_name_raw = list_ne(certs_pdf.course.values)
    course_desc_raw = list_ne(courses_scraped.Description.values)
    raw_data = '. ' .join(course_desc_raw) + '. '.join(course_name_raw) + ' R' *4
    joined_course_text = lemmatizer.lemmatize(raw_data)

    ## Generate the word cloud from the east_of_eden string
    cloud_courses = WordCloud(background_color="white",
                              stopwords=stop_words).generate(joined_course_text)
    ax3.imshow(cloud_courses, interpolation='bilinear')
    ax3.axis("off")
    ax3.set_title("Word Cloud of DataCamp Course Names",size=14)
    tech_list = courses_and_certs.columns[5:-9]
    courses_and_certs.resample('1 w')[tech_list].sum().plot(ax=ax4)

    ax4.set_title("DataCamp Course Completion by Technology")
    ax4.legend(loc='upper right', frameon=False)
    fig.savefig('DataCamp ' + datetime.isoformat(datetime.today())[:10]+'.png',bbox_inches="tight")
    fig.show()

    print('Tech Table')
    print(tech_table)
    
    print("Courses and Certs")
    courses_and_certs.groupby('Technology')[['ref','Course_Name',
                             'date','Description', 'Technology']].apply(lang_worksheets,
                             wb=writer)

    my_tracks = scrape_tracks(sel,css_dict,certs_pdf)
    my_tracks = my_tracks[['ref','course','date','c_type']]
    print(my_tracks)
    my_tracks.to_excel(writer, sheet_name='Tracks')

    print("Projects")
    my_projects = scrape_projects(sel,css_dict)
    print(my_projects.Project)
    my_projects.to_excel(writer, sheet_name='Projects')
    writer.close()
    
