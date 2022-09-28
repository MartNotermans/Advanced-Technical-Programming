from lexer import token, tag
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

def parser(tokenTree):
    if len(tokenTree.children) == 0:
        print("tokenTree empty")
        return
    
    AST = simpleStatement("root")
    parse(tokenTree, AST)

def parse(tokenTree : token, AST : simpleStatement, index = 0):
    ASTpiece = parserOptions( tokenTree.children[index] )
    parse(tokenTree, ASTpiece, index+1)
    AST.children.append(ASTpiece)

def parserOptions(newTag : tag) -> simpleStatement:
    tagName = newTag.name

    if tagName == "body": #declerationList
        declerations = tokenDict[tagName]()
        return declerations

    if tagName == "section": #function
        function = tokenDict[tokenList[0]][1]()
        declerationList.functions.append(function)
        tokenList = tokenList[1:]
        parseFunction(tokenList, function)

    if tagName == "article": #if statement
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