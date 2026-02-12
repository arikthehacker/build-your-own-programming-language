###########################################################
# letex.py
# Name: Ariella Marchuk
# Assignment 2: Handling Variables & Statements
# CS 358 Principles of Programming Languages, Winter 2026
# amarchuk@pdx.edu
############################################################

###############
# QUESTION 1: #  LetEx: An expression language w/ variable bindings
###############

# 1.1 (Parser)
#     * Copy arithex.py -> letex.py. 
#     * Extend the grammar part of the program to include the new let construct & variable
#     * Name the corresponding AST nodes let and var. 
#     * Test the parser portion of this program.

from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
?start: expr0

?expr0: "let" ID "=" expr0 "in" expr0   -> let
      | expr

?expr: expr "+" term   -> add
     | expr "-" term   -> sub
     | term
?term: term "*" atom   -> mul
     | term "/" atom   -> div
     | atom
?atom: "(" expr0 ")"
     | NUM             -> num
     | ID              -> var

%import common.INT -> NUM
%import common.CNAME -> ID
%ignore " "
"""

# create the parser from the grammar above
parser = Lark(grammar)

# 1.2 (Environment) Take mutable dictionary environment code from lecture notes
class Env(dict):
    def extend(self, x, v):
        if x in self:
            self[x].insert(0, v)
        else:
            self[x] = [v]

    def lookup(self, x):
        vals = super().get(x)
        if not vals:
            raise Exception("Undefined variable: " + x)
        return vals[0]

    def retract(self, x):
        assert x in self, "Undefined variable: " + x
        self[x].pop(0)

# 1.3 (Interpreter) Extend Eval() class to make letex.py a complete interpreter for LetEx
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        self.env = Env()

    def var(self, name):
        return self.env.lookup(str(name))

    def num(self, val):
        return int(val)

    def add(self, left, right):
        return self.visit(left) + self.visit(right)

    def sub(self, left, right):
        return self.visit(left) - self.visit(right)

    def mul(self, left, right):
        return self.visit(left) * self.visit(right)

    def div(self, left, right):
        return self.visit(left) // self.visit(right)

    def let(self, name, value_expr, body_expr):
        val = self.visit(value_expr)
        self.env.extend(str(name), val)
        result = self.visit(body_expr)
        self.env.retract(str(name))
        return result

@v_args(inline=True)
class ToPrefix(Interpreter):
    def num(self, val):
        return str(val)

    def add(self, left, right):
        return "+ " + self.visit(left) + " " + self.visit(right)

    def sub(self, left, right):
        return "- " + self.visit(left) + " " + self.visit(right)

    def mul(self, left, right):
        return "* " + self.visit(left) + " " + self.visit(right)

    def div(self, left, right):
        return "/ " + self.visit(left) + " " + self.visit(right)

def main():
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(tree.pretty())
            print("tree.Eval() =", Eval().visit(tree))
            print("tree.toPrefix() =", ToPrefix().visit(tree))
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
