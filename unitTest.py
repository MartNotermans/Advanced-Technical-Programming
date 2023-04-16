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

        emptyFile, tree = lexer.lex(testFile, lexer.tag("root"))
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
        self.assertEqual(parsmer.indexNoError(testList, 'b', 0), 1, "should be 1, b on place 1")
        self.assertEqual(parsmer.indexNoError(testList, 'f', 0), -1, "should be -1, f not in list")

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
        output.leftSide.rightSide = parsmer.codeBlockConstant(3)
        output.leftSide.leftSide = parsmer.codeBlockConstant(2)

        newTree = parsmer.operatorTocodeBlockStatement(codeBlockRPN1.pop() )
        parsmer.RPNtoTree(codeBlockRPN1, newTree)
        self.assertEqual(newTree, output)

    def testParseCodeBlock(self):
        codeBlockRPN1 = [lexer.numberToken('2')]
        self.assertEqual(parsmer.parseCodeBlock(codeBlockRPN1), parsmer.codeBlockConstant(2))

    def testParseParameter(self):
        # <mark>even</mark> <!--functie parameter-->

        testTree = lexer.tag("mark")
        testTree.codeBlock.append(lexer.identifierToken("even") )
        
        testStatement = parsmer.parseParameter(testTree)
        awnserStatement = parsmer.initVariable("even")
        self.assertEqual(testStatement, awnserStatement, "both tokens should be the same")

    def testParseIfStatement(self):
        # if(n==0){
        #     return true
        # }else{
        #     return false
        # }

        # <article> <!-- if statement-->
        #     <i>n == 0</i> <!--if statement condition-->
        #     <figure> <!--if statement body-->
        #         <nav> <!--return-->
        #             <h4>1</h4> <!--true-->
        #         </nav>
        #     </figure>
        #     <figure> <!--else statement body-->
        #         <nav> <!--return-->
        #             <h4>0</h4> <!--false-->
        #         </nav>
        #     </figure>
        # </article>

        #dit is de output van de lexer
        testTree = lexer.tag("article")
        testTree.children.append(lexer.tag("i"))
        testTree.children.append(lexer.tag("figure"))
        testTree.children.append(lexer.tag("figure"))

        testTree.children[0].codeBlock = [
            lexer.identifierToken('n'),
            lexer.operatorToken('=='),
            lexer.numberToken('0')
        ]
        testTree.children[1].children.append(lexer.tag("nav"))
        testTree.children[1].children[0].children.append(lexer.tag("h4"))
        testTree.children[1].children[0].children[0].codeBlock = [lexer.numberToken('1')]

        testTree.children[2].children.append(lexer.tag("nav"))
        testTree.children[2].children[0].children.append(lexer.tag("h4"))
        testTree.children[2].children[0].children[0].codeBlock = [lexer.numberToken('0')]



        #check
        ifCheck = parsmer.ifStatement()

        operator = parsmer.compareEqual()
        operator.leftSide = parsmer.codeBlockVariable('n')
        operator.rightSide = parsmer.codeBlockConstant(0)
        ifCheck.condition = operator

        ifReturn   = [parsmer.returnStatement(parsmer.codeBlockConstant(1))]
        elseReturn = [parsmer.returnStatement(parsmer.codeBlockConstant(0))]
        ifCheck.ifBody = ifReturn
        ifCheck.elseBody = elseReturn

        temp = parsmer.parseIfStatement(testTree)

        self.assertEqual(temp, ifCheck)

    def testInitialiseVariable(self):
        # <ins> <!--initialise-->
        #     <h2>var</h2><!--name-->
        #     <h4>0</h4>  <!--inisialize als 0, dummy waarde-->
        # </ins>

        testTree = lexer.tag("ins")
        testTree.children.append(lexer.tag("h2"))
        testTree.children[0].codeBlock = [lexer.identifierToken('var')]
        testTree.children.append(lexer.tag("h4"))
        testTree.children[1].codeBlock = [lexer.numberToken('0')]
        
        variableToCheck = parsmer.initialiseVariable(testTree)

        compareVariable = parsmer.initVariable()
        compareVariable.name = 'var'
        compareVariable.value = parsmer.codeBlockConstant(0)

        self.assertEqual(variableToCheck, compareVariable)

    def testparseWhile(self):

        # while(n>=1){
        #    result += n;
        #    n--;
        # }

        # <footer> <!--while-->
        #     <i>n >= 1</i>
        #     <figure> <!--body-->
        #         <ins>
        #             <h2>result</h2> <!--variable name-->
        #             <h4>result + n</h4> <!--value-->
        #         </ins>
        #         <ins>
        #             <h2>n</h2> <!--variable name-->
        #             <h4>n - 1</h4> <!--value-->
        #         </ins>
        #     </figure>
        # </footer>

        testTree = lexer.tag("footer")
        condition = lexer.tag("i")
        condition.codeBlock = [
            lexer.identifierToken('n'),
            lexer.operatorToken('>='),
            lexer.numberToken('1')
        ]
        body = lexer.tag("figure")
        incrementResult = lexer.tag("ins")
        resultName = lexer.tag("h2")
        resultName.codeBlock = [lexer.identifierToken('result')]
        resultValue = lexer.tag("h4")
        resultValue.codeBlock = [
            lexer.identifierToken('result'),
            lexer.operatorToken('+'),
            lexer.identifierToken('n')
        ]
        decrementN = lexer.tag("ins")
        nName = lexer.tag("h2")
        nName.codeBlock = [lexer.identifierToken('n')]###
        nValue = lexer.tag("h4")
        nValue.codeBlock = [
            lexer.identifierToken('n'),
            lexer.operatorToken('-'),
            lexer.numberToken('1')
        ]

        testTree.children.append(condition)
        testTree.children.append(body)
        body.children.append(incrementResult)
        incrementResult.children.append(resultName)
        incrementResult.children.append(resultValue)
        body.children.append(decrementN)
        decrementN.children.append(nName)
        decrementN.children.append(nValue)

        parsedTestTree = parsmer.parseWhile(testTree)



        compareWhile = parsmer.whileLoop()
        compareWhileCondition = parsmer.compareBiggerOrEqual()
        compareWhileCondition.leftSide = parsmer.codeBlockVariable('n')
        compareWhileCondition.rightSide = parsmer.codeBlockConstant(1)
        
        compareWhileLoop = []

        initVarResult = parsmer.initVariable()
        initVarResult.name = 'result'
        initVarResult.value = parsmer.plusOperator()
        initVarResult.value.leftSide = parsmer.codeBlockVariable('result')
        initVarResult.value.rightSide = parsmer.codeBlockVariable('n')

        initVarN = parsmer.initVariable()
        initVarN.name = 'n'
        initVarN.value = parsmer.minusOperator()
        initVarN.value.leftSide = parsmer.codeBlockVariable('n')
        initVarN.value.rightSide = parsmer.codeBlockConstant(1)

        compareWhileLoop.append(initVarResult)
        compareWhileLoop.append(initVarN)

        compareWhile.condition = compareWhileCondition
        compareWhile.loop = compareWhileLoop

        self.assertEqual(parsedTestTree, compareWhile)

    def testparseFunctionCall(self):
        # <summary> <!--functie aanroepen-->
        #     <h2>sommig</h2> <!--functie name-->
        #     <h3>n</h3> <!--place to return to, variable die al bestaat-->
        #     <h4>inputVar</h4> <!--functie parameter-->
        # </summary>

        callTag = lexer.tag("summary")
        funcName = lexer.tag("h2")
        #funcName.name = "sommig"
        #funcName.codeBlock.append("sommig")
        funcName.codeBlock.append(lexer.identifierToken("sommig") )
        
        returnPlaceName = lexer.tag("h3")
        returnPlaceName.codeBlock.append(lexer.identifierToken("n") )
        funcParameter = lexer.tag("h4")
        #funcParameter.codeBlock = "inputVar"
        funcParameter.codeBlock.append(lexer.identifierToken("inputVar") )
        callTag.children.append(funcName)
        callTag.children.append(returnPlaceName)
        callTag.children.append(funcParameter)

        parsedFuncCall = parsmer.parseFunctionCall(callTag)

        compareFuncCallStatement = parsmer.functionCallStatement()
        compareFuncCallStatement.functionName = 'sommig'
        compareFuncCallStatement.returnVariable = 'n'
        compareFuncCallStatement.parameters = [parsmer.codeBlockVariable('inputVar')]

        self.assertEqual(parsedFuncCall, compareFuncCallStatement)
    
if __name__ == '__main__':
    unittest.main()