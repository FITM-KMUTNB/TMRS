file = open("Result.txt","w") 
r = 1
query = ["a", "b"]

result = str(r)+" : ""%s\n" % query +"\n"
file.write(result) 
r = 2
query = ["c", "d"]
result = str(r)+" : ""%s\n" % query +"\n"
file.write(str(r)+" : ""%s\n" % query +"\n") 

file.close() 