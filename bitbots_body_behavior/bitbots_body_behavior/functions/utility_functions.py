import math

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
    

class SigmoidUF(UtilityFunction):
    @staticmethod
    def setup(position_x_axis: float = 1.0):
        return SigmoidUF(position_x_axis)
    
    def __init__(self, position_x_axis: float = 0):
        self.e = math.e
        self.position_x_axis = position_x_axis
       

    def apply(self,x): 
        return 1/(1+(self.e)**-(x+self.position_x_axis))
    
class NormVerteilungUF(UtilityFunction):
    @staticmethod
    def setup(factor: float = 1.0, sigma: float = 0.1):
        return NormVerteilungUF(factor, sigma)
    
    def __init__(self, factor: float, sigma: float = 0.1):
        self.factor = factor
        if sigma != 0:
            self.sigma = sigma
        else:
            self.sigma = 0.1
        self.f = lambda x: 1/(self.sigma*math.sqrt(2*math.pi))*math.e**-0.5(x/self.sigma)**2

    def apply(self, x):     
        return self.f(x)/self.f(0)
