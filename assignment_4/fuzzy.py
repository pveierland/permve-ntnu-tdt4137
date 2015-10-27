#!/usr/bin/python

class FuzzyAnd(object):
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __call__(self, a=None, b=None):
        return min(a() if a else self.a(),
                   b() if b else self.b())

class FuzzyGrade(object):
    def __init__(self, x0, x1, a=None):
        self.x0 = x0
        self.x1 = x1
        self.a  = a

    def __call__(self, a=None):
        value = a() if a else self.a()

        if value >= self.x1:
            output = 1.0
        elif value <= self.x0:
            output = 0.0
        else:
            output = (value - self.x0) / (self.x1 - self.x0)

        return output

class FuzzyNot(object):
    def __init__(self, a=None):
        self.a = a

    def __call__(self, a=None):
        return 1.0 - (a() if a else self.a())

class FuzzyOr(object):
    def __init__(self, a=None, b=None):
        self.a = a
        self.b = b

    def __call__(self, a=None, b=None):
        return max(a() if a else self.a(),
                   b() if b else self.b())

class FuzzyOutput(object):
    def __init__(self, rules):
        self.rules = rules

    def centroid(self, lower_bound, upper_bound, segments):
        segment_size = (upper_bound - lower_bound) / segments

        upper = 0.0
        lower = 0.0

        for i in range(segments + 1):
            x = lower_bound + i * segment_size

            value = max(rule(FuzzyValue(x))
                        for rule in self.rules)

            upper += x * value
            lower += value

        return upper / lower

class FuzzyReverseGrade(object):
    def __init__(self, x0, x1, a=None):
        self.x0 = x0
        self.x1 = x1
        self.a  = a

    def __call__(self, a=None):
        value = a() if a else self.a()

        if value <= self.x0:
            output = 1.0
        elif value >= self.x1:
            output = 0.0
        else:
            output = (self.x1 - value) / (self.x1 - self.x0)

        return output

class FuzzyRule(object):
    def __init__(self, membership, evaluation):
        self.membership = membership
        self.evaluation = evaluation

    def __call__(self, value):
        # Clipping
        return min(self.membership(), self.evaluation(value))

class FuzzyTriangle(object):
    def __init__(self, x0, x1, x2, a=None):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
        self.a  = a

    def __call__(self, a=None):
        value = a() if a else self.a()

        if value >= self.x0 and value <= self.x1:
            output = (value - self.x0) / (self.x1 - self.x0)
        elif value >= self.x1 and value <= self.x2:
            output = (self.x2 - value) / (self.x2 - self.x1)
        else:
            output = 0.0

        return output

class FuzzyValue(object):
    def __init__(self, value=None):
        self.value = value

    def __call__(self):
        return self.value

distance             = FuzzyValue(3.6)
delta                = FuzzyValue(1.1)

distance_very_small  = FuzzyReverseGrade(1.0, 2.5, distance)
distance_small       = FuzzyTriangle(1.5, 3.0, 4.5, distance)
distance_perfect     = FuzzyTriangle(3.5, 5.0, 6.5, distance)
distance_big         = FuzzyTriangle(5.5, 7.0, 8.5, distance)
distance_very_big    = FuzzyGrade(7.5, 9.0, distance)

delta_shrinking_fast = FuzzyReverseGrade(-4.0, -2.5, delta)
delta_shrinking      = FuzzyTriangle(-3.5, -2.0, -0.5, delta)
delta_stable         = FuzzyTriangle(-1.5, 0.0, 1.5, delta)
delta_growing        = FuzzyTriangle(0.5, 2.0, 3.5, delta)
delta_growing_fast   = FuzzyGrade(2.5, 4.0, delta)

action_none = FuzzyRule(
    FuzzyAnd(distance_small, delta_growing),
    FuzzyTriangle(-3.0, 0.0, 3.0))

action_slow_down = FuzzyRule(
    FuzzyAnd(distance_small, delta_stable),
    FuzzyTriangle(-7.0, -4.0, -1.0))

action_speed_up = FuzzyRule(
    FuzzyAnd(distance_perfect, delta_growing),
    FuzzyTriangle(1.0, 4.0, 7.0))

action_floor_it = FuzzyRule(
    FuzzyAnd(distance_very_big,
        FuzzyOr(FuzzyNot(delta_growing),
                FuzzyNot(delta_growing_fast))),
    FuzzyGrade(5.0, 8.0))

action_brake_hard = FuzzyRule(
    distance_very_small,
    FuzzyReverseGrade(-8.0, -5.0))

action = FuzzyOutput([action_none,
                      action_slow_down,
                      action_speed_up,
                      action_floor_it,
                      action_brake_hard])

print(action.centroid(-10.0, 10.0, 10000))

