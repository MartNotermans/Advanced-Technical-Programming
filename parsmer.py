from queue import Empty
from lexer import taglist, closingTagList
import sys
sys.setrecursionlimit(200000)



class simpleStatement:
    def __init__(self, name : str):
        self.name = name #the tag as in the html file
        self.children = [] #all other tags containd in this tag
        self.parent = 0

    #moet bij alle tags
    def __str__(self) -> str:
        return self.name

#<body>
class declerationList(simpleStatement):
    def __init__(self):
        self.functions = []
        self.variables = []

    def __str__(self) -> str:
        return self.functions, self.variables

#<section>
class function(simpleStatement):
    def __init__(self):
        self.functionName = str
        self.returnType = simpleStatement
        self.parameters = []
        self.body = []

    def __str__(self) -> str:
        return self.functionName

tokenDict = dict()
tokenDict['html'] = ("file start", lambda: simpleStatement("html") )
tokenDict['body'] = ("file start", lambda: declerationList() )
tokenDict['section'] = ("file start", lambda: function() )
tokenDict['/html'] = ("file start", lambda: print("eof") )

def parser(tokenList, tree = simpleStatement):
    if len(tokenList) == 0:
        print("list empty")
        return
    
    if tokenList[0] == "html":
        tree = tokenDict[tokenList[0]][1]()
        tokenList = tokenList[1:]
        parserOptions(tokenList, tree) 
    
def parserOptions(tokenList, tree, declerationList = simpleStatement):
    if len(tokenList) == 0:
        print("list empty")
        return

    if tokenList[0] == "body": #declerationList
        declerations = tokenDict[tokenList[0]][1]()
        tree.children.append(declerations)
        tokenList = tokenList[1:]
        return parserOptions(tokenList, tree, declerations)

    if tokenList[0] == "section": #function
        function = tokenDict[tokenList[0]][1]()
        declerationList.functions.append(function)
        tokenList = tokenList[1:]
        parseFunction(tokenList, function)

    if tokenList[0] == "article": #if statement
        parseIfStatement()
    


    
def parseFunction(tokenList, function):
    start = tokenList.find("i")
    end = tokenList.find("/i")
    return

def parseIfStatement():
    return

def recurtion():
    if len(tokenList) == 0:
        return tree
    
    tree = tokenDict[tokenList[0]][1]()
    print(tree)

    tokenList = tokenList[1:]
    return parser(tokenList, tree)