from typing import Tuple
import sys
sys.setrecursionlimit(200000)
import functools

whiteSpace = ' \n\r\t'
validTagChars = 'abcdefghijklmnopqrstuvwxyz0123456789/'

#class body(tag)

class tag:
    def __init__(self, name : str):
        self.name = name #the tag as in the file
        self.children = [] #all other tags containd in this tag
        self.code = "" #code contained in this tag
        self.closingTagIndex = 0
        #print(self.name, "found!")

#<section>
class function(tag):
    def __init__(self):
        self.functionName = tag
        self.returnType = tag
        self.parameter = tag
        self.body = tag


#Tuple[is het een tag, "naam van de tag", open of closing tag - open=true, lengte tag]
def checkIfTag(file : str, index) -> Tuple[bool, str, bool, int]:
    isOpenTag = True
    #check if first char is opening bracket
    if file[index] != '<':
        #geen tag
        return (False, "", isOpenTag, 0)
    index+=1


    #+1 is na de <
    #om de closing tag te vinden
    if file[index] == '/':
        isOpenTag = False
        #index+=1


    #als er een > op index zit vinden we die later en geven we dan alsnog een error
    #!!!!!!!!!!!!!!! wat is .find, hogere orde functie? telt als loop?
    endOfTag = file.find('>', index+1)
    if endOfTag == -1:
        #syntax error
        return (False, "", isOpenTag, 0)


    tagName = file[index: endOfTag]
    #lambda om te checken of alle characters in tagName in validTagChars zitten
    #b is een bool of alle vorige chars valid zijn
    #c is de huidige char
    if functools.reduce(lambda b, c: b and c in validTagChars, tagName, True):
        #valid tag
        return (True, tagName, isOpenTag, endOfTag+1)

    #syntax error
    return (False, "", isOpenTag, 0)

#Tuple[is a comment, lengte comment]
def checkIfComment(file, index) -> Tuple[bool, int]:
    if file[index: index+4] != "<!--":
        return (False, 0)

    #index+4 omdat <!-- 4 chars is, en ja daarna begind met zoeken
    endOfComment = file.find("-->", index+4)
    if endOfComment == -1:
        #syntax error
        return (False, 0)
    #endOfComment+3 omdat je de eerste char na de comment returnt
    return (True, endOfComment+3)

#alle html tags in volgorde nestelen
def findTags(file, currentTag : tag, index): #met loopjes
    #bool om bij te houden of er text in de huidige tag zit
    #als er text en childern in de huidige tag zitten heb je een syntax error
    foundTxt = False

    i = index
    #MAG NIET!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    while i < len(file):
        isTag = checkIfTag(file, i)
        #[0] is a valid tag?
        if isTag[0]:
            #[2] is an open tag?
            if isTag[2]:
                newTag = tag(isTag[1])
                currentTag.children.append(newTag)
                #isTag[3] is de eerste char na de huidige tag
                findTags(file, newTag, isTag[3])
                i = newTag.closingTagIndex
            #is this a maching closing tag?
            elif isTag[1] == currentTag.name:
                #isTag[3] is de eerste char na de closing tag
                currentTag.closingTagIndex = isTag[3]
                if len(currentTag.children) == 0:
                    #index is het eerste char na de opening tag
                    #i is het eerste char van de closing tag
                    currentTag.code = file[index: i]
                elif foundTxt:
                    #syntax error omdat er text en een child is, mag niet
                    pass
                return
            else:
                #syntax error, andere closing tag gevonden
                pass
        else:
            #skip over comments
            isComment = checkIfComment(file, i)
            if isComment[0]:
                i = isComment[1]
            else:
                if not file[i] in whiteSpace:
                    foundTxt = True
                i+=1

def FindOtherTags(currentTag, file, i):
    if i >= len(file):
        return currentTag        

def recursiveFindFirstTag(file, i): 
    if i >= len(file):
        return tag("error")
    chr = file[i]
    if chr in whiteSpace:
        i+=1
    elif chr == '<':
        #+6 is de lengte van <html>
        if file[i:i+6] == "<html>":
            #i+6 is het eerste char na <html>
            root = tag("html")
            FindOtherTags(root, file, i)
            return root
        else:
            i+=1
    else:
        i+=1
    recursiveFindFirstTag(file, i)

def lexer(file, i=0, tokens=[]):
    if i >= len(file):
        return tokens
    
    chr = file[i]
    if chr in whiteSpace:
        i+=1
    elif chr == '<':
        isTag = checkIfTag(file, i)
        #[0] is isTag a valid tag?
        if isTag[0]:
            tokens.append(isTag[1])
            i += isTag[3]


        isComment = checkIfComment(file, i)
        #[0] is isComment a valid comment?
        if isComment[0]:
            #ignore comment
            i += isComment[1]

    elif chr in validTagChars:
        i+=1

    else:
        i+=1
        return lexer(file, i, tokens)
    return lexer(file, i, tokens)


taglist = ["<html>", "<Body>", "<section>", "<h2>", "<h3>"]

#dict met tags
tagdict = dict()
tagdict["html"] = ("file start", lambda: print("file start found"))
tagdict["Body"] = ("body start", lambda: print("body Found"))
tagdict["section"] = ("function declaration", lambda: print("function"))
tagdict["h2"] = ("name", lambda: print("name found"))
tagdict["h3"] = ("variable type", lambda: print(""))
tagdict["mark"] = ("variable", lambda: print(""))
tagdict["h4"] = ("value or calculation", lambda: print(""))
tagdict["figure"] = ("code block", lambda: print(""))
tagdict["summary"] = ("function calling", lambda: print(""))
tagdict["article"] = ("if statement", lambda: print(""))
tagdict["i"] = ("condition", lambda: print(""))
tagdict["footer"] = ("while loop", lambda: print(""))
tagdict["nav"] = ("return statement", lambda: print(""))



print("--------start program--------")

with open("test.html", "r") as f: 
    file = f.read()

print(lexer(file))