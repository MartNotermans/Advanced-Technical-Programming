from typing import Tuple
import sys
sys.setrecursionlimit(200000)
import string

whiteSpace = ' \n\r\t'
validTagChars = 'abcdefghijklmnopqrstuvwxyz0123456789'

#class body(tag)

class tag:
    def __init__(self, name : str):
        self.name = name #the tag as in the file
        self.children = [] #all other tags containd in this tag
        self.code = "" #code contained in this tag
        self.closingTagIndex = 0
        print(self.name, "found!")


#Tuple[is het een tag, "naam van de tag", open of closing tag, first char after tag]
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
        index+=1

    if not file[index] in validTagChars:
        #geen tag, check if <>
        return(False, "", isOpenTag, 0)

    #index+1 opdat eerste char al gecheckt is
    for i in range (index+1, len(file) ):
        if file[i] == '>':
            #i+1 omdat je het eerste char na de tag returnt
            return (True, file[index: i], isOpenTag, i+1)
        elif not file[i] in validTagChars:
            return(False, "", isOpenTag, 0)

    #syntax error
    return (False, "", isOpenTag, 0)

#Tuple[is a comment, index of char na comment]
def checkIfComment(file, index) -> Tuple[bool, int]:
    if file[index: index+4] != "<!--":
        return (False, 0)

    for i in range(index+4, len(file)):
        #i+3 is het eerste char na de closing tag
        if file[i: i+3] == "-->":
            return (True, i+3)
    
    #syntax error
    return (False, 0)


def parser(file, currentTag : tag, index):
    #bool om bij te houden of er text in de huidige tag zit
    #als er text en childern in de huidige tag zitten heb je een syntax error
    foundTxt = False

    i = index
    while i < len(file):
        isTag = checkIfTag(file, i)
        #[0] is a valid tag?
        if isTag[0]:
            #[2] is an open tag?
            if isTag[2]:
                newTag = tag(isTag[1])
                currentTag.children.append(newTag)
                #isTag[3] is de eerste char na de huidige tag
                parser(file, newTag, isTag[3])
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


        

#infinite loop!!!
def startParser():
    i = 0
    with open("test.html", "r") as f:
        file = f.read()
        while i < len(file):
            chr = file[i]
            if chr in whiteSpace:
                i+=1
            elif chr == '<':
                #+6 is de lengte van <html>
                if file[i:i+6] == "<html>":
                    #i+6 is het eerste char na <html>
                    root = tag("html")
                    break
                else:
                    i+=1
            else:
                i+=1
    parser(file, root, i+6)
    return root



#dict met tags
tagdict = dict()
tagdict["<html>"] = ("fileStart", lambda: print("file Start"))
tagdict["</html>"] = ("fileEnd", lambda: print("file End"))
tagdict["<Body>"] = ("bodyStart", lambda: print("body Start"))
tagdict["</Body>"] = ("bodyEnd", lambda: print("body End"))
tagdict["<section>"] = ("functionStart", lambda: print("function Start"))
tagdict["</section>"] = ("functionEnd", lambda: print("function End"))
tagdict["<h2>"] = ("functionNameStart", lambda: print("function Name Start"))
tagdict["</h2>"] = ("functionNameEnd", lambda: print("function Name End"))
tagdict["<h3>"] = ("functionParameterStart", lambda: print("function parameter Start"))
tagdict["</h3>"] = ("functionParameterEnd", lambda: print("function parameter End"))
tagdict["<article>"] = ("functionBodyStart", lambda: print("function Body Start"))
tagdict["</article>"] = ("functionBodyEnd", lambda: print("function Body End"))
tagdict["<h4>"] = ("ifStatementStart", lambda: print("if Statement Start"))
tagdict["</h4>"] = ("ifStatementEnd", lambda: print("if Statement  End"))


startParser()
