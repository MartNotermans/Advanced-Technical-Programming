from parsmer import *
from lexer import *
from runner import *

testList = ['a', 'b', 'c', 'd', 'e']
print(indexNoError(testList, 'b', 0))

#with open("smollTest.html", "r") as f:   
#with open("test.html", "r") as f: 
#with open("test - no input.html", "r") as f:
with open("temptest.html", "r") as f: 
    file = f.read()


tokenTree = lexer(file)
#tokenTree.printTree()


AST = parser(tokenTree)
#AST.__str__
# print(str(AST) )

runner(AST)
print("done")