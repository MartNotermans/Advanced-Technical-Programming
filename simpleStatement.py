from typing import List

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
    def __init__(self, name):
        self.name:str = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.name == other.name

    def compute(self):
        pass
        #loopup wat waarde variable is
        #lijst met variablen moet recursief worden meegegeven

#getallen in een codeblock
class codeBlockCanstant(codeBlockStatement):
    def __init__(self, value):
        self.value:int = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.value == other.value

    def compute(self):
        return self.value

#variable gebruikt als een nieuw variable gedefined wordt
#int n = 3
class initVariable(simpleStatement):
    def __init__(self, name = None):
        self.name:str = name
        self.value:int = None

    def __str__(self) -> int:
        return self.value

    def __eq__(self, other) -> bool:
        return self.name == other.name and \
               self.value == other.value

    def set(self, value:int):
        self.value = value

    def get(self):
        return self.value

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
    
    def compute(self)->int:
        return self.leftSide.get() + self.rightSide.get()

#-
class minusOperator(operator):
    def returnOperator(self)-> str:
        return '-'
    
    def compute(self)->int:
        return self.leftSide.get() - self.rightSide.get()

#*
class multiplicationOperator(operator):
    def returnOperator(self)-> str:
        return '*'
    
    def compute(self)->int:
        return self.leftSide.get() * self.rightSide.get()

#/
class divisionOperator(operator):
    def returnOperator(self)-> str:
        return '/'
    
    def compute(self)->int:
        return self.leftSide.get() / self.rightSide.get()

#==
class compareEqual(operator):
    def returnOperator(self)-> str:
        return '=='
    
    def compute(self)->int:
        return boolToInt(self.leftSide.get() == self.rightSide.get() )

#!=
class compareNotEqual(operator):
    def returnOperator(self)-> str:
        return '!='
    
    def compute(self)->int:
        return boolToInt(self.leftSide.get() != self.rightSide.get() )

#<
class compareSmallerThan(operator):
    def returnOperator(self)-> str:
        return '<'
    
    def compute(self)->int:
        return boolToInt(self.leftSide.get() < self.rightSide.get() )

#>
class compareBiggerThan(operator):
    def returnOperator(self)-> str:
        return '>'
    
    def compute(self)->int:
        return boolToInt(self.leftSide.get() > self.rightSide.get() )

#<=
class compareSmallerOrEqual(operator):
    def returnOperator(self)-> str:
        return '<='
    
    def compute(self)->int:
        return boolToInt(self.leftSide.get() <= self.rightSide.get() )

#>=
class compareBiggerOrEqual(operator):
    def returnOperator(self)-> str:
        return '>='
    
    def compute(self)->int:
        return boolToInt(self.leftSide.get() <= self.rightSide.get() )



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
        self.condition = []
        self.loop = []

    def __str__(self) -> str:
        return self.condition

    def __eq__(self, other) -> bool:
        return self.condition == other.condition and \
               self.loop == other.loop