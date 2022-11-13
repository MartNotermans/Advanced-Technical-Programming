import unittest
import lexer
import parsmer

class testLexer(unittest.TestCase):

    def testSplitString(self):
        self.assertEqual(lexer.splitString("testString"), ("t", "estString"), "string should be split in 1st char and rest of the string")

    def testFuncLex(self):
        #<html>
        #   <body><!--comment-->
        #       <section>test</section>
        #   </body>
        #</html>
        testFile = "<html><body><!--comment--><section>even</section></body></html>"
        
        testTree = lexer.tag("root")
        testTree.children.append(lexer.tag("html") )
        testTree.children[0].children.append(lexer.tag("body") )
        testTree.children[0].children[0].children.append(lexer.tag("section") )
        testTree.children[0].children[0].children[0].codeBlock.append(lexer.token("even") )
        
        # print("---testtree---")
        # testTree.printTree()

        emptyFile, tree = lexer.funcLex(testFile, lexer.tag("root"))
        # print("---tree---")
        # tree.printTree()

        self.assertEqual(tree, testTree, "trees should be the same")

    def testFindTag(self):
        testString = "<html>test"
        index, tag, open = lexer.findTag(testString)
        self.assertEqual(index, 6, "should be 6")
        self.assertEqual(tag, "html", "should be html")
        self.assertTrue(open, "should be True")

    def testFindComment(self):
        testString = "<!--comment-->test"
        self.assertEqual(lexer.findComment(testString), 14, "should be 14")

    def testFindComment2(self):
        testString = "<!--commenttest"
        self.assertEqual(lexer.findComment(testString), None, "halve a comment, should be None")

    def testFindComment3(self):
        testString = "commenttest"
        self.assertEqual(lexer.findComment(testString), None, "not a comment, should be None")

    def testFindEnd(self):
        testString = "0123456789A123"
        self.assertEqual(lexer.findEnd(testString, lambda c: c.isnumeric()), 10, "should be 10")
        self.assertEqual(lexer.findEnd(testString, lambda c: c == 'B'), 0, "should be 0")
        self.assertEqual(lexer.findEnd(testString, lambda c: c.isalnum()), 14, "no end, should be 14")

    def testFindToken(self):
        testString = "even</h2>"
        testToken, testTokenLengh = lexer.findToken(testString)
        self.assertEqual(testToken.name, "even", "name should be even" )
        self.assertEqual(testTokenLengh, 4, "lengh should be 4")

