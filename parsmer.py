from lexer import tag, token, identifierToken, numberToken, operatorToken, parenthesesToken
from simpleStatement import *


from typing import List
import sys
sys.setrecursionlimit(200000)
#main parser functie, krijgt de <html> tag en maakt een AST
#parser :: tag -> declerationList
def parser(tokenTree: tag) -> declerationList:
    if len(tokenTree.children) != 1:
        print("tokenTree empty")
        return
    
    AST = declerationList()
    htmlTag = tokenTree.children[0]
    if htmlTag.name != "html" or len(htmlTag.children) != 2:
        return None

    childrenStringList = list(map(lambda x: x.name, htmlTag.children) )
    bodyIndex = indexNoError(childrenStringList, "body", 0)
    #higher order function | hogere order functie
    AST.functions = list(map(parseFunction, htmlTag.children[bodyIndex].children))
    
    mainIndex = indexNoError(childrenStringList, "main", 0)
    AST.mainFunction = parseFuncBody(htmlTag.children[mainIndex])

    return AST

#geeft de index van een item in een list, geeft -1 als het item niet in list zit
# indexNoError :: list -> str -> int -> int
def indexNoError(lst:list, item:str, start:int)->int:
    try:
        index = lst.index(item, start)
        return index
    except ValueError:
        index = -1
        return index

#geeft alle indexen van een item in een lijst, geeft lege lijst terug als item niet in lijst
#lst = lijst om in te zoeken, item = wat je wil zoeken, indexlist = return, start = 
#intern omdat python moeilijk doet met de indexlist die altijd leeg moet zijn aan het begin
# indexAllNoErrorIntern :: list -> str -> list -> int -> list
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


precedenceDict = dict()
precedenceDict['*'] = 1
precedenceDict['/'] = 1
precedenceDict['+'] = 2
precedenceDict['-'] = 2
precedenceDict['=='] = 3
precedenceDict['!='] = 3
precedenceDict['<'] = 3
precedenceDict['>'] = 3
precedenceDict['<='] = 3
precedenceDict['>='] = 3
#deze functie checkt de welke operator een hogere precedence heeft
#operator volgorde: () */ +- == != < > <= >=
#1 is firstToken, 2 is secondToken, 3 is zelfde precedence
# checkPrecedence :: token -> token -> int
def checkPrecedence(firstToken:token, secondToken:token)->int:
    if isinstance(secondToken, parenthesesToken):
        return 1
    if precedenceDict[firstToken.name] == precedenceDict[secondToken.name]:
        return 3
    if precedenceDict[firstToken.name] < precedenceDict[secondToken.name]:
        return 1
    else:
        return 2

#shunting yard algorithm naar Reverse Polish notation (RPN)
#operatorStack, toevoegen is append, weghalen is pop
#outputQueue, toevoegen is append, weghalen is pop(0)
# shuntingYardToRPN :: List[token] -> List[token] -> List[token] -> List[token]
def shuntingYardToRPN(codeblock:List[token], operatorStack:List[token], outputQueue:List[token])->List[token]:
    if len(codeblock) == 0 and len(operatorStack) == 0:
        return outputQueue
    
    if len(codeblock) == 0:
        #haakjes niet naar de output queue
        if operatorStack[-1].name != '(' or operatorStack[-1].name != ')':
            outputQueue.append( operatorStack.pop() )
        return shuntingYardToRPN(codeblock, operatorStack, outputQueue)

    tkn, *rest = codeblock
    if isinstance(tkn, numberToken) or isinstance(tkn, identifierToken):
        outputQueue.append(tkn)
        return shuntingYardToRPN(rest, operatorStack, outputQueue)
    if isinstance(tkn, operatorToken):
        if len(operatorStack) == 0:
            operatorStack.append(tkn)
            return shuntingYardToRPN(rest, operatorStack, outputQueue)
        else: #een andere operator
            check = checkPrecedence(tkn, operatorStack[-1])
            if check == 1:
                operatorStack.append(tkn)
                return shuntingYardToRPN(rest, operatorStack, outputQueue)
            else:
                #if operatorStack[-1].name != '(' or operatorStack[-1].name != ')':
                outputQueue.append( operatorStack.pop() )
                #codeblok en niet rest, omdat je doorgaat totdat rst een hogere precenence heeft
                return shuntingYardToRPN(codeblock, operatorStack, outputQueue)
    if isinstance(tkn, parenthesesToken):    
        if tkn.name == '(':
            operatorStack.append(tkn)
            return shuntingYardToRPN(rest, operatorStack, outputQueue)
        if tkn.name == ')':
            if len(operatorStack) == 0:
                print("error, mismatched parenthesis")
                return
            if operatorStack[-1].name == '(':
                operatorStack.pop()
                return shuntingYardToRPN(rest, operatorStack, outputQueue)
            else:
                #haakjes niet naar de output queue
                # if isinstance(operatorStack[-1], parenthesesToken):
                #     operatorStack.pop()
                outputQueue.append( operatorStack.pop() )
                #codeblok en niet rest, omdat je doorgaat totdat je de opening bracket gevonden hebt
                return shuntingYardToRPN(codeblock, operatorStack, outputQueue)

