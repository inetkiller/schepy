#!/bin/env python3
import re
import readline
# import operators
from objects import Cons, MainEnvironment, nil, Symbol


def parser(tree):
    if type(tree) is not list:
        return tree
    header = Cons(nil, nil)
    prev_cons = None
    for atom in tree:
        if type(atom) is list:
            atom = parser(atom)  # Recursion parser list.
        if len(tree) is 1:
            header = Cons(atom, nil)
        elif not header:
            header = Cons(atom, Cons(None, nil))
        elif header.cdr.car is None:
            cons = Cons(atom, nil)
            header.cdr.car = cons
            prev_cons = cons
        else:
            cons = Cons(atom, nil)
            prev_cons.cdr = cons
            prev_cons = cons
        # raise SyntaxError("Can't parser empty list.")
    return header


def is_tree(tree):
    try:
        return tree.cdr.cdr == nil and type(tree.cdr.car) is Cons
    except AttributeError:
        return False


def env_finder(env, atom):
    current = env
    result = None
    while current is not None:
        if atom in current:
            result = current[atom]
            break
        current = current.parent
    return result


def atom_evaler(env, atom, isfunc=False):
    if type(atom) is Symbol:
        return atom
    elif atom is None:
        return nil
    result = env_finder(env, atom)
    if result is None:
        if atom[0] == "\'":
            result = Symbol(atom[1:])
        else:
            try:
                result = eval(atom)  # TODO: Some datatype only.
            except (NameError, SyntaxError):
                raise NameError("This is not an object.")
    return result


def ealuator(env, tree):
    if not is_tree(tree):
        return atom_evaler(env, tree)
    func = tree.car
    if func == "define":
        li = tree.cdr.car
        env[li.car] = atom_evaler(env, li.cdr.car)
        return nil
    elif func == "quote":
        symbol = tree.cdr.car.car
        return Symbol(symbol)
    func = atom_evaler(env, tree.car, isfunc=True)
    argulist = list(tree.cdr.car)
    for index, atom in enumerate(argulist):
        if is_tree(atom):
            argulist[index] = ealuator(env, atom)
        else:
            argulist[index] = atom_evaler(env, atom)
    return func(*argulist)


def liquidator(statement):
    re_table = {
        r"^\s+": "",
        r"\s+$": "",
        r"\s+": " ",
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
    env = MainEnvironment()
    while True:
        statement = input("[%d] > " % line)
        if statement:
            try:
                for tree in lexical_analyzer(statement):
                    out = tree  # lexical_analyzer debug.
                    out = parser(out)  # parser debug.
                    out = ealuator(env, out)
                    print("[%d] : %s" % (line, out))
            except (SyntaxError, NameError) as e:
                print(e.__class__.__name__, ": ", format(e))
            line += 1


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("")
        exit()
