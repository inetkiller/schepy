class Environment(dict):
    pass


class Function():
    env = None
    arguments = []
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
        if self.cdr == Nil():
            return "(%s)" % (str(self.car))
        if self.cdr.__class__ is not Cons:
            return "(cons %s %s)" % (str(self.car), str(self.cdr))
        string = "("+str(self.car)
        current = self.cdr
        while current.__class__ is Cons:
            string += " " + str(current.car)
            current = current.cdr
        if current == Nil():
            string += ")"
        else:
            string += " . " + str(current) + ")"
        return string
