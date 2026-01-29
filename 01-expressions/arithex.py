# Name: Ariella Marchuk
# Exercise 2: The Lark Parser Generator
# CS 358 Principles of Programming Languages, Winter 2026
# amarchuk@pdx.edu


from lark import Lark, v_args
from lark.visitors import Interpreter

# Question 2(a):
# define the grammar for the ArithEx language.
# this grammar encodes operator precedence and associativity
# for +, -, *, /, and parentheses.


grammar = """
?start: expr
?expr: expr "+" term   -> add
     | expr "-" term   -> sub
     | term
?term: term "*" atom   -> mul
     | term "/" atom   -> div
     | atom
?atom: "(" expr ")"
     | NUM             -> num

%import common.INT -> NUM
%ignore " "
"""

# create the parser from the grammar above
parser = Lark(grammar)


@v_args(inline=True)
class Eval(Interpreter):
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


# Question 2(b):
# toPrefix is a second action over the same AST.
# it converts the expression tree into prefix notation.

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

