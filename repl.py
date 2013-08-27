#!/bin/env python3
import re
import readline
# import operators
from objects import Cons, Environment, Nil


def atom_evaler(env, atom, isfunc=False):
    if atom in env:
        atom = env[atom]
    else:
        try:
            atom = eval(atom)  # TODO: Some datatype only.
        except (NameError, SyntaxError):
            raise NameError("Not this object.")
    return atom


def parser(env, tree):
    if type(tree) is not list:
        return atom_evaler(env, tree)
    header = None
    prev_cons = None
    for i in tree:
        if type(i) is list:
            i = parser(env, i)
        if len(tree) is 1:
            i = atom_evaler(env, i, isfunc=True)
            header = Cons(i, Nil())
        elif header is None:
            i = atom_evaler(env, i, isfunc=True)
            header = Cons(i, Cons(None, Nil()))
        elif header.cdr.car is None:
            i = atom_evaler(env, i, isfunc=False)
            cons = Cons(i, Nil())
            header.cdr.car = cons
            prev_cons = cons
        else:
            if type(i) is not Cons:
                i = atom_evaler(env, i, isfunc=False)
            cons = Cons(i, Nil())
            prev_cons.cdr = cons
            prev_cons = cons
    if header is None:
        raise SyntaxError("had empty list.")
    return header


def is_tree(tree):
    try:
        return tree.cdr.cdr == Nil() and type(tree.cdr.car) is Cons
    except AttributeError:
        return False


def ealuator(env, tree):
    func = tree.car
    argulist = list(tree.cdr.car)
    for index, atom in enumerate(argulist):
        if is_tree(atom):
            argulist[index] = ealuator(env, atom)

    return func(*argulist)


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
    print("Schepy - scheme lite interpreter 0.01")
    print("by Soar Tsui <tioover@gmail.com>")
    line = 1
    env = Environment()
    while True:
        statement = input("[%d] > " % line)
        try:
            #printer(ealuator(env, parser(lexical_analyzer(statement))))
            for tree in lexical_analyzer(statement):
                print("[%d] : %s" % (line, ealuator(env, parser(env, tree))))
        except (SyntaxError, NameError) as e:
            print(e.__class__.__name__, ": ", format(e))
        line += 1


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("")
        exit()
