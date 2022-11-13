from parsmer import *
from lexer import *
from runner import *

#with open("smollTest.html", "r") as f:   
with open("test.html", "r") as f: 
    file = f.read()


tokenTree = lexer(file)
#tokenTree.printTree()


AST = parser(tokenTree)
#AST.__str__
# print(str(AST) )

runner(AST)
print("done")