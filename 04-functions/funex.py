# Ariella Marchuk
#

# CS358 Winter'26 Assignment 4 (Part 1)

# FunEx - an expression language with lambda functions
#
#   expr0 -> "let" ID "=" expr0 "in" expr0
#          | expr
#
#   expr -> "lambda" ID ":" expr 
#         | expr "(" expr ")"    
#         | aexpr 
#
#   aexpr -> aexpr "+" term
#          | aexpr "-" term
#          | term         
#
#   term -> term "*" atom
#         | term "/" atom
#         | atom
#
#   atom -> "(" expr ")"
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: expr0

  ?expr0: "let" ID "=" expr0 "in" expr0 -> let
       | expr

  ?expr: "lambda" ID ":" expr -> func
       | expr "(" expr ")"    -> call
       | aexpr 

  ?aexpr: aexpr "+" term  -> add
       |  aexpr "-" term  -> sub
       |  term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr0 ")"
       | ID             -> var
       | NUM            -> num
 
  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

parser = Lark(grammar, parser='lalr')

# Variable environment
#
class Env(dict):
    def __init__(self, outer=None):
        super().__init__()
        self.outer = outer

    def lookup(self, x):
        if x in self:
            return self[x]
        if self.outer:
            return self.outer.lookup(x)
        raise Exception("Undefined variable: " + x)

    def extend(self, x, v):
        self[x] = v

# Closure
#
class Closure():
    def __init__(self,id,body,env):
        self.id = id
        self.body = body
        self.env = env

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val):  return int(val)
    
    def __init__(self):
        self.env = Env()

    def var(self, name):
        return self.env.lookup(str(name))

    def add(self, x, y):
        return self.visit(x) + self.visit(y)

    def sub(self, x, y):
        return self.visit(x) - self.visit(y)

    def mul(self, x, y):
        return self.visit(x) * self.visit(y)

    def div(self, x, y):
        return self.visit(x) // self.visit(y)

    def let(self, name, val_expr, body_expr):
        val = self.visit(val_expr)
        new_env = Env(self.env)
        new_env.extend(str(name), val)
        old_env = self.env
        self.env = new_env
        result = self.visit(body_expr)
        self.env = old_env
        return result

    def func(self, name, body):
        return Closure(str(name), body, self.env)

    def call(self, fexpr, argexpr):
        closure = self.visit(fexpr)

        if not isinstance(closure, Closure):
            raise Exception("Attempting to call non-function")

        argv = self.visit(argexpr)

        new_env = Env(closure.env)
        new_env.extend(closure.id, argv)

        old_env = self.env
        self.env = new_env

        result = self.visit(closure.body)

        self.env = old_env

        return result

import sys
def main():
    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        print(Eval().visit(tree))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
