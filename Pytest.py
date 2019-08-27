<<<<<<< HEAD
import operator
c_file = open("Result1000(2).txt", 'r', encoding="latin-1")
file = open("Result1000(3).txt","w") 

for c in c_file: 
        text = c.translate(str.maketrans({"'":None}))
        #print(text)     
        text2 = text.split(":") 
        print(text2[1])    
        file.write(text2[1]) 
               
        
file.close() 

c_file.close()
=======
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
>>>>>>> 417f0510f7bfa8a3a2f3974b1325d2ce84a8ba85
