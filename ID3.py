# -*- coding: utf-8 -*-
from __future__ import division
from copy import deepcopy
import math
import sys
import graphviz as gv
g2 = gv.Digraph(format='png')
 #Input1
 gpu=["NVIDIA", 'Radeon', 'Don\'t care', 'NVIDIA', 'Radeon', 'Radeon', 'Radeon', 'Radeon', 'Don\'t care', 'NVIDIA', 'NVIDIA', 'NVIDIA']
 cpu=['Intel' ,'Intel' ,'AMD' ,'Intel' ,'Intel' ,'Intel' ,'AMD' ,'AMD' ,'AMD' ,'Intel' ,'AMD' ,'AMD']
 os=['ChromeOS', 'Linux', 'Windows', 'MS DOS', 'Windows', 'MS DOS', 'Windows', 'Linux', 'ChromeOS', 'Linux', 'ChromeOS', 'Windows']
 des=['N','Y','Y','N','Y','N','N','Y','N','Y','Y','N']
 parent={'GPU':gpu,"CPU":cpu,"OS":os,"DES":des}

#Input2
#outlook=["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny", "Rain", "Sunny", "Overcast", "Overcast", "Rain"]
#temp=["Hot","Hot","Hot","Mild","Cool","Cool","Cool","Mild","Cool","Mild","Mild","Mild","Hot","Mild"]
#hum=["High","High","High","High","Normal","Normal","Normal","High","Normal","Normal","Normal","High","Normal","High"]
#Wind=["Weak","Strong","Weak","Weak","Weak","Strong","Strong","Weak","Weak","Weak","Strong","Strong","Weak","Strong"]
#des=["No","No","Yes","Yes","Yes","No","Yes","No","Yes","Yes","Yes","Yes","Yes","No"]
#parent={"Outlook":outlook,"Temprature":temp,"Humidity":hum,"Wind":Wind,"DES":des}

graphcounter={}
for k,v in parent.iteritems():
    graphcounter[k]=0
def indcount(pa,arr,inst):
    p = 0
    n = 0
    for j in range(len(arr)):
        if arr[j] == inst and (pa["DES"][j] == 'Y' or pa["DES"][j] == 'Yes'):
            p += 1
        if arr[j] == inst and (pa["DES"][j] == 'N' or pa["DES"][j] == 'No'):
            n += 1
    return p,n

def count(pa,arr):
    data={}
    tempset=set(arr)
    for i in tempset:
        p,n=indcount(pa,arr,i)
        data[i]=[p,n]
    return data



def split(pa,at,inst):
    temppa =deepcopy(pa)
    arr=temppa[at]
    del temppa[at]
    for k,v in temppa.iteritems():
        temppa[k]=[]
    for i in range(len(arr)):
        if arr[i]==inst:
            for k,v in temppa.iteritems():
                temppa[k].append(pa[k][i])

    return temppa

def indentropy(v):
    total = v[0] + v[1]
    s1 = v[0] / total
    s2 = v[1] / total
    if s1 != 0:
        s1 = s1 * math.log(s1, 2)
    if s2 != 0:
        s2 = (s2) * math.log(s2, 2)
    val = s1 + s2
    val *= -1
    return val

def entropy(data):
    ans=0
    totalitems=0
    for k,v in data.iteritems():
        totalitems+=v[0]+v[1]
    for k, v in data.iteritems():
        total = v[0] + v[1]
        val=indentropy(v)
        ans+=(total/totalitems)*val
    return ans


def recur(pa,paentropy,panode=None,paedge=None):
    # print pa
    if paentropy==0:

        g2.node("DES"+str(graphcounter["DES"]),pa["DES"][0])
        g2.edge((panode),"DES"+str(graphcounter["DES"]),paedge)
        graphcounter["DES"]+=1
        return
    maxgain=-sys.maxint
    maxattr=''
    for k,v in pa.iteritems():
        if k!="DES":
            temp=count(pa,v)
            # print temp
            tempE=entropy(temp)

            if maxgain<(paentropy-tempE):
                maxgain=paentropy-tempE
                maxattr=k
    print paentropy
    print paedge
    print pa
    print maxgain
    print maxattr
    instances=set(pa[maxattr])
    g2.node(maxattr+str(graphcounter[maxattr]),maxattr)

    if panode!=None:
        g2.edge((panode),maxattr+str(graphcounter[maxattr]),paedge)
    graphcounter[maxattr] += 1
    for i in instances:
        newpa=split(pa,maxattr,i)
        currE=indentropy(indcount(pa,pa[maxattr],i))

        recur(newpa,currE,maxattr+str(graphcounter[maxattr]-1),i)



recur(parent,1)
g2.render('img1/g2')
print graphcounter





