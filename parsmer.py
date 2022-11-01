from curses import newwin
from lexer import tag, token, operatorList
from simpleStatement import *


from typing import List
import sys
sys.setrecursionlimit(200000)


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
#intern omdat python moeilijk doet met de indexlist die altijd leeg moet zijn aan het begin
def indexAllNoErrorIntern(lst:list, item:str, indexLst:list, start:int)->list:
    index = indexNoError(lst, item, start)
    if index == -1:
        return indexLst
    indexLst.append(index)
    return indexAllNoErrorIntern(lst, item, indexLst, index+1)

def indexAllNoError(lst:list, item:str):
    indexLst = []
    start = 0
    return indexAllNoErrorIntern(lst, item, indexLst, start)


#2+3 wordt plusoperator, left:2, right:3
#2+(1+3) wordt plusoperator, left:2,right:plusoperator, left:1, right:3
def parseCodeBlock(codeblock:List[token])->simpleStatement:
    codeblockStringList = list(map(lambda x: x.name, codeblock) )
    operatorIndexList = list(filter(lambda x: x == -1, map(lambda x: operatorList.find(x), codeblockStringList)))    #mag ik hier operatorlist gebruiken??? komt van een ander bestand
    # /\ list met operator indexen


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

def parseIfStatement(ifCode:tag)->simpleStatement:
    newIfStatement = ifStatement()

    ifCodeChildrenStringList = list(map(lambda x: x.name, ifCode.children) )
    #i is condidion
    conditionIndex = indexNoError(ifCodeChildrenStringList, "i")
    #condition: list van tokens, waar onder een operator
    newIfStatement.condition = parseCodeBlock(ifCode.children[conditionIndex].codeBlock)

    #ifElseBody[0] = if body, ifElseBody[1] = else body
    ifElseBody = indexAllNoError(ifCodeChildrenStringList, "figure")
    newIfStatement.ifBody = parseFuncBody(ifCode.children[ifElseBody[0]])
    newIfStatement.elseBody = parseFuncBody(ifCode.children[ifElseBody[1]])

    return newIfStatement

def initialiseVariable(variableTag:tag)->simpleStatement:
    tagyChildrenStringList = list(map(lambda x: x.name, variableTag.children) )
    nameIndex = indexNoError(tagyChildrenStringList, "h2")
    typeIndex = indexNoError(tagyChildrenStringList, "h3")
    valueIndex = indexNoError(tagyChildrenStringList, "h4")

    returnTypeStr = variableTag.children[typeIndex].codeBlock
    if returnTypeStr == "int":
        newVariable = intType()
    if returnTypeStr == "bool":
        newVariable = boolType()
    if returnTypeStr == "str" or returnTypeStr == "string":
        newVariable = strType()

    #moet codeblock parsen
    newVariable.name = variableTag.children[nameIndex].codeBlock
    if variableTag.children[valueIndex].codeBlock != -1:
        newVariable.value = variableTag.children[valueIndex].codeBlock
    return newVariable



def parseTagInFuncBody(tagy:tag)->simpleStatement:
    if tagy.name == "nav": #return
        pass
    elif tagy.name == "article": #if
        return parseIfStatement(tagy)
    elif tagy.name == "ins": #initialise
        return initialiseVariable(tagy)
    elif tagy.name == "summary": #functie aanroepen
        pass
    elif tagy.name == "footer": #while
        whileChildrenStringList = list(map(lambda x: x.name, tagy.children) )
        conditionIndex = indexNoError(whileChildrenStringList, "i")
        bodyIndex = indexNoError(whileChildrenStringList, "figure")
        newWhile = whileLoop()
        newWhile.condition = parseCodeBlock(tagy.children[conditionIndex].codeBlock)
        newWhile.loop = parseFuncBody(tagy.children[bodyIndex])
        return newWhile

#parse the body of a function, if statement or while loop
def parseFuncBody(funcBody:tag)->List[simpleStatement]:
    return list(map(parseTagInFuncBody, funcBody.children))

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


    functionTagChildrenStringList = list(map(lambda x: x.name, functionTag.children) )
    funcBodyIndex = indexNoError(functionTagChildrenStringList, "figure")
    newFunction.body = parseFuncBody(functionTag.children[funcBodyIndex])
    return newFunction