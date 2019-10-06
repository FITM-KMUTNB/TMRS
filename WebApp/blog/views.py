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

get_distance = None
get_path = None
get_hop = None 
current_centroid = None

def neighbor(request):
    global get_distance
    global get_path
    global get_hop
    global current_centroid
    if request.method == 'GET':
        centroid = request.GET.get('centroid')
       
        if '"' in centroid:
            centroid = centroid.strip('"')

        hop = request.GET.get('hop')
        print("Recieve : ", centroid)

        if not get_distance or current_centroid != centroid:
            current_centroid = centroid
            print("compute : graph")
            get_distance, get_path, get_hop = ts.disease_related(Cooccs, centroid)
            
        if centroid and not hop or int(hop) == 1:
            print("compute : first hop")
            
            node = [] # [{'name':node1}, {'name':node2}]
            link = [] # [{'source':index_n, 'target':index_n}, ..]
            color = dict()
            node_index = dict() # node index number.
            end_point = [] 
            index = 0
            limit_disease = 10
            disease_count = 0
            # iterate node sorted by distance. and store node member within hop 
            # and have end point is disease or symptom.
            for n in get_distance:
                
                
                # centroid or initial node.
                if n == centroid:
                    node.append({'name':centroid, 'size':20})
                    node_index[centroid] = index
                    color[centroid] = 'Red'
                    index += 1
                    print(n, ':', Cooccs.node[n]['occur'])
                # related to centroid.
                elif get_hop[n] <= 2:
                    
                    # if end node is disease or symptom.
                    if Cooccs.node[n]['tag'] == 'DS' or Cooccs.node[n]['tag'] == 'ST':
                        print(n, ':', Cooccs.node[n]['occur'])
                        end_point.append(n)
                        # store node in this path.
                        for p in get_path[n]:
                            
                            if p not in node_index:
                                node_fre = Cooccs.node[p]['occur']
                                node_size = 0
                                if node_fre <= 100:
                                    node_size = 10
                                elif node_fre > 100 and node_fre <= 500:
                                    node_size = 15
                                elif node_fre > 500:
                                    node_size = 20
                                node.append({'name':p, 'size':node_size})
                                node_index[p] = index
                                index += 1

                                #node color
                                if Cooccs.node[p]['tag'] == 'DS':
                                    color[p] = 'Red'
                                elif Cooccs.node[p]['tag'] == 'ST':
                                    color[p] = 'GreenYellow'
                                else:
                                    color[p] = '#0061ff'
                                                        

                        if Cooccs.node[n]['tag'] == 'DS':
                            disease_count += 1 # disease count
                        if disease_count == limit_disease:
                            break
            index = 0
            node_index = dict() # node index number.
            end_point = [] 
            node2 = []
            for n in node:
                if n['name'] == centroid:
                    node2.append(n)
                    node_index[n['name']] = index
                    index += 1
                elif get_hop[n['name']] == 1:
                    end_point.append(n['name'])
                    node2.append(n)
                    node_index[n['name']] = index
                    index += 1

            # create link from initial to end point.
            print("End point :", end_point)
            for p in end_point:
                
                print(get_path[p])
                link_cost = get_distance[p]
                print(link_cost)
                for sp in range(len(get_path[p])):
                    # path to end point
                    temp_link = dict()
                    if sp+1 >= len(get_path[p]) or sp+1 >= 2:
                        break
                    
                    temp_link['source'] = node_index[get_path[p][sp]]
                    temp_link['target'] = node_index[get_path[p][sp+1]]

                    
                    init_scale = 5 * 2
                    if link_cost <= init_scale:
                        temp_link['weight'] = 6
                    elif link_cost > init_scale and link_cost <= init_scale + 5:
                        temp_link['weight'] = 3
                    elif link_cost > init_scale + 5:
                        temp_link['weight'] = 1
                    if temp_link not in link:
                        link.append(temp_link)

         
            context = dict()
            context['my_centroid'] = json.dumps(centroid)
            context['my_node'] = json.dumps(node2)
            context['my_link'] = json.dumps(link)
            context['my_color'] = json.dumps(color)
            return render(request, 'blog/neighbors.html', context)
            
        if centroid and hop and int(hop) > 1:
            print("compute : ", hop," hop")
            node = [] # [{'name':node1}, {'name':node2}]
            link = [] # [{'source':index_n, 'target':index_n}, ..]
            color = dict()
            node_index = dict() # node index number.
            end_point = [] 
            index = 0
            limit_disease = 5 * int(hop)
            disease_count = 0
            # iterate node sorted by distance. and store node member within hop 
            # and have end point is disease or symptom.
            for n in get_distance:
                
                
                # centroid or initial node.
                if n == centroid:
                    node.append({'name':centroid, 'size':20})
                    node_index[centroid] = index
                    color[centroid] = 'Red'
                    index += 1
                    print(n, ':', Cooccs.node[n]['occur'])
                # related to centroid.
                elif get_hop[n] <= int(hop):
                    
                    # if end node is disease or symptom.
                    if Cooccs.node[n]['tag'] == 'DS' or Cooccs.node[n]['tag'] == 'ST':
                        print(n, ':', Cooccs.node[n]['occur'])
                        end_point.append(n)
                        # store node in this path.
                        for p in get_path[n]:
                            
                            if p not in node_index:
                                node_fre = Cooccs.node[p]['occur']
                                node_size = 0
                                if node_fre <= 100:
                                    node_size = 10
                                elif node_fre > 100 and node_fre <= 500:
                                    node_size = 15
                                elif node_fre > 500:
                                    node_size = 20
                                node.append({'name':p, 'size':node_size})
                                node_index[p] = index
                                index += 1

                                #node color
                                if Cooccs.node[p]['tag'] == 'DS':
                                    color[p] = 'Red'
                                elif Cooccs.node[p]['tag'] == 'ST':
                                    color[p] = 'GreenYellow'
                                else:
                                    color[p] = '#0061ff'
                                                        

                        if Cooccs.node[n]['tag'] == 'DS':
                            disease_count += 1 # disease count
                        if disease_count == limit_disease:
                            break


            # create link from initial to end point.
            print("End point :", end_point)
            for p in end_point:
                
                print(get_path[p])
                link_cost = get_distance[p]
                print(link_cost)
                for sp in range(len(get_path[p])):
                    # path to end point
                    temp_link = dict()
                    if sp+1 >= len(get_path[p]):
                        break
                    
                    temp_link['source'] = node_index[get_path[p][sp]]
                    temp_link['target'] = node_index[get_path[p][sp+1]]

                    
                    init_scale = 5 * 2
                    if link_cost <= init_scale:
                        temp_link['weight'] = 6
                    elif link_cost > init_scale and link_cost <= init_scale + 5:
                        temp_link['weight'] = 3
                    elif link_cost > init_scale + 5:
                        temp_link['weight'] = 1
                    if temp_link not in link:
                        link.append(temp_link)
            
            context = dict()
            context['my_centroid'] = json.dumps(centroid)
            context['my_node'] = json.dumps(node)
            context['my_link'] = json.dumps(link)
            context['my_color'] = json.dumps(color)
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