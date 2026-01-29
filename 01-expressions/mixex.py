# Ariella Marchuk
# CS358 Winter'26 Assignment 1 (Part 2)
# MixEx - a Mixed expression language
############################################

from lark import Lark, v_args
from lark.visitors import Interpreter

# 0. Grammar
#
# Merge grammars from arithex.py (Exercise 2) and boolex.py;
# you need to figure out the ordering of the grammar rules
# based on operator precedence
##########################################################

grammar = """
?start: expr

?expr: expr "or" andex        -> orop
     | andex

?andex: andex "and" notex     -> andop
      | notex

?notex: "not" notex           -> notop
      | aexpr

?aexpr: aexpr "+" term        -> add
     | aexpr "-" term         -> sub
     | term

?term: term "*" atom          -> mul
     | term "/" atom          -> div
     | atom

?atom: "(" expr ")"
     | NUM                    -> num
     | "True"                 -> truev
     | "False"                -> falsev

%import common.INT -> NUM
%ignore " "
"""

# 1. Parser
#
# It should return an AST.
#
# E.g. For input "1 + 2 or True and 3"
#      the AST should look like:
#          orop
#            add
#              num 1
#              num 2
#            andop
#              truev
#              num 3
#########################################################
parser = Lark(grammar)

# 2. Interpreter
#
# Evaluate an AST to a Boolean value.
# E.g. Evaluating the above AST should result in 3
#########################################################
@v_args(inline=True)
class Eval(Interpreter):

    # ... need code
    def num(self, val):
        return int(val)

    def truev(self):
        return True

    def falsev(self):
        return False

    def add(self, left, right):
        return self.visit(left) + self.visit(right)

    def sub(self, left, right):
        return self.visit(left) - self.visit(right)

    def mul(self, left, right):
        return self.visit(left) * self.visit(right)

    def div(self, left, right):
        return self.visit(left) // self.visit(right)

    def notop(self, val):
        return not self.visit(val)

    def andop(self, left, right):
        leftv = self.visit(left)
        if leftv:
            return self.visit(right)
        return leftv

    def orop(self, left, right):
        leftv = self.visit(left)
        if leftv:
            return leftv
        return self.visit(right)

# 3. Convert the AST to a prefix form
#
# E.g. Converting the above AST should return 
#      or + 1 2 and True 3
########################################################
@v_args(inline=True)
class toPrefix(Interpreter):

    # ... need code
    def num(self, val):
        return str(val)

    def truev(self):
        return "True"

    def falsev(self):
        return "False"

    def add(self, left, right):
        return "+ " + self.visit(left) + " " + self.visit(right)

    def sub(self, left, right):
        return "- " + self.visit(left) + " " + self.visit(right)

    def mul(self, left, right):
        return "* " + self.visit(left) + " " + self.visit(right)

    def div(self, left, right):
        return "/ " + self.visit(left) + " " + self.visit(right)

    def notop(self, val):
        return "not " + self.visit(val)

    def andop(self, left, right):
        return "and " + self.visit(left) + " " + self.visit(right)

    def orop(self, left, right):
        return "or " + self.visit(left) + " " + self.visit(right)

# main
##################################################################
def main():
    while True:
        try:
            expr = input("Enter a mixed expr: ")
            tree = parser.parse(expr)
            print(expr)
            print(tree.pretty(), end="")
            print("Eval: ", Eval().visit(tree))
            print("Prefix: ", toPrefix().visit(tree))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()

