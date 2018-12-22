

import re
from py2neo import Graph,Node,Relationship, NodeSelector
import pandas as pd

lines = []
with open("./glossary.dat", encoding="gbk") as file:
    lines = file.readlines()
errfile =  open("./error.txt", 'a+', encoding = 'utf8') 



graph = Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="123456"
)

selector = NodeSelector(graph)
li = []
regx = re.compile(r"(.*?)(\w+\|\w+)(.*)")


for i,value in enumerate(lines) :

    tx = graph.begin()

    triple = value.split()
    #create new phrase: id, name
    try:
        p = Node("phrase", id = i, name = triple[0])
        tx.create(p)
        # create relation : r_gx -> G_X : eg. NUM V ADJ
        gx = selector.select('G_X', value = triple[1]).first()
        tx.create( Relationship(p,"r_gx",gx) )
    except Exception as e:
        print(str(e), "can't find gx ", triple, file = errfile)
        continue
   
    
    for j in triple[2].split(","):
        try:
            tmp_3 = regx.match(j)
            relation = tmp_3.group(1) + tmp_3.group(3)
            ele_name = tmp_3.group(2)
            #create relation : explain {value = '*$&#'}
            ele = selector.select('ele_word', name = ele_name).first()
            if ele is None: 
                print("not find ele_word", ele_name)
                li.append("not find ele_word: which name is "+ ele_name)
                # print("not find ele_word: which name is "+ ele_name, file = errfile)
                continue;
            tx.create( Relationship(p, ("explain", {'value' : relation}), ele) )
            #value 之前移交给in定义过了，
            
        except AttributeError:
            li.append(value)
            print(value, file = errfile)

    tx.commit();
print("========================================================")
print(li)

