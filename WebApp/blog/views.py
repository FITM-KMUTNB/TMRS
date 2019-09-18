from django.views.generic import TemplateView
from django.shortcuts import render
import networkx as nx
import sys
sys.path.append('..')
import Tmrs as ts
import os
from django.template.defaulttags import register
import json
Cooccs = None
class HomeView(TemplateView):
    template_name = 'blog/home.html'
    
    def post(self, request):
        #Get keyword from webpage
        query = request.POST.get("query")
       
        print("Receive : "+query)
        query = checkgraphnode(Cooccs, query)

        #Find disease that proximity to keywords
        disease, centroid, hop = ts.disease(Cooccs, query)
        document = ts.disease_document(Cooccs, disease)
      
        #Limit five value in dictionary
        top5disease = {k: disease[k] for k in list(disease.keys())[:10]}
        context = {'symptom' : query, 'disease' : top5disease, 'diseasehop' : hop, 'centroid' : centroid, 'document' : document}
        return render(request, self.template_name, context)

def document(request):
    if request.method=='GET':
        doc = request.GET.get('doc')
        if not doc:
            return render(request, 'blog/home.html')
        else:
           
            text_file = open('../Document/corpus221/Wiki/'+doc,'r', encoding="utf8")
           
            context = {'docname':doc, 'read':text_file.readlines()}
            return render(request, 'blog/readdoc.html', context)


def neighbor(request):
    if request.method=='GET':
        centroid = request.GET.get('centroid')
        hop = request.GET.get('hop')
      
        if centroid and not hop:
                  
            node, link = ts.disease_neighbors(Cooccs, centroid)
            context = dict()
            context['my_centroid'] = json.dumps(centroid)
            context['my_node'] = json.dumps(node)
            context['my_link'] = json.dumps(link)
            return render(request, 'blog/neighbors.html', context)

        elif centroid and hop:
            if '"' in centroid:
                centroid = centroid.strip('"')
            node, link = ts.disease_neighbors(Cooccs, centroid, int(hop))
            context = dict()
            context['my_centroid'] = json.dumps(centroid)
            context['my_node'] = json.dumps(node)
            context['my_link'] = json.dumps(link)
            return render(request, 'blog/neighbors.html', context)

        else:
            return render(request, 'blog/home.html')

def ReadGraph():
    global Cooccs
    #Read graph from gpickle format
    Cooccs = nx.read_gpickle("../Database/Pickle/221tag.gpickle")
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