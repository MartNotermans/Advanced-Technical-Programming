from parsmer import *
from lexer import *

# tree = tag("html")
# tree.addNode("body")
# tree.addNode("section")
# tree.addNode("even")
# tree.addNode("/section")
# tree.addNode("section")
# tree.addNode("even")
# tree.addNode("/section")
# tree.addNode("/body")
# tree.addNode("/html")

# tree.printTree()

#with open("smollTest.html", "r") as f:   
with open("test.html", "r") as f: 
    file = f.read()


tokenTree = lexer(file)
print("------------")
tokenTree.printTree()
# print (tokenTree)

#AST = parser(tokens)