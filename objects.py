class Environment(dict):
    def __init__(self, parent=None):
        super(Environment, self).__init__()
        self.parent = parent


class MainEnvironment(Environment):
    def __init__(self, parent=None):
        super(MainEnvironment, self).__init__()
        self["+"] = lambda a, b: a+b
        self["-"] = lambda a, b: a-b
        self["*"] = lambda a, b: a*b
        self["/"] = lambda a, b: a/b


class Function():
    env = None
    arguments = []


class Symbol():
    def __init__(self, atom):
        if type(atom) is str:
            self.symbol = atom
        elif atom is None:
            self.symbol = "()"
        elif type(atom) is Cons:
            self.symbol = str(atom)
        else:
            print(type(atom))
            raise SyntaxError("Not symbol.")

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


class Nil():
    def __eq__(a, b):
        return type(b) is Nil

    def __bool__(self):
        return False


nil = Nil()


class Cons():
    car = None
    cdr = None

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __eq__(a, b):
        if hasattr(b, "car") and hasattr(b, "cdr"):
            return (a.car == b.car and a.cdr == b.cdr)
        else:
            return False

    def __len__(self):
        length = 0
        current = self
        while type(current) is Cons:
            length += 1
            current = current.cdr
        return length

    def __iter__(self):
        self.current = self
        self.stop_flag = False
        return self

    def __next__(self):
        if self.stop_flag:
            raise StopIteration
        elif self.current.cdr == nil:
            self.stop_flag = True
            return self.current.car
        else:
            result = self.current.car
            self.current = self.current.cdr
            return result

    def __bool__(self):
        return self.car != nil or self.cdr != nil

    def __str__(self):
        if self.cdr == nil:
            if self.car == nil:
                return "()"
            else:
                return "(%s)" % (str(self.car))

        if type(self.cdr) is not Cons:
            return "(cons %s %s)" % (str(self.car), str(self.cdr))
        string = "("+str(self.car)
        current = self.cdr
        while type(current) is Cons:
            string += " " + str(current.car)
            current = current.cdr
        if current == nil:
            string += ")"
        else:
            string += " . " + str(current) + ")"
        return string

    def __repr__(self):
        return str(self)
