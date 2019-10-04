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


def neighborold(request):
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

path = None # for neighbors
hop_distance = None
node_tag= None
neighbors_dis = None
def neighbor(request):
    global path
    global hop_distance
    global node_tag
    global neighbors_dis

    if request.method=='GET':
        centroid = request.GET.get('centroid')
        hop = request.GET.get('hop')
        
        if centroid and not hop:
                  
            path, hop_distance, node_tag, neighbors_dis = ts.disease_neighbors(Cooccs, centroid)
            hop = 1
            link = []
            temp_node = []
            node_id = dict()
            node_color = dict()
            number = 0
            

            for p in range(len(path)):
                for n in range(len(path[p])):
                    node_name = dict()
                    if path[p][n] not in node_id and hop_distance[path[p][n]] <= hop:
                        node_id[path[p][n]] = number
                        node_name['name'] = path[p][n]
                        temp_node.append(node_name)
                        number += 1

                        if node_tag[path[p][n]] == 'DS':
                            node_color[path[p][n]] = 'Red'

                        elif node_tag[path[p][n]] == 'ST':
                            node_color[path[p][n]] = 'GreenYellow '

            for p in range(len(path)):
                for n in range(len(path[p])):
                    source_target = dict()
                    if n+1 >= len(path[p]):
                        continue
                    if path[p][n] in node_id and path[p][n+1] in node_id:
                        source_target['source'] = node_id[path[p][n]]
                        source_target['target'] = node_id[path[p][n+1]]
                        if source_target not in link:
                            link.append(source_target)

            context = dict()
            context['my_centroid'] = json.dumps(centroid)
            context['my_node'] = json.dumps(temp_node)
            context['my_link'] = json.dumps(link)
            context['my_color'] = json.dumps(node_color)
            return render(request, 'blog/neighbors.html', context)

        elif centroid and hop:
            if '"' in centroid:
                centroid = centroid.strip('"')
         
            link = []
            temp_node = []
            node_id = dict()
            node_color = dict()
            number = 0

            first_n = []
            limit = 10 * int(hop)
            for nd in neighbors_dis:
                if len(first_n) >= limit:
                    break
                first_n.append(nd)

            for p in range(len(path)):
                for n in range(len(path[p])):
                    node_name = dict()
                    if path[p][n] not in node_id and hop_distance[path[p][n]] <= int(hop) and path[p][n] in first_n:
                        node_id[path[p][n]] = number
                        node_name['name'] = path[p][n]
                        temp_node.append(node_name)
                        number += 1

                    if node_tag[path[p][n]] == 'DS':
                            node_color[path[p][n]] = 'Red'

                    elif node_tag[path[p][n]] == 'ST':
                        node_color[path[p][n]] = 'GreenYellow '

            for p in range(len(path)):
                for n in range(len(path[p])):
                    source_target = dict()
                    if n+1 >= len(path[p]):
                        continue
                    if path[p][n] in node_id and path[p][n+1] in node_id:
                        source_target['source'] = node_id[path[p][n]]
                        source_target['target'] = node_id[path[p][n+1]]
                        if source_target not in link:
                            link.append(source_target)

            context = dict()
            context['my_centroid'] = json.dumps(centroid)
            context['my_node'] = json.dumps(temp_node)
            context['my_link'] = json.dumps(link)
            context['my_color'] = json.dumps(node_color)
            return render(request, 'blog/neighbors.html', context)

        else:
            return render(request, 'blog/home.html')


def show_graph(request):
    print("show graph")
    if request.method=='GET':
        node, link = ts.get_all_graph(Cooccs)
        context = dict()
        context['my_node'] = json.dumps(node)
        context['my_link'] = json.dumps(link)
        return render(request, 'blog/graph.html', context)

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