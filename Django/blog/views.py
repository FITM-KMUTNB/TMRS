from django.views.generic import TemplateView
from django.shortcuts import render
import networkx as nx
import sys
sys.path.append('..')
import Tmrs as ts
import os
from django.template.defaulttags import register
import json
import plotly.graph_objs as go
import plotly.offline as opy
import random

Cooccs = None
keywords = None
first_centorid = None
class HomeView(TemplateView):
    template_name = 'blog/home.html'
    
    def post(self, request):
        global first_centorid
        global keywords
        #Get keyword from webpage
        query = request.POST.get("query")
       
        print("Receive : "+query)
        query = checkgraphnode(Cooccs, query)
        keywords = query
        #Find disease that proximity to keywords
        disease, centroid, hop = ts.disease(Cooccs, query)
        document = ts.disease_document(Cooccs, disease)
      
        #Limit five value in dictionary
        top5disease = {k: disease[k] for k in list(disease.keys())[:10]}
        first_centorid = list(top5disease)[0]
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

def show_graph_sc(request):
    if request.method == 'GET':
        centroid = first_centorid
        nb = dict()
        path = {}
        node = []
        node_id = dict()
        link = []
        color = dict()
        temp_nodeid = dict()
        id = 0
        distance, symptom = nx.single_source_dijkstra(Cooccs, centroid, weight='cost')
     
        # Add node [{'name':'node1'},{'name':'node2'}]
        for n in symptom:
            if n in keywords:
                path[n] = symptom[n]
                for sn in path[n]:
                    temp_node = dict()
                    temp_node['name'] = sn
                    node_fre = Cooccs.node[sn]['occur']
                    node_size = 0
                    if node_fre <= 100:
                        node_size = 10
                    elif node_fre > 100 and node_fre <= 500:
                        node_size = 15
                    elif node_fre > 500:
                        node_size = 20
                    temp_node['size'] = node_size
                    if temp_node not in node:
                        
                        node.append(temp_node)
                        node_id[sn] = id
                        temp_nodeid[sn] = id
                        id += 1

                        if Cooccs.node[sn]['tag'] == 'DS' or sn == centroid:
                            color[sn] = 'Red'
                        elif Cooccs.node[sn]['tag'] == 'ST':
                            color[sn] = 'GreenYellow'
                        else:
                            color[sn] = '#0061ff'
       
       
   
        # Add link [{'source':0, 'target':1}, {'source':1, 'target':2}]
        for p in path:
            for sp in range(len(path[p])):
                if sp + 1 >= len(path[p]):
                    break

                temp_link = dict()
                temp_link['source'] = node_id[path[p][sp]]
                temp_link['target'] = node_id[path[p][sp+1]]

                link_cost = Cooccs[path[p][sp]][path[p][sp+1]]['cost']
                init_scale = 5 * 2
                if link_cost <= init_scale:
                    temp_link['weight'] = 6
                elif link_cost > init_scale and link_cost <= init_scale + 5:
                    temp_link['weight'] = 3
                elif link_cost > init_scale + 5:
                    temp_link['weight'] = 1
                if temp_link not in link:
                    link.append(temp_link)

        for sn in temp_nodeid:                
            distance, node_connected = nx.single_source_dijkstra(Cooccs, sn, weight='cost')
          
            blue_count = 0
            dt_lim = 10
            dt_no = 0
            for np in distance:
            
                if len(node_connected[np]) < 2:
                    continue
                seconde = node_connected[np][1]
                
                if sn == centroid:
                    
                    if len(node_connected[np]) > 3:
                        continue
                    if Cooccs.node[np]['tag'] == 'DS':
                        if np not in node_id:
                            dt_no += 1
                    for subn in range(len(node_connected[np])):
                        mem_ct = node_connected[np][subn]
                        if Cooccs.node[np]['tag'] == 'DS' and dt_no <= dt_lim:
                            
                            if subn + 1 >= len(node_connected[np]):
                                break
                            
                          
                            if mem_ct not in node_id:
                                
                                #source node
                                temp_node = dict()
                                temp_node['name'] = mem_ct
                                node_fre = Cooccs.node[mem_ct]['occur']
                                node_size = 0
                                if node_fre <= 100:
                                    node_size = 10
                                elif node_fre > 100 and node_fre <= 500:
                                    node_size = 15
                                elif node_fre > 500:
                                    node_size = 20
                                temp_node['size'] = node_size
                                
                                node.append(temp_node)
                                node_id[mem_ct] = id
                                id += 1

                                if Cooccs.node[mem_ct]['tag'] == 'DS':
                                    color[mem_ct] = 'Red'
                                elif Cooccs.node[mem_ct]['tag'] == 'ST':
                                    color[mem_ct] = 'GreenYellow'
                                else:
                                    color[mem_ct] = '#0061ff'

                            #target node
                            nex_ct = node_connected[np][subn+1]
                            if nex_ct not in node_id:
                                temp_node = dict()
                                temp_node['name'] = nex_ct
                                node_fre = Cooccs.node[nex_ct]['occur']
                                node_size = 0
                                if node_fre <= 100:
                                    node_size = 10
                                elif node_fre > 100 and node_fre <= 500:
                                    node_size = 15
                                elif node_fre > 500:
                                    node_size = 20
                                temp_node['size'] = node_size
                                
                                node.append(temp_node)
                                node_id[nex_ct] = id
                                id += 1

                                if Cooccs.node[nex_ct]['tag'] == 'DS':
                                    color[nex_ct] = 'Red'
                                elif Cooccs.node[nex_ct]['tag'] == 'ST':
                                    color[nex_ct] = 'GreenYellow'
                                else:
                                    color[nex_ct] = '#0061ff'

                            temp_path = []
                            temp_path = [mem_ct, nex_ct]
                            path[nex_ct] = temp_path

                        if Cooccs.node[np]['tag'] == 'ST':
                            if subn + 1 >= len(node_connected[np]):
                                break
                            
                            if mem_ct not in node_id:
                                
                                #source node
                                temp_node = dict()
                                temp_node['name'] = mem_ct
                                node_fre = Cooccs.node[mem_ct]['occur']
                                node_size = 0
                                if node_fre <= 100:
                                    node_size = 10
                                elif node_fre > 100 and node_fre <= 500:
                                    node_size = 15
                                elif node_fre > 500:
                                    node_size = 20
                                temp_node['size'] = node_size
                                
                                node.append(temp_node)
                                node_id[mem_ct] = id
                                id += 1

                                if Cooccs.node[mem_ct]['tag'] == 'DS':
                                    color[mem_ct] = 'Red'
                                elif Cooccs.node[mem_ct]['tag'] == 'ST':
                                    color[mem_ct] = 'GreenYellow'
                                else:
                                    color[mem_ct] = '#0061ff'

                            #target node
                            nex_ct = node_connected[np][subn+1]
                            if nex_ct not in node_id:
                                temp_node = dict()
                                temp_node['name'] = nex_ct
                                node_fre = Cooccs.node[nex_ct]['occur']
                                node_size = 0
                                if node_fre <= 100:
                                    node_size = 10
                                elif node_fre > 100 and node_fre <= 500:
                                    node_size = 15
                                elif node_fre > 500:
                                    node_size = 20
                                temp_node['size'] = node_size
                                
                                node.append(temp_node)
                                node_id[nex_ct] = id
                                id += 1

                                if Cooccs.node[nex_ct]['tag'] == 'DS':
                                    color[nex_ct] = 'Red'
                                elif Cooccs.node[nex_ct]['tag'] == 'ST':
                                    color[nex_ct] = 'GreenYellow'
                                else:
                                    color[nex_ct] = '#0061ff'

                            temp_path = []
                            temp_path = [mem_ct, nex_ct]
                            path[nex_ct] = temp_path
                            

                else:
                    if seconde not in node_id:
                        
                        if Cooccs.node[seconde]['tag'] == 'DS' or Cooccs.node[seconde]['tag'] == 'ST':
                            
                            temp_path = []
                            temp_path = [sn, seconde]
                            path[seconde] = temp_path
                            temp_node = dict()
                            temp_node['name'] = seconde
                            node_fre = Cooccs.node[seconde]['occur']
                            node_size = 0
                            if node_fre <= 100:
                                node_size = 10
                            elif node_fre > 100 and node_fre <= 500:
                                node_size = 15
                            elif node_fre > 500:
                                node_size = 20
                            temp_node['size'] = node_size
                            
                            node.append(temp_node)
                            node_id[seconde] = id
                            id += 1

                            if Cooccs.node[seconde]['tag'] == 'DS':
                                color[seconde] = 'Red'
                            elif Cooccs.node[seconde]['tag'] == 'ST':
                                color[seconde] = 'GreenYellow'
                            else:
                                color[seconde] = '#0061ff'

                        if Cooccs.node[seconde]['tag'] == 'NN' and blue_count != 3:
                            temp_path = []
                            temp_path = [sn, seconde]
                            path[seconde] = temp_path
                            temp_node = dict()
                            temp_node['name'] = seconde
                            node_fre = Cooccs.node[seconde]['occur']
                            node_size = 0
                            if node_fre <= 100:
                                node_size = 10
                            elif node_fre > 100 and node_fre <= 500:
                                node_size = 15
                            elif node_fre > 500:
                                node_size = 20
                            temp_node['size'] = node_size
                        
                            node.append(temp_node)
                            node_id[seconde] = id
                            id += 1
                            blue_count += 1

                            color[seconde] = '#0061ff'
                
    
        # Add link. [{'source':0, 'target':1}, {'source':1, 'target':2}]
        for p in path:
            for sp in range(len(path[p])):
                if sp + 1 >= len(path[p]):
                    break

                temp_link = dict()
                temp_link['source'] = node_id[path[p][sp]]
                temp_link['target'] = node_id[path[p][sp+1]]

                link_cost = Cooccs[path[p][sp]][path[p][sp+1]]['cost']
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
        context['keywords'] = json.dumps(keywords)
        context['my_node'] = json.dumps(node)
        context['my_link'] = json.dumps(link)
        context['my_color'] = json.dumps(color)
        return render(request, 'blog/graph.html', context)

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
                    if Cooccs.node[n]['tag'] == 'DS' and disease_count < limit_disease:
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
                    
                    if Cooccs.node[n]['tag'] == 'ST':
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
                    if Cooccs.node[n]['tag'] == 'DS' and disease_count < limit_disease:
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
                    
                    if Cooccs.node[n]['tag'] == 'ST':
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

            for n in get_distance:
                # centroid or initial node.
                if n == centroid:
                    pass
                # related to centroid.
                elif get_hop[n] <= int(hop):
                    # if end node is disease or symptom.
                    if n in keywords and n not in end_point:
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

