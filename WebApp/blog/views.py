from django.views.generic import TemplateView
from django.shortcuts import render
import networkx as nx
import sys
sys.path.append('..')
from time import time, strftime, localtime
from datetime import timedelta
import DiseaseCentroid as dc
import os
from django.template.defaulttags import register
Cooccs = None

class HomeView(TemplateView):
    template_name = 'blog/home.html'
    
    def post(self, request):
        #Get keyword from webpage
        query = request.POST.get("query")
        start = time()
        print("Receive : "+query)
        query = checkgraphnode(Cooccs, query)
        #Find disease that proximity to keywords
        disease, centroid, diseasehop = dc.disease(Cooccs, query)
        document = dc.diseasedocument(Cooccs, disease)
        end = time()
        xtime = end - start
        print('Processing Time:', secondsToStr(xtime)) 
        #Limit five value in dictionary
        top5disease = {k: disease[k] for k in list(disease.keys())[:10]}
        context = {'symptom' : query, 'disease' : top5disease, 'diseasehop' : diseasehop, 'centroid' : centroid, 'document' : document}
        return render(request, self.template_name, context)
  

def ReadGraph():
    global Cooccs
    #Read graph from gpickle format
    Cooccs = nx.read_gpickle("../Database/Pickle/221clean.gpickle")
    #Display graph information
    print(nx.info(Cooccs))

def checkgraphnode(G, keywords):
    keywords = keywords.split()
    node = []
    for word in keywords:
        if G.has_node(word):
            node.append(word)
    return node
#For get key value of dictionary
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    
#For if in list condition
@register.filter
def is_in(var, obj):
    return var in obj

#Covert Time from second to HH.MM.SS format
def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed)) 
            
ReadGraph()