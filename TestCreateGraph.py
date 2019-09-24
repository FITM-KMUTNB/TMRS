import Library as ct
import networkx as nx
def create_tmrs_graph():
    input_text_dir = "Document/corpus221/cleantag/"
    g_file = "Database/Pickle/221test.gpickle"
    ct.create_graph(input_text_dir, g_file)


#create_tmrs_graph()
G = nx.read_gpickle("Database/Pickle/221test.gpickle")
print(nx.info(G))
neighbor = G.neighbors('disease')

for n in neighbor:
    print('disease - ', n," : ", G['disease'][n]['cost'])