def d3neighbor(request):
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
                    color[centroid] = '#ee2727'#red
                    index += 1
                    #print(n, ':', Cooccs.node[n]['occur'])
                # related to centroid.
                elif get_hop[n] <= 2:
                    
                    # if end node is disease or symptom.
                    if Cooccs.node[n]['tag'] == 'DS' or Cooccs.node[n]['tag'] == 'ST':
                        #print(n, ':', Cooccs.node[n]['occur'])
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
                                    color[p] = '#f7ff00'#yellow
                                else:
                                    color[p] = '#0061ff'#blue
                                                        

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
            #print("End point :", end_point)
            for p in end_point:
                
                #print(get_path[p])
                link_cost = get_distance[p]
                #print(link_cost)
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
            context['my_centroid'] = centroid
            context['graph'] = plot_3dgraph(node2, link, color, centroid)
            return render(request, 'blog/d3graph.html', context)
            
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
                    color[centroid] = '#ee2727'
                    index += 1
                    #print(n, ':', Cooccs.node[n]['occur'])
                # related to centroid.
                elif get_hop[n] <= int(hop):
                    
                    # if end node is disease or symptom.
                    if Cooccs.node[n]['tag'] == 'DS' or Cooccs.node[n]['tag'] == 'ST':
                        #print(n, ':', Cooccs.node[n]['occur'])
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
                                    color[p] = '#ee2727'
                                elif Cooccs.node[p]['tag'] == 'ST':
                                    color[p] = '#f7ff00'
                                else:
                                    color[p] = '#0061ff'
                                                        

                        if Cooccs.node[n]['tag'] == 'DS':
                            disease_count += 1 # disease count
                        if disease_count == limit_disease:
                            break


            # create link from initial to end point.
            #print("End point :", end_point)
            for p in end_point:
                
                print(get_path[p])
                link_cost = get_distance[p]
                #print(link_cost)
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
            context['my_centroid'] = centroid
            context['graph'] = plot_3dgraph(node, link, color, centroid)
            return render(request, 'blog/d3graph.html', context)
        else:
            return render(request, 'blog/home.html')


