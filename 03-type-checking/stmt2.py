# stmt2.py
# Name: Ariella Marchuk
# Assignment 3: More Constructs & Simple Type-checking
# CS 358 Principles of Programming Languages, Winter 2026
# amarchuk@pdx.edu

# Stmt2 - an extended statement language 
#
#   prog -> stmt
#
#   stmt -> ID "=" expr 
#         | "if" "(" expr ")" stmt ["else" stmt]
#         | "while" "(" expr ")" stmt
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#         | "var" ID "=" expr                // new 
#         | "for" "(" ID "in" expr ")" stmt  // new 
#
#   expr -> aexpr "<"  aexpr  // *new* 
#         | aexpr "==" aexpr  // *new* 
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
#         | "range" "(" expr "," expr ")"  // new
#         | atom "[" expr "]"              // new
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: stmt

   stmt: ID "=" expr                  -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
       | "while" "(" expr ")" stmt    -> whstmt
       | "print" "(" expr ")"         -> prstmt
       | "{" stmt (";" stmt)* "}"     -> block      
       | "var" ID "=" expr            -> decl
       | "for" "(" ID "in" expr ")" stmt  -> forlp

  ?expr: aexpr "<"  aexpr -> less
       | aexpr "==" aexpr -> equal
       | aexpr 

  ?aexpr: aexpr "+" term  -> add
       |  aexpr "-" term  -> sub
       |  term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr ")"
       | "range" "(" expr "," expr ")" -> rng
       | atom "[" expr "]" -> idx
       | ID                -> var
       | NUM               -> num

  COMMENT: "#" /[^\\n]*/ "\\n"
  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore COMMENT
  %ignore WS
"""

# With an 'lalr' parser, Lark handles the 'dangling else' 
# case correctly.
parser = Lark(grammar, parser='lalr')

# Variable environment
#
class Env(dict):

    # ...  need code
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
            raise Exception("[Stmt2] Variable already defined")
        self[x] = v

    def lookup(self, x):
        if x in self:
            return self[x]
        for e in reversed(self.prev):
            if x in e:
                return e[x]
        raise Exception("[Stmt2] Variable undefined")

    def update(self, x, v):
        if x in self:
            self[x] = v
            return
        for e in reversed(self.prev):
            if x in e:
                e[x] = v
                return
        raise Exception("[Stmt2] Variable undefined") 

env = Env()

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val): 
        return int(val)

    # ... need code
    def var(self, name):
        return env.lookup(str(name))

    def assign(self, name, expr):
        val = self.visit(expr)
        env.update(str(name), val)

    def decl(self, name, expr):
        val = self.visit(expr)
        env.extend(str(name), val)

    def prstmt(self, expr):
        val = self.visit(expr)
        print(val)

    def block(self, first, *rest):
        global env
        env = env.openScope()
        self.visit(first)
        for s in rest:
            self.visit(s)
        env = env.closeScope()

    def ifstmt(self, cond, s1, s2=None):
        val = self.visit(cond)
        if val:
            self.visit(s1)
        elif s2:
            self.visit(s2)

    def whstmt(self, cond, stmt):
        while self.visit(cond):
            self.visit(stmt)

    def forlp(self, name, expr, stmt):
        global env
        rng_val = self.visit(expr)

        if type(rng_val) != range:
            raise Exception(f"[Stmt2] for-loop expects range, got {rng_val}")

        lo = rng_val.start
        hi = rng_val.stop

        env = env.openScope()
        env.extend(str(name), lo)

        while env.lookup(str(name)) < hi:
            self.visit(stmt)
            curr = env.lookup(str(name))
            env.update(str(name), curr + 1)

        env = env.closeScope()

# + - * /

    def add(self, x, y): 
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt2] Arith/Rel op expects int operand, got {xv} and {yv}")
        return xv + yv

    def sub(self, x, y):
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt2] Arith/Rel op expects int operand, got {xv} and {yv}")
        return xv - yv

    def mul(self, x, y):
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt2] Arith/Rel op expects int operand, got {xv} and {yv}")
        return xv * yv

    def div(self, x, y):
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt2] Arith/Rel op expects int operand, got {xv} and {yv}")
        return xv // yv

# < =

    def less(self, x, y):
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt2] Arith/Rel op expects int operand, got {xv} and {yv}")
        return 1 if xv < yv else 0

    def equal(self, x, y):
        xv = self.visit(x)
        yv = self.visit(y)
        if type(xv) != int or type(yv) != int:
            raise Exception(f"[Stmt2] Arith/Rel op expects int operand, got {xv} and {yv}")
        return 1 if xv == yv else 0

# range constructor

    def rng(self, lo, hi):
        lov = self.visit(lo)
        hiv = self.visit(hi)
        if type(lov) != int or type(hiv) != int:
            raise Exception(f"[Stmt2] range bounds must be integers, got {lov} and {hiv}")
        return range(lov, hiv)

#index

    def idx(self, r, i):
        rv = self.visit(r)
        iv = self.visit(i)
        if type(rv) != range:
            raise Exception(f"[Stmt2] Index expects range, got {rv}")
        if type(iv) != int:
            raise Exception(f"[Stmt2] Index expects int index, got {iv}")
        return rv[iv]


# A new input routine - sys.stdin.read() 
# - It allows source program be written in multiple lines
#
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
