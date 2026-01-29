# Ariella Marchuk
# CS358 Winter'26 Assignment 1 (Part 3)
# RelEx - a relational expression language
#
#   relex -> relex rop atom
#         |  atom
#   atom  -> "(" relex ")"
#         |  NUM
#   rop   -> "<"|"<="|">"|">="|"=="|"!="
#############################################

from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
?start: relex

?relex: relex ROP atom   -> relop
      | atom

?atom: "(" relex ")"
     | NUM               -> num

ROP: "<=" | "<" | ">=" | ">" | "==" | "!="

%import common.INT -> NUM
%import common.WS
%ignore WS
"""

parser = Lark(grammar)

# An interpreter with C semantics
# - return 1 or 0
#############################################
@v_args(inline=True)
class EvalC(Interpreter):

    # ... need code
    def num(self, val):
        return int(val)

    def relop(self, left, op, right):
        l = self.visit(left)
        r = self.visit(right)
        op = op.value

        if op == "<":
            return 1 if l < r else 0
        if op == "<=":
            return 1 if l <= r else 0
        if op == ">":
            return 1 if l > r else 0
        if op == ">=":
            return 1 if l >= r else 0
        if op == "==":
            return 1 if l == r else 0
        if op == "!=":
            return 1 if l != r else 0

# An interpreter with Python semantics
# - return True or False
#############################################
@v_args(inline=True)
class EvalP(Interpreter):

    # ... need code
    def num(self, val):
        return int(val)

    def relop(self, left, op, right):
        op = op.value

        # left is itself a relational expression??
        if hasattr(left, 'data') and left.data == 'relop':
            a = left.children[0]
            b = left.children[2]

            first = self.visit(left)
            second = self.visit_rel(b, op, right)
            return first and second

        l = self.visit(left)
        r = self.visit(right)
        return self.apply_op(l, op, r)

    # helper evaluating single 
    def apply_op(self, l, op, r):
        if op == "<":
            return l < r
        if op == "<=":
            return l <= r
        if op == ">":
            return l > r
        if op == ">=":
            return l >= r
        if op == "==":
            return l == r
        if op == "!=":
            return l != r

    # helper chained
    def visit_rel(self, lnode, op, rnode):
        l = self.visit(lnode)
        r = self.visit(rnode)
        return self.apply_op(l, op, r)


# main
########################################################
def main():
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(prog)
            print(tree.pretty(),end="")
            print("EvalC:", EvalC().visit(tree))
            print("EvalP:", EvalP().visit(tree))
            print()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()