class testParser(unittest.TestCase):
    #functie nog niet af \/
    def testParser(self):
        self.assertEqual(True, True)
    
    def testIndexNoError(self):
        testList = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(parsmer.indexNoError(testList, 'b'), 1, "should be 1, b on place 1")
        self.assertEqual(parsmer.indexNoError(testList, 'f'), -1, "should be -1, f not in list")

    def testIndexAllNoError(self):
        testList = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']
        
        self.assertEqual(parsmer.indexAllNoError(testList, 'b'), [1, 6], "should be 1 and 6, b on place 1 and 6")
        self.assertEqual(parsmer.indexAllNoError(testList, 'f'), [], "should be empty list, f not in list")

    def testCheckPrecedence(self):
        parenthesisTkn = lexer.parenthesesToken('(')
        multiTkn= lexer.operatorToken('*')
        plusTkn = lexer.operatorToken('+')
        equalTkn = lexer.operatorToken('==')
        self.assertEqual(parsmer.checkPrecedence(multiTkn, parenthesisTkn), 1), "should be 1, parenthesis goes before multiplication"
        self.assertEqual(parsmer.checkPrecedence(equalTkn, plusTkn), 2), "should be 2, plus goes before equals"
        self.assertEqual(parsmer.checkPrecedence(plusTkn, plusTkn), 3), "should be 3, the tokens are the same"

    def testShuntingYardToRPN(self):
        #5+5
        codeBlock1 = [
            lexer.numberToken('5'),
            lexer.operatorToken('+'),
            lexer.numberToken('5')
        ]
        #55+
        output1 = [
            lexer.numberToken('5'),
            lexer.numberToken('5'),
            lexer.operatorToken('+')
        ]
        self.assertEqual(parsmer.shuntingYardToRPN(codeBlock1, [], []), output1)

        #(2+3)*q
        codeBlock2 = [
            lexer.parenthesesToken('('),
            lexer.numberToken('2'),
            lexer.operatorToken('+'),
            lexer.numberToken('3'),
            lexer.parenthesesToken(')'),
            lexer.operatorToken('*'),
            lexer.identifierToken('q')
        ]
        #23+q*
        output2 = [
            lexer.numberToken('2'),
            lexer.numberToken('3'),
            lexer.operatorToken('+'),
            lexer.identifierToken('q'),
            lexer.operatorToken('*')
        ]
        self.assertEqual(parsmer.shuntingYardToRPN(codeBlock2, [], []), output2)

        #voorbeeld uit video https://www.youtube.com/watch?v=Wz85Hiwi5MY
        #(5*4+3*)-1
        codeBlock3 = [
            lexer.parenthesesToken('('),
            lexer.numberToken('5'),
            lexer.operatorToken('*'),
            lexer.numberToken('4'),
            lexer.operatorToken('+'),
            lexer.numberToken('3'),
            lexer.operatorToken('*'),
            lexer.parenthesesToken(')'),
            lexer.operatorToken('-'),
            lexer.numberToken('1')
        ]

        output3 = [
            lexer.numberToken('5'),
            lexer.numberToken('4'),
            lexer.operatorToken('*'),
            lexer.numberToken('3'),
            lexer.operatorToken('*'),
            lexer.operatorToken('+'),
            lexer.numberToken('1'),
            lexer.operatorToken('-')
        ]
        self.assertEqual(parsmer.shuntingYardToRPN(codeBlock3, [], []), output3)

         #4
        codeBlock4 = [lexer.numberToken('4')]

        output4 = [lexer.numberToken('4')]
        self.assertEqual(parsmer.shuntingYardToRPN(codeBlock4, [], []), output4)

    def testOperatorTocodeBlockStatement(self):
        self.assertEqual(parsmer.operatorTocodeBlockStatement(lexer.operatorToken('+')), parsmer.plusOperator(), "should be plusoperator")

    def testRPNtoTree(self):
        #23+q*
        codeBlockRPN1 = [
            lexer.numberToken('2'),
            lexer.numberToken('3'),
            lexer.operatorToken('+'),
            lexer.identifierToken('q'),
            lexer.operatorToken('*')
        ]

        #     *
        #   +   q
        #  2 3
        output = parsmer.multiplicationOperator()
        output.rightSide = parsmer.codeBlockVariable('q')
        output.leftSide = parsmer.plusOperator()
        output.leftSide.rightSide = parsmer.codeBlockCanstant(3)
        output.leftSide.leftSide = parsmer.codeBlockCanstant(2)

        newTree = parsmer.operatorTocodeBlockStatement(codeBlockRPN1.pop() )
        parsmer.RPNtoTree(codeBlockRPN1, newTree)
        self.assertEqual(newTree, output)

    def testParseCodeBlock(self):
        codeBlockRPN1 = [lexer.numberToken('2')]
        self.assertEqual(parsmer.parseCodeBlock(codeBlockRPN1), parsmer.codeBlockCanstant(2))

    def testParseParameter(self):
        # <mark>even</mark> <!--functie parameter-->

        testTree = lexer.tag("mark")
        testTree.codeBlock.append(lexer.identifierToken("even") )
        
        testStatement = parsmer.parseParameter(testTree)
        awnserStatement = parsmer.initVariable("even")
        self.assertEqual(testStatement, awnserStatement, "both tokens should be the same")

    #functie nog niet af \/ \/ \/
    def testParseIfStatement(self):
        self.assertEqual(True, True)

    def testInitialiseVariable(self):
        self.assertEqual(True, True)

    def testparseWhile(self):
        self.assertEqual(True, True)

    def testparseFunctionCall(self):
        self.assertEqual(True, True)
    
    def testParseTagInFuncBody(self):
        self.assertEqual(True, True)

    #overbodig???
    def testParseFuncBody(self):
        self.assertEqual(True, True)

    def testParseFunction(self):
        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()