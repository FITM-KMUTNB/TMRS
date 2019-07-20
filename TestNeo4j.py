from py2neo import Graph

graph = Graph(password = "tmrs_1234")
try:
    graph.run("Match () Return 1 Limit 1")
    print('Connected to database')
except Exception:
    print('Can\'t Connect to database')


results = graph.run("MATCH (n:SINGLE_NODE) where n.disease = 1 RETURN n LIMIT 25")

print("List of Disease")
for disease in results:
    shdisease = {disease}
    print(shdisease)

results = graph.run("MATCH (n:SINGLE_NODE) where n.symptom = 1 RETURN n LIMIT 25")

print("List of Symptom")
for symptom in results:
    shsymptom = {symptom}
    print(shsymptom)