#functie om van een operator een codeBlockStatement te maken
# operatorTocodeBlockStatement :: token -> codeBlockStatement
def operatorTocodeBlockStatement(token)->codeBlockStatement:
    operator = token.name
    if operator == '+':
        return plusOperator()
    if operator == '-':
        return minusOperator()
    if operator == '*':
        return multiplicationOperator()
    if operator == '/':
        return divisionOperator()
    if operator == '==':
        return compareEqual()
    if operator == '!=':
        return compareNotEqual()
    if operator == '<':
        return compareSmallerThan()
    if operator == '>':
        return compareBiggerThan()
    if operator == '<=':
        return compareSmallerOrEqual()
    if operator == '>=':
        return compareBiggerOrEqual()
    else:
        #not an operator
        return

#Reverse Polish notation to operator tree
# RPNtoTree :: List[token] -> operator -> operator
def RPNtoTree(codeBlockRPN:List[token], tree:operator)->operator:
    if len(codeBlockRPN) == 0:
        return tree
    
    tkn = codeBlockRPN.pop()

    if isinstance(tkn, operatorToken):
        newOperator = operatorTocodeBlockStatement(tkn)
        if tree.rightSide == None:
            tree.rightSide = RPNtoTree(codeBlockRPN, newOperator)
        else:
            tree.leftSide = RPNtoTree(codeBlockRPN, newOperator)
    elif isinstance(tkn, numberToken):
        if tree.rightSide == None:
            tree.rightSide = codeBlockConstant(int(tkn.name))
            return RPNtoTree(codeBlockRPN, tree)
        else:
            tree.leftSide = codeBlockConstant(int(tkn.name))
            return RPNtoTree(codeBlockRPN, tree)
    #identifier
    else:
        if tree.rightSide == None:
            tree.rightSide = codeBlockVariable(tkn.name)
            return RPNtoTree(codeBlockRPN, tree)
        else:
            tree.leftSide = codeBlockVariable(tkn.name)
            return RPNtoTree(codeBlockRPN, tree)

#parse een codeblock token
# parseCodeBlock :: List[token] -> codeBlockStatement
def parseCodeBlock(codeblock:List[token])->codeBlockStatement:
    codeBlockRPN = shuntingYardToRPN(codeblock, [], [])
    
    if isinstance(codeBlockRPN[-1], operatorToken):
        newTree = operatorTocodeBlockStatement(codeBlockRPN.pop() )
        return RPNtoTree(codeBlockRPN, newTree)
    elif isinstance(codeBlockRPN[-1], numberToken):
        return codeBlockConstant(int(codeBlockRPN[-1].name))
    else:
        return codeBlockVariable(codeBlockRPN[-1].name)

#parse een parameter tag
# parseParameter :: tag -> initVariable
def parseParameter(parameter:tag)->initVariable:
    if parameter.name == "mark":
        if isinstance(parameter.codeBlock[0], token):
            return initVariable(parameter.codeBlock[0].name)
        print("error, parameter name is not an identifier")

#parse een if statement tag
# parseIfStatement :: tag -> simpleStatement
def parseIfStatement(ifCode:tag)->simpleStatement:
    newIfStatement = ifStatement()

    ifCodeChildrenStringList = list(map(lambda x: x.name, ifCode.children) )
    #i is condidion
    conditionIndex = indexNoError(ifCodeChildrenStringList, "i", 0)
    #condition: list van tokens, waar onder een operator
    newIfStatement.condition = parseCodeBlock(ifCode.children[conditionIndex].codeBlock)

    #ifElseBody[0] = if body, ifElseBody[1] = else body
    ifElseBody = indexAllNoError(ifCodeChildrenStringList, "figure")
    newIfStatement.ifBody = parseFuncBody(ifCode.children[ifElseBody[0]])
    if len(ifElseBody) == 2:
        newIfStatement.elseBody = parseFuncBody(ifCode.children[ifElseBody[1]])

    return newIfStatement

