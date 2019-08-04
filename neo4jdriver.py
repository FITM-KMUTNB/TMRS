from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'tmrs_2019'))
session = driver.session()

print('Connect to database...', end="", flush=True)
try:
    session.run("Match () Return 1 Limit 1")
    print(' Success !')
except Exception:
    print(' Failed !')


def createNode(driver, props):
    Label = 'SINGLE_NODE'
    with driver.session() as session:
        return session.run("CREATE (a:"+Label+" {props}) "
                            "RETURN id(a)",  {'props':props}).single().value()
        
        
def matchNode(name):
    Label = 'SINGLE_NODE'
    try:
        return session.run("MATCH (a:"+Label+") WHERE a.name= $name " 
                            "RETURN id(a)", name=name).single().value()
    except Exception:
        return None

def setProperty(id, props):
    session.run("MATCH (a) WHERE id(a)= {id} " 
                "SET a+= {props}", {'id':id, 'props':props})
   
def setRelProperty(id, props):
    session.run("MATCH ()-[r]-() WHERE id(r)= {id} " 
                "SET r+= {props}", {'id':id, 'props':props})

def getProps(id, props):
    try:
        return session.run("MATCH (a) WHERE id(a)= {id} " 
                           "RETURN a."+props+"", {'id':id}).single().value()
    except:
        return session.run("MATCH ()-[r]-() WHERE id(r)= {id} " 
                           "RETURN r."+props+"", {'id':id}).value()[0]
    
def createRelation(n1,n2,props):
    Label = 'SINGLE_NODE'
    return session.run("MATCH (a:"+Label+"),(b:"+Label+") WHERE id(a) = {n1} AND id(b) = {n2} "
                       "CREATE (a)-[rel:IS_CONNECTED {props}]->(b) RETURN rel",  {'n1':n1,'n2':n2,'props':props}).single().value() 
def matchRelationship(n1,n2):
    Label = 'SINGLE_NODE'
    return session.run("MATCH (a:"+Label+")-[rel:IS_CONNECTED]-(b:"+Label+") WHERE id(a)= $n1 and id(b)= $n2 " 
                       "RETURN id(rel)", n1=n1,n2=n2).single().value()
                      
def findRelation(start_node):
    Label = 'SINGLE_NODE'
    return session.run("MATCH (a:"+Label+")-[rel:IS_CONNECTED]-(b:"+Label+") WHERE id(a)= $start_node " 
                       "RETURN id(b)", start_node=start_node).value()

tempRel = [1234,1423]
if 4444 not in tempRel:
    print("add")
driver.close()