def plot_3dgraph(node, link, color, centroid):
    node_pos = {}
    node_size = []
    node_color = []
    name = []
    x_node = []
    y_node = []
    z_node = []
    
    for n in node:
        coordinate = []
        name.append(n['name'])
        node_size.append(n['size']*2)
        node_color.append(color[n['name']])
        for i in range(3):
            randnum = random.randint(10, 800)
            coordinate.append(randnum)

        node_pos[n['name']] = coordinate
        x_node.append(coordinate[0])
        y_node.append(coordinate[1])
        z_node.append(coordinate[2])

    x_link = []
    y_link = []
    z_link = []
    link_size = []
  
    for p in link:
        source_name = node[p['source']]['name']
        target_name = node[p['target']]['name']
        x = [node_pos[source_name][0], node_pos[target_name][0], None]
        y = [node_pos[source_name][1], node_pos[target_name][1], None]
        z = [node_pos[source_name][2], node_pos[target_name][2], None]
        x_link.append(x)
        y_link.append(y)
        z_link.append(z)
        link_size.append(p['weight'])
  
     
    print(x_link)
    print(y_link)
    print(z_link)
    traces={}
    for i in range(0, len(x_link)):
        traces['trace_' + str(i)]=go.Scatter3d(x = x_link[i], 
                                            y = y_link[i],
                                            z = z_link[i],
                                            mode='lines',
                                            line=dict(color='#0061ff',width=link_size[i]))
   
    traces['node']= go.Scatter3d(
                x = x_node, y = y_node,
                z = z_node,
                mode='markers+text',
                marker=dict(symbol='circle',
                size=node_size,
                color= node_color
                
                ),
                text=name,
                textposition="top center",
                hoverinfo='text'
            )
    
    axis=dict(
                showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    layout = go.Layout(
                title=centroid,
                width=1300,
                height=600,
                showlegend=False,
                scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
                ),
                margin=dict(
                    t=100
                ),
                hovermode='closest',
                )
    data=list(traces.values())
  
    fig = go.Figure(data = data, layout=layout)

    return opy.plot(fig, auto_open=False, output_type='div')


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