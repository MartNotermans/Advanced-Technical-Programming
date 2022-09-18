import sys
sys.setrecursionlimit(200000)

whiteSpace = ' \n\r\t'
taglist = ["html", "body", "section", "h2", "h3", "mark", "figure", "article", "i", "nav", "h4", "summary", "main", "ins", "output"]
closingTagList = ["/html", "/body", "/section", "/h2", "/h3", "/mark", "/figure", "/article", "/i", "/nav", "/h4", "/summary", "/main", "/ins", "/output"]

class tag:
    def __init__(self, name : str):
        self.name = name #the tag as in the html file
        self.children = [] #all other tags containd in this tag
        self.parent = 0

    #moet bij alle tags
    def __str__(self) -> str:
        return self.name

def findTag(file):
    endOfTag = file.find('>')
    if endOfTag == -1:
        return None #geen tag
    
    # 1 om '<' niet mee te nemen
    if file[1:endOfTag] in taglist:
        return file[1:endOfTag]
    elif file[1:endOfTag] in closingTagList:
        return file[1:endOfTag]
    else:
        return None #geen tag

def findComment(file):
    #print(findComment)
    if file[:4] != "<!--":
        return None #geen comment

    #index+4 omdat <!-- 4 chars is, en je daarna begind met zoeken
    endOfComment = file.find("-->")
    if endOfComment == -1:
        return None #halve comment?
    #endOfComment+3 omdat je de eerste char na de comment returnt
    return (file[:endOfComment+3])

def findWord(wordFile):
    nextSpace = wordFile.find(' ')
    if nextSpace == -1:
        return wordFile
    return wordFile[:nextSpace]

def getNextTag(file) -> tuple:
    #ingore whitespaces
    chr = file[0]
    if chr in whiteSpace:
        file = file[1:]
        return lexer(file)

    if chr == '<':
        tag = findTag(file)
        if tag != None:
            #+2 voor de <> van de tag
            file = file[len(tag)+2:]
            return file, tag
        
        comment = findComment(file)
        if comment != None:
            file = file[len(comment):]
            return lexer(file)

    beginNextTag = file.find('<')
    WordFile = file[:beginNextTag]
    word = findWord(WordFile)
    file = file[len(word):]
    return file, word

# def updateTree(newTag, tree = tag):
#     if True:
#         tree = tag()

def lexer(file, lst = [], tree = tag):

    #returnt tuple
    newFileAndTag = getNextTag(file)
    lst.append(newFileAndTag[1])
    file = newFileAndTag[0]
    print(newFileAndTag[1])

    if newFileAndTag[1] == "html":
        tree = tag("html")

    #stop the lexer when the last closing tag is found
    #?????????????????WERKT NIET???????????????????????????
    if newFileAndTag[1] == "/html":
        return lst

    return lexer(file, lst)