import unittest
from src.lexer import Lexer, TokenLocation
from src.tokens import Token, Identifier, Literal, Keyword, Separator, Operator


class LexerTest(unittest.TestCase):
    def test_empty_file(self):
        with open("empty_test.lmu", "w") as f:
            f.write("")
        lexer = Lexer("empty_test.lmu")
        self.assertEqual(lexer.get_tokens(), [])
        self.assertEqual(lexer.get_locations(), [])

    def test_single_line_comment(self):
        with open("comment_test.lmu", "w") as f:
            f.write("# This is a comment")
        lexer = Lexer("comment_test.lmu")
        self.assertEqual(lexer.get_tokens(), [])
        self.assertEqual(lexer.get_locations(), [])

    def test_simple_identifier(self):
        with open("identifier_test.lmu", "w") as f:
            f.write("variable")
        lexer = Lexer("identifier_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "variable")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], TokenLocation(0, 0, 7))

    def test_simple_literal(self):
        with open("literal_test.lmu", "w") as f:
            f.write("123")
        lexer = Lexer("literal_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Literal)
        self.assertEqual(tokens[0].value, 123)
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], TokenLocation(0, 0, 2))

    def test_simple_keyword(self):
        with open("keyword_test.lmu", "w") as f:
            f.write("class")
        lexer = Lexer("keyword_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Keyword)
        self.assertEqual(tokens[0].value, "class")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], TokenLocation(0, 0, 4))

    def test_simple_separator(self):
        with open("separator_test.lmu", "w") as f:
            f.write(";")
        lexer = Lexer("separator_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Separator)
        self.assertEqual(tokens[0].value, ";")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

    def test_simple_operator(self):
        with open("operator_test.lmu", "w") as f:
            f.write("+")
        lexer = Lexer("operator_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "+")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

    def test_assignment_operator(self):
        with open("assignment_test.lmu", "w") as f:
            f.write("=")
        lexer = Lexer("assignment_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "=")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

    def test_equals_operator(self):
        with open("equals_test.lmu", "w") as f:
            f.write("==")
        lexer = Lexer("equals_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "==")
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0], TokenLocation(0, 0, 1))

    def test_complex_expression(self):
        with open("complex_test.lmu", "w") as f:
            f.write("x = 10 + y;")
        lexer = Lexer("complex_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 6)

        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 2, 2))

        self.assertIsInstance(tokens[2], Literal)
        self.assertEqual(tokens[2].value, 10)
        self.assertEqual(locations[2], TokenLocation(0, 4, 5))

        self.assertIsInstance(tokens[3], Operator)
        self.assertEqual(tokens[3].value, "+")
        self.assertEqual(locations[3], TokenLocation(0, 7, 7))

        self.assertIsInstance(tokens[4], Identifier)
        self.assertEqual(tokens[4].value, "y")
        self.assertEqual(locations[4], TokenLocation(0, 9, 9))

        self.assertIsInstance(tokens[5], Separator)
        self.assertEqual(tokens[5].value, ";")
        self.assertEqual(locations[5], TokenLocation(0, 10, 10))

    def test_multiple_lines(self):
        with open("multiline_test.lmu", "w") as f:
            f.write("x = 10;\ny = 20;")
        lexer = Lexer("multiline_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 8)

        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 2, 2))

        self.assertIsInstance(tokens[2], Literal)
        self.assertEqual(tokens[2].value, 10)
        self.assertEqual(locations[2], TokenLocation(0, 4, 5))

        self.assertIsInstance(tokens[3], Separator)
        self.assertEqual(tokens[3].value, ";")
        self.assertEqual(locations[3], TokenLocation(0, 6, 6))

        self.assertIsInstance(tokens[4], Identifier)
        self.assertEqual(tokens[4].value, "y")
        self.assertEqual(locations[4], TokenLocation(1, 0, 0))

        self.assertIsInstance(tokens[5], Operator)
        self.assertEqual(tokens[5].value, "=")
        self.assertEqual(locations[5], TokenLocation(1, 2, 2))

        self.assertIsInstance(tokens[6], Literal)
        self.assertEqual(tokens[6].value, 20)
        self.assertEqual(locations[6], TokenLocation(1, 4, 5))

        self.assertIsInstance(tokens[7], Separator)
        self.assertEqual(tokens[7].value, ";")
        self.assertEqual(locations[7], TokenLocation(1, 6, 6))

    def test_whitespace_handling(self):
        with open("whitespace_test.lmu", "w") as f:
            f.write("  x   =   10  ;  ")
        lexer = Lexer("whitespace_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 4)

        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 2, 2))

        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 6, 6))

        self.assertIsInstance(tokens[2], Literal)
        self.assertEqual(tokens[2].value, 10)
        self.assertEqual(locations[2], TokenLocation(0, 10, 11))

        self.assertIsInstance(tokens[3], Separator)
        self.assertEqual(tokens[3].value, ";")
        self.assertEqual(locations[3], TokenLocation(0, 14, 14))

    def test_location_tracking(self):
        with open("location_test.lmu", "w") as f:
            f.write("if x == 10 then")
        lexer = Lexer("location_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 4)

        self.assertIsInstance(tokens[0], Keyword)
        self.assertEqual(tokens[0].value, "if")
        self.assertEqual(locations[0], TokenLocation(0, 0, 1))

        self.assertIsInstance(tokens[1], Identifier)
        self.assertEqual(tokens[1].value, "x")
        self.assertEqual(locations[1], TokenLocation(0, 3, 3))

        self.assertIsInstance(tokens[2], Operator)
        self.assertEqual(tokens[2].value, "==")
        self.assertEqual(locations[2], TokenLocation(0, 5, 6))

        self.assertIsInstance(tokens[3], Keyword)
        self.assertEqual(tokens[3].value, "then")
        self.assertEqual(locations[3], TokenLocation(0, 8, 11))

    def test_file_not_found(self):
        with self.assertRaises(SystemExit) as cm:
            Lexer("nonexistent_file.lmu")
        self.assertEqual(cm.exception.code, -1)

    def test_newline_handling(self):
        with open("newline_test.lmu", "w") as f:
            f.write("x =\n10")
        lexer = Lexer("newline_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 2, 2))
        self.assertIsInstance(tokens[2], Literal)
        self.assertEqual(tokens[2].value, 10)
        self.assertEqual(locations[2], TokenLocation(1, 0, 1))

    def test_line_ends_with_operator(self):
        with open("line_ends_operator.lmu", "w") as f:
            f.write("x =")
        lexer = Lexer("line_ends_operator.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0],TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1],TokenLocation(0, 2, 2))

    def test_line_ends_with_separator(self):
        with open("line_ends_separator.lmu", "w") as f:
            f.write("x ;")
        lexer = Lexer("line_ends_separator.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Separator)
        self.assertEqual(tokens[1].value, ";")
        self.assertEqual(locations[1], TokenLocation(0, 2, 2))

    def test_combined_operators(self):
        with open("combined_operators.lmu", "w") as f:
            f.write("<=")
        lexer = Lexer("combined_operators.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "<=")
        self.assertEqual(locations[0], TokenLocation(0, 0, 1))

    def test_not_equal_operator(self):
         with open("not_equal_test.lmu", "w") as f:
              f.write("!=")
         lexer = Lexer("not_equal_test.lmu")
         tokens = lexer.get_tokens()
         locations = lexer.get_locations()

         self.assertEqual(len(tokens), 1)
         self.assertIsInstance(tokens[0], Operator)
         self.assertEqual(tokens[0].value, "!=")
         self.assertEqual(locations[0], TokenLocation(0, 0, 1))

    def test_not_operator(self):
        with open("not_operator_test.lmu", "w") as f:
            f.write("!")
        lexer = Lexer("not_operator_test.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "!")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

    def test_multiple_newlines(self):
        with open("multiple_newlines.lmu", "w") as f:
            f.write("\n\nx = 10\n\n")
        lexer = Lexer("multiple_newlines.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(2, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(2, 2, 2))
        self.assertIsInstance(tokens[2], Literal)
        self.assertEqual(tokens[2].value, 10)
        self.assertEqual(locations[2], TokenLocation(2, 4, 5))

    def test_operator_newline_operator(self):
        with open("operator_newline_operator.lmu", "w") as f:
            f.write("+\n+")

        lexer = Lexer("operator_newline_operator.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)

        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "+")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "+")
        self.assertEqual(locations[1], TokenLocation(1, 0, 0))

    def test_identifier_newline_operator(self):
        with open("identifier_newline_operator.lmu", "w") as f:
            f.write("x\n+")

        lexer = Lexer("identifier_newline_operator.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)

        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))

        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "+")
        self.assertEqual(locations[1], TokenLocation(1, 0, 0))

    def test_operator_followed_by_identifier(self):
        with open("operator_followed_by_identifier.lmu", "w") as f:
            f.write("+x")
        
        lexer = Lexer("operator_followed_by_identifier.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "+")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Identifier)
        self.assertEqual(tokens[1].value, "x")
        self.assertEqual(locations[1], TokenLocation(0, 1, 1))
    
    def test_equals_with_space(self):
        with open("equals_with_space.lmu", "w") as f:
            f.write("= =")
        
        lexer = Lexer("equals_with_space.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "=")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 2, 2))
    
    def test_identifier_equals_newline_literal(self):
        with open("identifier_equals_newline_literal.lmu", "w") as f:
            f.write("x = \n 10")
        
        lexer = Lexer("identifier_equals_newline_literal.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        
        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 2, 2))
        self.assertIsInstance(tokens[2], Literal)
        self.assertEqual(tokens[2].value, 10)
        self.assertEqual(locations[2], TokenLocation(1, 1, 2))
    
    def test_identifier_space_equals_space_literal(self):
        with open("identifier_space_equals_space_literal.lmu", "w") as f:
            f.write("x = 10")
            
        lexer = Lexer("identifier_space_equals_space_literal.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        
        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 2, 2))
        self.assertIsInstance(tokens[2], Literal)
        self.assertEqual(tokens[2].value, 10)
        self.assertEqual(locations[2], TokenLocation(0, 4, 5))

    def test_consecutive_operators(self):
        with open("consecutive_operators.lmu", "w") as f:
            f.write("++")
        lexer = Lexer("consecutive_operators.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "+")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "+")
        self.assertEqual(locations[1], TokenLocation(0, 1, 1))
    
    def test_just_newline(self):
        with open("just_newline.lmu", "w") as f:
            f.write("\n")
        lexer = Lexer("just_newline.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        
        self.assertEqual(len(tokens), 0)
        self.assertEqual(len(locations), 0)
    
    def test_newline_then_equals(self):
        with open("newline_then_equals.lmu", "w") as f:
            f.write("\n=")
        lexer = Lexer("newline_then_equals.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        
        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "=")
        self.assertEqual(locations[0], TokenLocation(1, 0, 0))

    def test_equals_newline(self):
        with open("equals_newline.lmu", "w") as f:
            f.write("=\n")
        lexer = Lexer("equals_newline.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "=")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
    
    def test_identifier_newline_equals(self):
        with open("identifier_newline_equals.lmu", "w") as f:
            f.write("x\n=")
        lexer = Lexer("identifier_newline_equals.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 2)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(1, 0, 0))

    def test_newline_equals_newline(self):
        with open("newline_equals_newline.lmu", "w") as f:
            f.write("\n=\n")
        lexer = Lexer("newline_equals_newline.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()

        self.assertEqual(len(tokens), 1)
        self.assertIsInstance(tokens[0], Operator)
        self.assertEqual(tokens[0].value, "=")
        self.assertEqual(locations[0], TokenLocation(1, 0, 0))
    
    def test_identifier_equals_identifier(self):
        with open("identifier_equals_identifier.lmu", "w") as f:
            f.write("x=y")
        lexer = Lexer("identifier_equals_identifier.lmu")
        tokens = lexer.get_tokens()
        locations = lexer.get_locations()
        
        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], Identifier)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(locations[0], TokenLocation(0, 0, 0))
        self.assertIsInstance(tokens[1], Operator)
        self.assertEqual(tokens[1].value, "=")
        self.assertEqual(locations[1], TokenLocation(0, 1, 1))
        self.assertIsInstance(tokens[2], Identifier)
        self.assertEqual(tokens[2].value, "y")
        self.assertEqual(locations[2], TokenLocation(0, 2, 2))

    def tearDown(self):
        import os
        for filename in ["empty_test.lmu", "comment_test.lmu", "identifier_test.lmu", "literal_test.lmu",
                         "keyword_test.lmu", "separator_test.lmu", "operator_test.lmu", "assignment_test.lmu",
                         "equals_test.lmu", "complex_test.lmu", "multiline_test.lmu",
                         "whitespace_test.lmu", "location_test.lmu", "newline_test.lmu", "line_ends_operator.lmu",
                         "line_ends_separator.lmu", "combined_operators.lmu", "not_equal_test.lmu",
                         "not_operator_test.lmu", "multiple_newlines.lmu", "operator_newline_operator.lmu",
                         "identifier_newline_operator.lmu", "operator_followed_by_identifier.lmu",
                         "equals_with_space.lmu", "identifier_equals_newline_literal.lmu",
                         "identifier_space_equals_space_literal.lmu", "consecutive_operators.lmu",
                         "just_newline.lmu", "newline_then_equals.lmu", "equals_newline.lmu",
                         "identifier_newline_equals.lmu", "newline_equals_newline.lmu",
                         "identifier_equals_identifier.lmu"]:
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    unittest.main()
