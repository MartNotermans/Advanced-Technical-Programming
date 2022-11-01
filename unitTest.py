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

    def testParseParameter(self):
        # <mark> <!--functie parameter-->
        #     <h2>even</h2> <!--parameter name-->
        #     <h3>bool</h3> <!--parameter type-->
        # </mark>
        testTree = lexer.tag("mark")
        testTree.children.append(lexer.tag("h2") )
        testTree.children.append(lexer.tag("h3") )
        testTree.children[0].codeBlock.append(lexer.tag("even") )
        testTree.children[1].codeBlock.append(lexer.tag("bool") )
        
        testStatement = parsmer.parseParameter(testTree)
        awnserStatement = parsmer.boolType("even")
        self.assertEqual(testStatement, awnserStatement, "both boolTypes should be the same")

    #functie nog niet af \/ \/ \/
    def testParseIfStatement(self):
        self.assertEqual(True, True)

    def testParseFuncBody(self):
        self.assertEqual(True, True)

    def testParseFunction(self):
        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()