import sys
sys.setrecursionlimit(200000)

whiteSpace = ' \n\r\t'
taglist = ["html", "body", "section", "h2", "h3", "mark", "figure", "article", "i", "nav", "h4", "summary", "main", "ins", "output"]
closingTagList = ["/html", "/body", "/section", "/h2", "/h3", "/mark", "/figure", "/article", "/i", "/nav", "/h4", "/summary", "/main", "/ins", "/output"]


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

def lexer(file, tokens = []):
    #stop the lexer when the last closing tag is found
    if len(tokens) > 1:
        if '/html' in tokens:
            return tokens

    #ingore whitespaces
    chr = file[0]
    if chr in whiteSpace:
        file = file[1:]
        return lexer(file, tokens)

    if chr == '<':
        tag = findTag(file)
        if tag != None:
            tokens.append(tag)
            #+2 voor de <> van de tag
            file = file[len(tag)+2:]
            return lexer(file, tokens)
        
        comment = findComment(file)
        if comment != None:
            file = file[len(comment):]
            return lexer(file, tokens)

    beginNextTag = file.find('<')
    WordFile = file[:beginNextTag]
    word = findWord(WordFile)
    tokens.append(word)
    file = file[len(word):]
    return lexer(file, tokens)