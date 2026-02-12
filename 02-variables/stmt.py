##########################################################
# stmt.py
# Name: Ariella Marchuk
# Assignment 2: Handling Variables & Statements
# CS 358 Principles of Programming Languages, Winter 2026
# amarchuk@pdx.edu
############################################################

###############
# QUESTION 2: #  Stmt: A Simple Statement Language
###############

# 2. implement an interpreter using Lark for this language. 
#     * grammar above is already in the right form for Lark parser
#     * copy arithex.py to stmt.py to use as its starting version

import sys 

from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
?start: stmt

?stmt: ID "=" expr                -> assign
     | "if" "(" expr ")" stmt "else" stmt   -> ifelse
     | "if" "(" expr ")" stmt               -> ifonly
     | "while" "(" expr ")" stmt            -> while_stmt
     | "print" "(" expr ")"                 -> print
     | "{" stmt (";" stmt)* "}"             -> block

?expr: expr "+" term   -> add
     | expr "-" term   -> sub
     | term

?term: term "*" atom   -> mul
     | term "/" atom   -> div
     | atom

?atom: "(" expr ")"
     | ID              -> var
     | NUM             -> num

%import common.CNAME -> ID
%import common.INT -> NUM
%import common.WS
%ignore WS
"""

# create the parser from the grammar above
parser = Lark(grammar)

class Env(dict):
    def lookup(self, x):
        return self.get(x, 0)

    def assign(self, x, v):
        self[x] = v

@v_args(inline=True)
class Eval(Interpreter):

    def __init__(self):
        self.env = Env()

    def num(self, val):
        return int(val)

    def var(self, name):
        return self.env.lookup(str(name))

    def add(self, left, right):
        return self.visit(left) + self.visit(right)

    def sub(self, left, right):
        return self.visit(left) - self.visit(right)

    def mul(self, left, right):
        return self.visit(left) * self.visit(right)

    def div(self, left, right):
        return self.visit(left) // self.visit(right)

    def assign(self, name, expr):
        val = self.visit(expr)
        self.env.assign(str(name), val)

    def print(self, expr):
        val = self.visit(expr)
        print(val)

    def ifonly(self, cond, stmt):
        if self.visit(cond) != 0:
            self.visit(stmt)

    def ifelse(self, cond, stmt1, stmt2):
        if self.visit(cond) != 0:
            self.visit(stmt1)
        else:
            self.visit(stmt2)

    def while_stmt(self, cond, stmt):
        while self.visit(cond) != 0:
            self.visit(stmt)

    def block(self, first_stmt, *rest):
        self.visit(first_stmt)
        for s in rest:
            self.visit(s)

def main():
    if len(sys.argv) > 1:
        # run file
        with open(sys.argv[1], 'r') as f:
            prog = f.read()
        tree = parser.parse(prog)
        Eval().visit(tree)
    else:
        while True:
            try:
                prog = input("Enter a stmt: ")
                tree = parser.parse(prog)
                print(tree.pretty())
                Eval().visit(tree)
            except EOFError:
                break
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()
