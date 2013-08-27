#!/bin/env python3
import re
# import operators
# import objects


def parser(tree):
    print(tree)


def ealuator(env, tree):
    pass


def printer(result):
    pass


def liquidator(statement):
    re_table = {
        r"^\s+": "",
        r"\s+$": "",
        r"\s+": " ",
        r"#\(": "(vector",
        r"`": "'",
        r"'\(": "(quote",
        # TODO: (define (foo bar)()) => (define foo (lambda bar ()))
    }
    statement = statement.replace("(", " ( ")
    statement = statement.replace(")", " ) ")
    for pattern, repl in re_table.items():
        statement = re.sub(pattern, repl, statement)
    return statement


def lexical_analyzer(statement):
    statement = liquidator(statement)
    tree = []
    stack = []
    for block in statement.split(" "):
        current = tree
        for index in stack:
            current = current[index]
        num = len(current)
        if block is "(":
            current.append([])
            stack.append(num)
        elif block is ")":
            try:
                stack.pop()
            except IndexError:
                raise SyntaxError("read: unexpected `)")
        elif block is ".":
            current.insert(0, "cons")
        else:
            current.append(block)
    if stack:
        raise SyntaxError("read: lack `)")
    return tree


def main():
    print("Schepy - scheme lite interpreter 0.00")
    print("by Soar Tsui <tioover@gmail.com>")
    #env = Environment()
    while True:
        statement = input("> ")
        try:
            #printer(ealuator(env, parser(lexical_analyzer(statement))))
            for tree in lexical_analyzer(statement):
                parser(tree)
        except SyntaxError as e:
            print("SyntaxError: ", format(e))

if __name__ == '__main__':
    try:
        main()
    except EOFError:
        print("")
        exit()
