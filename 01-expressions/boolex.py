# Ariella Marchuk
# CS358 Winter'26 Assignment 1 (Part 1)
# BoolEx - a Boolean expression language
#########################################

from lark import Lark, v_args
from lark.visitors import Interpreter

# 0. Grammar
#
# (a) port BoolEx's grammar here
# (b) attach AST nodes: andop, orop, notop, truev, falsev
##########################################################

# boolean expressions follow this structure:
# expr -> expr "or" term 
#       | term

# term -> term "and" factor
#       | factor

# factor -> "not" factor
#       | "True"
#       | "False"
#       | "(" expr ")"

# precedence from highest to lowest:
# not
# and
# or
########################################

grammar = """
?start: expr

?expr: expr "or" term   -> orop
     | term

?term: term "and" factor -> andop
     | factor

?factor: "not" factor   -> notop
       | "True"         -> truev
       | "False"        -> falsev
       | "(" expr ")"

%ignore " "
"""


# 1. Parser
#
# It should return an AST.
#
# E.g. For input "(True or not False) and True",
#      the AST should look like:
#          andop  
#            orop
#              truev
#              notop
#                falsev
#            truev
#################################################
parser = Lark(grammar)

# 2. Interpreter
#
# Evaluate an AST to a Boolean value.
#
# E.g. Evaluating the above AST should result in True
####################################################
@v_args(inline=True)
class Eval(Interpreter):

    # ... need code
    def truev(self):
        return True
    def falsev(self):
        return False

    def notop(self, val):
        return not self.visit(val)

    def andop(self, left, right):
        if not self.visit(left):
            return False
        return self.visit(right)

    def orop(self, left, right):
        if self.visit(left):
            return True
        return self.visit(right)

# 3. Convert the AST to a prefix form
#
# E.g. Converting the above AST should return 
#      and or True not False True
####################################################
@v_args(inline=True)
class toPrefix(Interpreter):

    # ... need code
    def truev(self):
        return "True"

    def falsev(self):
        return "False"

    def notop(self, val):
        return "not " + self.visit(val)

    def andop(self, left, right):
        return "and " + self.visit(left) + " " + self.visit(right)

    def orop(self, left, right):
        return "or " + self.visit(left) + " " + self.visit(right)

def main():
    while True:
        try:
            expr = input("Enter a bool expr: ")
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
