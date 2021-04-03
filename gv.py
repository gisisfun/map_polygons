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

dot = Digraph(comment='The Round Table')
dot.attr('node', shape='ellipse')
dot.node('A', label = 'King Arthur', shape="diamond")
dot.node('B', 'Sir Bedevere the Wise',shape="box")
dot.node('L', 'Sir Lancelot the Brave',shape="ellipse")

dot.edge('A','B',label='Yes')
dot.edge('A','L',label='No')
#dot.edge('B', 'L', constraint='false')
print(dot.source)
dot.render('test-output/round-table.gv', view=True)

g = Graph('G', filename='process.gv', engine='sfdp')

g.edge('run', 'intr')
g.edge('intr', 'runbl')
g.edge('runbl', 'run')
g.edge('run', 'kernel')
g.edge('kernel', 'zombie')
g.edge('kernel', 'sleep')
g.edge('kernel', 'runmem')
g.edge('sleep', 'swap')
g.edge('swap', 'runswap')
g.edge('runswap', 'new')
g.edge('runswap', 'runmem')
g.edge('new', 'runmem')
g.edge('sleep', 'runmem')

g.render('test-output/process.gv', view=True)
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
