# Ariella Marchuk
#

# CS358 Winter'26 Assignment 4 (Part 2)

# Stmt3 - an imperative language with functions
#
#   stmt -> "var" ID "=" expr
#         | ID "=" expr 
#         | "if" "(" expr ")" stmt ["else" stmt]
#         | "while" "(" expr ")" stmt
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#         | "def" ID "(" ID ")" ":" body    
#         | ID "(" expr ")"
#
#   body -> "{" (stmt ";")* "return" expr "}"
#         | "return" expr
#
#   expr -> aexpr "<"  aexpr
#         | aexpr "==" aexpr
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
#   atom: "(" expr ")"
#         | ID "(" expr ")"
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: stmt

   stmt: "var" ID "=" expr            -> decl
       | ID "=" expr                  -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
       | "while" "(" expr ")" stmt    -> whstmt
       | "print" "(" expr ")"         -> prstmt
       | "{" stmt (";" stmt)* "}"     -> block      
       | "def" ID "(" ID ")" ":" body -> fdef
       | ID "(" expr ")"              -> call

   body: "{" (stmt ";")* "return" expr "}" -> body
       | "return" expr                -> sbody

  ?expr: aexpr "<"  aexpr  -> less
       | aexpr "==" aexpr  -> equal
       | aexpr 

  ?aexpr: aexpr "+" term  -> add
       |  aexpr "-" term  -> sub
       |  term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr ")"
       | ID "(" expr ")"  -> call
       | ID               -> var
       | NUM              -> num

  COMMENT: "#" /[^\\n]*/ "\\n"
  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore COMMENT
  %ignore WS
"""

parser = Lark(grammar, parser='lalr')

# Variable environment
#
class Env(dict):
    prev = []

    def openScope(self):
        new_env = Env()
        new_env.prev = self.prev + [self]
        return new_env

    def closeScope(self):
        if not self.prev:
            raise Exception("No outer scope")
        return self.prev[-1]

    def extend(self, x, v):
        if x in self:
            raise Exception("[Stmt3] Variable already defined")
        self[x] = v

    def lookup(self, x):
        if x in self:
            return self[x]
        for e in reversed(self.prev):
            if x in e:
                return e[x]
        raise Exception("[Stmt3] Variable undefined")

    def update(self, x, v):
        if x in self:
            self[x] = v
            return
        for e in reversed(self.prev):
            if x in e:
                e[x] = v
                return
        raise Exception("[Stmt3] Variable undefined")

env = Env()


# Closure
#
class Closure():
    def __init__(self,param,body,env):
        self.param = param
        self.body = body
        self.env = env

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value



@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val):  return int(val)

    # variables + assignment + decl
    def var(self, name):
        return env.lookup(str(name))

    def decl(self, name, expr):
        val = self.visit(expr)
        env.extend(str(name), val)

    def assign(self, name, expr):
        val = self.visit(expr)
        env.update(str(name), val)

    # + - * /
    def add(self, x, y):
        return self.visit(x) + self.visit(y)

    def sub(self, x, y):
        return self.visit(x) - self.visit(y)

    def mul(self, x, y):
        return self.visit(x) * self.visit(y)

    def div(self, x, y):
        return self.visit(x) // self.visit(y)

    # rel
    def less(self, x, y):
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt3] Arith/Rel op expects int operand, got {xv} and {yv}")
        return 1 if xv < yv else 0

    def equal(self, x, y):
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt3] Arith/Rel op expects int operand, got {xv} and {yv}")
        return 1 if xv == yv else 0

    # ctrl + prnt + block scopes
    def prstmt(self, expr):
        print(self.visit(expr))

    def ifstmt(self, cond, s1, s2=None):
        if self.visit(cond):
            self.visit(s1)
        elif s2 is not None:
            self.visit(s2)

    def whstmt(self, cond, stmt):
        while self.visit(cond):
            self.visit(stmt)

    def block(self, first, *rest):
        global env
        env = env.openScope()
        self.visit(first)
        for s in rest:
            self.visit(s)
        env = env.closeScope()

    # funcs
    def fdef(self, fname, param, body):
        closure = Closure(str(param), body, env)
        env.extend(str(fname), closure)

    def sbody(self, expr):
        raise ReturnValue(self.visit(expr))

    def body(self, *parts):
        *stmts, expr = parts
        for s in stmts:
            self.visit(s)
        raise ReturnValue(self.visit(expr))

    def call(self, fname, argexpr):
        global env

        fname = str(fname)   # convert token to string

        closure = env.lookup(fname)

        if not isinstance(closure, Closure):
            raise Exception("[Stmt3] Attempting to call non-function")

        argval = self.visit(argexpr)

        old_env = env
        env = closure.env.openScope()
        env.extend(closure.param, argval)

        try:
            self.visit(closure.body)
            raise Exception("[Stmt3] Missing return")
        except ReturnValue as rv:
            result = rv.value
        finally:
            env = old_env

        return result




import sys
def main():
    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        Eval().visit(tree)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
