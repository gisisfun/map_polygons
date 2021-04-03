#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 13:31:35 2021

@author: me
"""
# https://graphviz.readthedocs.io/en/stable/examples.html#g-c-n-py

from txtoflow import txtoflow

txtoflow.generate(
    '''
    First Node;
    if (A != 10) {
        B;
    } else if (Just a String) {
        Another String;
    } else {
        Else Body;
        More Statements;
        while (While also works) {
            While Body;
        }
        Link back;
    }
    Final Node;
    '''
)




from graphviz import Digraph,Graph

dot = Digraph(comment='DataCamp_Charts')
dot.attr('node', shape='ellipse')
dot.node('PDF', 'PDF Files',shape="box")
dot.node('ExtractText','Extract\nText',shape='ellipse')
dot.node('Certs','Certificates',shape='ellipse')
dot.node('HTML', 'HTML File',shape="box")
dot.node('Scrape', 'Scrape\nHTML',shape="ellipse")
dot.node('Courses_s', 'Scraped\nCourses',shape="ellipse")
dot.node('Topics', 'Scraped\nTopics',shape="ellipse")
dot.node('Tracks_s', 'Scraped\nTracks',shape="ellipse")
dot.node('Tracks', 'Tracks\nCerts',shape="ellipse")
dot.node('Courses', 'Coursess\nCerts',shape="ellipse")
dot.node('Excel', 'Excel',shape="ellipse")
dot.node('Chart', 'Chart',shape="ellipse")

#dot.node('A', label = 'King Arthur', shape="diamond")
#dot.node('B', 'Sir Bedevere the Wise',shape="box")
#dot.node('L', 'Sir Lancelot the Brave',shape="ellipse")
dot.edge('PDF','ExtractText',label='')
dot.edge('ExtractText','Certs',label='')
dot.edge('HTML','Scrape',label='')
dot.edge('Scrape','Courses_s',label='')
dot.edge('Scrape','Tracks_s',label='')
dot.edge('Scrape','Topics',label='')
dot.edge('Courses_s','Courses',label='')
dot.edge('Certs','Courses',label='')
dot.edge('Tracks_s','Tracks',label='')
dot.edge('Certs','Tracks',label='')
dot.edge('Tracks','Excel',label='')
dot.edge('Courses','Excel',label='')
dot.edge('Topics','Excel',label='')
dot.edge('Tracks','Chart',label='')
dot.edge('Courses','Chart',label='')
#dot.edge('B', 'L', constraint='false')
dot.format='png'
print(dot.source)
dot.render('test-output/datacamp_certs.gv', view=True)
dot
#g = Graph('G', filename='process.gv', engine='sfdp')
#
#g.edge('run', 'intr')
#g.edge('intr', 'runbl')
#g.edge('runbl', 'run')
#g.edge('run', 'kernel')
#g.edge('kernel', 'zombie')
#g.edge('kernel', 'sleep')
#g.edge('kernel', 'runmem')
#g.edge('sleep', 'swap')
#g.edge('swap', 'runswap')
#g.edge('runswap', 'new')
#g.edge('runswap', 'runmem')
#g.edge('new', 'runmem')
#g.edge('sleep', 'runmem')
#
#g.render('test-output/process.gv', view=True)
#g
#import pygraphviz as pgv
#
#A = pgv.AGraph()
#
#A.add_edge(1, 2)
#A.add_edge(2, 3)
#A.add_edge(1, 3)
#
#print(A.string())  # print to screen
#A.write("simple.dot")  # write to simple.dot
#
#B = pgv.AGraph("simple.dot")  # create a new graph from file
#B.layout()  # layout with default (neato)
#B.draw("simple.png")  # draw png
