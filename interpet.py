import sys
sys.setrecursionlimit(200000)
import string

whiteSpace = ' \n\r\t'
validTagBeginChars = 'abcdefghijklmnopqrstuvwxyz'
validTagChars = 'abcdefghijklmnopqrstuvwxyz0123456789'

class body(tag)

class tag:
    def __init__(self, name : str, file, index):
        self.name = name
        self.children = []
        self.code = ""
        self.closingTagIndex = 0
        print(self.name, "found!")
        print(index)


        #todo
        #niet in constructor maar in eigen functie lexen
        #kan recursief
        i = index
        while i < len(file):
            if file[i] == '<':
                #+1 is na de <
                if file[i+1] == '/':
                    #als het zijn eigen closing tag is
                    #i+2:i+2+len(self.name) is de index van het begin en het eind van de naam van de closing tag
                    if file[i+2:i+2+len(self.name)] == self.name:
                        #i + 3 + len(self.name) is het eerste char na de closing tag
                        self.closingTagIndex = i + 3 + len(self.name)
                        if len(self.children) == 0:
                            #index is einde opening tag, i is begin closing tag
                            self.code = file[index:i]
                        break
                    else:
                        #syntax error
                        pass
                #+1 is na de <
                elif file[i+1] in validTagBeginChars:
                    #+2 is na het eerste char van de tag naam
                    for j in range (i+2, len(file) ):
                        if file[j] == '>':
                            #+1 is het eerste char van de tagnaam
                            #j+1 is de index van de char na het einde van de tag
                            child = tag(file[i+1:j], file, j+1)
                            self.children.append(child)
                            #de -1 is omdat i later +=1 wordt gemaakt
                            i = child.closingTagIndex-1
                            break
            i+=1

        

def parser():
    with open("test.html", "r") as f:
        file = f.read()
        i = 0
        while i < len(file):
            chr = file[i]
            if chr in whiteSpace:
                i+=1
            elif chr == '<':
                #+6 is de lengte van <html>
                if file[i:i+6] == "<html>":
                    #i+6 is het eerste char na <html>
                    root = tag("html", file, i+6 )
                    break
            else:
                i+=1



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


parser()

# if file[i+1] == ' ' and file[i-1] == ' ':
#     #items.append("<")
#     i+=1