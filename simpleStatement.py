from typing import List
from typing import Dict

class programState():
    def __init__(self):
        #self.variables:List[stateVariable] = []
        self.variables:Dict[str, int] = {}

class simpleStatement:
    def __init__(self):
        pass
    #     self.name = name #the tag as in the html file
    #     self.children = [] #all other tags containd in this tag

    # #moet bij alle tags
    # def __str__(self) -> str:
    #     return self.name

    # def __repr__(self) -> str:
    #     return self.name

    # def __eq__(self, other) -> bool:
    #     return self.name == other.name and \
    #            self.children == other.children

class codeBlockStatement:
    def __init__(self):
        pass

#wordt gebruikt als je een variable tegen komt in een code block,
#in de runner bijhouden wat de waarde voor elk variable op een gegeven moment is
#return n + 3
class codeBlockVariable(codeBlockStatement):
    def __init__(self, name:str):
        self.name:str = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.name == other.name

    def compute(self, state:programState):
        return state.variables[self.name]
        #loopup wat waarde variable is
        #lijst met variablen moet recursief worden meegegeven

#getallen in een codeblock
class codeBlockConstant(codeBlockStatement):
    def __init__(self, value):
        self.value:int = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.value == other.value

    def compute(self, state:programState):
        return self.value

#variable gebruikt als een nieuw variable gedefined wordt
#int n = 3
class initVariable(simpleStatement):
    def __init__(self, name = None):
        self.name:str = name
        self.value:codeBlockStatement = None

    def __str__(self) -> int:
        return self.value

    def __eq__(self, other) -> bool:
        return self.name == other.name and \
               self.value == other.value

    def set(self, value:int):
        self.value = value

def boolToInt(bl:bool)->int:
    if bl == True:
        return 1
    else:
        return 0
    #return 1 if bl else 0

#for internal use
class operator(codeBlockStatement):
    def __init__(self):
        self.leftSide:codeBlockStatement = None
        self.rightSide:codeBlockStatement = None

    #used to print
    def returnOperator(self)-> str:
        pass

    #reverse polish otation
    def __str__(self) -> str:
        return str(self.leftSide) + str(self.rightSide) + self.returnOperator()

    def __eq__(self, other) -> bool:
        return self.leftSide == other.leftSide and \
               self.rightSide == other.rightSide

#+
class plusOperator(operator):
    def returnOperator(self)-> str:
        return '+'
    
    def compute(self, state:programState)->int:
        return self.leftSide.compute(state) + self.rightSide.compute(state)

#-
class minusOperator(operator):
    def returnOperator(self)-> str:
        return '-'
    
    def compute(self, state:programState)->int:
        return self.leftSide.compute(state) - self.rightSide.compute(state)

#*
class multiplicationOperator(operator):
    def returnOperator(self)-> str:
        return '*'
    
    def compute(self, state:programState)->int:
        return self.leftSide.compute(state) * self.rightSide.compute(state)

#/
class divisionOperator(operator):
    def returnOperator(self)-> str:
        return '/'
    
    def compute(self, state:programState)->int:
        return self.leftSide.compute(state) / self.rightSide.compute(state)

#==
class compareEqual(operator):
    def returnOperator(self)-> str:
        return '=='
    
    def compute(self, state:programState)->int:
        return boolToInt(self.leftSide.compute(state) == self.rightSide.compute(state) )

#!=
class compareNotEqual(operator):
    def returnOperator(self)-> str:
        return '!='
    
    def compute(self, state:programState)->int:
        return boolToInt(self.leftSide.compute(state) != self.rightSide.compute(state) )

#<
class compareSmallerThan(operator):
    def returnOperator(self)-> str:
        return '<'
    
    def compute(self, state:programState)->int:
        return boolToInt(self.leftSide.compute(state) < self.rightSide.compute(state) )

#>
class compareBiggerThan(operator):
    def returnOperator(self)-> str:
        return '>'
    
    def compute(self, state:programState)->int:
        return boolToInt(self.leftSide.compute(state) > self.rightSide.compute(state) )

#<=
class compareSmallerOrEqual(operator):
    def returnOperator(self)-> str:
        return '<='
    
    def compute(self, state:programState)->int:
        return boolToInt(self.leftSide.compute(state) <= self.rightSide.compute(state) )

#>=
class compareBiggerOrEqual(operator):
    def returnOperator(self)-> str:
        return '>='
    
    def compute(self, state:programState)->int:
        return boolToInt(self.leftSide.compute(state) <= self.rightSide.compute(state) )



#<body>
class declerationList(simpleStatement):
    def __init__(self):
        self.functions:List[function] = []
        self.mainFunction:List[simpleStatement] = []
    
    def __str__(self) -> str:
        return str(self.functions) + str(self.mainFunction)

    def __eq__(self, other) -> bool:
        return self.functions == other.functions and \
               self.mainFunction == other.mainFunction

#<section>
class function(simpleStatement):
    def __init__(self):
        self.functionName:str
        self.parameters = []
        self.body = []

    def __str__(self) -> str:
        return self.functionName

    def __eq__(self, other) -> bool:
        return self.functionName == other.functionName and \
               self.parameters == other.parameters and \
               self.body == other.body

class ifStatement(simpleStatement):
    def __init__(self):
        self.condition:codeBlockStatement
        self.ifBody:List[simpleStatement] = []
        self.elseBody:List[simpleStatement] = []

    def __str__(self) -> str:
        return str(self.condition)

    def __eq__(self, other) -> bool:
        return self.condition == other.condition and \
               self.ifBody == other.ifBody and \
               self.elseBody == other.elseBody

class whileLoop(simpleStatement):
    def __init__(self):
        self.condition:codeBlockStatement
        self.loop:List[simpleStatement] = []

    def __str__(self) -> str:
        return self.condition

    def __eq__(self, other) -> bool:
        return self.condition == other.condition and \
               self.loop == other.loop

class returnStatement(simpleStatement):
    def __init__(self, value):
        self.value:codeBlockStatement = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def compute(self, state:programState):
        return self.value.compute(state)

class printStatement(simpleStatement):
    def __init__(self, value):
        self.value:codeBlockStatement = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def compute(self, state:programState):
        return self.value.compute(state)

class inputStatement(simpleStatement):
    def __init__(self, variable):
        #variable moet al bestaan
        self.variable:codeBlockVariable = variable
        self.input:operator

    def __str__(self) -> str:
        return str(self.input)
    
    def __eq__(self, other) -> bool:
        return self.variable == other.variable and \
               self.input == other.input

class functionCallStatement(simpleStatement):
    def __init__(self):
        self.functionName:str
        self.parameters:List[codeBlockStatement]
        self.returnVariable:str

    def __str__(self) -> str:
        return self.functionName
    
    def __eq__(self, other) -> bool:
        return self.functionName == other.functionName and \
               self.parameters == other.parameters and \
               self.returnVariable == other.returnVariable