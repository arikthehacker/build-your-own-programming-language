# build-your-own-language

A small programming language built up feature by feature over a term, using Python and
the Lark parser generator. It starts as arithmetic and boolean expressions and grows
into a language with variables, let-binding, type checking, functions, recursion, and
closures.

Portland State University, CS 358 Principles of Programming Languages (Winter 2026).

The grammars and some of the starting scaffolding for each stage come from the course
handouts. The interpreters, AST handling, and test programs are mine.

## Layout

Each stage is a folder, in the order the language was built:

```
01-expressions/   arithmetic, boolean, mixed, and relational expressions
02-variables/     variables, let-binding, and a small statement language
03-type-checking/ more statements plus simple type checking
04-functions/     first-class functions, recursion, and closures
```

Each stage keeps my short report for that assignment.

## What it does

By the last stage the language runs real programs. Recursive factorial, with `def`,
`if`, and `return`:

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
```

And higher-order functions and currying, where `twice(inc)(3)` applies `inc` twice:

```
let twice = lambda f: lambda x: f(f(x)) in
let inc = lambda x: x + 1 in
twice(inc)(3)
```

## How to build and run

The interpreters need Python 3 and Lark:

```
pip install lark
```

Each interpreter reads a program from standard input and runs it:

```
cd 04-functions
python3 stmt3.py < fac.st3
python3 funex.py < twice.fn
```

The `.st`, `.st2`, `.st3`, and `.fn` files in each stage are test programs written in
the language.

## How it works

Each stage uses Lark to parse a program into a tree, then an `Interpreter` subclass
walks the tree. As the language grows, the interpreter gains an environment for
variables, scope handling for blocks, a type-checking pass, and finally closures that
capture their environment so functions can be passed around and returned.

## What was hard

In my own words, from the assignment 4 report:

> The biggest issue I ran into that caused an interesting result was forgetting to
> include `@v_args(inline=True)` on my Eval class which then caused Lark to pass tree
> objects instead of raw values. It produced several strange recursion errors, but
> placing that back properly fixed what looked like a bad recursion bug quite quickly.
> Overall, I learned more about debugging an interpreter yet again, and believe I got
> better at my ability to distinguish between different parsing errors, and actual
> runtime logic errors.

Earlier stages had their own sticking points: understanding how Lark turns grammar
rules into AST nodes (assignment 1), matching AST node names to interpreter methods and
remembering to map `ID` in the grammar (assignment 2), and getting block structure,
nested `if` statements, and the `for` loop to follow the grammar exactly rather than
leaning on Python's own behavior (assignment 3).

## What I'd change now

TODO (Ariella, optional).
