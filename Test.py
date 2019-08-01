from py2neo import Graph,Node, NodeMatcher, Relationship,RelationshipMatcher,Record
graph = Graph(password = "tmrs_2019")
matcher = NodeMatcher(graph)
relmatcher = RelationshipMatcher(graph)

count = len(open("Document/output_allWords_/2.txt.txt.s_allWords_sentences.txt").readlines())
print(count)
nodeid1 = 0
for nid in graph.run("match (n:SINGLE_NODE {name: 'KEY'}) return id(n) as NODEID"):
        nodeid1 = nid["NODEID"]
        print(nodeid1)
    
nodeid2 = 0
for nid in graph.run("match (n:SINGLE_NODE {name: 'ROOM'}) return id(n) as NODEID"):
        nodeid2 = nid["NODEID"]
        print(nodeid2)

n1 = graph.nodes[nodeid1]
n2 = graph.nodes[nodeid2]

ckrel = relmatcher.match(nodes=(n1, n2), r_type="IS_CONNECTED")
print(list(ckrel))
relfound = False
if relmatcher.match(nodes=(n2, n1), r_type="IS_CONNECTED"):
    print("Match!!")
    relfound = True
if not relfound:
    print("IN!!")

result = matcher.match("SINGLE_NODE", name="KEY")
a = Node("SINGLE_NODE", name="KEY")
print("result->", result)
print("a->", a)

"""for rel in matcher.match("SINGLE_NODE"):
    print(rel)
    print("name:", rel["name"])
    print("occur:", rel["occur"])
    print("pos:", rel["pos"])
"""
"""
num=1
VectorRow =[]
for x in range(len(matcher.match("SINGLE_NODE"))):
    VectorRow.append(num)
    print(x)
    num+=1

for i in range(len(VectorRow)):
    print("No.", i),
    print(VectorRow[i])


a = "me"
b = "me"

if not (a == b):
    print("Match")
"""

tx = graph.begin() 


create = True
if not create:
    a = Node("SINGLE_NODE", name="a") 
    tx.create(a)
    b = Node("SINGLE_NODE", name="b") 
    tx.create(b)
    c = Node("SINGLE_NODE", name="c") 
    tx.create(c)
    d = Node("SINGLE_NODE", name="d") 
    tx.create(d)
tx.commit()

    
tx = graph.begin()
rel = True
if not rel:
    nodeid1 = 0
    for nid in graph.run("match (n:SINGLE_NODE {name: 'a'}) return id(n) as NODEID"):
         nodeid1 = nid["NODEID"]
    
    nodeid2 = 0
    for nid in graph.run("match (n:SINGLE_NODE {name: 'b'}) return id(n) as NODEID"):
        nodeid2 = nid["NODEID"]
    a = graph.nodes[nodeid1]
    b = graph.nodes[nodeid2]
    ab = Relationship(a, "IS_CONNECTED", b, count=2)
    tx.create(ab)
    print("Create rel success")
tx.commit()
    
#print(graph.nodes[124]) #fetch by id



