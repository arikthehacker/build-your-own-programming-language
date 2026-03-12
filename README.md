# build-your-own-programming-language

![language](https://img.shields.io/badge/language-Python-blue) ![platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)
![CI](https://github.com/arikthehacker/build-your-own-programming-language/actions/workflows/ci.yml/badge.svg)

A small programming language built up feature by feature, using Python and the Lark
parser generator. It grows from arithmetic and boolean expressions into a language with
variables, let-binding, type checking, functions, recursion, and closures.

## quickstart

```
git clone https://github.com/arikthehacker/build-your-own-programming-language.git
cd build-your-own-programming-language
pip install lark
make run
```

expected output:

```
{
def fac(n): {
    var result = 0;
    if (n == 0) result = 1
    else result = n * fac(n - 1);
    return result
};
print(fac(5))
}

120
```

Each stage is a folder, in the order the language was built:

```
01-expressions/   arithmetic, boolean, mixed, and relational expressions
02-variables/     variables, let-binding, and a statement language
03-type-checking/ more statements plus simple type checking
04-functions/     first-class functions, recursion, and closures
```

Each interpreter reads a program from standard input. The `.st`, `.st2`, `.st3`, and
`.fn` files are programs written in the language, for example a recursive factorial
(`04-functions/fac.st3`) and a curried higher-order function (`04-functions/twice.fn`,
where `twice(inc)(3)` applies `inc` twice).

## how it works

Each stage uses Lark to parse a program into a tree, then an `Interpreter` subclass walks
the tree. By the last stage, functions are closures that capture the environment they
were defined in, so they can be passed around and returned:

```python
def func(self, name, body):
    return Closure(str(name), body, self.env)

def call(self, fexpr, argexpr):
    closure = self.visit(fexpr)
    argv = self.visit(argexpr)

    new_env = Env(closure.env)        # chain onto the captured environment
    new_env.extend(closure.id, argv)
    ...
```

A `let` builds a new environment layer, evaluates the body under it, then restores the
previous environment, so bindings have the scope you expect.
