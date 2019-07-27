from py2neo import Graph,Node, NodeMatcher
graph = Graph(password = "tmrs_1234")
matcher = NodeMatcher(graph)
result = matcher.match("SINGLE_NODE", name="KEY")
a = Node("SINGLE_NODE", name="KEY")


for rel in matcher.match("SINGLE_NODE"):
    print(rel)
    print("name:", rel["name"])
    print("occur:", rel["occur"])
    print("pos:", rel["pos"])

def node_id(node):

    return None
#print(graph.nodes[124]) #fetch by id