#initialize een variable van een tag
# initialiseVariable :: tag -> simpleStatement
def initialiseVariable(variableTag:tag)->simpleStatement:
    tagyChildrenStringList = list(map(lambda x: x.name, variableTag.children) )
    nameIndex = indexNoError(tagyChildrenStringList, "h2", 0)
    valueIndex = indexNoError(tagyChildrenStringList, "h4", 0)

    newVariable = initVariable()
    newVariable.name = variableTag.children[nameIndex].codeBlock[0].name

    newVariable.value = parseCodeBlock(variableTag.children[valueIndex].codeBlock )
    return newVariable

#parse een while loop
# parseWhile :: tag -> whileLoop
def parseWhile(whileTag:tag)->whileLoop:
    whileChildrenStringList = list(map(lambda child: child.name, whileTag.children) )
    conditionIndex = indexNoError(whileChildrenStringList, "i", 0)
    bodyIndex = indexNoError(whileChildrenStringList, "figure", 0)
    newWhile = whileLoop()
    newWhile.condition = parseCodeBlock(whileTag.children[conditionIndex].codeBlock)
    newWhile.loop = parseFuncBody(whileTag.children[bodyIndex])
    return newWhile

#parse een functie call
# parseFunctionCall :: tag -> functionCallStatement
def parseFunctionCall(callTag:tag)->functionCallStatement:
    callTagChildrenStringList = list(map(lambda x: x.name, callTag.children) )
    nameIndex = indexNoError(callTagChildrenStringList, "h2", 0)
    returnVariableIndex = indexNoError(callTagChildrenStringList, "h3", 0)
    functieParametersIndex = indexAllNoError(callTagChildrenStringList, "h4")
    
    newFunctionCall = functionCallStatement()
    newFunctionCall.functionName = callTag.children[nameIndex].codeBlock[0].name
    newFunctionCall.returnVariable = callTag.children[returnVariableIndex].codeBlock[0].name
    newFunctionCall.parameters = list(map(lambda index: parseCodeBlock(callTag.children[index].codeBlock), functieParametersIndex))
    return newFunctionCall

#parse een tag in een functie body
# parseTagInFuncBody :: tag -> simpleStatement
def parseTagInFuncBody(tagy:tag)->simpleStatement:
    if tagy.name == "nav": #return
        #testen
        return returnStatement(parseCodeBlock(tagy.children[0].codeBlock))
    elif tagy.name == "article": #if
        return parseIfStatement(tagy)
    elif tagy.name == "ins": #initialise
        return initialiseVariable(tagy)
    elif tagy.name == "summary": #functie aanroepen
        return parseFunctionCall(tagy)
    elif tagy.name == "output": #print
        #testen
        return printStatement(parseCodeBlock(tagy.children[0].codeBlock))
    elif tagy.name == "footer": #while
        return parseWhile(tagy)
    elif tagy.name == "input": #user input
        return inputStatement(parseCodeBlock(tagy.children[0].codeBlock))
        

#parse the body of a function, if statement or while loop
# parseFuncBody :: tag -> List[simpleStatement]
def parseFuncBody(funcBody:tag)->List[simpleStatement]:
    return list(map(parseTagInFuncBody, funcBody.children))

#parse een function
# parseFunction :: tag -> function
def parseFunction(functionTag:tag)->function:
    if functionTag.name != "section":
        #geen function
        return None
    
    newFunction = function()

    tagChildrenStringList = list(map(lambda x: x.name, functionTag.children) )
    nameIndex = indexNoError(tagChildrenStringList, "h2", 0)
    newFunction.functionName = functionTag.children[nameIndex].codeBlock[0].name

    #volgorde parameters blijft behouden
    newFunction.parameters = list(filter(None, map(parseParameter, functionTag.children) ))


    functionTagChildrenStringList = list(map(lambda x: x.name, functionTag.children) )
    funcBodyIndex = indexNoError(functionTagChildrenStringList, "figure", 0)
    newFunction.body = parseFuncBody(functionTag.children[funcBodyIndex])
    return newFunction