from typing import List

class simpleStatement:
    def __init__(self, name : str):
        self.name = name #the tag as in the html file
        self.children = [] #all other tags containd in this tag

    #moet bij alle tags
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return self.name == other.name and \
               self.children == other.children

class intType(simpleStatement):
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

#for internal use
class intOperator(simpleStatement):
    def __init__(self, left, right):
        self.leftSide:intType = left
        self.rightSide:intType = right

#+
class plusOperator(intOperator):
    def compute(self)->int:
        return self.leftSide.get() + self.rightSide.get()

#-
class minusOperator(intOperator):
    def compute(self)->int:
        return self.leftSide.get() - self.rightSide.get()

#*
class multiplicationOperator(intOperator):
    def compute(self)->int:
        return self.leftSide.get() * self.rightSide.get()

#/
class divisionOperator(intOperator):
    def compute(self)->int:
        return self.leftSide.get() / self.rightSide.get()

#==
class compareEqual(intOperator):
    def compute(self)->bool:
        return self.leftSide.get() == self.rightSide.get()

#!=
class compareNotEqual(intOperator):
    def compute(self)->bool:
        return self.leftSide.get() != self.rightSide.get()

#<
class compareSmallerThan(intOperator):
    def compute(self)->bool:
        return self.leftSide.get() < self.rightSide.get()

#>
class compareBiggerThan(intOperator):
    def compute(self)->bool:
        return self.leftSide.get() > self.rightSide.get()

#>
class compareSmallerOrEqual(intOperator):
    def compute(self)->bool:
        return self.leftSide.get() <= self.rightSide.get()

#<
class compareBiggerOrEqual(intOperator):
    def compute(self)->bool:
        return self.leftSide.get() <= self.rightSide.get()

#=
class assign(intOperator):
    def compute(self)->None:
        self.leftSide.set(self.rightSide.get())

#+=
class plusAssign(intOperator):
    def compute(self)->None:
        self.leftSide.set(self.leftSide.get() + self.rightSide.get() )

#-=
class minusAssign(intOperator):
    def compute(self)->None:
        self.leftSide.set(self.leftSide.get() - self.rightSide.get() )

#*=
class multiplicationAssign(intOperator):
    def compute(self)->None:
        self.leftSide.set(self.leftSide.get() * self.rightSide.get() )

#/=
class divitionAssign(intOperator):
    def compute(self)->None:
        self.leftSide.set(self.leftSide.get() / self.rightSide.get() )

class boolType(simpleStatement):
    def __init__(self, name = None):
        self.name:str = name
        self.value:bool = None

    def __eq__(self, other) -> bool:
        return self.name == other.name and \
               self.value == other.value

    def __str__(self) -> bool:
        return self.value

    def set(self, value:bool):
        self.value = value

    def get(self) -> bool:
        return self.value

class boolOperator(simpleStatement):
    def __init__(self, left:boolType, right:boolType):
        self.left = left
        self.right = right

#=
class assign(boolOperator):
    def compute(self)->None:
        self.leftSide.set(self.rightSide.get())

class compareEqual(boolOperator):
    def compute(self)->None:
        self.leftSide.get () == self.rightSide.get()
#more bool operators?????      

class strType(simpleStatement):
    def __init__(self, name = None):
        self.name:str = name
        self.value:str = None

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        return self.name == other.name and \
               self.value == other.value

    def set(self, value:str):
        self.value = value

    def get(self):
        return self.value

class strOperator(simpleStatement):
    def __init__(self, left:strType, right:strType):
        self.left = left
        self.right = right

#+
class plusOperator(strOperator):
    def compute(self)->int:
        return self.leftSide.get() + self.rightSide.get()

#=
class assign(strOperator):
    def compute(self)->None:
        self.leftSide.set(self.rightSide.get())

#<body>
class declerationList(simpleStatement):
    def __init__(self):
        self.functions:List[function] = []
        self.mainFunction:List[simpleStatement] = []
        
    def __str__(self) -> str:
        return self.functions, self.mainFunction

    def __eq__(self, other) -> bool:
        return self.functions == other.functions and \
               self.mainFunction == other.mainFunction

#<section>
class function(simpleStatement):
    def __init__(self):
        self.functionName:str
        self.returnType:simpleStatement
        self.parameters = []
        self.body = []

    def __str__(self) -> str:
        return self.functionName

    def __eq__(self, other) -> bool:
        return self.functionName == other.functionName and \
               self.returnType == other.returnType and \
               self.parameters == other.parameters and \
               self.body == other.body

class ifStatement(simpleStatement):
    def __init__(self):
        self.condition = []
        self.ifBody = []
        self.elseBody = []

    def __str__(self) -> str:
        return self.condition

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