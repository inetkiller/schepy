class Environment():
    pass


class Function():
    env = None
    pass


class Symbol():
    def __init__(self, string):
        if string[0] is not "\'":
            raise SyntaxError("Not symbol.")
        self.symbol = string[1:]

    def __str__(self):
        result = "'" + self.symbol
        return result

    def __repr__(self):
        return str(self)

    def __eq__(x, y):
        if hasattr(y, "symbol"):
            return x.symbol == y.symbol
        return False

    def __nozero__(self):
        return self.symbol != "()"


class Nil(Symbol):
    def __init__(self):
        super(Nil, self).__init__("'()")


class Cons():
    car = None
    cdr = None

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        if self.cdr.__class__ is not Cons:
            return "(cons %s %s)" % (str(self.car), str(self.cdr))
        string = "("+str(self.car)
        current = self.cdr
        while current.cdr.__class__ is Cons:
            string += " " + str(current.car)
            current = current.cdr
        if current.cdr == Nil():
            string += " " + str(current.car) + ")"
        else:
            string += " . " + str(current.cdr) + ")"
        return string


def make_cons_list(li):
    if not li:
        return None
    header = None
    prev_cons = None
    for i in li:
        if type(i) is list:
            i = make_cons_list(i)
        if not header:
            header = Cons(i, Nil())
            prev_cons = header
        else:
            cons = Cons(i, Nil())
            prev_cons.cdr = cons
            prev_cons = cons
    return header

