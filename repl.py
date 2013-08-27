#!/bin/env python3
import re


class Environment():
    pass


class Function():
    env = None
    pass


def car(cons):
    return cons[0]


def cdr(cons):
    return cons[1]


def parser(statement):
    pass


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
        # TODO: (foo . bar) => (cons foo bar)
    }
    for pattern, repl in re_table.items():
        statement = re.sub(pattern, repl, statement)
    return statement


def lexical_analyzer(statement):
    statement = statement.replace("(", " ( ")
    statement = statement.replace(")", " ) ")
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
            print(lexical_analyzer(statement))
        except SyntaxError as e:
            print("SyntaxError: ", format(e))

if __name__ == '__main__':
    try:
        main()
    except EOFError:
        print("")
        exit()
