from cgitb import html

from numpy import append
from lexer import token, tag

from typing import Tuple, List
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

    def __repr__(self) -> str:
        return self.name


class intType(simpleStatement):
    def __init__(self, name = None):
        self.name:str = name
        self.value:int

    def __str__(self) -> int:
        return self.value

    def set(self, value:int):
        self.value = value

    def get(self):
        return self.value

class boolType(simpleStatement):
    def __init__(self, name = None):
        self.name:str = name
        self.value:bool

    def __str__(self) -> bool:
        return self.value

    def set(self, value:bool):
        self.value = value

    def get(self):
        return self.value

class strType(simpleStatement):
    def __init__(self, name = None):
        self.name:str = name
        self.value:str

    def __str__(self) -> str:
        return self.value

    def set(self, value:str):
        self.value = value

    def get(self):
        return self.value


#<body>
class declerationList(simpleStatement):
    def __init__(self):
        self.functions:List[function] = []
        self.mainFunction:List[simpleStatement] = []
        
    def __str__(self) -> str:
        return self.functions, self.mainFunction

#<section>
class function(simpleStatement):
    def __init__(self):
        self.functionName:str
        self.returnType:simpleStatement
        self.parameters = []
        self.body = []

    def __str__(self) -> str:
        return self.functionName

class ifStatement(simpleStatement):
    def __init__(self):
        self.condition = []
        self.ifBody = []
        self.elseBody = []

class operator(simpleStatement):
    def __init__(self, left, right):
        self.leftSide = left
        self.rightSide = right

def parser(tokenTree: tag):
    if len(tokenTree.children) != 1:
        print("tokenTree empty")
        return
    
    AST = declerationList()
    htmlTag = tokenTree.children[0]
    if htmlTag.name != "html" or len(htmlTag.children) != 2:
        return None

    childrenStringList = list(map(lambda x: x.name, htmlTag.children) )
    bodyIndex = indexNoError(childrenStringList, "body")
    #higher order function | hogere order functie
    AST.functions = list(map(parseFunction, htmlTag.children[bodyIndex].children))
    
    #todo: main functie ook parsen
    mainIndex = indexNoError(childrenStringList, "main")

    return AST

#geeft de index van een item in een list, geeft -1 als item niet in list
def indexNoError(lst:list, item:str, start:int = 0)->int:
    try:
        index = lst.index(item, start)
        return index
    except ValueError:
        index = -1
        return index

#geeft alle indexen van een item in een lijst, geeft lege lijst terug als item niet in lijst
#lst = lijst om in te zoeken, item = wat je wil zoeken, indexlist = return, start = 
def indexAllNoError(lst:list, item:str, indexLst:list = [], start:int = 0)->list:
    index = indexNoError(lst, item, start)
    if index == -1:
        return indexLst
    indexLst.append(index)
    return indexAllNoError(lst, item, indexLst, index+1)

def parseParameter(parameter:tag)->simpleStatement:
    if parameter.name == "mark":
        #higher order function | hogere order functie
        childrenStringList = list(map(lambda x: x.name, parameter.children) )
        nameIndex = indexNoError(childrenStringList, "h2")
        typeIndex = indexNoError(childrenStringList, "h3")

        #de returntype zoals in de html file
        returnTypeStr = parameter.children[typeIndex].codeBlock[0].name
        if returnTypeStr == "int":
            return intType(parameter.children[nameIndex].codeBlock[0].name)
        if returnTypeStr == "bool":
            return boolType(parameter.children[nameIndex].codeBlock[0].name)
        if returnTypeStr == "str" or returnTypeStr == "string":
            return strType(parameter.children[nameIndex].codeBlock[0].name)

def parseIfStatement(ifCode:tag):
    conditionIndex = indexNoError(ifCode.children, "i")
    #ifElseBody[0] = if body, ifElseBody[1] = else body
    ifElseBody = indexAllNoError(ifCode.children, "figure")
    
    return

def parseFuncBody(funcBody:tag)->List[simpleStatement]:
    stringNameList = list(map(lambda x: x.name, funcBody.children))
    #article is een if statement
    ifIndexList = indexAllNoError(stringNameList, "article")
    ifstatements = list(map(lambda index: parseIfStatement(funcBody.children[index]), ifIndexList) )
    
    return

def parseFunction(functionTag:tag)->function:
    if functionTag.name != "section":
        #geen function
        return None
    
    newFunction = function()

    tagChildrenStringList = list(map(lambda x: x.name, functionTag.children) )
    nameIndex = indexNoError(tagChildrenStringList, "h2")
    newFunction.name = functionTag.children[nameIndex].codeBlock[0].name

    returnIndex = indexNoError(tagChildrenStringList, "h3")
    #de returntype zoals in de html file
    returnTypeStr = functionTag.children[returnIndex].codeBlock[0].name
    if returnTypeStr == "int":
        newFunction.returnType = intType()
    if returnTypeStr == "bool":
        newFunction.returnType = boolType()
    if returnTypeStr == "str" or returnTypeStr == "string":
        newFunction.returnType = strType()

    newFunction.parameters = list(filter(None, map(parseParameter, functionTag.children) ))



    funcBodyIndex = indexNoError(functionTag.children, "figure")
    newFunction.body = parseFuncBody(functionTag.children[funcBodyIndex])
    return newFunction