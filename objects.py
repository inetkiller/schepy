class Environment():
    pass


class Function():
    env = None
    pass


class Cons():
    car = None
    cdr = None

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return "(%s, %s)" % (self.car, self.cdr)


def make_cons_list(li):
    if not li:
        return None
    header = None
    prev_cons = None
    for i in li:
        if not header:
            header = Cons(i, None)
            prev_cons = header
        else:
            cons = Cons(i, None)
            prev_cons.cdr = cons
            prev_cons = cons
    return header
