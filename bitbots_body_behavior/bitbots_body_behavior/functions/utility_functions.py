class UtilityFunction:
    def apply(self):
        raise NotImplementedError


class LinearUF(UtilityFunction):
    @staticmethod
    def setup(factor: float = 1.0, max_x: float = 1.0):
        return LinearUF(factor, max_x)

    def __init__(self, factor: float, max_x: float):
        self.factor = factor
        self.max_x = max_x

    def apply(self, x):
        return self.factor * x / self.max_x


class PiecewiseUF(UtilityFunction):
    @staticmethod
    def setup(utility_function, zero_point: float = 0.0, one_point: float = 1.0):
        return PiecewiseUF(utility_function, zero_point, one_point)

    def __init__(self, utility_function, zero_point: float, one_point: float):
        self.utility_function = utility_function
        self.zero_point = zero_point
        self.one_point = one_point

    def apply(self, x):
        if x <= self.zero_point:
            return 0.0
        elif x >= self.one_point:
            return 1.0
        else:
            return self.utility_function.apply(x)


class ExponentialUF(UtilityFunction):
    @staticmethod
    def setup(factor: float = 1.0, exponent: float = 1.0, max_x: float = 1.0):
        return ExponentialUF(factor, exponent, max_x)

    def __init__(self, factor: float, exponent: float, max_x: float):
        self.factor = factor
        self.exponent = exponent
        self.max_x = max_x

    def apply(self, x):
        return (self.factor * x) ** self.exponent / self.max_x
