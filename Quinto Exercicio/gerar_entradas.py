# -*- coding: utf-8 -*-
# Python3 code to demonstrate  
# to compute all possible permutations 
# using list comprehension  

#create file
file_obj  = open("arguments.txt", "w+")
  
# initializing lists  
c = [1, 1.25, 1.5]
df = [0.1, 0.5, 0.9]
dimensao = [10, 20, 30, 40, 50] 
npop = [25, 50, 100]
ngen = [25, 50, 100]
  
# printing lists  
print ("A lista de parametros são: " + str(df) +
                               " " + str(c) +
                               " " + str(dimensao) + 
                               " " + str(npop) +
                               " " + str(ngen)) 
  
# using list comprehension  
# to compute all possible permutations 
res = [[i, j, k, l, m] for m in ngen
                 for i in df
                 for j in c 
                 for k in dimensao
                 for l in npop] 

  
# printing result 
#print ("All possible permutations are : " +  str(res)) 
string_form = ""
for combination in res:
    for argument in combination:
        string_form += " " + str(argument)
    string_form += "\n"

print("Todas as combinações foram escritas com sucesso!")
file_obj.write(string_form)