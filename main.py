from parsmer import *
from lexer import *


#with open("smollTest.html", "r") as f:   
with open("test.html", "r") as f: 
    file = f.read()

#print(file)

tokens = lexer(file)
#print (tokens)

#tokenTree = parser(tokens)