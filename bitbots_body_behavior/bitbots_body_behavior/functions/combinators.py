import math


class Combinator:
    @staticmethod
    def apply(inputs: list[float]) -> float:
        raise NotImplementedError


class AndCombinator(Combinator):
    @staticmethod
    def apply(inputs: list[float]) -> float:
        return min(inputs)


class OrCombinator(Combinator):
    @staticmethod
    def apply(inputs: list[float]) -> float:
        return max(inputs)


class Inverter(Combinator):
    @staticmethod
    def apply(input: float) -> float:
        return 1 - input


class Prioritization(Combinator):
    @staticmethod
    def apply(inputs: list[float], weights: list[float]) -> float:
        result = 0
        weights_summed = 0
        for weight in weights:
            weights_summed += weight

        if weights_summed == 0:
            return 0
        else:
            for i in range(len(weights)):
                weights[i] /= weights_summed

            for i in range(len(inputs)):
                result += inputs[i] * weights[i]

            return result


class NaturalLogarithm(Combinator):
    @staticmethod
    def abs(number):
        if number >= 0:
            return number
        else:
            return -number

    @staticmethod
    def apply(inputs: list[float], constant: float = 1.0) -> float:
        input_sub = 0
        for input in inputs:
            input_sub -= input

        return math.exp(-abs(constant * (input_sub)))
