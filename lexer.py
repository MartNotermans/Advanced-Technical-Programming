#from curses.ascii import isalpha
#from pickle import FALSE
import sys
sys.setrecursionlimit(200000)

whiteSpace = ' \n\r\t'
taglist = ["html", "body", "section", "h2", "h3", "mark", "figure", "article", "i", "nav", "h4", "summary", "main", "ins", "output"]
operatorList = ["+", "-", "*", "/", "%", "**", "//", "=", "+=", "-=", "*=", "/=", "%=", "//=", "**=", "&=", "|=", "^=", ">>=", "<<=", "==", "!=", "<", ">", ">=", "<=", "&", "|", "^", "~", "<<", "<<"]
#niet toegevoegt: and, or, not, is, is not, in, not in

def searchOpenNode(lst, i = 0):
        if len(lst) == 0:
            return None

        if lst[0].closed == False:
            return i
        else:
            lst = lst[1:]
            i = i+1
            return searchOpenNode(lst, i)

class token:
    def __init__(self, name : str):
        self.name = name

    def __str__(self) -> str:
        return self.name

class identifier(token):
    def __init__(self, name : str):
        self.name = name\

class number(token):
    def __init__(self, name : str):
        self.name = name

class operator(token):
    def __init__(self, name : str):
        self.name = name

class tag:
    def __init__(self, name : str):
        self.name = name #the tag as in the html file
        self.codeBlock = [] #code block in tag
        self.children = [] #all other tags containd in this tag
        self.closed = False #closed als closing tag gevonden is

    def lex(self, file, index = 0) -> int:
        if index >= len(file):
            return self
        
        
        #ingore whitespaces
        chr = file[index]
        if chr in whiteSpace:
            index+=1
            return self.lex(file, index)

        if chr == '<':
            commentIndex = findComment(file, index)
            if commentIndex != None:
                return self.lex(file, commentIndex)

            tagTuple = findTag(file, index)
            if tagTuple != None:
                index = tagTuple[0]
                #if closing tag
                if tagTuple[2] == False:
                    #eigen closing tag?
                    if tagTuple[1] == self.name:
                        return index
                    else:
                        print("wrong closing tag found")
                        return index
                else:
                    newTag = tag(tagTuple[1])
                    self.children.append(newTag)
                    index = newTag.lex(file, index)
                    return self.lex(file, index)
        
        #wat als geen tag, maar codeblock
        newIndexAndToken = findToken(file, index)
        self.codeBlock.append(newIndexAndToken[1])
        index = newIndexAndToken[0]
        
        return self.lex(file, index)

    #moet bij alle tags
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def printTree(self, level = 0):
        print (' |  ' * level, self.name)
        if len(self.codeBlock) != 0:
            for code in self.codeBlock:
                print(' |  ' * (level+1),'[', code.name, ']')
        #for mag niet!!
        for child in self.children:
            child.printTree(level+1)

#lex maar functional
def funcLex():
    pass

#tuple(index na de tag, de tag, True=open of False=close)
def findTag(file:str, index:int)->tuple:
    endOfTag = file.find('>', index)
    if endOfTag == -1:
        print("geen tag")
        return None #geen tag
    
    # 1 om '<' niet mee te nemen
    if file[index+1:endOfTag] in taglist:
        #return index na de tag, de tag, is open tag
        return endOfTag+1, file[index+1:endOfTag], True
    elif file[index+1] == '/' and file[index+2:endOfTag] in taglist:
        #return index na de tag, de tag, is close tag
        return endOfTag+1, file[index+2:endOfTag], False
    else:
        print("invalid tag")
        return None #geen tag

def findComment(file:str, index:int) -> int:
    if file[index:(index+4)] != "<!--":
        print("geen comment")
        return None #geen comment

    #index+4 omdat <!-- 4 chars is, en je daarna begind met zoeken
    endOfComment = file.find("-->", index+4)
    if endOfComment == -1:
        print("halve comment?")
        return None #halve comment?
    #endOfComment+3 omdat je de eerste char na de comment returnt
    return endOfComment+3

#higher order function
#returnt eerste index dat de proposition False is
def findEnd(file:str, index:int, proposition)->int:
    if index >= len(file):
        print("geen end")
        return None
    if proposition(file[index]):
        return findEnd(file, index+1, proposition)
    return index

def findToken(file:str, index:int)->tuple: #tuple(nieuwe index, identifier)
    #eerste teken van een identefier moet uit een letter bestaan
    if file[index].isalpha():
        #zoekt het einde van een woord, woorden bestaan uit letters, cijfers en _
        endOfWord = findEnd(file, index, 
            lambda c: c.isalpha() or c.isdecimal() or c == '_')

        newToken = identifier(file[index:endOfWord])
        return endOfWord, newToken
    if file[index].isdecimal():
        endOfNumber = findEnd(file, index, 
            lambda c: c.isdecimal())

        newToken = number(file[index:endOfNumber])
        return endOfNumber, newToken

    #+2 omdat tot index+2, niet tot en met
    if file[index:index+2] in operatorList:
        newToken = operator(file[index:index+2])
        return index+2, newToken
    if file[index] in operatorList:
        newToken = operator(file[index])
        return index+1, newToken


    

def lexer(file):
    tree = tag("root")
    tree.lex(file)

    return tree