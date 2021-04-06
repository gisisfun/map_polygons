#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 13:31:35 2021
@author: me
"""
# https://graphviz.readthedocs.io/en/stable/examples.html#g-c-n-py

#from txtoflow import txtoflow
#
#txtoflow.generate(
#    '''
#    First Node;
#    if (A != 10) {
#        B;
#    } else if (Just a String) {
#        Another String;
#    } else {
#        Else Body;
#        More Statements;
#        while (While also works) {
#            While Body;
#        }
#        Link back;
#    }
#    Final Node;
#    '''
#)




from graphviz import Digraph,Source

dot = Digraph(comment='DataCamp_Charts',node_attr={"rankdir":"LR"})
dot.attr(rankdir='LR')
dot.attr('node', shape='ellipse')
dot.node('PDF', 'PDF Files',shape="box")
dot.node('Certs','Certificates',shape='ellipse')
dot.node('HTML', 'HTML File',shape="box")
dot.node('Courses_s', 'Scraped\nCourses',shape="ellipse")
dot.node('Topics', 'Scraped\nTopics',shape="ellipse")
dot.node('Tracks_s', 'Scraped\nTracks',shape="ellipse")
dot.node('Tracks', 'Tracks\nCerts',shape="ellipse")
dot.node('Courses', 'Courses\nCerts',shape="ellipse")
dot.node('Excel', 'Excel',shape="box")
dot.node('Chart', 'Chart',shape="box")
dot.node('Document', 'Word or\nPDF Document',shape="box")
dot.node('Dataset', 'Data set\nfor BI Tool',shape="box")

#dot.node('A', label = 'King Arthur', shape="diamond")
#dot.node('B', 'Sir Bedevere the Wise',shape="box")
#dot.node('L', 'Sir Lancelot the Brave',shape="ellipse")
dot.edge('PDF','Certs',label='Extract Text')
dot.edge('HTML','Courses_s',label='Scrape')
dot.edge('HTML','Tracks_s',label='Scrape')
dot.edge('HTML','Topics',label='Scrape')
dot.edge('Courses_s','Courses',label='fuzzy')
dot.edge('Certs','Courses',label='clean')
dot.edge('Tracks_s','Tracks',label='')
dot.edge('Certs','Tracks',label='Fix missing letters')
dot.edge('Tracks','Excel',label='')
dot.edge('Courses','Excel',label='filter')
dot.edge('Topics','Excel',label='')
dot.edge('Tracks','Chart',label='reshape')
dot.edge('Courses','Chart',label='reshape')
dot.edge('Tracks','Document',label='TODO')
dot.edge('Courses','Document',label='TODO')
dot.edge('Chart','Document',label='TODO')
dot.edge('Tracks','Dataset',label='TODO')
dot.edge('Courses','Dataset',label='TODO')
#dot.edge('B', 'L', constraint='false')

dot_src = Source("""// DataCamp_Charts
digraph {
	node [rankdir=LR]
	rankdir=LR
	node [shape=ellipse]
	PDF [label="PDF Files" shape=box]
	Certs [label=Certificates shape=ellipse]
	HTML [label="HTML File" shape=box]
	Courses_s [label="Scraped
Courses" shape=ellipse]
	Topics [label="Scraped
Topics" shape=ellipse]
	Tracks_s [label="Scraped
Tracks" shape=ellipse]
	Tracks [label="Tracks
Certs" shape=ellipse]
	Courses [label="Courses
Certs" shape=ellipse]
	Excel [label=Excel shape=box]
	Chart [label=Chart shape=box]
	Document [label="Word or
PDF Document" shape=box]
	Dataset [label="Data set
for BI Tool" shape=box]
	PDF -> Certs [label="Extract Text"]
	HTML -> Courses_s [label=Scrape]
	HTML -> Tracks_s [label=Scrape]
	HTML -> Topics [label=Scrape]
	Courses_s -> Courses [label=fuzzy]
	Certs -> Courses [label=clean]
	Tracks_s -> Tracks [label=""]
	Certs -> Tracks [label="Fix missing letters"]
	Tracks -> Excel [label=""]
	Courses -> Excel [label=filter]
	Topics -> Excel [label=""]
	Tracks -> Chart [label=reshape]
	Courses -> Chart [label=reshape]
	Tracks -> Document [label=TODO]
	Courses -> Document [label=TODO]
	Chart -> Document [label=TODO]
	Tracks -> Dataset [label=TODO]
	Courses -> Dataset [label=TODO]
}""")


dot_src.format='png'
print(dot.source)
dot_src.render('test-output/datacamp_certs.gv', view=True)
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
