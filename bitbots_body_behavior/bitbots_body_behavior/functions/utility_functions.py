import math


class UtilityFunction:
    def apply(self):
        raise NotImplementedError


class LinearUF(UtilityFunction):
    @staticmethod
    def setup(factor: float = 1.0, max_x: float = 1.0, y: float = 0):
        return LinearUF(factor, max_x, y)

    def __init__(self, factor: float, max_x: float, y: float):
        self.factor = factor
        self.y = y
        self.max_x = max_x

    def apply(self, x):
        return self.factor / self.max_x * x + self.y


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
        return self.factor * x**self.exponent / self.max_x


class EulerExponentialUF(UtilityFunction):
    @staticmethod
    def setup(factor: float = 1.0, exponent_factor: float = 1.0, max_x: float = 1.0):
        return EulerExponentialUF(factor, exponent_factor, max_x)

    def __init__(self, factor: float, exponent_factor: float, max_x: float):
        self.factor = factor
        self.exponent_factor = exponent_factor
        self.max_x = max_x

    def apply(self, x):
        return self.factor * math.e ** (self.exponent_factor * x) / self.max_x


class SigmoidUF(UtilityFunction):
    @staticmethod
    def setup(nenner_factor: float = 1.0, zaehler_wert: float = 1.0):
        return SigmoidUF(nenner_factor, zaehler_wert)

    def __init__(self, nenner_factor: float = 0.0, zaehler_wert: float = 0.0):
        self.e = math.e
        self.nenner_factor = nenner_factor
        self.zaehler_wert = zaehler_wert

    def apply(self, x):
        return self.zaehler_wert / (1 + (self.e) ** -(x / self.nenner_factor))


class SigmoidTwoXUF(UtilityFunction):
    @staticmethod
    def setup(
        nenner_factor: float = 1.0,
        zaehler_wert: float = 1.0,
        zaehler_factor: float = 1.0,
        x_verschiebung: float = 0.0,
        y_spiegelung: float = 1.0,
    ):
        return SigmoidTwoXUF(nenner_factor, zaehler_wert, zaehler_factor, x_verschiebung, y_spiegelung)

    def __init__(
        self,
        nenner_factor: float = 0.0,
        zaehler_wert: float = 0.0,
        zaehler_factor: float = 0.0,
        x_verschiebung: float = 0.0,
        y_spiegelung: float = 0.0,
    ):
        self.e = math.e
        self.nenner_factor = nenner_factor
        self.zaehler_wert = zaehler_wert
        self.zaehler_factor = zaehler_factor
        self.x_verschiebung = x_verschiebung
        self.y_spiegelung = y_spiegelung

    def apply(self, x):
        return self.zaehler_wert * (
            self.e ** ((self.y_spiegelung * x + self.x_verschiebung) * self.zaehler_factor)
            / (1 + (self.e) ** ((self.y_spiegelung * x + self.x_verschiebung) * self.nenner_factor))
        )


class NormVerteilungUF(UtilityFunction):
    @staticmethod
    def setup(sigma: float = 0.1):
        return NormVerteilungUF(sigma)

    def __init__(self, sigma: float = 0.1):
        if sigma != 0:
            self.sigma = sigma
        else:
            self.sigma = 0.1
        self.f = lambda x: (1 / (self.sigma * math.sqrt(2 * math.pi))) * math.e ** (-0.5 * (x / self.sigma) ** 2)

    def apply(self, x):
        return self.f(x) / self.f(0)
