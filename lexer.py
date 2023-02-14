from typing import Tuple, List
import sys
sys.setrecursionlimit(200000)

whiteSpace = ' \n\r\t'
taglist = ["html", "body", "section", "h2", "h3", "mark", "figure", "article", "i", "nav", "h4", "summary", "main", "ins", "output", "footer", "input"]
#operatorList = ["+", "-", "*", "/", "%", "**", "//", "=", "+=", "-=", "*=", "/=", "%=", "//=", "**=", "&=", "|=", "^=", ">>=", "<<=", "==", "!=", "<", ">", ">=", "<=", "&", "|", "^", "~", "<<", "<<"]
#niet toegevoegt: and, or, not, is, is not, in, not in

#selectie van de operators, alleen die we gebruiken
# ( en ) zijn geen operators, maar parenthesesToken
operatorList = "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="

class token:
    def __init__(self, name : str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.name == other.name

class identifierToken(token):
    def __init__(self, name : str):
        self.name = name

class numberToken(token):
    def __init__(self, name : str):
        self.name = name

class operatorToken(token):
    def __init__(self, name : str):
        self.name = name

class parenthesesToken(token):
    def __init__(self, name : str):
        self.name = name

class tag:
    def __init__(self, name : str):
        self.name = name #the tag as in the html file
        self.codeBlock:List[token] = [] #code block in tag
        self.children:List[tag] = [] #all other tags containd in this tag

    #moet bij alle tags
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return self.name == other.name and \
               self.codeBlock == other.codeBlock and \
               self.children == other.children

    def printTree(self, level = 0):
        print (' |  ' * level, self.name)
        if len(self.codeBlock) != 0:
            #for code in self.codeBlock:
            #    print(' |  ' * (level+1),'[', code.name, ']')
            list(map(lambda code: print(' |  ' * (level+1),'[', code.name, ']'), self.codeBlock))
        #for child in self.children:
        #    child.printTree(level+1)
        list(map(lambda child: child.printTree(level+1) ) )

#splits a string in the first character and the rest of the string
# splitString :: str -> Tuple[str, str]
def splitString(file:str) -> Tuple[str, str]:
    return file[0], file[1:]

#lex a file, returned a tree, also returns a str, this is the remainder of the file to work with recursion
#maakt een tree met de tags zoals die in de html file staan
# lex :: str -> tag -> Tuple[str, tag]
def lex(file:str, tree:tag)-> Tuple[str, tag]:
    if len(file) == 0:
        return file, tree
    
    chr, restFile = splitString(file)

    #ingore whitespaces
    if chr in whiteSpace:
        return lex(restFile, tree)

    if chr == '<':
        commentIndex = findComment(file)
        if commentIndex != None:
            return lex(file[commentIndex:], tree)

        tagIndex, tagName, isOpen = findTag(file)
        if tagIndex != None:
            #if closing tag
            if isOpen == False:
                #eigen closing tag?
                if tagName == tree.name:
                    return file[tagIndex:], tree
                else:
                    print("error, wrong closing tag found")
                    return file[tagIndex:], tree #error
            else:
                #lex de child
                newFile, childTree = lex(file[tagIndex:], tag(tagName))
                tree.children.append(childTree)
                #door met lexen na child
                return lex(newFile, tree)

    #wat als geen tag, maar codeblock
    newToken, tokenLenght = findToken(file)
    tree.codeBlock.append(newToken)
    
    return lex(file[tokenLenght:], tree)

#functie om te checken of iets een tag is, zo ja, returned de index na de tag, de tag en of het een open of closing tag is
#tuple(index na de tag, de tag, True=open of False=close)
# findTag :: str -> Tuple[int, str, bool]
def findTag(file:str)->Tuple[int, str, bool]:
    endOfTag = file.find('>')
    if endOfTag == -1:
        #print("geen tag")
        return None, None, None #geen tag
    
    # 1 om '<' niet mee te nemen
    if file[1:endOfTag] in taglist:
        #return index na de tag, de tag, is open tag
        return endOfTag+1, file[1:endOfTag], True
    elif file[1] == '/' and file[2:endOfTag] in taglist:
        #return index na de tag, de tag, is close tag
        return endOfTag+1, file[2:endOfTag], False
    else:
        #print("invalid tag")
        return None, None, None #geen tag

#functie om te checken of iets een comment is, zo ja, returned de lengte van de comment
# findComment :: str -> int
def findComment(file:str) -> int:
    if file[:4] != "<!--":
        #print("geen comment")
        return None #geen comment

    #index+4 omdat <!-- 4 chars is, en je daarna begind met zoeken
    endOfComment = file.find("-->", 4)
    if endOfComment == -1:
        print("error, halve comment?")
        return None #halve comment?
    #endOfComment+3 omdat je de eerste char na de comment returnt
    return endOfComment+3

#higher order function | hogere order functie
#returnt eerste index dat de proposition False is
def findEnd(file:str, proposition, index=0)->int:
    if index >= len(file):
        #print("no end")
        return index
    if proposition(file[index]):
        return findEnd(file, proposition, index+1)
    return index

#functie om te checken of iets een token is, zo ja, returned de token en de lengte van de token
#return tuple(de token, lengte token)
# findToken :: str -> Tuple[token, int]
def findToken(file:str)->Tuple[token, int]:
    chr, restFile = splitString(file)
    #eerste teken van een identefier moet uit een letter bestaan
    if chr.isalpha():
        #zoekt het einde van een woord, woorden bestaan uit letters, cijfers en _
        endOfWord = findEnd(file, 
            lambda c: c.isalpha() or c.isdecimal() or c == '_')

        newToken = identifierToken(file[:endOfWord])
        return newToken, endOfWord
    if chr.isdecimal():
        endOfNumber = findEnd(file,
            lambda c: c.isdecimal())

        newToken = numberToken(file[:endOfNumber])
        return newToken, endOfNumber

    if chr == '(' or chr == ')':
        return parenthesesToken(chr), 1

    if len(file) >= 2:
        #operator van 2 characters
        if file[:2] in operatorList:
            newToken = operatorToken(file[:2])
            return newToken, 2
        #operator van 1 character
        if chr in operatorList:
            newToken = operatorToken(chr)
            return newToken, 1
    #error
    return None, None



#functie om het progrtamma te starten
# lexer :: str -> tag
def lexer(file:str) -> tag:
    # tree = tag("root")
    # tree.lex(file)

    emptyFile, tree = lex(file, tag("root"))

    return tree