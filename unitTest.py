import unittest
import lexer

#test lexer
class testLexer(unittest.TestCase):

    def testSplitString(self):
        self.assertEqual(lexer.splitString("testString"), ("t", "estString"), "string should be split in 1st char and rest of the string")

    def testFuncLex(self):
        pass
    
    def testFindTag(self):
        testString = "<html>test"
        index, tag, open = lexer.findTag(testString)
        self.assertEqual(index, 6, "should be 6")
        self.assertEqual(tag, "html", "should be html")
        self.assertEqual(open, True, "should be true")

    def testFindComment(self):
        testString = "<!--comment-->test"
        indexAfterComment = lexer.findComment(testString)
        self.assertEqual(indexAfterComment, 14, "should be 14")

    def testFindEnd(self):
        pass

    def testFindToken(self):
        pass

if __name__ == '__main__':
    unittest.main()