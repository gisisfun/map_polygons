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

def list_ne(sent_list): #,pos):
    """Process list of course names for point of speech tags
    """
    token_sentences = [nltk.word_tokenize(sent) for sent in sent_list]
    pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences]
    #print(pos_sentences[:5])

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
                print(chunk)
                ne_words = ' '.join(ne_line)
                ne_list.append(ne_words)        
    return ne_list

if __name__ == "__main__":
    #course_as = sel.css( 'div.course-block > a' )
    # Selecting all href attributes chaining with css
    #hrefs_from_css = course_as.css( '::attr(href)' )
    # Selecting all href attributes chaining with xpath
    #hrefs_from_xpath = course_as.xpath( './@href' )
    
    # courses page css definitions
    css_c_course_name='h2.css-1mzwl36-baseStyle-baseHeaderStyle-multiLineStyle::text'
    css_c_course_desc='h2.css-1mzwl36-baseStyle-baseHeaderStyle-multiLineStyle + p::text'
    css_json='script#__NEXT_DATA__::text'

    # profile page css definitions
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
    thecourses= open('all_courses.txt','r')

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


        
    all_course_html = thecourses.read()
    all_course_sel = Selector(text=all_course_html)
    json_text = [x.replace('\\u[a-z0-9](4)','') for x in all_course_sel.css(css_json).extract()]
    origdict = json.loads(json_text[0])
    thedict = origdict['props']['pageProps']['initialChunks'][0]['items']

    #dicts=[d.append() for d in origdict['props']['pageProps']['initialChunks'][0]['items']]

    
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
    my_topic_xp.sort_values(by='XP',ascending=True,inplace=True)
    #my_topic_xp.plot(kind='barh')
    #fig,(ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15,3))
    fig,((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize=(10,6))
    
    fig.tight_layout(h_pad=5, w_pad=5)
    ax1.barh(y=my_topic_xp.Topic,width=my_topic_xp.XP)
    #ax1.xticks(rotation=90)
    ax1.set_ylabel("XP")
    ax1.set_xlabel("Topic")
    ax1.set_title("Topics by XP",size=14)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    #plt.gcf().subplots_adjust(bottom=1)
    #plt.savefig('topic_chart.png',bbox_inches="tight")
    #plt.show()

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

    scraped_course_list = sel.css(css_course_list).extract()
    lang_raw=sel.xpath(xsel_course_lang).extract()
    scraped_tech_list=just_words(lang_raw,is_amp,['0'])
    scraped_urls_list=sel.css(css_course_urls).extract()
    scraped_desc_list=[line.strip() for line in 
                         sel.css(css_course_descriptions).extract()]


    scraped_courses = pd.DataFrame(list(zip(scraped_tech_list,
                                            scraped_course_list,
                                            scraped_desc_list,
                                            scraped_urls_list)), \
                              columns =['Technology',
                                        'Course_Name',
                                        'Description',
                                        'URL'])
    
    scraped_courses.Technology = scraped_courses.Technology.str.title()
    scraped_courses.Course_Name = scraped_courses.Course_Name.str.title()
    scraped_courses['course_lower'] = scraped_courses.Course_Name.str.lower().str.strip()
    course_counts_df = pd.get_dummies(scraped_courses.Technology)
    courses_and_counts= pd.concat([scraped_courses,course_counts_df],
                                  axis=1,sort=False)
    # add cert data
    courses_and_certs = pd.DataFrame.merge(courses_and_counts, cert_df, how='left', 
                                         on='course_lower', 
                                         sort=False, suffixes=('_x', '_y'))
    courses_and_certs['date_completed'] = pd.to_datetime(courses_and_certs.date_fmt)
    courses_and_certs['week'] = courses_and_certs['date_completed'].dt.week
    courses_and_certs['month'] = courses_and_certs['date_completed'].dt.month
    courses_and_certs['year'] = courses_and_certs['date_completed'].dt.year
    courses_and_certs.set_index(courses_and_certs['date_completed'],inplace=True)
    scraped_courses.groupby('Technology', as_index=False)['Course_Name'].count()
    
    tech_table=scraped_courses. \
     groupby('Technology',as_index=False)['Course_Name']. \
    count().rename(columns={"Course_Name":"Course_Count"})
    tech_table['Technology']  = tech_table.Technology.astype("category")
    tech_table.sort_values(by='Course_Count',ascending=True,inplace=True)
    tech_table.plot.barh('Technology', legend=False,ax=ax2)
    ax2.set_title("DataCamp Courses by Technology",size=14)
    ax2.set_ylabel('Courses')
    
    
    # word could ax3
    #import nltk
    #nltk.download()
    #nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    course_name_raw = list_ne(cert_df.course.values)
    course_desc_raw = list_ne(scraped_courses.Description.values)
    raw_data = ' ' .join(course_desc_raw) + ' '.join(course_name_raw)
    joined_course_text = lemmatizer.lemmatize(raw_data)
    stop_words=['Intermediate','Introduction','to','in','working','for','and'
                ,'with','Data', 'Science','get','use','learn','Learning',
                'writing','programming','everyone','the','toolbox','dealing',
                'foundations','building','efficient','part','thinking','of',
                'oriented','level','continue','master','postg','sas',
                'consolidate','dive','create','imitate','discover','explore',
                'school','case','exploratory','advanced']
    ## Generate the word cloud from the east_of_eden string
    cloud_courses = WordCloud(background_color="white",
                              stopwords=stop_words).generate(joined_course_text)
    ax3.imshow(cloud_courses, interpolation='bilinear')
    ax3.axis("off")
    ax3.set_title("Word Cloud of DataCamp Course Names",size=14)
    
    courses_and_certs.resample('1 w')['Python','Theory',
                              'R','Sql','Scala',
                              'Shell','Tableau',
                              'Power_Bi','Excel'].sum().plot(ax=ax4)
    ax4.set_title("DataCamp Course Completion by Technology")
    ax4.legend(loc='upper right', frameon=False)
    fig.savefig('DataCamp ' + datetime.isoformat(datetime.today())[:10]+'.png',bbox_inches="tight")
    fig.show()
    #a = list_ne(cert_df.course.values)
    #a = list_ne(scraped_courses.Description.values)
    #nlp_certs_string= ' '.join(a)
    #nlp_certs = WordCloud(background_color="white", 
    #stopwords=stop_words).generate(nlp_certs_string)
    #plt.imshow(nlp_certs, interpolation='bilinear')
#
    #    row_cells[2].text = desc
    print(tech_table)
    tech_table.to_excel(writer, index=False, sheet_name='Courses by Technology')


    print('Python Courses')
    python_courses = courses_and_certs[['ref','Course_Name','date',
                                      'Description', 'Technology']]\
    .loc[courses_and_certs.Technology=='Python'] \
          .sort_values(by='Course_Name').reset_index(drop=True)
    print(python_courses[['ref','Course_Name','date']])
    python_courses.to_excel(writer, index=False, sheet_name='Python Courses')
    
    print('R Courses')    
    r_courses = courses_and_certs \
        .loc[courses_and_certs.Technology=='R','Course_Name'] \
        .sort_values().reset_index(drop=True)    
    r_courses = courses_and_certs[['ref','Course_Name','date',
                                 'Description','Technology']]\
    .loc[courses_and_certs.Technology=='R'] \
          .sort_values(by='Course_Name').reset_index(drop=True)
          
    print(r_courses[['ref','Course_Name','date']])
    r_courses.to_excel(writer, index=False, sheet_name='R Courses')

    print('SQL Courses')    
    sql_courses = courses_and_certs \
        .loc[courses_and_certs.Technology=='Sql','Course_Name'] \
        .sort_values().reset_index(drop=True)    
    sql_courses = courses_and_certs[['ref','Course_Name','date',
                                 'Description','Technology']]\
    .loc[courses_and_certs.Technology=='Sql'] \
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
    tracks_and_certs = pd.DataFrame.merge(wp_tracks, cert_df, how='left', 
                                        left_on='Skill_Track', right_on='course', 
                                        sort=False, suffixes=('_x', '_y'))

    
    my_tracks_df = tracks_and_certs[['ref','course','date','c_type']]
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

    my_tech = courses_and_certs.Technology.unique()
    
    # Tokenize the article into sentences: sentences
# lemmatize
# Import spacy
    
#import spacy
#
## Instantiate the English model: nlp
#nlp = spacy.load('en',tagger=False,parser=False,matcher=False)
#
## Create a new document: doc
#doc = nlp(article)
#
## Print all of the found entities and their labels
#for ent in doc.ents:
#    print(ent.label_, ent.text)

    

