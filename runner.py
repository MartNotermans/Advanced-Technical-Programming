from simpleStatement import *
from parsmer import *

def runner(AST:declerationList):
    state = programState()
    runFunction(AST, AST.mainFunction,state)
    
def runFunction(AST:declerationList, function:List[simpleStatement], state:programState)->programState:
    if len(function) == 0:
        return state
    
    statement, *rest = function

    if isinstance(statement, initVariable):
        state.variables[statement.name] = statement.value.compute(state)
        return runFunction(AST, rest, state)

    if isinstance(statement, inputStatement):
        state.variables[statement.variable.name] = int(input(statement.variable.name + ": ") )
        return runFunction(AST, rest, state)

    if isinstance(statement, printStatement):
        print("output: ", statement.compute(state))
        return runFunction(AST, rest, state)

    if isinstance(statement, functionCallStatement):
        #get the fuction names in a list as strings
        functionNamesStringList = list(map(lambda function: function.functionName, AST.functions) )
        #search for the index of the function were looking for: statement
        functionIndex = indexNoError(functionNamesStringList, statement.functionName, 0)
        
        #the state with the parameters to run the function
        functionState = programState
        #make a dict by combining with zip: the names from AST.functions and the values from statement.parameters
        functionState.variables = dict(zip( list(map(lambda x: x.name, AST.functions[functionIndex].parameters)), list(map(lambda x: x.compute(state), statement.parameters)) ))
        
        #run the function with the functionState
        tempstate = programState
        tempstate = runFunction(AST, AST.functions[functionIndex].body, functionState)
        if "returnValue" in tempstate.variables.keys():
            state.variables[statement.returnVariable] = tempstate.variables["returnValue"]
        return runFunction(AST, rest, state)

    if isinstance(statement, ifStatement):
        if statement.condition.compute(state) == 1:
            state = runFunction(AST, statement.ifBody, state)
            return runFunction(AST, rest, state)
        else:
            state = runFunction(AST, statement.elseBody, state)
            return runFunction(AST, rest, state)

    if isinstance(statement, whileLoop):
        #test???
        if statement.condition.compute(state) == 0:
            state = runFunction(AST, statement.loop, state)
            return runFunction(AST, function, state)
        return runFunction(AST, rest, state)

    if isinstance(statement, returnStatement):
        returnValue = programState
        returnValue.variables = {"returnValue": statement.value.compute(state) }
        return returnValue