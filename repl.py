#!/bin/env python3
# import re


class Environment():
    pass


def parser(statement):
    pass


def ealuator(env, tree):
    pass


def printer(result):
    pass


def liquidator(statement):
    #replace_table = {
    #    "#(": "(vector"
    #}.items()
    statement = statement.replace("")
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
