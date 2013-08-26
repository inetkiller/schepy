#!/bin/env python3
import re


class Cons():
    car = None
    cdr = None


class Environment():
    pass


class Function():
    env = None
    pass


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
    statement = liquidator(statement)
    pass


def main():
    print("Schepy - scheme lite interpreter. 0.00")
    print("by Soar Tsui <tioover@gmail.com>")
    env = Environment()
    while True:
        statement = input("> ")
        printer(ealuator(env, parser(lexical_analyzer(statement))))

if __name__ == '__main__':
    main()
